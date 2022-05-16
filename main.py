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



batmatrice = RENDER_BATMATRICE(map, 60, 60)

trouve = np.where(map == TypeBatiment.MAISON.value)


import time

t = time.time()
print("="*50, f"\nPour {len(trouve[0])} maisons :\n")
for i in range(len(trouve[0])):
    paul = Citoyen((trouve[0][i], trouve[1][i]))
    bat = paul.trouverBatiment(TypeBesoin.ALIMENTATION)
    print(map[bat], bat)

print(time.time() - t)

print("helmo !")
game.run()

#résultats des tests :
# - la map est retournée sur elle-même
# - 12.5 minutes pour que les 317 maisons trouvent un supermarché
# - soit environ 2 secondes pour l'algo en lui même