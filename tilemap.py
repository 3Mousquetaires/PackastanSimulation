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



defaultMap = np.asarray(
    [[9, 4, 0, 0, 9, 6, 0, 5, 9, 6, 7, 7, 9, 2, 3, 6, 9, 0, 1, 5, 9, 0,
        8, 2, 9, 8, 0, 1, 9, 6, 7, 8, 9, 5, 3, 4, 9, 8, 7, 6, 9, 6, 8, 1,
        9, 0, 4, 4, 9, 5, 1, 3, 9, 4, 0, 1, 9, 0, 2, 2],
       [9, 4, 7, 8, 9, 7, 1, 7, 9, 1, 8, 2, 9, 5, 3, 1, 9, 2, 3, 7, 9, 1,
        0, 3, 9, 8, 1, 3, 9, 3, 6, 6, 9, 4, 1, 2, 9, 5, 7, 0, 9, 8, 6, 1,
        9, 8, 5, 5, 9, 6, 7, 6, 9, 1, 5, 6, 9, 5, 5, 7],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 1, 2, 8, 9, 5, 1, 2, 9, 0, 7, 6, 9, 2, 0, 0, 9, 7, 2, 6, 9, 4,
        4, 7, 9, 6, 8, 4, 9, 4, 8, 2, 9, 2, 4, 4, 9, 8, 0, 8, 9, 6, 2, 5,
        9, 3, 0, 6, 9, 0, 7, 4, 9, 4, 2, 4, 9, 2, 8, 2],
       [9, 5, 5, 6, 9, 2, 6, 1, 9, 4, 7, 7, 9, 8, 1, 8, 9, 5, 8, 3, 9, 4,
        6, 0, 9, 3, 4, 6, 9, 3, 5, 5, 9, 2, 0, 1, 9, 5, 5, 2, 9, 2, 2, 3,
        9, 6, 5, 6, 9, 5, 0, 4, 9, 0, 0, 2, 9, 3, 5, 0],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 1, 3, 5, 9, 6, 3, 1, 9, 8, 5, 4, 9, 7, 1, 4, 9, 5, 5, 6, 9, 3,
        2, 3, 9, 1, 2, 0, 9, 2, 7, 1, 9, 0, 4, 3, 9, 3, 3, 8, 9, 2, 7, 2,
        9, 4, 2, 7, 9, 3, 2, 3, 9, 0, 2, 0, 9, 5, 2, 0],
       [9, 5, 4, 4, 9, 8, 6, 4, 9, 2, 7, 1, 9, 5, 8, 8, 9, 4, 6, 3, 9, 8,
        2, 4, 9, 8, 0, 2, 9, 6, 0, 1, 9, 5, 2, 3, 9, 1, 1, 6, 9, 8, 3, 6,
        9, 6, 3, 4, 9, 0, 7, 6, 9, 6, 8, 4, 9, 3, 0, 2],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 2, 3, 4, 9, 7, 5, 8, 9, 8, 4, 5, 9, 0, 4, 7, 9, 0, 0, 6, 9, 5,
        2, 2, 9, 6, 5, 1, 9, 4, 0, 8, 9, 4, 7, 1, 9, 0, 3, 5, 9, 3, 6, 3,
        9, 1, 8, 7, 9, 7, 1, 1, 9, 7, 5, 7, 9, 0, 0, 4],
       [9, 0, 5, 1, 9, 3, 7, 0, 9, 3, 6, 3, 9, 5, 8, 1, 9, 8, 0, 1, 9, 0,
        2, 2, 9, 6, 8, 7, 9, 5, 4, 5, 9, 7, 8, 8, 9, 0, 1, 1, 9, 1, 6, 7,
        9, 4, 4, 8, 9, 2, 8, 1, 9, 2, 1, 1, 9, 8, 8, 7],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 8, 0, 2, 9, 5, 1, 7, 9, 2, 5, 5, 9, 4, 2, 4, 9, 5, 2, 8, 9, 4,
        4, 1, 9, 2, 6, 3, 9, 4, 3, 4, 9, 5, 6, 7, 9, 2, 2, 5, 9, 2, 8, 1,
        9, 5, 0, 5, 9, 5, 1, 1, 9, 5, 0, 4, 9, 7, 2, 6],
       [9, 4, 0, 8, 9, 3, 3, 2, 9, 5, 3, 6, 9, 2, 3, 5, 9, 0, 5, 7, 9, 7,
        6, 4, 9, 0, 4, 7, 9, 1, 4, 3, 9, 1, 1, 6, 9, 6, 0, 2, 9, 0, 7, 0,
        9, 0, 1, 8, 9, 4, 5, 1, 9, 3, 7, 2, 9, 5, 7, 5],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 5, 4, 0, 9, 3, 2, 4, 9, 7, 5, 5, 9, 6, 0, 8, 9, 8, 5, 8, 9, 5,
        2, 6, 9, 7, 1, 0, 9, 8, 0, 2, 9, 0, 6, 3, 9, 1, 0, 6, 9, 1, 0, 0,
        9, 8, 6, 1, 9, 7, 2, 6, 9, 7, 4, 2, 9, 1, 8, 7],
       [9, 6, 2, 1, 9, 6, 3, 8, 9, 7, 6, 8, 9, 5, 7, 6, 9, 8, 7, 3, 9, 8,
        5, 0, 9, 1, 0, 1, 9, 5, 8, 1, 9, 8, 2, 5, 9, 8, 6, 6, 9, 2, 4, 6,
        9, 0, 0, 5, 9, 4, 8, 5, 9, 2, 4, 2, 9, 5, 0, 6],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 2, 4, 2, 9, 0, 4, 3, 9, 5, 6, 5, 9, 0, 4, 3, 9, 0, 7, 4, 9, 7,
        8, 5, 9, 5, 6, 4, 9, 3, 0, 7, 9, 4, 4, 1, 9, 0, 7, 5, 9, 7, 6, 1,
        9, 8, 4, 8, 9, 2, 4, 6, 9, 5, 2, 2, 9, 5, 4, 7],
       [9, 1, 7, 7, 9, 8, 8, 6, 9, 8, 1, 0, 9, 1, 8, 0, 9, 4, 5, 1, 9, 5,
        2, 7, 9, 6, 5, 5, 9, 1, 1, 6, 9, 5, 7, 5, 9, 0, 1, 3, 9, 3, 2, 1,
        9, 1, 4, 2, 9, 7, 5, 6, 9, 3, 7, 6, 9, 5, 4, 6],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 7, 5, 1, 9, 4, 6, 5, 9, 3, 5, 0, 9, 3, 6, 7, 9, 6, 3, 2, 9, 8,
        5, 3, 9, 5, 5, 5, 9, 8, 2, 7, 9, 8, 0, 5, 9, 5, 5, 6, 9, 1, 4, 6,
        9, 8, 1, 4, 9, 6, 7, 1, 9, 3, 8, 8, 9, 3, 8, 0],
       [9, 6, 0, 4, 9, 4, 0, 3, 9, 6, 3, 1, 9, 2, 0, 5, 9, 1, 8, 6, 9, 0,
        1, 1, 9, 5, 3, 5, 9, 0, 6, 3, 9, 2, 6, 7, 9, 8, 4, 3, 9, 4, 7, 4,
        9, 1, 6, 6, 9, 1, 1, 6, 9, 8, 5, 1, 9, 5, 3, 4],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 2, 6, 8, 9, 3, 1, 0, 9, 0, 3, 7, 9, 4, 3, 7, 9, 5, 8, 7, 9, 1,
        1, 4, 9, 2, 7, 0, 9, 3, 7, 5, 9, 6, 4, 1, 9, 6, 5, 2, 9, 3, 4, 8,
        9, 8, 0, 2, 9, 7, 0, 2, 9, 2, 4, 7, 9, 3, 2, 0],
       [9, 5, 8, 3, 9, 7, 0, 4, 9, 1, 6, 3, 9, 2, 1, 3, 9, 1, 8, 6, 9, 6,
        8, 7, 9, 6, 5, 4, 9, 0, 0, 2, 9, 7, 7, 4, 9, 8, 2, 3, 9, 4, 3, 6,
        9, 8, 1, 8, 9, 8, 0, 8, 9, 2, 2, 4, 9, 7, 7, 4],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 1, 0, 4, 9, 1, 2, 4, 9, 8, 5, 1, 9, 8, 2, 1, 9, 4, 1, 2, 9, 3,
        2, 1, 9, 4, 1, 5, 9, 5, 1, 6, 9, 4, 2, 1, 9, 8, 3, 5, 9, 8, 5, 4,
        9, 2, 5, 0, 9, 8, 0, 4, 9, 3, 1, 5, 9, 7, 4, 8],
       [9, 2, 1, 2, 9, 7, 5, 5, 9, 7, 1, 7, 9, 7, 6, 6, 9, 2, 8, 3, 9, 3,
        6, 6, 9, 5, 3, 0, 9, 6, 4, 7, 9, 4, 8, 5, 9, 8, 2, 1, 9, 3, 0, 4,
        9, 7, 5, 6, 9, 6, 3, 7, 9, 0, 1, 2, 9, 6, 0, 1],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 8, 6, 8, 9, 7, 8, 1, 9, 2, 0, 4, 9, 7, 1, 5, 9, 7, 3, 0, 9, 1,
        1, 8, 9, 6, 4, 1, 9, 3, 2, 6, 9, 4, 3, 2, 9, 7, 8, 4, 9, 3, 4, 5,
        9, 4, 3, 0, 9, 2, 4, 5, 9, 0, 7, 8, 9, 1, 7, 6],
       [9, 6, 0, 3, 9, 2, 2, 7, 9, 3, 3, 8, 9, 4, 0, 8, 9, 7, 7, 2, 9, 4,
        8, 2, 9, 2, 2, 0, 9, 7, 4, 2, 9, 0, 2, 1, 9, 0, 5, 7, 9, 5, 2, 4,
        9, 6, 5, 4, 9, 6, 7, 3, 9, 5, 3, 0, 9, 2, 3, 5],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 2, 3, 0, 9, 7, 7, 8, 9, 2, 3, 7, 9, 0, 7, 1, 9, 4, 8, 6, 9, 8,
        0, 5, 9, 3, 3, 2, 9, 7, 3, 2, 9, 4, 1, 2, 9, 7, 0, 3, 9, 0, 3, 4,
        9, 6, 8, 7, 9, 3, 4, 2, 9, 3, 8, 5, 9, 5, 2, 1],
       [9, 5, 3, 0, 9, 2, 8, 7, 9, 2, 8, 7, 9, 2, 8, 1, 9, 7, 6, 0, 9, 5,
        2, 4, 9, 3, 6, 0, 9, 5, 1, 6, 9, 2, 2, 4, 9, 2, 6, 8, 9, 2, 8, 8,
        9, 7, 2, 2, 9, 3, 8, 0, 9, 4, 7, 0, 9, 6, 6, 0],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 4, 3, 8, 9, 1, 4, 0, 9, 0, 6, 3, 9, 1, 8, 3, 9, 4, 4, 4, 9, 8,
        3, 7, 9, 1, 7, 8, 9, 0, 8, 6, 9, 5, 1, 0, 9, 3, 5, 7, 9, 5, 3, 3,
        9, 1, 4, 7, 9, 1, 5, 2, 9, 0, 4, 7, 9, 4, 8, 2],
       [9, 5, 8, 0, 9, 1, 2, 7, 9, 5, 8, 8, 9, 5, 3, 0, 9, 0, 4, 0, 9, 5,
        3, 8, 9, 7, 1, 2, 9, 7, 3, 3, 9, 7, 0, 4, 9, 1, 7, 2, 9, 0, 4, 7,
        9, 1, 5, 4, 9, 0, 1, 1, 9, 2, 1, 3, 9, 7, 4, 3],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 2, 8, 5, 9, 5, 5, 4, 9, 5, 5, 3, 9, 2, 7, 4, 9, 6, 1, 6, 9, 1,
        5, 6, 9, 0, 7, 7, 9, 4, 5, 6, 9, 1, 7, 3, 9, 8, 1, 8, 9, 0, 1, 6,
        9, 7, 2, 4, 9, 1, 2, 8, 9, 0, 6, 0, 9, 3, 5, 4],
       [9, 2, 8, 3, 9, 7, 4, 1, 9, 1, 1, 5, 9, 5, 5, 4, 9, 1, 1, 4, 9, 8,
        7, 5, 9, 0, 7, 8, 9, 2, 8, 1, 9, 5, 0, 3, 9, 5, 4, 2, 9, 7, 2, 6,
        9, 4, 1, 2, 9, 8, 0, 8, 9, 1, 8, 2, 9, 5, 1, 2],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 7, 2, 5, 9, 7, 1, 3, 9, 1, 3, 5, 9, 3, 7, 3, 9, 1, 8, 5, 9, 4,
        1, 3, 9, 6, 5, 6, 9, 7, 4, 1, 9, 2, 7, 6, 9, 5, 5, 8, 9, 4, 8, 6,
        9, 2, 8, 4, 9, 2, 8, 6, 9, 5, 0, 1, 9, 2, 1, 8],
       [9, 4, 0, 3, 9, 8, 1, 1, 9, 1, 2, 8, 9, 4, 0, 1, 9, 8, 5, 4, 9, 1,
        6, 5, 9, 2, 7, 6, 9, 7, 7, 6, 9, 8, 2, 8, 9, 6, 6, 1, 9, 5, 7, 7,
        9, 1, 2, 5, 9, 7, 0, 0, 9, 6, 2, 3, 9, 4, 2, 7],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 3, 1, 7, 9, 5, 8, 2, 9, 5, 1, 7, 9, 2, 6, 7, 9, 3, 7, 1, 9, 2,
        6, 2, 9, 3, 5, 1, 9, 3, 1, 4, 9, 0, 2, 1, 9, 0, 1, 4, 9, 0, 8, 2,
        9, 2, 4, 7, 9, 1, 5, 1, 9, 8, 7, 4, 9, 2, 8, 3],
       [9, 6, 5, 7, 9, 0, 8, 3, 9, 8, 3, 2, 9, 8, 7, 1, 9, 4, 2, 7, 9, 3,
        6, 2, 9, 2, 3, 7, 9, 8, 4, 4, 9, 1, 3, 1, 9, 1, 3, 8, 9, 7, 3, 0,
        9, 5, 6, 2, 9, 3, 8, 4, 9, 2, 2, 5, 9, 8, 2, 5],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 8, 5, 4, 9, 2, 8, 4, 9, 3, 6, 1, 9, 4, 2, 8, 9, 4, 2, 4, 9, 8,
        1, 6, 9, 5, 0, 1, 9, 0, 2, 6, 9, 1, 0, 1, 9, 3, 8, 7, 9, 5, 6, 6,
        9, 0, 3, 7, 9, 4, 1, 8, 9, 7, 5, 7, 9, 4, 6, 5],
       [9, 5, 3, 5, 9, 2, 6, 8, 9, 2, 6, 8, 9, 6, 0, 1, 9, 7, 6, 5, 9, 4,
        4, 6, 9, 2, 5, 2, 9, 0, 3, 4, 9, 0, 7, 6, 9, 2, 5, 1, 9, 6, 4, 3,
        9, 2, 1, 5, 9, 0, 2, 6, 9, 3, 4, 7, 9, 1, 2, 8],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 0, 6, 8, 9, 6, 3, 8, 9, 8, 8, 5, 9, 4, 6, 2, 9, 6, 6, 3, 9, 0,
        4, 1, 9, 4, 5, 7, 9, 5, 8, 0, 9, 5, 7, 3, 9, 5, 5, 5, 9, 5, 3, 1,
        9, 0, 3, 3, 9, 4, 0, 8, 9, 8, 0, 8, 9, 3, 8, 0],
       [9, 5, 7, 2, 9, 3, 0, 6, 9, 7, 4, 3, 9, 7, 1, 1, 9, 7, 2, 2, 9, 1,
        8, 0, 9, 1, 5, 8, 9, 4, 1, 0, 9, 1, 3, 5, 9, 2, 0, 7, 9, 1, 1, 7,
        9, 4, 2, 2, 9, 2, 5, 0, 9, 6, 7, 3, 9, 4, 2, 0],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 3, 3, 2, 9, 5, 2, 1, 9, 8, 0, 0, 9, 2, 3, 0, 9, 6, 3, 6, 9, 8,
        3, 2, 9, 4, 6, 4, 9, 7, 4, 3, 9, 4, 7, 2, 9, 7, 3, 3, 9, 8, 4, 7,
        9, 8, 3, 3, 9, 5, 2, 1, 9, 2, 7, 4, 9, 6, 5, 5],
       [9, 8, 8, 3, 9, 5, 5, 7, 9, 6, 3, 8, 9, 6, 1, 5, 9, 7, 2, 7, 9, 8,
        8, 0, 9, 0, 5, 4, 9, 4, 1, 5, 9, 6, 4, 2, 9, 6, 5, 1, 9, 7, 4, 5,
        9, 3, 1, 8, 9, 5, 0, 6, 9, 2, 4, 4, 9, 1, 2, 1],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 5, 2, 1, 9, 7, 6, 6, 9, 4, 1, 8, 9, 5, 0, 4, 9, 2, 4, 0, 9, 2,
        8, 2, 9, 0, 0, 0, 9, 7, 7, 2, 9, 8, 6, 4, 9, 8, 2, 4, 9, 2, 3, 8,
        9, 5, 1, 7, 9, 0, 6, 5, 9, 0, 6, 5, 9, 0, 6, 5],
       [9, 0, 7, 2, 9, 3, 5, 5, 9, 7, 7, 5, 9, 5, 7, 8, 9, 0, 2, 0, 9, 6,
        5, 0, 9, 8, 0, 5, 9, 1, 7, 7, 9, 7, 8, 0, 9, 0, 8, 4, 9, 1, 5, 7,
        9, 1, 7, 3, 9, 2, 8, 6, 9, 5, 8, 6, 9, 6, 5, 1],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 6, 2, 1, 9, 2, 7, 1, 9, 1, 4, 3, 9, 4, 6, 7, 9, 2, 8, 7, 9, 3,
        6, 6, 9, 8, 8, 0, 9, 2, 4, 3, 9, 2, 8, 2, 9, 2, 7, 8, 9, 8, 3, 4,
        9, 3, 4, 4, 9, 8, 0, 2, 9, 5, 3, 6, 9, 2, 8, 3],
       [9, 6, 5, 7, 9, 8, 8, 8, 9, 8, 8, 2, 9, 0, 0, 1, 9, 6, 3, 8, 9, 2,
        2, 4, 9, 7, 0, 2, 9, 5, 2, 8, 9, 0, 7, 5, 9, 1, 0, 8, 9, 0, 0, 6,
        9, 1, 0, 1, 9, 4, 2, 6, 9, 5, 8, 7, 9, 4, 4, 0],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 3, 3, 6, 9, 4, 6, 1, 9, 5, 7, 5, 9, 1, 1, 2, 9, 8, 7, 6, 9, 6,
        0, 8, 9, 6, 0, 5, 9, 2, 7, 7, 9, 5, 3, 2, 9, 6, 2, 0, 9, 4, 7, 4,
        9, 1, 3, 8, 9, 3, 5, 0, 9, 4, 0, 1, 9, 0, 2, 3],
       [9, 1, 5, 1, 9, 0, 0, 5, 9, 3, 0, 2, 9, 1, 1, 3, 9, 7, 1, 3, 9, 0,
        5, 1, 9, 5, 8, 3, 9, 5, 6, 4, 9, 4, 7, 0, 9, 6, 7, 2, 9, 4, 2, 7,
        9, 7, 3, 5, 9, 2, 1, 8, 9, 8, 0, 7, 9, 8, 4, 6],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 0, 1, 5, 9, 7, 0, 8, 9, 6, 6, 1, 9, 2, 3, 1, 9, 8, 1, 2, 9, 1,
        0, 7, 9, 4, 5, 0, 9, 3, 1, 5, 9, 5, 0, 6, 9, 1, 2, 4, 9, 4, 8, 5,
        9, 0, 2, 3, 9, 4, 3, 6, 9, 2, 1, 1, 9, 8, 6, 0],
       [9, 1, 1, 5, 9, 6, 1, 2, 9, 1, 4, 3, 9, 1, 1, 6, 9, 7, 8, 0, 9, 7,
        6, 0, 9, 5, 6, 5, 9, 7, 6, 1, 9, 6, 1, 2, 9, 8, 1, 8, 9, 7, 5, 0,
        9, 7, 0, 0, 9, 4, 6, 7, 9, 8, 4, 8, 9, 1, 2, 7],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 8, 0, 3, 9, 6, 4, 4, 9, 0, 4, 4, 9, 3, 3, 7, 9, 5, 6, 3, 9, 8,
        1, 0, 9, 4, 5, 1, 9, 6, 1, 6, 9, 0, 2, 3, 9, 5, 8, 1, 9, 8, 3, 0,
        9, 7, 2, 8, 9, 4, 6, 5, 9, 3, 6, 5, 9, 0, 3, 4],
       [9, 8, 6, 7, 9, 1, 1, 0, 9, 3, 2, 3, 9, 0, 1, 7, 9, 1, 8, 1, 9, 8,
        1, 7, 9, 4, 5, 5, 9, 0, 0, 8, 9, 8, 2, 3, 9, 0, 3, 6, 9, 6, 3, 2,
        9, 3, 0, 3, 9, 0, 6, 8, 9, 0, 3, 7, 9, 3, 7, 0],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 5, 5, 6, 9, 3, 1, 0, 9, 4, 8, 4, 9, 0, 6, 3, 9, 7, 5, 8, 9, 1,
        7, 4, 9, 8, 8, 6, 9, 7, 0, 7, 9, 5, 8, 1, 9, 5, 7, 7, 9, 2, 5, 1,
        9, 5, 2, 1, 9, 3, 4, 8, 9, 6, 6, 2, 9, 8, 6, 1],
       [9, 0, 4, 7, 9, 4, 1, 0, 9, 8, 6, 7, 9, 1, 3, 3, 9, 3, 4, 2, 9, 1,
        0, 5, 9, 6, 6, 8, 9, 8, 0, 6, 9, 0, 7, 0, 9, 8, 3, 0, 9, 8, 1, 6,
        9, 8, 7, 7, 9, 6, 8, 6, 9, 2, 5, 7, 9, 7, 1, 7],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 2, 4, 0, 9, 0, 5, 5, 9, 3, 8, 2, 9, 6, 4, 2, 9, 7, 4, 2, 9, 4,
        0, 6, 9, 3, 1, 0, 9, 8, 5, 4, 9, 0, 3, 7, 9, 5, 7, 8, 9, 3, 6, 6,
        9, 6, 3, 3, 9, 5, 7, 0, 9, 8, 6, 2, 9, 5, 0, 5],
       [9, 4, 8, 7, 9, 3, 8, 4, 9, 2, 4, 3, 9, 0, 1, 6, 9, 5, 5, 4, 9, 7,
        1, 4, 9, 2, 3, 8, 9, 2, 5, 0, 9, 5, 8, 1, 9, 4, 2, 2, 9, 5, 2, 3,
        9, 3, 1, 2, 9, 3, 5, 7, 9, 6, 7, 1, 9, 8, 5, 0],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 1, 7, 0, 9, 0, 1, 6, 9, 6, 0, 7, 9, 6, 3, 1, 9, 4, 5, 8, 9, 0,
        8, 8, 9, 8, 3, 1, 9, 1, 1, 7, 9, 8, 1, 7, 9, 0, 0, 3, 9, 5, 0, 0,
        9, 5, 0, 4, 9, 7, 8, 5, 9, 4, 4, 2, 9, 4, 3, 5],
       [9, 8, 7, 2, 9, 7, 2, 1, 9, 8, 8, 6, 9, 2, 7, 5, 9, 5, 2, 4, 9, 4,
        4, 7, 9, 1, 6, 7, 9, 6, 7, 1, 9, 4, 0, 5, 9, 6, 1, 7, 9, 0, 5, 8,
        9, 4, 8, 8, 9, 3, 3, 5, 9, 2, 0, 5, 9, 0, 2, 2],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 2, 1, 8, 9, 3, 2, 3, 9, 2, 6, 1, 9, 6, 7, 6, 9, 7, 1, 1, 9, 0,
        3, 0, 9, 8, 1, 8, 9, 0, 4, 5, 9, 0, 2, 2, 9, 7, 7, 7, 9, 2, 7, 6,
        9, 3, 4, 5, 9, 7, 6, 1, 9, 6, 0, 4, 9, 6, 7, 4],
       [9, 6, 3, 3, 9, 7, 8, 8, 9, 1, 7, 3, 9, 7, 3, 2, 9, 6, 1, 5, 9, 0,
        7, 0, 9, 3, 0, 3, 9, 7, 4, 0, 9, 8, 3, 7, 9, 8, 2, 4, 9, 2, 5, 1,
        9, 1, 2, 3, 9, 2, 5, 1, 9, 5, 1, 7, 9, 3, 7, 0],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 7, 3, 6, 9, 3, 7, 4, 9, 7, 2, 3, 9, 1, 8, 5, 9, 8, 3, 7, 9, 2,
        7, 0, 9, 3, 4, 1, 9, 7, 4, 0, 9, 4, 6, 0, 9, 4, 1, 8, 9, 1, 8, 7,
        9, 1, 3, 4, 9, 8, 2, 6, 9, 4, 1, 7, 9, 1, 7, 6],
       [9, 8, 4, 2, 9, 6, 5, 4, 9, 3, 1, 4, 9, 2, 7, 4, 9, 3, 7, 3, 9, 4,
        2, 2, 9, 6, 3, 0, 9, 2, 8, 7, 9, 3, 2, 3, 9, 3, 6, 6, 9, 4, 2, 2,
        9, 8, 3, 1, 9, 8, 4, 6, 9, 4, 4, 5, 9, 8, 5, 2],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
       [9, 3, 7, 2, 9, 7, 3, 8, 9, 0, 1, 0, 9, 5, 0, 0, 9, 1, 3, 6, 9, 1,
        6, 0, 9, 7, 1, 0, 9, 7, 8, 7, 9, 4, 3, 4, 9, 4, 8, 0, 9, 7, 2, 0,
        9, 3, 6, 2, 9, 8, 2, 2, 9, 4, 5, 3, 9, 5, 2, 8],
       [9, 5, 4, 0, 9, 1, 1, 5, 9, 4, 4, 4, 9, 3, 2, 8, 9, 2, 2, 5, 9, 4,
        1, 4, 9, 8, 3, 4, 9, 4, 0, 5, 9, 7, 4, 1, 9, 1, 8, 4, 9, 1, 1, 6,
        9, 0, 8, 0, 9, 5, 5, 7, 9, 3, 8, 3, 9, 7, 1, 8],
       [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]]
)