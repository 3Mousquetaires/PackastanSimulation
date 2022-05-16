import pygame
from pygame.locals import *
import numpy as np
import tileset
import tilemap
import game
from base.batiment import TypeBatiment, RENDER_BATMATRICE
from base.besoin import TypeBesoin

from base.citoyen import Citoyen


file='ressources/tileset.png'

game = game.Game()

print(game.tilemap.get_map())
map = game.tilemap.get_map()


game.run()