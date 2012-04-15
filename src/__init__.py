#!/usr/bin/python
"""
Author: Jeremy M. Stober
Program: TILES.PY
Date: Monday, March 31 2008
Description: A simple CMAC implementation.
"""

import os, sys, getopt, pdb
from numpy import *
from numpy.random import *
import pylab
#import matplotlib.axes3d as axes3d
from mpl_toolkits.mplot3d import Axes3D
import pickle
import cmac.fast
pylab.ioff()

class CMAC(object):

    def __init__(self, nlevels, quantization, beta):
        self.nlevels = nlevels
        self.quantization = quantization
        self.weights = {}
        self.beta = beta

    def save(self,filename):
        pickle.dump(self,open(filename,'wb'),pickle.HIGHEST_PROTOCAL)

    def quantize_alt(self, vector):

        quantized = []
        for x in vector:
            if x >= 0:
                quantized.append(int(x / self.quantization))
            else:
                quantized.append(int((x - self.quantization + 1) / self.quantization))

        points = []
        for i in range(self.nlevels):
            index = []
            for x in quantized:
                if x >= i:
                    index.append(x - (x - i) % self.nlevels)
                else:
                    index.append(x + 1 + (i - (x + 1)) % self.nlevels - self.nlevels)
            points.append(index)
        return points

    def quantize_fast(self, vector):
        return cmac.fast.quantize(array(vector), self.nlevels, self.quantization)
                    
    def quantize(self, vector):
        """
        Generate receptive field coordinates for each level of the CMAC.
        """

        # some error checking to make sure that the input size doesn't change
        if hasattr(self, 'input_size') and len(vector) != self.input_size:
            raise ValueError, "Different input size in call to quantize!"
        elif not hasattr(self, 'input_size'):
            self.input_size = len(vector)
        else:
            pass

        quantized = (array(vector) / self.quantization).astype(int)
        #print quantized
        coords = []

        for i in range(self.nlevels):
            # Note that the tile size is nlevels * quantization!

            # Coordinates for this tile.
            point = list(quantized - (quantized - i) % self.nlevels)

            # Label the ith tile so that it gets hashed uniquely.
            point.append(i)

            coords.append(tuple(point))

        return coords

    def response(self, vector, response, quantized = False):
        """
        Train the CMAC.
        """

        # Coordinates for each level tiling.
        coords = None
        if quantized == False:
            coords = self.quantize(vector)
        else:
            coords = vector

        # Use Python's own hashing for storing feature weights. If you
        # roll your own you'll have to learn about Universal Hashing.
        prediction = sum([self.weights.setdefault(pt, 0.0) for pt in coords]) / len(coords)
        error = self.beta * (response - prediction)

        for pt in coords:
            self.weights[pt] += error

        return prediction

    def __len__(self):
        return len(self.weights)

    def eval(self, vector, quantized = False):
        """
        Eval the CMAC.
        """

        # Coordinates for each level tiling.
        coords = None
        if quantized == False:
            coords = self.quantize(vector)
        else:
            coords = vector
        
        return sum([self.weights.setdefault(pt, 0.0) for pt in coords]) / len(coords)


class TraceCMAC(CMAC):

    """
    CMAC that can be easily plugged into TD learning with eligibility traces.
    """

    def __init__(self, nlevels, quantization, beta, decay, inc = 1.0, replace = True, init = 1.0):

        # initialize parent class attributes
        CMAC.__init__(self, nlevels, quantization, beta)
        self.traces = {} # traces
        self.decay = decay # decay parameter
        self.inc = inc
        self.replace = replace
        self.init = init

    def train(self, vector, delta):
        coords = self.quantize(vector)

        todelete = []
        for (key,val) in self.traces.items():
            self.traces[key] = self.decay * val
            if self.traces[key] < 0.00000001:
                todelete.append(key)

        for key in todelete:
            del self.traces[key]

        # increment active traces
        if self.replace:
            for pt in coords:
                self.traces[pt] = self.inc
        else:
            for pt in coords:
                self.traces[pt] = self.inc + self.traces.setdefault(pt,0.0)

        # update params
        for (key, val) in self.traces.items():
            self.weights[key] = self.weights.setdefault(key,self.init) + self.beta * delta * val

    def eval(self, vector, quantized = False):
        """
        Eval the CMAC.
        """

        # Coordinates for each level tiling.
        coords = None
        if quantized == False:
            coords = self.quantize(vector)
        else:
            coords = vector
        
        return sum([self.weights.setdefault(pt, self.init) for pt in coords]) / len(coords)


    def reset(self):
        self.traces = {}

def test(name):

    if name == 'sin':

        cmac = CMAC(32, .01, 0.1)
        points = uniform(low=0,high=2*pi,size=1000)
        responses = sin(points)

        errors = []
        for (point,response) in zip(points,response):
            predicted = cmac.response(array([point]),response)
            errors.append(abs(response - predicted))
            #print point, response, predicted

        points = uniform(low=0, high=2*pi, size=100)
        actual = []
        for point in points:
            actual.append(cmac.eval(array([point])))

        pylab.figure(1)
        pylab.plot(points,actual, '.')

        pylab.figure(2)
        pylab.plot(errors)

        pylab.show()

    elif name == 'wave':

        cmac = CMAC(32, .1, 0.01)
        points = uniform(low=0,high=2*pi,size=(10000,2))
        responses = sin(points[:,0]) + cos(points[:,1])

        errors = []
        for (point,response) in zip(points,responses):
            predicted = cmac.response(point,response)
            errors.append(abs(response - predicted))
            #print point, response, predicted


        fig1 = pylab.figure(1)
        ax1 = Axes3D(fig1)
        ax1.scatter3D(points[:,0], points[:,1], responses)

        points = uniform(low=0,high=2*pi,size=(10000,2))
        predictions = []
        for point in points:
            predictions.append(cmac.eval(point))

        fig2 = pylab.figure(2)
        ax2 = Axes3D(fig2)
        ax2.scatter3D(points[:,0], points[:,1], predictions)

        # print len(cmac)
        # pylab.plot(errors)
        pylab.show()


def main():

    def usage():
	print sys.argv[0] + "[-h] [-d]"

    try:
        (options, args) = getopt.getopt(sys.argv[1:], 'dh', ['help','debug'])
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)

    for o, a in options:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
	elif o in ('-d', '--debug'):
	    pdb.set_trace()

    test('wave')

if __name__ == "__main__":
    main()
