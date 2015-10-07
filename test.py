class A(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        print "appel a new avec arguments",args,kwargs
        return super(A, cls).__new__(cls)
    def __init__(self, *args, **kwargs):
        print "appel a init avec arguments",args,kwargs
        #reset pygame


A('hello')
