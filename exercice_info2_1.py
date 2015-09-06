from gardenworld import *
init('info2_1')

def avk(k):
    for i in range(k):
        av()

def rak(k):
    L = []
    for i in range(k):
        o = ra(); av()
        L += [o]
    return L

def dt():
    tg();tg()

dt()
avk(10); td(); av(); td()
print rak(20)
