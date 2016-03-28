from __future__ import absolute_import, print_function, unicode_literals
from core.spritebuilder import SpriteBuilder
from core import glo
import pygame
from collections import OrderedDict
import random
from core.sprite import MySprite,MovingSprite,SurfaceViergeSprite
from functools import wraps
import copy
import time
import os, sys

try:
    from toolz import first
except:
    def first(g): return next(iter(g))

from core.collisions2 import CollisionHandler2



def check_init_game_done(fun):
    """ decorator checking if init() has correctly been called before anything """
    @wraps(fun)
    def fun_checked(*args,**kwargs):
        get_game()
        return fun(*args,**kwargs)
    return fun_checked


def get_game():
    '''
    Safe way to get the instance of Game object.
    If game object is not initialized, raises an error
    '''
    try:
        Game.single_instance.screen
    except:
        raise Exception('Vous devez appeler la fonction init() avant toute chose')

    return Game.single_instance





class Game(object):
    """ Design Pattern 'Singleton', so only one instance of Game can exist """
    single_instance = None
    def __new__(cls, *args, **kwargs):
        if cls.single_instance is None:
            cls.single_instance = object.__new__(cls, *args, **kwargs)

        return cls.single_instance


    def __init__(self, fichiercarte=None, _SpriteBuilder=None,screen_width=None,screen_height=None):
        # if no parameter is given, then __init__ will just create an empty Game object
        if fichiercarte is None or _SpriteBuilder is None:
            return

        #reset pygame
        pygame.quit() ; pygame.init()

        # callbacks is a dictionary of functions to call depending on key pressed
        self.callbacks = {}

        # charge la carte et le spritesheet
        self.spriteBuilder = _SpriteBuilder(fichiercarte)


        # cree la fenetre pygame
        if screen_width is None or screen_height is None:
            screen_width = self.spriteBuilder.spritesize * self.spriteBuilder.rowsize
            screen_height = self.spriteBuilder.spritesize * self.spriteBuilder.colsize
        else:
            assert (screen_width % self.spriteBuilder.spritesize)== 0 and (screen_height % self.spriteBuilder.spritesize)== 0, 'Attention : La taille de la fenetre doit etre un multiple de la taille des sprites'

        self.screen = pygame.display.set_mode([screen_width,screen_height])


        pygame.display.set_caption("pySpriteWorld Experiment")
        self.spriteBuilder.screen = self.screen

        #self.fps = 10
        self.frameskip = 0
        self.auto_refresh = True

        # converti les sprites meme format que l'ecran
        self.spriteBuilder.prepareSprites()

        # cree un groupe de sprites pour chaque layer
        self.layers = self.spriteBuilder.buildGroups()
        pass
        # cherche le premier sprite joueur
        if (len(self.layers["joueur"]) > 0):
            self.player = first(self.layers["joueur"])

        # prepare le bitmap 'background'
        self.background = pygame.Surface([self.screen.get_width(), self.screen.get_height()]).convert()
        self.layers["bg1"].draw(self.background)
        self.layers["bg2"].draw(self.background)

        # cree un masque de la taille de l'ecran, et calcule les collisions
        self.mask = CollisionHandler2(self.screen,self.spriteBuilder.spritesize,self)
        self.mask.update_fastCollider(self.layers)

        # click clock
        self.clock = 0
        self.framecount = 0
        self.auto_refresh = True
        self.surfaceDessinable = None
        self.pen_color = (255,0,0)

    def update(self):
        for layer in glo.NON_BG_LAYERS:
            self.layers[layer].update()

    def draw(self):
        self.screen.blit(self.background, (0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()))
        for layer in glo.NON_BG_LAYERS:
            if layer != "cache":
                self.layers[layer].draw(self.screen)

        pygame.display.flip()


    def prepare_dessinable(self):
        if self.surfaceDessinable is None:
            s = SurfaceViergeSprite('dessinable',0,0,self.screen.get_width(), self.screen.get_height())
            self.layers['dessinable'].add( s )
            self.surfaceDessinable = s.image




    def mainiteration(self,allow_frameskip=True,check_auto_refresh_flag=False):
        '''
        If check_auto_refresh_flag is True then it will first check that self.auto_refresh is True (otherwise quit)

        Calls self.update() and self.draw()
            => immediately if
                - allow_frameskip==False

            => Once every game.frameskip iterations otherwise
                - mode is 'allow_skip_frames'
        '''

        if check_auto_refresh_flag and not self.auto_refresh:
            return

        self.framecount += 1
        if not allow_frameskip or (self.framecount > self.frameskip):

            self.framecount = 0
            self.update()
            self.draw()

            if os.environ.get("SDL_VIDEODRIVER") != 'dummy': # if there is a real x-server
                if pygame.event.peek():
                    for event in pygame.event.get():  # User did something
                        if event.type == pygame.QUIT:  # If user clicked close
                            pygame.quit()
                            quit()


    def mainloop(self):
        while True:
            self.mainiteration()


    #def throw_rays(self,sprite,radian_angle_list,coords=None,show_rays=False):
    #    mask.update_bitmasks()



    ############## MANAGE SPRITES (ADDITION, DELETION) ################

    def del_sprite(self,s):
        ''' delete sprite '''
        s.kill()
        try:
            self.mask.remove_sprite(s)
        except:
            pass

    def del_all_sprites(self,layername):
        ''' delete all sprites
            for example, call del_all_sprites('dessinable') '''
        while self.layers[layername]:
            s = first(self.layers[layername])
            self.del_sprite(s)

    def add_sprite_to_layer(self,s,layername):
        if layername == 'joueur' and self.mask.check_collision_and_update(s):
            return False
        else:
            self.layers[layername].add(s)
            self.mask.add_or_update_sprite(s)
            self.mainiteration(check_auto_refresh_flag=True)
            return True


    def add_new_sprite(self,layername,tileid,xy,tiled=False):
        assert type(xy) is tuple
        x,y = xy

        if tiled:
            x,y = x*self.spriteBuilder.spritesize,y*self.spriteBuilder.spritesize

        s = self.spriteBuilder.basicSpriteFactory(layername,tileid,x,y)
        if self.add_sprite_to_layer(s,layername):
            if layername == 'joueur' and len(self.layers['joueur'])==1:
                self.player = s
            return s
        else:
            return False


    def add_players(self,xy,player=None,tiled=False):
        """
            Attemps to add one or many new players at position x,y
            Fails if the new player is colliding something, and then return False
            if success, then adds the new player to group of players and returns its reference
            :param xy:  either a tuple (x,y) of coordinates of the new sprite, either an iterable of tuples ((x1,y1),(x2,y2)...)
            :param player: an existing players or None. If not None, this function will use player.image for the new player
            :param tiled: if True, then x and y are not in pixel coordinates but tile coordinates
            :param draw_now: if True, then the main iteration loop is called
            :return: the list of sprites created successfully
            :example:
            >>> # Here, the attempt to create a new sprite fails because of collision
            >>> game.add_players( (2,3) , game.player )
            []
        """
        try:
            tileid = player.tileid
        except:
            tileid = None

        return self.add_new_sprite('joueur',tileid,xy,tiled)
