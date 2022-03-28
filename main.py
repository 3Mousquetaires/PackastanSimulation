import pygame
import time

class Ville:
    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = 0

    def generer( self ) :
        with open( self.fichier, "r") as fichier:
            structure_ville = []
            for ligne in fichier:
                ligne_ville = []
                for sprite in ligne:
                    if sprite != '\n' :
                        ligne_ville.append(sprite)
                structure_ville.append(ligne_ville)
            self.structure = structure_ville

    def afficher( self, fenetre):
        fenetre.blit(accueil, (0,0))


pygame.init()
fenetre = pygame.display.set_mode((750, 750))
image_ville="ville2.png"

accueil = pygame.image.load(image_ville).convert()
fenetre.blit(accueil, (0,0))
pygame.display.flip()