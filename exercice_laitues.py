from gardenworld import *
# le but de cet exercice est de programmer une tortue qui doit transferer 8 laitues dans l'enclos du chateau

# quelques macros
def fonce():
    # avance tout droit tant qu'on est pas bloques par un obstacle
    while avance():
        pass

def demitour():
    tournegauche();tournegauche()

# fonctions principales
def aller_devant_laitues():
    demitour()
    avance() ; avance()
    tournedroite()
    fonce()

    tournedroite(); avance();tournegauche()
    for i in range(5):
      avance()
    tournegauche()
    fonce()
    tournedroite()
    avance()
    tournegauche()


def ramasse_laitues():

    def ramasse_rangee():
        for j in range(4):
            ramasse()
            avance()

    avance()
    ramasse_rangee()
    for i in range(2):
        tournedroite()
        avance()
    ramasse_rangee()



def rentre_au_chateau():
    # reviens en haut a tournegauche du chateau
    fonce()
    tournedroite(); avance(); avance();
    tournegauche();
    for i in range(4):
        avance()
    for i in range(2):
        tournegauche()
        fonce()
    demitour()


def repose_laitues():
    for i in range(4):
        depose()
        tournedroite()
        avance()
        depose()
        tournegauche();tournegauche()
        avance();tournedroite()
        avance()


aller_devant_laitues()
ramasse_laitues()
rentre_au_chateau()
repose_laitues()
