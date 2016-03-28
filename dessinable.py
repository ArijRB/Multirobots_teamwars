import core.gameclass
import pygame


def frameskip(n):
    """
    frameskip(n) n'affichera qu'une image sur n.
    frameskip(0) affiche tout, et donc c'est assez lent.
    """
    core.gameclass.get_game().frameskip = n

def color(c):
    """
    color(c) change la couleur du dessin.
    par exemple, pour avoir du bleu, faire color((0,255,0))
    Attention, il y a un bug: la couleur bleue ne fonctionne pas
    """
    core.gameclass.get_game().pencolor = c

def efface(force_efface_tout=False):
    """
    efface()     efface les dessins crees avec circle, pendown, etc...
    efface(True) efface aussi les rayons lances par les joueurs
    """
    game = core.gameclass.get_game()
    if force_efface_tout:
        game.del_all_sprites('dessinable')
    game.prepare_dessinable()
    game.surfaceDessinable.fill( (0,0,0) )
    game.mainiteration(check_auto_refresh_flag=True)

def line(x1,y1,x2,y2):
    """
    line(x1,y1,x2,y2,wait=False) dessine une ligne de (x1,y1) a (x2,y2)
    si wait est True, alors la mise a jour de l'affichage est differe, ce qui
    accelere la fonction.
    """
    game = core.gameclass.get_game()
    game.prepare_dessinable()
    pygame.draw.aaline(game.surfaceDessinable, game.pencolor, (int(x1),int(y1)), (int(x2),int(y2)))
    game.mainiteration(check_auto_refresh_flag=True)

def circle(x1,y1,r=10):
    """
    circle(x,y,r) dessine un cercle
    si wait est True, alors la mise a jour de l'affichage est differe, ce qui
    accelere la fonction.
    """
    game = core.gameclass.get_game()
    game.prepare_dessinable()
    pygame.draw.circle(game.surfaceDessinable, game.pencolor, (int(x1),int(y1)), r)

    game.mainiteration(check_auto_refresh_flag=True)


def taille_terrain():
    return core.gameclass.get_game().screen.get_width(),core.gameclass.get_game().screen.get_height()
