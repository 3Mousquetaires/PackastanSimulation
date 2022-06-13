import pygame
from pygame.locals import *
import game
import random
import app_renforcement
import base.batiment as bat


file='ressources/tileset.png'

game = game.Game()

print(game.tilemap.get_map())
map = game.tilemap.get_map()

type_bat = (random.randint(0 , 8))


l_action = [app_renforcement.ajouter , app_renforcement.retirer ]


etat0 = 50 ; etat1 = 50 ; etat2 = 50 ; etat3 = 50 ; etat4 = 50
etat5 = 50 ; etat6 = 50 ; etat7 = 50 ; etat8 = 50

etats = [ etat0 , etat1 , etat2 , etat3 , etat4 ,etat5 , etat6 , etat7 , etat8 ]

etat_moyen = (etat0 + etat1 + etat2 + etat3 + etat4 + etat5 + etat6 + etat7 + etat8) / 9
etat_precedent = (etat0 + etat1 + etat2 + etat3 + etat4 + etat5 + etat6 + etat7 + etat8) / 9

l_recompense = []
l_etat_vu = []

for i in range(10) :
    app_renforcement.renforcement(type_bat , etats , etat_moyen , etat_precedent , l_recompense , l_etat_vu , l_action , map)
    pygame.display.update()
    game.run()
pygame.quit()