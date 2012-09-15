import numpy as np
cimport numpy as np

DTYPE = np.double
ctypedef np.double_t DTYPE_t

ITYPE = np.int
ctypedef np.int_t ITYPE_t

def quantize(np.ndarray[DTYPE_t,ndim=1] vector, int nlevels, double resolution):
     
     cdef int n = vector.shape[0]
     cdef unsigned int i
     cdef np.ndarray[ITYPE_t, ndim=1] quantized = (vector / resolution).astype(int)
     cdef np.ndarray[ITYPE_t, ndim=2] coords = np.zeros((nlevels,n+1),dtype=ITYPE)
     coords[:,n] = np.arange(nlevels)
     
     for i in range(nlevels):
         coords[i,:n] = quantized - (quantized - i) % nlevels

     return coords
     	 
