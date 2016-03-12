import pygame
import pygame.sprite
import random
from itertools import chain
import fast_rect_collision
from sprite import MovingSprite



class CollisionHandler2:
    pixel_perfect = True             # calls pixel_collision otherwise box_collision
    allow_overlaping_players = False

    def __init__(self, screen,spritesize,g):
        self.game = g
        self.mask_obstacles = pygame.mask.from_surface(screen)
        self.mask_players   = pygame.mask.from_surface(screen)

        self.mask_obstacles.clear()
        self.mask_players.clear()

        wh = max( screen.get_width() , screen.get_height() )
        self.fastGroupCollide = fast_rect_collision.FastGroupCollide(group={},display_size=wh,max_interv=spritesize)


    def _erase_player_mask(self, spr, backup=False):
        self.mask_players.erase(spr.mask, spr.get_pos(backup))

    def _draw_player_mask(self, spr, backup=False):
        self.mask_players.draw(spr.mask, spr.get_pos(backup))

    def _collide_player_w_players(self, spr, backup=False):
        return self.mask_players.overlap(spr.mask, spr.get_pos(backup))

    def _collide_player_w_obstacles(self, spr, backup=False):
        return self.mask_obstacles.overlap(spr.mask, spr.get_pos(backup))

    def _fill_with_sprites(self, bitmask , group, backup=False):
        bitmask.clear()
        for spr in group:
            bitmask.draw(spr.mask, spr.get_pos(backup))

    #### Interface to fastGroupCollide

    def add_or_update_sprite(self,spr):
        self.fastGroupCollide.add_or_update_sprite(spr)

    def remove_sprite(self,spr):
        self.fastGroupCollide.remove_sprite(spr)

    def sprites_on_tile(self,i,j,group_filter=None):
        l = self.fastGroupCollide.get_all_sprites_on_tile(i,j)
        return _filter_by_layername(l,group_filter)

    def _naive_collision_check(self,spr):
        sz = self.fastGroupCollide.array_size
        arr= self.fastGroupCollide.array
        interv = self.fastGroupCollide.max_interval

        i0,j0 = spr.rect.y // interv , spr.rect.x // interv

        if self.out_of_screen(spr):
            return True
        biggroup = list(self.game.layers['joueur']) + list(self.game.layers['obstacle'])
        for s2 in biggroup:
        #for i in range(i0-1,i0+2):
        #    for j in range(j0-1,j0+2):
        #        if i >= 0 and j >= 0 and i < sz and j < sz:
        #            l = arr[i,j]
        #            for cys in l:
        #                s2 = cys.sprite
            if pygame.sprite.collide_mask(s2,spr) and id(s2) != id(spr):
                return True
        return False

    def collision_list(self,s,group_filter=None):
        l = self.fastGroupCollide.compute_collision_list(s,pygame.sprite.collide_mask)
        return _filter_by_layername(l,group_filter)

    def collision_blocking_player(self,s):
        blockinglayers = {'obstacle'} if self.allow_overlaping_players else {'obstacle','joueur'}
        return self.collision_list(s,blockinglayers)

    def check_collision_and_update(self,s):
        #if self.collision_blocking_player(s) or self.out_of_screen(s):
        if self._naive_collision_check(s):
            return True
        else:
            self.add_or_update_sprite(s)
            return False

    def collision_with_point(self,x,y,group_filter):
        s = PointSprite(x=x,y=y)
        return self.collision_list(s,group_filter)

    ###############  compute collision ###################

    def update_bitmasks(self,gDict):
        self._fill_with_sprites(self.mask_obstacles,gDict["obstacle"])
        self._fill_with_sprites(self.mask_players,gDict["joueur"])

    def update_fastCollider(self,gDict):
        good_layernames = set(gDict) - {'bg1','bg2','dessinable'}
        for layername in good_layernames:
            for spr in gDict[layername]:
                self.fastGroupCollide.add_or_update_sprite(spr)


    def synchronous_collision_handler(self, gDict,_safe_collision=True):

        persos = list(gDict["joueur"])

        allow_overlap = CollisionHandler2.allow_overlaping_players
        multi_player_and_not_allow_overlap = len(persos)>1 and not allow_overlap

        random.shuffle(persos)

        self._fill_with_sprites(self.mask_obstacles,gDict["obstacle"])
        self.mask_players.clear()

        # test if sprites at backup position do not collide anything and draw them on the mask
        for j in persos:
            if _safe_collision:
                assert not self._collide_player_w_obstacles(j, backup=True), "sprite collision with obstacles before any movement !!!"
                if multi_player_and_not_allow_overlap:
                    assert not self._collide_player_w_players(j, backup=True), "sprite collision before any movement !!!"
                    self._draw_player_mask(j, backup=True)

        # try their new position one by one

        for j in persos:

            if multi_player_and_not_allow_overlap: self._erase_player_mask(j, backup=True)

            c1 = self._collide_player_w_obstacles(j)
            c2 = self._collide_player_w_players(j)


            if c1 or (c2 and not allow_overlap) or self.out_of_screen(j):
                j.resume_to_backup()

            self._draw_player_mask(j)


        self.update_fastCollider(gDict)
        MovingSprite.up_to_date = True


    def out_of_screen(self, player):
        w, h = self.mask_obstacles.get_size()
        w -= player.rect.w
        h -= player.rect.h
        return player.rect.x > w or player.rect.x < 0 or player.rect.y > h or player.rect.y < 0




def _filter_by_layername(lst,layernames):
    return [s for s in lst if (layernames is None or s.layername in layernames)]


''' UNUSED CODE :

    self._collision_lock = None # if not None, then cannot call 'handle_collision'
                                # allows external functions to use self.mask,
                                # without risking this mask to be modified by handle_collision

    def capture_lock(self,name):
        assert self._collision_lock is None
        self._collision_lock = name

    def release_lock(self,name):
        assert self._collision_lock == name
        self._collision_lock = None

    self.capture_lock('handle_collision')
    self.release_lock('handle_collision')

'''