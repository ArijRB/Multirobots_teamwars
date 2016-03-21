#cython: boundscheck=False, nonecheck=False,wraparound=False,initializedcheck=False,cdivision=True

import cython
import pygame
cimport numpy as cnp
#from libc.math cimport sin,cos
from libc.stdlib cimport abs

### Includes from pygame internals ###

cdef extern from "pygame/bitmask.h":
    ctypedef struct bitmask_t:
        int w,h
        unsigned long int bits[1]

    int bitmask_getbit(const bitmask_t *m, int x, int y) nogil;

ctypedef bitmask_t* bitmaskptr_t

cdef extern from "pygame/mask.h":
    ctypedef struct PyMaskObject:
        bitmask_t *mask

### Fast Inline Functions ###


cdef inline bitmaskptr_t cyGetBitmask(object mymask):
    return (<PyMaskObject*>mymask).mask

cdef inline int cyBitmaskGetbit(bitmaskptr_t bm,int i,int j) nogil:
    return bitmask_getbit(bm,i,j)


"""  -  -  -  -  -  -  -   """


@cython.locals(x=cython.int,y=cython.int,x2=cython.int,y2=cython.int,\
               w=cython.int,h=cython.int,\
               steep=cython.int,i=cython.int,\
               sx=cython.int,sy=cython.int,d=cython.int,dx=cython.int,dy=cython.int,\
               _cython_compiled=cython.bint,bm1=bitmaskptr_t,bm2=bitmaskptr_t)
cpdef rayon(m1,m2,x,y,angle_degree,w,h,max_radius)
