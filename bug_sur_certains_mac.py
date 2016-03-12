import pygame
import glo

pygame.init()
screen = pygame.display.set_mode([512,512])
background = pygame.Surface([512,512]).convert()

file_name = 'SpriteSheet-32x32/tiny-Complete-Spritesheet-32x32-fruits.bmp'
sprite_sheet = pygame.image.load(file_name)


s = pygame.Surface([32, 32])
s.blit(sprite_sheet, (0, 0), (32*11,32*4, 32,32))
screen.blit(s, (32, 32))

s2 = pygame.Surface([32, 32])
s2.blit(sprite_sheet, (0, 0), (32*11,32*4-16, 32,32))
screen.blit(s2, (96, 32))

s = pygame.Surface([32, 32])
s.blit(sprite_sheet, (0, 0), (32*11,32*4+1, 32,32))
screen.blit(s, (160, 32))


pygame.display.flip()

raw_input()
