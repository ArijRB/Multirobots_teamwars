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
    gw.game.player.forward(gw.game.player.rect.width)
    coll = gw.game.mask.get_box_collision_list(gw.game.groupDict, gw.game.player)
    gw.game.player.resume_to_backup()
    for j in coll:
        if j in gw.game.groupDict["personnages"]:
            row,col = j.y//32 , j.x // 32
            nom = personnages.get((row,col), 'personne')
            print ("vous parlez à "+nom)
            print("vous lui dites \'"+texte+"\'")
            if texte.lower() == ('bonjour '+nom).lower():
                ## tu as ete poli, le personnage te repond
                if nom == 'Roi':
                    print("il vous répond :")
                    print(""" « Puisque tu es venu(e) jusqu'à Moi, je vais te révèler la position de ceux de mes guerriers qui bon accueil te feront. Vas les voir immédiatement et salue les par leur nom. »
[utiliser amis = parle('bonjour Roi') pour mémoriser la liste, puis parle('bonjour Robin') face à Robin, etc.]""")
                    amis = [(j - 9, 9 - i, guerriers_sympas[(i,j)]) for i,j in guerriers_sympas]
                    print amis
                    return amis
                elif nom == 'personne':
                    print("personne ne vous répond.")
                elif (row, col) in guerriers_sympas:
                    #cool c'est un guerrier sympa on a un cadeau
                    print nom + " vous répond : « Bienvenue à toi ! Voici un cadeau. »."
                    for r in gw.game.groupDict['cache']:
                        if r.rect.x//32 == col and r.rect.y//32 == row:
                            r.rect.y+= 32
                            r.nom = 'potion'
                            r.layername='ramassable'
                            gw.game.groupDict['ramassable'].add(r)
                            print  "Il dépose une potion devant lui."
                            gw.game.mainiteration(gw.fps)
                else:
                    #il y a quelqu'un de pas sympa ici
                    print("Il répond : « Grrr »")
                    print("Ne reste pas là !")

#init('tiny_complete')
#avk(3);td();av()
