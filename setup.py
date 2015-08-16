# ce fichier se compile avec la commande
# python setup.py build_ext --inplace
#

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

ext  =  [Extension( "rayon", sources=["rayon.py"] ,extra_compile_args=["-Wno-unused-function"])]

setup(
   cmdclass={'build_ext' : build_ext},
   include_dirs = [numpy.get_include()],
   ext_modules=ext
   )
