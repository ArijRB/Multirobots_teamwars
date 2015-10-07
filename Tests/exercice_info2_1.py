from gardenworld import *
from collections import Counter



def avance_many(k):
    for i in range(k):
        av()


def ramasse_rangee():
    L = []
    while True:
        o = ramasse()
        if not o is None:
            L.append(o)
        if obstacle():
            break
        avance()
    return L


def ramasse_tout():
    L = []
    for i in range(4):
        L += ramasse_rangee()
        tg();
        av();
        tg()
        L += ramasse_rangee()
        td();
        av();
        td()
    return L


def va_dans_jardin():
    avance_many(7)
    tg()
    avance_many(10)
    tg()
    avance_many(7)
    tg();
    tg()


def enregistre_rangee():
    L = []
    while True:
        L.append(cherche())
        if obstacle():
            break
        avance()
    return L


def plante_rangee(L):
    for leg in L:
        ramasse()
        depose(leg)
        avance()


def plante_jardin():
    L = enregistre_rangee()
    for i in range(4):
        tg();
        tg();
        avance_many(15);
        tg();
        av();
        tg()
        plante_rangee(L)


def main():
    init('info2_1')
    gw.fps = 65

    panier = ramasse_tout()
    print ("J'ai ramasse: ", dict(Counter(panier)))
    va_dans_jardin()
    plante_jardin()

if __name__ == '__main__':
    main()
