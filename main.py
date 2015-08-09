from board import Board
import constants
import pygame
from spritefactory import basicSpriteFactory
from collections import OrderedDict
from toolz import first

if __name__ == '__main__':

    pygame.init()

    #board  = Board('TileWorld/gardenofdelight.json')
    board  = Board('TileWorld/le_terrain_2Ddemi.json')

    screen = pygame.display.set_mode([ board.spritesize*board.rowsize ,  board.spritesize*board.colsize ])
    pygame.display.set_caption("Pygame Experiment")

    board.sheet.convert_sprites()
    groupdict = board.build_sprite_groups(basicSpriteFactory)

    try:
        player = first(groupdict["joueur"])
    except Exception:
        raise IndexError("Je ne trouve pas de joueur dans le fichier TMX")


    # prepare background surface
    background = pygame.Surface([ screen.get_width(), screen.get_height() ]).convert()
    groupdict["bg1"].draw(background)
    groupdict["bg2"].draw(background)

    clock = pygame.time.Clock()

    done = False
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_x = -32
                if event.key == pygame.K_RIGHT:
                    player.change_x =  32
                if event.key == pygame.K_UP:
                    player.change_y = -32
                if event.key == pygame.K_DOWN:
                    player.change_y =  32

            player.update(screen,groupdict["obstacles"])

            if player.rect.x >= screen.get_width():
                player.rect.x = screen.get_width()

            if player.rect.x < 0:
                player.rect.x = 0

        screen.blit(background, (0, 0), (0, 0, screen.get_width(), screen.get_height()))

        for layer in constants.NON_BG_LAYERS:
            groupdict[layer].draw(screen)

        clock.tick(60)
        pygame.display.flip()


    pygame.quit()
