from pygame.locals import *
import game


file='ressources/tileset.png'

game = game.Game(500_000)

print(game.tilemap.get_map())
map = game.tilemap.get_map()

game.run()