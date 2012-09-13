#! /usr/bin/env python
"""
Author: Jeremy M. Stober
Program: TEST_CMAC.PY
Date: Saturday, April 14 2012
Description: Test code for CMAC implementation.
"""

from cmac import CMAC
import numpy as np
import numpy.random as npr
import pdb
import pylab
from utils import dual_scatter, create_cluster_colors_rgb,lvl_scatter

c = CMAC(1,0.5,0.1)


# t = [[0.2,0.2],[.6,.6],[.2,.6],[.6,.2]]
# for i in t:
#     print i, c.quantize(i), c.quantize_alt(i), c.quantize_fast(i)

c = CMAC(3,0.15,0.1)

#pdb.set_trace()
#c.quantize_alt([0.05, 0.1])

data = []
for i in range(1000):
    t = npr.rand(2) * 2 - 1
    pts = c.quantize(t)
    data.append([t,pts])

lvl1_labels = [d[1][0] for d in data]
lvl2_labels = [d[1][1] for d in data]
lvl3_labels = [d[1][2] for d in data]
pts = np.array([d[0] for d in data])

print set(lvl1_labels)
print set(lvl2_labels)
print set(lvl3_labels)

def gen_colors(lbls):
    uniq = set(lbls)
    c = create_cluster_colors_rgb(len(uniq))
    cmap = dict(zip(uniq,c))
    return [cmap[i] for i in lbls]


colors = [gen_colors(lvl1_labels),gen_colors(lvl2_labels),gen_colors(lvl3_labels)]
p = [pts,pts,pts]
lvl_scatter(p,colors,show=True)
pylab.scatter(pts[:,0],pts[:,1],c=gen_colors(lvl3_labels))
pylab.show()

# t = np.array([[0.2,0.2],[.6,.6],[.2,.6],[.6,.2]])

# print c.quantize([0.29,0.30])

# for i in t:
#     print np.array(i / 0.15).astype(int)
#     #pdb.set_trace()
#     print i, c.quantize(i), c.quantize_alt(i), c.quantize_fast(i)

# for i in t:
#     print -i, c.quantize(-i), c.quantize_alt(-i), c.quantize_fast(-i)
    
# for i in range(10):
#     t = npr.rand(2) * 2 - 1
#     print t, c.quantize(t), c.quantize_alt(t), c.quantize_fast(t)

