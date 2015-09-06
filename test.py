x = None

def f():
    global x
    x = "hello"
    print x
"""
strange behavior:
>>> from test import *
>>> print x
None
>>> f()
>>> print x
None
"""
