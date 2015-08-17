from gameclass import Game
from spritebuilder import SpriteBuilder
import pygame
import constants

class GameKeyboard(Game):
    rayon_hit_point = None

    def update(self,event):
        game.player.move_with_keyboard(event,game.player.rect.width)
        game.player.ramasse_depose_with_keyboard(event,game.groupDict)
        game.player.throw_ray_with_keyboard(event,game.mask)
        Game.update(self,None)
        self.rayon_hit_point = game.player.throw_ray_with_keyboard(event,game.mask)

    def draw(self):
        self.screen.blit(self.background, (0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()))

        for layer in constants.NON_BG_LAYERS:
            if layer == "joueur" and self.rayon_hit_point != None:
                pygame.draw.line(self.screen,(255,0,0),(game.player.center_x,game.player.center_y),self.rayon_hit_point,4)
            self.groupDict[layer].draw(self.screen)

        self.clock.tick(60)
        pygame.display.flip()


if __name__ == '__main__':

    game = GameKeyboard('Cartes/gardenofdelight.json',SpriteBuilder)

    print """regles du Jeu :
             deplacer le joueur avec les touches du clavier
             taper c pour chercher un objet ramassable
             taper r pour ramasser
             taper d pour deposer
             taper t pour lancer le telemetre
             le but est de transferer 8 laitues dans l'enclos du chateau"""

    game.mainloop()
