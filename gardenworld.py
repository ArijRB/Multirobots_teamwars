from gameclass import Game
from spritebuilder import SpriteBuilder
from players import Player
from ontology import Ontology
import pygame
import glo

"""
    Ce fichier est specifique au sprite dans le monde discret (e.g. tiles 32x32),
    Il contient aussi les commandes de base (tournegauche, avance...)
"""


class GardenSpriteBuilder(SpriteBuilder):
    """ classe permettant d'afficher le personnage sous 4 angles differents
    """

    def basicSpriteFactory(self, spritegroups, layername, tileid, x, y, img):
        if layername == "joueur":
            imglist = [self.sheet[i, j] for i, j in ((10, 0), (8, 0), (9, 0), (11, 0))]
            p = Player(layername, tileid, x, y, imglist)
            if tileid[0] in [10, 8, 9, 11]:
                p.translate_sprite(0, 0, 90 * [10, 8, 9, 11].index(tileid[0]))
            spritegroups[layername].add(p)
        else:
            SpriteBuilder.basicSpriteFactory(spritegroups, layername, tileid, x, y, img)


#############################################################################

class gw:
    game = None
    fps = None
    O = None
    name = 'gardenofdelight'


def init(_boardname=None):
    global player
    pygame.quit()
    if _boardname: gw.name = _boardname
    gw.fps = 4  # frames per second
    gw.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    gw.game = Game('Cartes/' + gw.name + '.json', GardenSpriteBuilder)
    gw.game.mainiteration(60)
    player = gw.game.player


def tournegauche():
    try:
        player.translate_sprite(0, 0, -90)
        gw.game.mainiteration(gw.fps)
    except NameError:
        print("Erreur: appeler la fonction init() avant toute chose")

def tournedroite():
    try:
        player.translate_sprite(0, 0, 90)
        gw.game.mainiteration(gw.fps)
    except NameError:
        print("Erreur: appeler la fonction init() avant toute chose")


def avance():
    try:
        player.forward(player.rect.width)
        gw.game.mainiteration(gw.fps)
        return player.position_changed()
    except NameError:
        print("Erreur: appeler la fonction init() avant toute chose")


def ramasse():
    try:
        o = gw.game.player.ramasse(gw.game.groupDict)
        gw.game.mainiteration(gw.fps)
        return gw.O.firstname(o)
    except NameError:
        print("Erreur: appeler la fonction init() avant toute chose")


def obstacle():
    try:
        player.forward(player.rect.width)
        c = gw.game.mask.check_box_collisions_single_player(gw.game.groupDict, player)
        player.resume_to_backup()
        return c
    except NameError:
        print("Erreur: appeler la fonction init() avant toute chose")


def depose(nom=None):
    try:
        def _filtre(o): return nom in gw.O.names(o) + [None]

        o = player.depose(gw.game.groupDict, _filtre)
        gw.game.mainiteration(gw.fps)
        return gw.O.firstname(o)
    except NameError:
        print("Erreur: appeler la fonction init() avant toute chose")


def cherche(nom=None):
    try:
        def _filtre(o): return nom in gw.O.names(o) + [None]

        o = player.cherche_ramassable(gw.game.groupDict, _filtre)
        gw.game.mainiteration(gw.fps)
        return gw.O.firstname(o)
    except NameError:
        print("Erreur: appeler la fonction init() avant toute chose")



tg, td, av, ra, dp, ch, reset, ob = tournegauche, tournedroite, avance, ramasse, depose, cherche, init, obstacle
