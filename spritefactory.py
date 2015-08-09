import pygame
import constants
from sprite import MySprite,MovingSprite




def basicSpriteFactory(layername,row,col):
    if layername   == "joueur":
        return MovingSprite(row,col)
    else:
        return MySprite(row,col)
