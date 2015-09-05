import numpy as np
import csv
import sys
#import cytoolz # pip install cytoolz
from collections import defaultdict



def construit_ontologie(pairs=True,filename='tiny_spritesheet_ontology.csv'):
    '''
        Construit un dictionnaire (de type cles=pairs d entier ou juste entier, valeur=ensemble de strings)
        Ce dictionnaire decrit ce qu'il y a dans les tiles, en reprenant l information d un fichier csv

        Par exemple :

        si pairs = True, on a         ontology[(15,1)] = {'blob'}
        si pairs = False,on aurait    ontology[ 241 ]  = {'blob'}

        Car a la ligne 15, colonne 1 (qui est la 241 case) dans l'image data/tiny-Complete-Spritesheet-32x32.png, il y a un blob
        L'indexation commence a partir de 0.

        Si un tile est decrit par plusieurs elements e1,e2,e3  alors on rajoute a la fin l element e1-e2-e3
        Ainsi, ontology[(15,12)] = {'araignee', 'mort','araignee-mort'}
    '''

    ontology = {}
    f = open(filename, 'r')
    reader = csv.reader(f)
    for i,row in enumerate(reader):
        for j,s in enumerate(row):
            l = s.lower().split(' ')
            summary = '-'.join(l)
            if summary not in l:
                l.append(summary)
            ontology[(i,j) if pairs else i*len(row)+j] = l
    f.close()
    return ontology





def construit_categories(ontologie):
    '''
        cree un dictionnaire (key=categorie, valeur=ensemble d indexs)
        par exemple, on a:
        >>> c["salade"]
        set([(10, 11)])
        >>> c["citrouille"]
        set([(10, 12)])
        >>> c["epinards"]
        set([(2, 8)])
    '''
    cat = defaultdict(set)

    for idx,descr in ontologie.iteritems():
        for nom in descr:
            cat[nom].add( idx )
    return cat


def construit_ontologie_complete(pairs=True):
    onto = construit_ontologie(pairs)
    cate = construit_categories(onto)
    return onto , cate
