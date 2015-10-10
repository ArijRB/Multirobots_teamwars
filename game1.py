# -*- coding: utf-8 -*-
"""
ce qui me manque comme fonctions:
- trouver le tileid a partir du nom (dans ontology?)
- creer un sprite au row/col donne
- trouver les sprites dans le layer au row/col donne
- l'ontology doit ecrire dans le champs nom des sprites
- une fonction game.which_layers(sprite) qui trouve les layers d'appartenance d'un sprite
"""


import gardenworld
from gardenworld import *

def avk(k):
    for i in range(k):
        av()

def init(s):
    global personnages_tiled,personnages,guerriers_sympas
    print("new init")
    gardenworld.init(s)
    personnages_tiled = {perso.get_rowcol():game.O.secondname(perso) for perso in game.layers['personnage'] }
    personnages = dict(((y, x), personnages_tiled[y,x]) for (y, x) in personnages_tiled)
    guerriers_sympas = dict((k, personnages[k]) for k in personnages if personnages[k] ['Guldur', 'Pam', 'Maruk', 'Roi'])
    print personnages_tiled
    print personnages


# coordonnees sprites

def parle(texte=''):
    j = game.player

    j.forward(j.rect.width)
    coll_boxes = game.mask.get_box_collision_list( game.layers['personnage'], j)
    j.resume_to_backup()

    print 'je suis en ',game.player.get_rowcol()
    for p in coll_boxes:
        row,col = p.get_rowcol()
        nom = personnages.get((row,col), 'personne')
        print ("vous parlez à "+nom+"\nvous lui dites \'"+texte+"\'")

        if texte.lower() == ('bonjour '+nom).lower():
            ## tu as ete poli, le personnage te repond
            if nom == 'Roi':
                print("il vous répond :")
                print(""" « Puisque tu es venu(e) jusqu'à Moi, je vais te révèler la position de ceux de mes guerriers qui bon accueil te feront. Vas les voir immédiatement et salue les par leur nom. »
[utiliser amis = parle('bonjour Roi') pour mémoriser la liste, puis parle('bonjour Robin') face à Robin, etc.]""")
                amis = [(b - 9, 9 - a, guerriers_sympas[(a,b)]) for a,b in guerriers_sympas]
                print (amis)
                return amis
            elif nom == 'personne':
                print("personne ne vous répond.")
            elif (row, col) in guerriers_sympas:
                #cool c'est un guerrier sympa on a un cadeau
                print (nom + " vous répond : Bienvenue à toi !")
                for r in game.layers['cache']:
                    r_row,r_col= r.get_rowcol()
                    if r_col == col and r_row == row:
                        print("Voici un cadeau")
                        r.set_rowcol(r_row+1,r_col)
                        r.nom = 'potion'
                        game.layers['ramassable'].add(r)
                        print ("Il dépose une potion devant lui.")
                        game.mainiteration()
            else:
                #il y a quelqu'un de pas sympa ici
                print("Il répond : « Grrr »")
                print("Ne reste pas là !")
    print('')
#init('tiny_complete')
#avk(3);td();av()
