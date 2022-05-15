import pygame
from pygame.locals import *
import numpy as np
import tileset
from tilemap import *

from base.batiment import TypeBatiment, Batiment
from base.citoyen import Citoyen

file='ressources/tileset.png'

class Game:
    W = 600
    H = 600
    SIZE = W, H

    def __init__(self):
        pygame.init()
        self.tileset = tileset.Tileset(file)
        self.tilemap = Tilemap(self.tileset)
        self.screen = pygame.display.set_mode((600, 600))

        self.tilemap.set_zero()
        pygame.display.set_caption('Packastan')
        self.running = True

        #init batliste
        self.batliste = []
        for ligne_bat_int in range(self.tilemap.get_map().shape[0] ):
            ligne = []
            for bat_int in range(self.tilemap.get_map().shape[1]):
                bat = Batiment(
                    TypeBatiment(self.tilemap.get_map()[ligne_bat_int][bat_int]),
                    (ligne_bat_int, bat_int))
                ligne.append(bat)
            
            self.batliste.append(ligne)
        
        
    def test_citoyen(self):
        #On créé un citoyen, il habite à la première maison
        C = Citoyen(self.batliste[0][18])
        

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                elif event.type == KEYDOWN:
                    if event.key == K_m:
                        print(self.tilemap.map)
                    elif event.key == K_r:
                        self.tilemap.set_random()
                    elif event.key == K_z:
                        self.tilemap.set_zero()
                    #elif event.key == K_s:
                    #    self.save_image()
                            
            self.tilemap.image = pygame.transform.scale(self.tilemap.image, self.SIZE)
            self.screen.blit(self.tilemap.image, self.tilemap.rect)
            pygame.display.update()
        pygame.quit()