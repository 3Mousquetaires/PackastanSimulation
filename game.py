import pygame
from pygame.locals import *
import numpy as np
import tileset
import tilemap

file='tileset.png'

class Game:
    W = 1920
    H = 1080
    SIZE = W, H

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.SIZE)
        pygame.display.set_caption('Pygame Tile Demo')
        self.running = True

        self.tileset = tileset.Tileset(file)
        self.tilemap = tilemap.Tilemap(self.tileset)
        self.map2 = tilemap.Tilemap(self.tileset)

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
                    elif event.key == K_s:
                        self.save_image()
                        

            self.screen.blit(self.tilemap.image, self.tilemap.rect)
            pygame.display.update()
        pygame.quit()