# -*- coding: utf-8 -*-
from gardenworld import *

def avk(k):
    for i in range(k):
        av()

#coordonnees Tiled.app
personnages_tiled = {
    (1, 4):'Guldur',
    (5, 3): 'Thomas',
    (3, 7): 'Maruk',
    (3, 15): 'Milton',
    (15, 14):'Pim',
    (13, 15):'Pam',
    (16, 17):'Poum',
    (15, 7):'Robin',
    (13, 2):'Mmouarf',
    (9, 9):'Roi'
    }

# coordonnees sprites
personnages = dict(((y, x), personnages_tiled[x,y]) for (x, y) in personnages_tiled)

guerriers_sympas = dict((k, personnages[k]) for k in personnages if personnages[k] not in ['Guldur', 'Pam', 'Maruk', 'Roi'])

def parle(texte=''):
    j = game.player

    j.forward(j.rect.width)
    coll_boxes = game.mask.collision_list( j , {'personnage'})
    j.resume_to_backup()

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
