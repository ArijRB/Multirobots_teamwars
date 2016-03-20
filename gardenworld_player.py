import pygame
from core.sprite import MySprite,MovingSprite,Player,RecursiveDrawGroup,DrawOnceSprite
from functools import partial
from random import random



class GardenPlayer(Player):
    """ cette classe modelise un sprite controlable par l'utilisateur
        soit au tile pres, soit au pixel pres
        soit au clavier directement, soit par instructions
    """
    def __init__(self,*args,**kwargs):
        MovingSprite.__init__(self,*args,**kwargs)
        self.inventory = pygame.sprite.Group()


    def cherche_ramassable(self,layers,filtre = lambda x:True,verb=False):
        for obj in layers["ramassable"]:
            if filtre(obj):
                if self.mask.overlap(obj.mask,(obj.rect.x - self.rect.x,obj.rect.y - self.rect.y)):
                    if verb: print ("j'en ai trouve un")
                    return obj
        if verb: print ("rien a ramasser")
        return None

    def ramasse(self,layers,verb=False):
        o = self.cherche_ramassable(layers)
        if o is None:
            if verb: print ("rien a ramasser")
            return None
        self.inventory.add( o )
        o.remove( layers.values() )
        return o


    def depose(self,layers,filtre = lambda x:True,verb=False):
        # remove object from existing groups displayed on the screen
        candidats = [o for o in self.inventory if filtre(o)]

        if not candidats:
            if verb: print ("rien a deposer")
            return None
        obj = candidats[0]
        self.inventory.remove( obj )
        obj.translate_sprite(self.x,self.y,0,False)
        layers['ramassable'].add( obj )
        return obj



