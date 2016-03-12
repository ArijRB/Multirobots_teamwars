from gardenworld import *

def av_jusqu_au_mur():
    while not obstacle():
        av()

def demitour():
    tg()
    tg()

def monte():
    tg()
    av()
    td()

def oriente_mur_a_droite():
    while not obstacle():
        tg()
    tg()

def si_sortie_droite_vasy():
    td()
    if not obstacle():
        av()
        av()
    else:
        tg()

def cherche_sortie_long_mur():
    while not obstacle():
        si_sortie_droite_vasy()
        av()

def oriente_mur_a_droite():
    """
    attention cette fonction ne doit
    etre appellee que si le personnage
    est contre un mur
    """
    while not obstacle():
        td()
    tg()

def longe_mur():
    """
    attention, le mur doit etre
    a ma gauche
    """
    while True:
        tg()
        if obstacle():
            td()
            av()
        else:
            av()


def exoj():
    init('L1TD2JK')
    for i in range(5):
        av_jusqu_au_mur()
        tg()

def exok():
    init('L1TD2JK')
    av_jusqu_au_mur()
    for i in range(5):
        cherche_sortie_long_mur()
        tg()


def exol():
    init('L1TD2L')
    while True:
        if cherche() == 'chou':
             ra()
             demitour()
             av_jusqu_au_mur()
             tg()
             av_jusqu_au_mur()
             break
        elif obstacle():
            demitour()
            av_jusqu_au_mur()
            demitour()
            monte()
        else:
            av()



def exom():
    init('L1TD2M')
    oriente_mur_a_droite()
    for i in range(4):
        av_jusqu_au_mur()
        tg()
    av()

def exon():
    init('L1TD2N')
    av_jusqu_au_mur()
    td()
    longe_mur()


exoj()
exok()
exol()
exom()
exon()
