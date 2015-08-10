from gameclass import Game
from spritebuilder import SpriteBuilder
import pygame

if __name__ == '__main__':

    game = Game('data/gardenofdelight.json',SpriteBuilder)

    while True:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                pygame.quit()
                quit()

            game.player.move_with_keyboard(event,game.player.rect.width)

            game.update()
            game.draw()
