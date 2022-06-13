from pygame.locals import *
import game

import matplotlib.pyplot as plt


file='ressources/tileset.png'

game = game.Game(500_000)

print(game.tilemap.get_map())
map = game.tilemap.get_map()

tickrate = game.run()

plt.plot(tickrate)
plt.show()
