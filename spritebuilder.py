from spritesheet_functions import SpriteSheet
import json
import glo
import pygame
from collections import OrderedDict
from sprite import MySprite,MovingSprite,RecursiveDrawGroup
from players import Player,Turtle
import os


class SpriteBuilder(object):
    '''
        cette classe charge le fichier TMX decrivant la carte du monde
        ensuite, elle cree des sprites et des groupes de sprites

        Remarque: dans le fichier TMX, il y a le nom du fichier image des sprites,
                  qui est charge aussi par la fonction load_sprite_sheet()
    '''


    carte    = None                 # json data from file
    sheet    = None                 # SpriteSheet object
    spritesize = 0                  # sprite size in pixels (assume its a square)
    rowsize,colsize = None,None     # number of sprites in a row , column


    def __init__(self, file_name):
        ''' (1) charge le fichier TMX
            (2) charge le fichier image ou se trouvent les sprites dans l'objet sheet
        '''
        dirname = os.path.dirname(os.path.abspath(__file__))

        with open(dirname + "/" + file_name, 'r') as f:
            self.carte = json.load(f)

        assert self.carte["tilewidth"]==self.carte["tileheight"], "les sprites doivent etre carres"

        self.spritesize               = self.carte["tilewidth"]
        self.rowsize , self.colsize   = self.carte["width"],self.carte["height"]

        try:
            sheet_filename  = dirname + "/" + self.carte["tilesets"][0]["image"]
            self.sheet      = SpriteSheet(sheet_filename,self.spritesize)
        except pygame.error:
            try:
                sheet_filename  = dirname + "/Cartes/" + self.carte["tilesets"][0]["image"]
                self.sheet      = SpriteSheet(sheet_filename,self.spritesize)
            except pygame.error as e2:
                print "Error - impossible de trouver le fichier images des sprites -"
                raise e2

    def prepareSprites(self):
        self.sheet.convert_sprites()


    def buildGroups(self):
        """ builds one group of sprites for each layer """

        # build ordered dictionary - first add groups from glo.ALL_LAYERS, with correct order
        Grps = OrderedDict( [(gr,self.basicGroupFactory(gr)) for gr in glo.ALL_LAYERS])
        Grps.update( {l["name"]:self.basicGroupFactory(l["name"]) for l in self.carte["layers"] if l["name"] not in Grps} )


        for l in self.carte["layers"]:
            layername = l["name"]
            g = Grps[layername]

            for idx,e in enumerate(l["data"]):
                y,x = (idx // self.rowsize)*self.spritesize , (idx % self.rowsize)*self.spritesize
                if e > 0:
                    self.basicSpriteFactory( Grps , layername , self.sheet.get_row_col(e-1) , x,y , self.sheet[e-1])

        return Grps

    ##########  Methodes a surcharger pour adapter la classe ##########
    @classmethod
    def basicSpriteFactory(self,spritegroups , layername,tileid,x,y,img):
        if layername == "joueur":
            spritegroups[layername].add( Player(layername,tileid,x,y,[img]) )

        elif layername == "ramassable":
            spritegroups[layername].add( MovingSprite(layername,tileid,x,y,[img]) )
        else:
            spritegroups[layername].add( MySprite(layername,tileid,x,y,[img]) )

    @classmethod
    def basicGroupFactory(self,layername):
        if layername in ["eye_candy","joueur"]:
            return RecursiveDrawGroup()
        else:
            return pygame.sprite.Group()

    ##################################################################
