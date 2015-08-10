from gameclass import Game
from spritebuilder import SpriteBuilder
import pygame

if __name__ == '__main__':

    game = Game('data/gardenofdelight.json',SpriteBuilder)

    print """regles du Jeu :
             deplacer le joueur avec les touches du clavier
             taper c pour chercher un objet ramassable
             taper r pour ramasser
             taper d pour deposer
             le but est de transferer 8 laitures dans l'enclos du chateau"""

    while True:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                pygame.quit()
                quit()

            game.player.move_with_keyboard(event,game.player.rect.width)
            game.player.ramasse_depose_with_keyboard(event,game.groupDict)

            game.update()
            game.draw()
