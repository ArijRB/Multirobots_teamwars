from turtleinterface import *

# s'orienter vers la gauche
def aller_devant_laitues():
    gauche() ; gauche()
    avance() ; avance()
    droite()
    for i in range(3):
      avance()

    droite(); avance();gauche()
    for i in range(5):
      avance()
    gauche()
    for i in range(5):
        avance()
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
    droite()
    avance()
    droite()
    avance()
    ramasse_rangee()

def rentre_au_chateau():
    # reviens en haut a gauche du chateau
    avance(); avance()
    droite(); avance(); avance();
    gauche();
    for i in range(4):
        avance()
    gauche()
    for i in range(4):
        avance()
    gauche()
    for i in range(4):
        avance()
    droite();droite()

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
