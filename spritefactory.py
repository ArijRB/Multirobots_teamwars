import pygame
import constants
from sprite import MySprite,MovingSprite




def basicSpriteFactory(layername,tileid,x,y,img):
    if layername   == "joueur":
        return MovingSprite(tileid,x,y,img)
    else:
        return MySprite(tileid,x,y,img)
