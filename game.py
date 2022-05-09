import pygame
from pygame.locals import *
import numpy as np
import tileset
from tilemap import *

file='ressources/tileset.png'

class Game:
    W = 1700
    H = 1080
    SIZE = W, H

    def __init__(self):
        pygame.init()
        self.tileset = tileset.Tileset(file)
        self.tilemap = Tilemap(self.tileset)
        self.screen = pygame.display.set_mode(self.tilemap.get_size())

        self.tilemap.set_zero()
        pygame.display.set_caption('Packastan')
        self.running = True

        

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
                        

            self.screen.blit(self.tilemap.image, self.tilemap.rect)
            pygame.display.update()
        pygame.quit()