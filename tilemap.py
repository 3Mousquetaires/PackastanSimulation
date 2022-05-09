import pygame
import numpy as np
import tileset

class Tilemap:
    def __init__(self, tileset, size=(60, 60), rect=None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((32*w, 32*h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def get_size(self):
        w, h = self.size
        w = 32*w
        h = 32*h
        return h, w

    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*32, i*32))

    def set_zero(self):
        self.map = defaultMap
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'

    def get_map(self):
        return self.map


defaultMap = np.asarray([
[8,3,9,3,3,9,4,5,9,1,3,9,5,3,9,4,5,9,7,1,9,4,5,9,6,3,9,2,4,9,3,1,9,4,1,9,7,3,9,3,3,9,7,7,9,7,4,9,9,5,9,6,6,9,3,1,9,7,1,9],
[1,5,9,8,8,9,5,7,9,9,7,9,5,1,9,8,5,9,4,8,9,3,1,9,8,5,9,6,3,9,8,1,9,6,3,9,1,9,9,8,4,9,4,2,9,1,8,9,2,4,9,8,9,9,9,2,9,8,1,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[5,2,9,4,7,9,6,7,9,5,5,9,6,7,9,2,5,9,2,7,9,5,3,9,8,2,9,4,9,9,1,7,9,5,9,9,2,9,9,5,1,9,4,3,9,6,1,9,6,2,9,6,8,9,9,8,9,1,3,9],
[5,5,9,9,8,9,5,8,9,4,4,9,2,1,9,1,1,9,9,7,9,1,6,9,7,3,9,3,7,9,3,2,9,4,7,9,5,9,9,3,2,9,8,9,9,6,3,9,8,6,9,7,1,9,6,6,9,5,2,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[2,3,9,9,4,9,9,6,9,1,5,9,1,8,9,8,6,9,4,6,9,1,8,9,2,3,9,6,6,9,6,6,9,8,6,9,5,2,9,6,9,9,7,2,9,5,6,9,6,3,9,5,5,9,8,6,9,2,8,9],
[9,2,9,1,3,9,2,1,9,3,6,9,5,7,9,8,9,9,3,5,9,6,2,9,6,7,9,9,2,9,2,5,9,1,7,9,1,6,9,4,1,9,8,7,9,3,3,9,6,4,9,2,4,9,2,3,9,6,5,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[9,2,9,4,9,9,4,1,9,5,5,9,6,3,9,6,4,9,1,2,9,7,2,9,5,4,9,7,6,9,1,6,9,5,8,9,4,9,9,6,7,9,2,7,9,6,3,9,7,3,9,9,2,9,4,7,9,8,4,9],
[7,2,9,8,9,9,7,4,9,1,9,9,2,2,9,7,3,9,3,9,9,8,4,9,7,1,9,9,9,9,1,2,9,3,5,9,8,4,9,4,9,9,3,1,9,8,2,9,9,9,9,9,7,9,8,8,9,1,1,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[5,7,9,5,2,9,9,9,9,4,5,9,1,7,9,6,4,9,4,3,9,4,4,9,5,5,9,1,1,9,8,8,9,5,6,9,2,2,9,5,9,9,9,7,9,9,8,9,2,1,9,8,5,9,2,5,9,3,5,9],
[9,2,9,1,6,9,5,2,9,8,5,9,8,5,9,3,1,9,2,8,9,9,4,9,6,3,9,3,5,9,3,6,9,1,2,9,4,9,9,7,9,9,2,1,9,7,5,9,3,8,9,2,4,9,1,4,9,4,4,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[4,4,9,4,8,9,4,5,9,1,9,9,1,2,9,2,1,9,2,7,9,7,9,9,2,6,9,9,5,9,5,8,9,5,8,9,4,2,9,1,6,9,8,9,9,2,8,9,3,8,9,2,1,9,6,5,9,7,4,9],
[8,1,9,1,9,9,9,9,9,3,2,9,1,8,9,1,8,9,8,7,9,4,1,9,7,8,9,3,8,9,9,8,9,6,5,9,8,4,9,8,2,9,1,5,9,1,2,9,6,1,9,4,8,9,1,8,9,3,5,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[5,8,9,2,1,9,9,7,9,4,9,9,2,3,9,8,3,9,2,5,9,7,1,9,3,9,9,2,1,9,2,9,9,8,9,9,8,1,9,9,5,9,6,9,9,2,5,9,5,8,9,6,4,9,1,8,9,8,8,9],
[2,1,9,3,6,9,7,4,9,8,7,9,6,6,9,2,7,9,6,8,9,4,8,9,1,1,9,2,1,9,3,7,9,6,4,9,3,3,9,8,5,9,1,1,9,2,8,9,7,4,9,8,6,9,1,3,9,6,2,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[3,2,9,8,3,9,4,7,9,3,4,9,3,5,9,7,6,9,9,6,9,8,9,9,1,6,9,2,3,9,7,9,9,1,3,9,2,5,9,6,1,9,4,7,9,7,8,9,1,6,9,1,2,9,7,8,9,2,2,9],
[2,2,9,4,5,9,9,3,9,6,9,9,9,4,9,1,9,9,8,9,9,6,1,9,3,9,9,9,4,9,4,9,9,5,4,9,8,7,9,2,8,9,7,5,9,5,8,9,9,2,9,8,7,9,3,4,9,1,8,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[5,4,9,2,6,9,8,3,9,6,4,9,4,6,9,4,5,9,9,9,9,5,6,9,7,3,9,9,4,9,5,4,9,5,9,9,5,3,9,6,5,9,6,3,9,7,9,9,8,8,9,2,7,9,7,2,9,9,1,9],
[7,6,9,6,9,9,4,6,9,1,3,9,3,4,9,6,8,9,9,5,9,6,5,9,4,9,9,2,8,9,1,9,9,7,7,9,2,9,9,9,6,9,5,6,9,2,2,9,2,4,9,8,1,9,6,8,9,6,5,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[2,6,9,6,5,9,6,1,9,4,4,9,1,9,9,6,3,9,3,7,9,6,5,9,9,6,9,1,9,9,2,1,9,4,7,9,4,3,9,5,5,9,3,1,9,2,7,9,6,1,9,7,4,9,5,3,9,6,6,9],
[6,2,9,4,7,9,2,2,9,4,4,9,8,9,9,8,7,9,7,4,9,6,3,9,6,3,9,3,5,9,8,7,9,2,9,9,7,6,9,1,8,9,8,1,9,4,9,9,3,1,9,1,9,9,1,5,9,8,2,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[9,5,9,6,6,9,2,6,9,6,8,9,4,4,9,3,1,9,8,8,9,2,3,9,7,4,9,1,1,9,8,2,9,7,1,9,8,5,9,7,4,9,2,9,9,6,6,9,8,6,9,7,9,9,8,1,9,1,5,9],
[3,8,9,8,7,9,1,9,9,8,6,9,4,8,9,9,5,9,7,9,9,1,2,9,2,6,9,1,8,9,5,7,9,6,5,9,2,1,9,7,9,9,9,6,9,8,9,9,9,2,9,8,9,9,4,4,9,4,5,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[9,7,9,2,8,9,2,8,9,4,6,9,4,3,9,6,3,9,1,9,9,3,3,9,2,8,9,2,7,9,9,7,9,2,2,9,4,5,9,9,5,9,8,6,9,3,9,9,2,2,9,6,7,9,6,9,9,6,6,9],
[2,9,9,6,6,9,8,9,9,6,8,9,6,2,9,4,8,9,3,9,9,9,9,9,2,3,9,8,9,9,4,8,9,5,3,9,8,8,9,1,6,9,5,5,9,1,1,9,7,1,9,9,9,9,9,8,9,5,8,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[2,8,9,1,1,9,3,8,9,9,2,9,4,7,9,6,9,9,8,3,9,3,1,9,1,6,9,1,2,9,3,7,9,4,2,9,1,7,9,2,7,9,5,2,9,3,1,9,1,6,9,2,1,9,2,5,9,1,8,9],
[6,6,9,3,7,9,7,6,9,6,4,9,7,8,9,6,7,9,4,3,9,2,1,9,1,7,9,1,5,9,5,6,9,6,2,9,2,9,9,9,1,9,7,4,9,2,3,9,5,8,9,8,7,9,5,2,9,8,4,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[8,7,9,1,9,9,9,6,9,8,1,9,6,8,9,4,3,9,9,8,9,8,9,9,8,9,9,7,4,9,6,8,9,9,8,9,8,3,9,5,1,9,1,1,9,7,2,9,9,7,9,4,6,9,1,7,9,3,3,9],
[6,1,9,6,2,9,9,8,9,2,5,9,4,2,9,6,5,9,8,2,9,9,9,9,7,5,9,7,5,9,1,6,9,1,1,9,8,3,9,7,8,9,5,4,9,2,5,9,8,3,9,6,1,9,7,5,9,8,9,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[6,8,9,7,2,9,2,7,9,6,5,9,4,9,9,6,3,9,2,1,9,5,6,9,9,1,9,6,3,9,5,9,9,1,7,9,9,5,9,1,6,9,6,2,9,9,3,9,9,7,9,2,5,9,7,5,9,3,4,9],
[6,9,9,4,7,9,4,7,9,7,2,9,2,6,9,1,8,9,4,3,9,1,6,9,9,2,9,4,6,9,8,2,9,8,5,9,3,5,9,9,1,9,1,2,9,6,1,9,7,3,9,8,3,9,4,6,9,1,2,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[3,9,9,1,6,9,6,3,9,2,7,9,2,7,9,8,9,9,6,9,9,1,4,9,6,1,9,5,5,9,4,9,9,6,2,9,5,8,9,6,4,9,7,7,9,6,6,9,3,6,9,7,8,9,7,2,9,7,2,9],
[5,3,9,6,5,9,5,6,9,4,8,9,7,1,9,6,8,9,3,3,9,5,5,9,3,3,9,8,7,9,2,2,9,4,4,9,4,5,9,8,5,9,8,9,9,4,5,9,8,3,9,3,8,9,8,1,9,8,3,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[9,7,9,7,4,9,3,9,9,2,6,9,5,5,9,8,7,9,4,5,9,2,1,9,4,3,9,8,9,9,4,3,9,9,5,9,4,3,9,4,8,9,9,2,9,5,4,9,2,3,9,4,3,9,5,5,9,8,3,9],
[8,8,9,3,1,9,3,4,9,3,8,9,4,5,9,2,7,9,6,5,9,9,7,9,9,2,9,5,8,9,5,7,9,9,9,9,7,4,9,5,1,9,8,4,9,1,9,9,6,3,9,8,7,9,7,3,9,4,4,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[7,6,9,1,5,9,8,4,9,9,9,9,9,2,9,6,1,9,7,7,9,3,8,9,2,2,9,6,8,9,7,4,9,5,5,9,5,3,9,8,4,9,2,4,9,1,7,9,7,2,9,3,5,9,9,9,9,8,3,9],
[2,6,9,1,4,9,8,2,9,1,5,9,4,5,9,1,2,9,3,7,9,1,6,9,2,7,9,6,8,9,7,4,9,3,9,9,9,5,9,9,2,9,9,6,9,1,1,9,1,7,9,1,3,9,1,5,9,5,4,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[4,9,9,5,4,9,4,4,9,5,3,9,7,2,9,1,8,9,9,6,9,3,8,9,8,7,9,9,3,9,9,6,9,3,4,9,9,1,9,3,8,9,5,9,9,7,2,9,6,7,9,7,7,9,3,1,9,1,2,9],
[4,3,9,1,9,9,7,4,9,1,6,9,9,2,9,1,1,9,1,6,9,8,6,9,8,1,9,2,6,9,7,5,9,5,9,9,2,5,9,8,8,9,9,9,9,1,7,9,4,3,9,3,8,9,9,1,9,2,8,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
[4,3,9,2,3,9,3,6,9,9,6,9,6,3,9,7,7,9,9,2,9,2,2,9,6,3,9,1,6,9,1,6,9,4,5,9,4,6,9,4,5,9,5,2,9,6,4,9,5,7,9,1,3,9,3,1,9,3,3,9],
[4,6,9,3,1,9,2,2,9,1,1,9,2,7,9,7,5,9,7,4,9,5,6,9,7,9,9,4,1,9,8,2,9,3,9,9,3,7,9,2,7,9,9,2,9,4,4,9,3,1,9,5,2,9,4,3,9,8,9,9],
[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9]], dtype=int);



