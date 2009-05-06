'''
Created on May 5, 2009

@author: stober
'''

from distutils.core import setup

setup(name='cmac',
      version='1.0',
      description='CMAC implementation using Python',
      author='Jeremy Stober',
      author_email='stober@cs.utexas.edu',
      package_dir={'cmac':'src'},
      packages=['cmac']
      )