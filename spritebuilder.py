from spritesheet_functions import SpriteSheet
import json
import constants
import pygame
from collections import OrderedDict
from sprite import MySprite,MovingSprite,Player


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
        with open(file_name, 'r') as f:
            self.carte = json.load(f)

        assert self.carte["tilewidth"]==self.carte["tileheight"], "les sprites doivent etre carres"

        self.spritesize               = self.carte["tilewidth"]
        self.rowsize , self.colsize   = self.carte["width"],self.carte["height"]

        try:
            sheet_filename  = self.carte["tilesets"][0]["image"]
            self.sheet      = SpriteSheet(sheet_filename,self.spritesize)
        except Exception as e:
            print "Error - impossible de trouver le fichier images des sprites -"
            raise e

    def prepareSprites(self):
        self.sheet.convert_sprites()


    def build_one_group(self,layername):
        """
            input: a layername. for example "bg1"
            output: an object pygame.sprite.Group containing all sprites from specified layer
        """
        g = self.basicGroupFactory()
        for l in self.carte["layers"]:
            if l["name"] == layername:
                for idx,e in enumerate(l["data"]):
                    y,x = (idx // self.rowsize)*self.spritesize , (idx % self.rowsize)*self.spritesize
                    if e > 0:
                        self.basicSpriteFactory( g , layername , self.sheet.get_row_col(e-1) , x,y , self.sheet[e-1])
        return g


    def buildGroups(self):
        """ builds one group of sprites for each layer """
        return OrderedDict( [ (name,self.build_one_group(name)) for name in constants.ALL_LAYERS ] )

    ##########  Methodes a surcharger pour adapter la classe ##########

    def basicSpriteFactory(self,spritegroup , layername,tileid,x,y,img):
        if layername == "joueur":
            spritegroup.add( Player(tileid,x,y,img) )
        else:
            spritegroup.add( MySprite(tileid,x,y,img) )

    def basicGroupFactory(self):
        return pygame.sprite.Group()

    ##################################################################
