try:
    """ if cython is available, it will be used"""
    import cython
    cythonized = cython.compiled
except:
    cythonized = False

print cythonized



import numpy as np
if cythonized:
    cimport numpy as cnp

print "yo"
