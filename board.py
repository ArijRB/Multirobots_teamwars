from spritesheet_functions import SpriteSheet
import json
import constants
import pygame
from spritefactory import basicSpriteFactory
from collections import OrderedDict


class Board(object):
    '''
        cette classe charge le fichier TMX decrivant la carte du monde
        Pour editer les fichiers TMX, utiliser l'application Tiled

        Remarque: dans le fichier TMX, il y a le nom du fichier image des sprites,
                  qui est charge aussi par la fonction load_sprite_sheet()
    '''
    carte    = None
    sheet    = None
    spritesize = None
    # number of sprites in a row , column
    rowsize,colsize = None,None


    def __init__(self, file_name):
        ''' (1) charge le fichier TMX
            (2) charge le fichier image ou se trouvent les sprites dans l'objet sheet
        '''
        with open(file_name, 'r') as f:
            self.carte = json.load(f)

        self.spritesize               = self.carte["tilewidth"]
        self.rowsize , self.colsize   = self.carte["width"],self.carte["height"]

        try:
            sheet_filename  = self.carte["tilesets"][0]["image"]
            self.sheet      = SpriteSheet(sheet_filename,self.spritesize)
        except Exception as e:
            print "Error - impossible de trouver le fichier images des sprites -"
            raise e


    def build_sprite_group(self,layername,spriteFactory):
        """
            input: a layername. for example "bg1"
            output: an object pygame.sprite.Group containing all sprites from specified layer
        """
        g = pygame.sprite.Group()
        for l in self.carte["layers"]:
            if l["name"] == layername:
                for idx,e in enumerate(l["data"]):
                    i,j = idx // self.rowsize , idx % self.rowsize
                    if e > 0:
                        print "layer=",layername," , idx=",idx," , e=",e," , i,j=",i,j
                        spr = spriteFactory( layername , *self.sheet.get_row_col(e-1) )
                        spr.image = self.sheet[e-1]
                        spr.rect  = spr.image.get_rect()
                        spr.rect.x , spr.rect.y = j*self.spritesize , i*self.spritesize
                        g.add(spr)
        return g



    def build_sprite_groups(self,spriteFactory = basicSpriteFactory ):
        return OrderedDict( [ (name,self.build_sprite_group(name,spriteFactory)) for name in constants.ALL_LAYERS ] )
