from gameclass import Game
from spritebuilder import SpriteBuilder
import pygame
import constants

class GameKeyboard(Game):
    rayon_hit_point = None

    def update(self,event):
        game.player.move_with_keyboard(event,game.player.rect.width)
        game.player.ramasse_depose_with_keyboard(event,game.groupDict)
        self.rayon_hit_point =game.player.throw_ray_with_keyboard(event,game.mask,game.groupDict)
        Game.update(self,None)



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
