from discreteturtleinterface import *
# le but de cet exercice est de programmer une tortue qui doit transferer 8 laitues dans l'enclos du chateau

# quelques macros
def fonce():
    # avance tout droit tant qu'on est pas bloques par un obstacle
    while avance():
        pass

def demitour():
    gauche();gauche()

# fonctions principales
def aller_devant_laitues():
    demitour()
    avance() ; avance()
    droite()
    fonce()

    droite(); avance();gauche()
    for i in range(5):
      avance()
    gauche()
    fonce()
    droite()
    avance()
    gauche()


def ramasse_laitues():

    def ramasse_rangee():
        for j in range(4):
            ramasse()
            avance()

    avance()
    ramasse_rangee()
    for i in range(2):
        droite()
        avance()
    ramasse_rangee()



def rentre_au_chateau():
    # reviens en haut a gauche du chateau
    fonce()
    droite(); avance(); avance();
    gauche();
    for i in range(4):
        avance()
    for i in range(2):
        gauche()
        fonce()
    demitour()


def repose_laitues():
    for i in range(4):
        depose()
        droite()
        avance()
        depose()
        gauche();gauche()
        avance();droite()
        avance()


aller_devant_laitues()
ramasse_laitues()
rentre_au_chateau()
repose_laitues()
