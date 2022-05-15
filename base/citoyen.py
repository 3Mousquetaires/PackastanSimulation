from base.batiment import Batiment, TypeBatiment, RENDER_BATMATRICE
from numpy import array, where, log2, where

import game
import pygame
from pygame.locals import *
import numpy as np
import tileset
import tilemap

from random import choice, uniform

from base.besoin import TypeBesoin


BESOINS_COEFFS = {0:16, 1:16, 2:16, 3:8, 4:8, 5:8, 6:4, 7:4, 8:2}


class Citoyen :
    def __init__(self, maison):
        self.age = 0
        self.besoins = array([.99 for _ in range(0, 9)]) #array([uniform(.5, 1) for _ in range(0, 9)])
        self.maison = maison

    def tour(self):
        besoin = self.selectionnerBesoin()

        #selection du batiment
        #navigation vers le batiment

        #interface batiment

        return
    

    def getbesoins(self):
        return self.besoins


    def getmaison(self):
        return self.maison


    def selectionnerBesoin(self):
        #on prend les 3 derniers
        besoins_min_list = sorted(self.besoins)
        besoinTt = choice(besoins_min_list[:3])
        besoin_i = where(self.besoins == besoinTt)[0][0]

        print(besoin_i, "selectionné !")
        #on update tous les autres
        for i_b in range(len(self.besoins)):
            if i_b != besoin_i:
                self.besoins[i_b] *= 1/(log2(BESOINS_COEFFS[i_b])+1) #self.besoins[i_b]

        return TypeBesoin(besoin_i) #on le retourne sous forme d'un Besoin (version enum)

        
    def trouverBatiment(self, besoin):
        """renvoie l'adresse du premier batiment trouvé répondant
        à *besoin*."""
        type_bat = besoin.value #en int

        x0, y0 = self.maison

        File = [(x0, y0)]
        deja_vus = []

        map = game.Game().tilemap.get_map()
        while len(File) != 0 :
            x, y = File.pop()
            deja_vus.append((x, y))
            #il faut explorer le carré autour
            for i in [x-1, x, x+1]:
                for j in [y-1, y, y+1]:
                    if (i, j) in deja_vus:
                        continue
                    try:
                        if map[i, j] == type_bat:
                            return (i, j) #on a trouvé une adresse
                    except IndexError:
                        #on est hors de la map, inutile de continuer
                        continue

                    if map[i, j] == 9: #une route
                        File.append( (i, j) )


                



