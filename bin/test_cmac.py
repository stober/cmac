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

c = CMAC(1,0.5,0.1)


t = [[0.2,0.2],[.6,.6],[.2,.6],[.6,.2]]
for i in t:
    print i, c.quantize(i), c.quantize_alt(i), c.quantize_fast(i)

c = CMAC(2,0.15,0.1)

#pdb.set_trace()
#c.quantize_alt([0.05, 0.1])


t = np.array([[0.2,0.2],[.6,.6],[.2,.6],[.6,.2]])
for i in t:
    #pdb.set_trace()
    print i, c.quantize(i), c.quantize_alt(i), c.quantize_fast(i)

for i in t:
    print -i, c.quantize(-i), c.quantize_alt(-i), c.quantize_fast(-i)
    
for i in range(10):
    t = npr.rand(2) * 2 - 1
    print t, c.quantize(t), c.quantize_alt(t), c.quantize_fast(t)

