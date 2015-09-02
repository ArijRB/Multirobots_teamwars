from gameclass import Game
from spritebuilder import SpriteBuilder
import pygame
import constants




game = Game('Cartes/gardenofdelight.json',SpriteBuilder)
game.setup_keyboard_callbacks()

print """regles du Jeu :
         deplacer le joueur avec les touches du clavier
         taper c pour chercher un objet ramassable
         taper r pour ramasser
         taper d pour deposer
         taper t pour lancer le telemetre
         le but est de transferer 8 laitues dans l'enclos du chateau"""

game.mainloop()
