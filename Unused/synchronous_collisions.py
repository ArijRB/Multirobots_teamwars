
# Used to be in collision2.py
# Unused function now...
    def synchronous_collision_handler(self, gDict,_safe_collision=True):

        persos = list(gDict["joueur"])

        allow_overlap = CollisionHandler2.allow_overlapping_players
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