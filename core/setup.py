# ce fichier se compile avec la commande
# python setup.py build_ext --inplace
#
import sys,os
if len(sys.argv) == 1: sys.argv = ['setup.py','build_ext','--inplace']
os.system('pwd')
os.system('rm *.so')

from distutils.core import setup
from Cython.Distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
import pygame

ext  = [Extension( "rayon", ["rayon.py"] ,\
        cython_include_dirs = ['.'],\
        extra_compile_args=["-Wno-unused-function"]),\
        Extension( "fast_rect_collision", ["fast_rect_collision.py"] ,\
        extra_compile_args=["-Wno-unused-function"])]

setup(
   cmdclass={'build_ext' : build_ext},
   include_dirs = [numpy.get_include(),'.'],
   ext_modules=ext
   )
