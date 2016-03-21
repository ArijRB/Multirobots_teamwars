from robosim import *
from random import random
from core.sprite import DrawOnceSprite

def main():
    init()
    game.auto_refresh = False
    DrawOnceSprite.lifespan = 1

    p2 = game.add_players( (160,123) , game.player , tiled=False)
    tournegauche( random()*360 ,p2)
    p3 = game.add_players( (110,50) , game.player , tiled=False)
    tournegauche( random()*360 ,p3)

    def throw(angles=[0]):
        d = throw_rays_for_many_players(game,game.layers['joueur'],angles,show_rays=True)
        efface()
        for p,l in d.items():
            for r in l:
                if r.layer == 'obstacle':
                    color((0,0,255))
                    circle(r.x,r.y)
                elif r.layer == 'joueur':
                    color((255,0,0))
                    circle(r.x,r.y)

    for i in range(360):
        tournegauche( 1 , game.player)
        tournegauche( -1 , p2)
        tournegauche( 1.5 , p3)
        throw()
        game.mainiteration()

if __name__ == '__main__':
    main()