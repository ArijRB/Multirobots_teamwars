from gameclass import Game
from sprite import MySprite,MovingSprite,Player,Turtle
from spritebuilder import SpriteBuilder
import random
import math

class TurtleSpriteBuilder(SpriteBuilder):
    def basicSpriteFactory(self,spritegroups , layername,tileid,x,y,img):
        if layername == "joueur":
            j = Turtle(layername,tileid,x,y,img)
            spritegroups[layername].add( j )
            spritegroups["eye_candy"].add( j.build_fleche( "eye_candy" ) )
        else:
            SpriteBuilder.basicSpriteFactory(spritegroups,layername,tileid,x,y,img)

###########################################


class TurtleGame(Game):

    def update(self,event):
        angle_radian = random.random()*2*math.pi
        rayon_hit = game.player.throw_ray(angle_radian , game.mask,game.groupDict)
        if rayon_hit:
            if game.player.dist(*rayon_hit) > 10:
                game.player.translate_sprite(5*math.cos(angle_radian),5*math.sin(angle_radian))
        Game.update(self,None)



if __name__ == '__main__':

    game = TurtleGame('Cartes/robot_obstacles.json',TurtleSpriteBuilder)
    game.mainloop()
