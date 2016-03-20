def gen_callbacks(player,incr,gDict,mask):
    transl = player.translate_sprite
    return {
        pygame.K_LEFT:  partial(transl,x= -incr , y=0, a=0),
        pygame.K_RIGHT: partial(transl,x=  incr , y=0, a=0),
        pygame.K_UP:    partial(transl,x=  0    , y= -incr, a=0),
        pygame.K_DOWN:  partial(transl,x=  0    , y=  incr, a=0),
        pygame.K_c:     partial(player.cherche_ramassable,layers=gDict,verb=True),
        pygame.K_r:     partial(player.ramasse,layers=gDict,verb=True),
        pygame.K_d:     partial(player.depose,layers=gDict,verb=True),
        pygame.K_t:     partial(player.throw_ray,radian_angle=None,mask=mask,layers=gDict)
    }

#
#    def setup_keyboard_callbacks(self):
#        self.callbacks = self.player.gen_callbacks(self.player.rect.w, self.layers, self.mask)
