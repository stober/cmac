'''
Created on May 5, 2009

@author: stober
'''

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
import os

np_lib = os.path.dirname(numpy.__file__)
np_inc = [os.path.join(np_lib, 'core/include')]

ext_modules = [Extension("cmac.fast",["src/fast.pyx"], include_dirs=np_inc)]

setup(name='cmac',
      version='1.0',
      description='CMAC implementation using Python',
      author='Jeremy Stober',
      author_email='stober@cs.utexas.edu',
      package_dir={'cmac':'src'},
      packages=['cmac'],
      cmdclass = {'build_ext' : build_ext},
      ext_modules = ext_modules
      )
