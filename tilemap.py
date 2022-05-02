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


defaultMap = np.asarray([[8,3,0,9,3,0,4,9,0,1,3,0,5,3,0,4,5,0,7,1,0,4,5,0,6,3,0,2,4,0,3,1,0,4,1,0,7,3,0,3,3,0,7,7,0,7,4,0,9,5,0,6,6,0,3,1,0,7,1,0],
[1,5,0,8,8,0,5,7,0,9,7,0,5,1,0,8,5,0,4,8,0,3,1,0,8,5,0,6,3,0,8,1,0,6,3,0,1,9,0,8,4,0,4,2,0,1,8,0,2,4,0,8,9,0,9,2,0,8,1,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[5,2,0,4,7,0,6,7,0,5,5,0,6,7,0,2,5,0,2,7,0,5,3,0,8,2,0,4,9,0,1,7,0,5,9,0,2,9,0,5,1,0,4,3,0,6,1,0,6,2,0,6,8,0,9,8,0,1,3,0],
[5,5,0,9,8,0,5,8,0,4,4,0,2,1,0,1,1,0,9,7,0,1,6,0,7,3,0,3,7,0,3,2,0,4,7,0,5,9,0,3,2,0,8,9,0,6,3,0,8,6,0,7,1,0,6,6,0,5,2,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,3,0,9,4,0,9,6,0,1,5,0,1,8,0,8,6,0,4,6,0,1,8,0,2,3,0,6,6,0,6,6,0,8,6,0,5,2,0,6,9,0,7,2,0,5,6,0,6,3,0,5,5,0,8,6,0,2,8,0],
[9,2,0,1,3,0,2,1,0,3,6,0,5,7,0,8,9,0,3,5,0,6,2,0,6,7,0,9,2,0,2,5,0,1,7,0,1,6,0,4,1,0,8,7,0,3,3,0,6,4,0,2,4,0,2,3,0,6,5,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[9,2,0,4,9,0,4,1,0,5,5,0,6,3,0,6,4,0,1,2,0,7,2,0,5,4,0,7,6,0,1,6,0,5,8,0,4,9,0,6,7,0,2,7,0,6,3,0,7,3,0,9,2,0,4,7,0,8,4,0],
[7,2,0,8,9,0,7,4,0,1,9,0,2,2,0,7,3,0,3,9,0,8,4,0,7,1,0,9,9,0,1,2,0,3,5,0,8,4,0,4,9,0,3,1,0,8,2,0,9,9,0,9,7,0,8,8,0,1,1,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[5,7,0,5,2,0,9,9,0,4,5,0,1,7,0,6,4,0,4,3,0,4,4,0,5,5,0,1,1,0,8,8,0,5,6,0,2,2,0,5,9,0,9,7,0,9,8,0,2,1,0,8,5,0,2,5,0,3,5,0],
[9,2,0,1,6,0,5,2,0,8,5,0,8,5,0,3,1,0,2,8,0,9,4,0,6,3,0,3,5,0,3,6,0,1,2,0,4,9,0,7,9,0,2,1,0,7,5,0,3,8,0,2,4,0,1,4,0,4,4,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,4,0,4,8,0,4,5,0,1,9,0,1,2,0,2,1,0,2,7,0,7,9,0,2,6,0,9,5,0,5,8,0,5,8,0,4,2,0,1,6,0,8,9,0,2,8,0,3,8,0,2,1,0,6,5,0,7,4,0],
[8,1,0,1,9,0,9,9,0,3,2,0,1,8,0,1,8,0,8,7,0,4,1,0,7,8,0,3,8,0,9,8,0,6,5,0,8,4,0,8,2,0,1,5,0,1,2,0,6,1,0,4,8,0,1,8,0,3,5,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[5,8,0,2,1,0,9,7,0,4,9,0,2,3,0,8,3,0,2,5,0,7,1,0,3,9,0,2,1,0,2,9,0,8,9,0,8,1,0,9,5,0,6,9,0,2,5,0,5,8,0,6,4,0,1,8,0,8,8,0],
[2,1,0,3,6,0,7,4,0,8,7,0,6,6,0,2,7,0,6,8,0,4,8,0,1,1,0,2,1,0,3,7,0,6,4,0,3,3,0,8,5,0,1,1,0,2,8,0,7,4,0,8,6,0,1,3,0,6,2,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[3,2,0,8,3,0,4,7,0,3,4,0,3,5,0,7,6,0,9,6,0,8,9,0,1,6,0,2,3,0,7,9,0,1,3,0,2,5,0,6,1,0,4,7,0,7,8,0,1,6,0,1,2,0,7,8,0,2,2,0],
[2,2,0,4,5,0,9,3,0,6,9,0,9,4,0,1,9,0,8,9,0,6,1,0,3,9,0,9,4,0,4,9,0,5,4,0,8,7,0,2,8,0,7,5,0,5,8,0,9,2,0,8,7,0,3,4,0,1,8,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[5,4,0,2,6,0,8,3,0,6,4,0,4,6,0,4,5,0,9,9,0,5,6,0,7,3,0,9,4,0,5,4,0,5,9,0,5,3,0,6,5,0,6,3,0,7,9,0,8,8,0,2,7,0,7,2,0,9,1,0],
[7,6,0,6,9,0,4,6,0,1,3,0,3,4,0,6,8,0,9,5,0,6,5,0,4,9,0,2,8,0,1,9,0,7,7,0,2,9,0,9,6,0,5,6,0,2,2,0,2,4,0,8,1,0,6,8,0,6,5,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,6,0,6,5,0,6,1,0,4,4,0,1,9,0,6,3,0,3,7,0,6,5,0,9,6,0,1,9,0,2,1,0,4,7,0,4,3,0,5,5,0,3,1,0,2,7,0,6,1,0,7,4,0,5,3,0,6,6,0],
[6,2,0,4,7,0,2,2,0,4,4,0,8,9,0,8,7,0,7,4,0,6,3,0,6,3,0,3,5,0,8,7,0,2,9,0,7,6,0,1,8,0,8,1,0,4,9,0,3,1,0,1,9,0,1,5,0,8,2,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[9,5,0,6,6,0,2,6,0,6,8,0,4,4,0,3,1,0,8,8,0,2,3,0,7,4,0,1,1,0,8,2,0,7,1,0,8,5,0,7,4,0,2,9,0,6,6,0,8,6,0,7,9,0,8,1,0,1,5,0],
[3,8,0,8,7,0,1,9,0,8,6,0,4,8,0,9,5,0,7,9,0,1,2,0,2,6,0,1,8,0,5,7,0,6,5,0,2,1,0,7,9,0,9,6,0,8,9,0,9,2,0,8,9,0,4,4,0,4,5,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[9,7,0,2,8,0,2,8,0,4,6,0,4,3,0,6,3,0,1,9,0,3,3,0,2,8,0,2,7,0,9,7,0,2,2,0,4,5,0,9,5,0,8,6,0,3,9,0,2,2,0,6,7,0,6,9,0,6,6,0],
[2,9,0,6,6,0,8,9,0,6,8,0,6,2,0,4,8,0,3,9,0,9,9,0,2,3,0,8,9,0,4,8,0,5,3,0,8,8,0,1,6,0,5,5,0,1,1,0,7,1,0,9,9,0,9,8,0,5,8,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,8,0,1,1,0,3,8,0,9,2,0,4,7,0,6,9,0,8,3,0,3,1,0,1,6,0,1,2,0,3,7,0,4,2,0,1,7,0,2,7,0,5,2,0,3,1,0,1,6,0,2,1,0,2,5,0,1,8,0],
[6,6,0,3,7,0,7,6,0,6,4,0,7,8,0,6,7,0,4,3,0,2,1,0,1,7,0,1,5,0,5,6,0,6,2,0,2,9,0,9,1,0,7,4,0,2,3,0,5,8,0,8,7,0,5,2,0,8,4,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[8,7,0,1,9,0,9,6,0,8,1,0,6,8,0,4,3,0,9,8,0,8,9,0,8,9,0,7,4,0,6,8,0,9,8,0,8,3,0,5,1,0,1,1,0,7,2,0,9,7,0,4,6,0,1,7,0,3,3,0],
[6,1,0,6,2,0,9,8,0,2,5,0,4,2,0,6,5,0,8,2,0,9,9,0,7,5,0,7,5,0,1,6,0,1,1,0,8,3,0,7,8,0,5,4,0,2,5,0,8,3,0,6,1,0,7,5,0,8,9,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[6,8,0,7,2,0,2,7,0,6,5,0,4,9,0,6,3,0,2,1,0,5,6,0,9,1,0,6,3,0,5,9,0,1,7,0,9,5,0,1,6,0,6,2,0,9,3,0,9,7,0,2,5,0,7,5,0,3,4,0],
[6,9,0,4,7,0,4,7,0,7,2,0,2,6,0,1,8,0,4,3,0,1,6,0,9,2,0,4,6,0,8,2,0,8,5,0,3,5,0,9,1,0,1,2,0,6,1,0,7,3,0,8,3,0,4,6,0,1,2,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[3,9,0,1,6,0,6,3,0,2,7,0,2,7,0,8,9,0,6,9,0,1,4,0,6,1,0,5,5,0,4,9,0,6,2,0,5,8,0,6,4,0,7,7,0,6,6,0,3,6,0,7,8,0,7,2,0,7,2,0],
[5,3,0,6,5,0,5,6,0,4,8,0,7,1,0,6,8,0,3,3,0,5,5,0,3,3,0,8,7,0,2,2,0,4,4,0,4,5,0,8,5,0,8,9,0,4,5,0,8,3,0,3,8,0,8,1,0,8,3,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[9,7,0,7,4,0,3,9,0,2,6,0,5,5,0,8,7,0,4,5,0,2,1,0,4,3,0,8,9,0,4,3,0,9,5,0,4,3,0,4,8,0,9,2,0,5,4,0,2,3,0,4,3,0,5,5,0,8,3,0],
[8,8,0,3,1,0,3,4,0,3,8,0,4,5,0,2,7,0,6,5,0,9,7,0,9,2,0,5,8,0,5,7,0,9,9,0,7,4,0,5,1,0,8,4,0,1,9,0,6,3,0,8,7,0,7,3,0,4,4,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[7,6,0,1,5,0,8,4,0,9,9,0,9,2,0,6,1,0,7,7,0,3,8,0,2,2,0,6,8,0,7,4,0,5,5,0,5,3,0,8,4,0,2,4,0,1,7,0,7,2,0,3,5,0,9,9,0,8,3,0],
[2,6,0,1,4,0,8,2,0,1,5,0,4,5,0,1,2,0,3,7,0,1,6,0,2,7,0,6,8,0,7,4,0,3,9,0,9,5,0,9,2,0,9,6,0,1,1,0,1,7,0,1,3,0,1,5,0,5,4,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,9,0,5,4,0,4,4,0,5,3,0,7,2,0,1,8,0,9,6,0,3,8,0,8,7,0,9,3,0,9,6,0,3,4,0,9,1,0,3,8,0,5,9,0,7,2,0,6,7,0,7,7,0,3,1,0,1,2,0],
[4,3,0,1,9,0,7,4,0,1,6,0,9,2,0,1,1,0,1,6,0,8,6,0,8,1,0,2,6,0,7,5,0,5,9,0,2,5,0,8,8,0,9,9,0,1,7,0,4,3,0,3,8,0,9,1,0,2,8,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[4,3,0,2,3,0,3,6,0,9,6,0,6,3,0,7,7,0,9,2,0,2,2,0,6,3,0,1,6,0,1,6,0,4,5,0,4,6,0,4,5,0,5,2,0,6,4,0,5,7,0,1,3,0,3,1,0,3,3,0],
[4,6,0,3,1,0,2,2,0,1,1,0,2,7,0,7,5,0,7,4,0,5,6,0,7,9,0,4,1,0,8,2,0,3,9,0,3,7,0,2,7,0,9,2,0,4,4,0,3,1,0,5,2,0,4,3,0,8,9,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]], dtype=int);



