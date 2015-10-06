from gardenworld import *

def avk(k):
    for i in range(k):
        av()

personnages = {
    (3, 1):'Guldur',
    (3, 5): 'Thomas',
    (7, 3): 'Maruk',
    (15, 3): 'Milton',
    (14, 15):'Pim',
    (15, 13):'Pam',
    (17,16):'Poum',
    (7,15):'Robin',
    (2, 13):'Mmouarf',
    (9,9):'Roi'
    }

def parle(texte=''):
    gw.game.player.forward(gw.game.player.rect.width)
    coll = gw.game.mask.get_box_collision_list(gw.game.groupDict, gw.game.player)
    gw.game.player.resume_to_backup()
    for j in coll:
        if j in gw.game.groupDict["personnages"]:
            row,col = j.y//32 , j.x // 32
            nom = personnages.get((row,col),'personne')
            print ("vous parlez a "+nom)
            print("vous lui dites \'"+texte+"\'")
            if texte.lower() == ('bonjour '+nom).lower():
                ## tu as ete poli, le personnage te repond
                if nom == 'Roi':
                    print("il vous repond:")
                    print("""Puisque tu es venue jusqu'a moi,je vais te reveler
la position de chacun de mes guerriers. Cet appel a la fonction parle() renvoie la liste en question""")
                    return [(i,j,personnages[(i,j)]) for i,j in personnages]
                for r in gw.game.groupDict['cache']:
                    if r.rect.x//32 == col and r.rect.y//32 == row:
                        print "il vous repond 'voici une potion en cadeau. je l'ai depose devant moi'"
                        r.rect.y+= 32
                        r.nom = 'potion'
                        gw.game.groupDict['ramassable'].add(r)
                        gw.game.mainiteration(gw.fps)



#init('tiny_complete')
#avk(3);td();av()
