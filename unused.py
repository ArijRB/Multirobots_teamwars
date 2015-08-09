def display_spritegroup(self,surf,g):
    '''
        affiche dans la surface 'surf' tous les sprites des layers de layerlist
    '''
    for l in self.carte["layers"]:
        if l["name"] in layerlist:
            for idx,e in enumerate(l["data"]):
                i,j = idx // self.rowsize , idx % self.rowsize
                if e > 0:
                    surf.blit(self.sheet[e-1], (j*self.spritesize, i*self.spritesize), (0, 0, self.spritesize, self.spritesize))
