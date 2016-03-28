import pygame
import pygame.sprite
import random
from itertools import chain
from core import fast_rect_collision
from core.sprite import MovingSprite,PointSprite



class CollisionHandler2:
    pixel_perfect = True             # calls pixel_collision otherwise box_collision
    allow_overlapping_players = False

    def __init__(self, screen,spritesize,g):
        self.game = g
        self.mask_obstacles = pygame.mask.from_surface(screen)
        self.mask_players   = pygame.mask.from_surface(screen)

        wh = max( screen.get_width() , screen.get_height() )
        self.fastGroupCollide = fast_rect_collision.FastGroupCollide(group={},display_size=wh,max_interv=spritesize)

    def _erase_player_mask(self, spr, backup=False):
        self.mask_players.erase(spr.mask, spr.get_pos(backup))

    def _draw_player_mask(self, spr, backup=False):
        self.mask_players.draw(spr.mask, spr.get_pos(backup))

    #def _erase_sprite_mask(self, spr, backup=False):
    #    if spr.layername == 'joueur':
    #    else:
    #        self.mask_obstacles.erase(spr.mask, spr.get_pos(backup))
    #
    #def _draw_sprite_mask(self, spr, backup=False):
    #    self.mask_obstacles.draw(spr.mask, spr.get_pos(backup))


    def _fill_with_sprites(self, bitmask , group, backup=False):
        bitmask.clear()
        for spr in group:
            bitmask.draw(spr.mask, spr.get_pos(backup))

    def update_bitmasks(self,layers):
        '''
        Call this function to make the obstacle and player mask
        '''
        self._fill_with_sprites(self.mask_obstacles,layers["obstacle"])
        self._fill_with_sprites(self.mask_players,layers["joueur"])

    #### Interface to fastGroupCollide


    def add_or_update_sprite(self,spr):
        self.fastGroupCollide.add_or_update_sprite(spr)

    def remove_sprite(self,spr):
        self.fastGroupCollide.remove_sprite(spr)

    def get_sprites_on_tile(self,i,j,group_filter=None):
        l = self.fastGroupCollide.get_all_sprites_on_tile(i,j)
        return [s for s in l if (group_filter is None or s.layername in group_filter)]

    def _naive_collision_check(self,spr):
        '''
        N^2 algorithm to compute collisions between sprites
        '''
        if self.out_of_screen(spr): return True

        biggroup = list(self.game.layers['obstacle']) + list(self.game.layers['joueur'])

        for s2 in biggroup:
            if pygame.sprite.collide_mask(s2,spr) and id(s2) != id(spr):
                return True
        return False

    def collision_list(self,s,group_filter=None):
        return self.fastGroupCollide.compute_collision_list(s,pygame.sprite.collide_mask,gFilter=group_filter)

    def collision_blocking_player(self,s):
        blockinglayers = {'obstacle'} if self.allow_overlapping_players else {'obstacle','joueur'}
        return self.collision_list(s,blockinglayers)

    def check_collision_and_update(self,s):
        if self.collision_blocking_player(s) or self.out_of_screen(s):
        #if self._naive_collision_check(s):
            return True
        else:
            self.add_or_update_sprite(s)
            return False

    def who_is_at(self,x,y,group_filter=None):
        '''
        who_is_at(x,y) returns the list of all sprites colliding the point (x,y)
        '''
        s = PointSprite(x=x,y=y)
        return self.collision_list(s,group_filter)

    def test_who_is_at():
        import gardenworld as gw

        gw.init()
        gw.game.mask.update_fastCollider(gw.game.layers)
        for i in range(25,40):
            print( 'i=',i,'  and  collisions=',gw.game.mask.who_is_at(i,i) )

    ###############  compute collision ###################

    def update_fastCollider(self,layers):
        good_layernames = set( layers.keys() ) - {'bg1','bg2','dessinable'}
        for layername in good_layernames:
            for spr in layers[layername]:
                self.fastGroupCollide.add_or_update_sprite(spr)


    def out_of_screen(self, player):
        w, h = self.mask_obstacles.get_size()
        w -= player.rect.w
        h -= player.rect.h
        return player.rect.x > w or player.rect.x < 0 or player.rect.y > h or player.rect.y < 0
