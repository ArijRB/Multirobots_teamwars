from gardenworld import *

def avk(k):
    for i in range(k):
        av()

personnages = {
    (4, 1):'Guldur',
    (4, 5): 'Thomas',
    (7, 3): 'Maruk',
    (15, 3): 'Milton',
    (15, 13):'Pim',
    (14, 15):'Pam',
    (17,13):'Poum',
    (7, 15):'Robin',
    (12, 13):'Mmouarf',
    (9,9):'Roi'
    }

def parle(texte=''):
    gw.game.player.forward(gw.game.player.rect.width)
    coll = gw.game.mask.get_box_collision_list(gw.game.groupDict, gw.game.player)
    gw.game.player.resume_to_backup()
    for j in coll:
        if j in gw.game.groupDict["personnages"]:
            row,col = j.y//32 , j.x // 32
            print row,col
            print ("vous parlez a "+personnages.get((row,col),'personne'))
            print(" vous lui dites \'"+texte+"\'")
            if texte == 'bonjour '+personnages.get((row,col),'personne'):
                print "yes!!"
                for r in gw.game.groupDict['cache']:
                    if r.rect.x//32 == col and r.rect.y//32 == row:
                        r.rect.y+= 32
                        gw.game.groupDict['ramassable'].add(r)


#init('tiny_complete')
#avk(3);td();av()
