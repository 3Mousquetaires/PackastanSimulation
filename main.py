import pygame
from pygame.locals import *
import numpy as np
import tileset
import tilemap
import game

file='ressources/tileset.png'

game = game.Game()
print(type(game.tilemap.get_map()))
game.run()

