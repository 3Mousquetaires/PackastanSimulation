import pygame
from pygame.locals import *
import numpy as np
import tileset
from tilemap import *
import random

from base.batiment import Maison, Batiment, TypeBatiment
from base.citoyen import Citoyen

file='ressources/tileset.png'

class Game:
    W = 600
    H = 600
    SIZE = W, H

    def __init__(self, n_citoyen = 0):
        """Classe moteur graphique + interface backend
        Gère la ville entière"""
        #On commence par la partie graphique
        pygame.init()
        self.tileset = tileset.Tileset(file)
        self.tilemap = Tilemap(self.tileset)
        self.screen = pygame.display.set_mode((600, 600))

        self.tilemap.set_zero()
        pygame.display.set_caption('Packastan')
        self.running = True

        listemaison = []

        #on créé maintenant la batmatrice à partir de la tileset
        matrice_liste = []
        for ligne_bat_int in range(self.tilemap.get_map().shape[0] ):
            ligne = []
            for bat_int in range(self.tilemap.get_map().shape[1]):
                type_bat = TypeBatiment(self.tilemap.get_map()[ligne_bat_int][bat_int])
                if type_bat == TypeBatiment.MAISON:
                    bat = Maison((ligne_bat_int, bat_int), self.tilemap.get_map())
                    listemaison.append(bat)
                    print(bat.memoire_batiments)
                else:
                    bat = Batiment(type_bat, (ligne_bat_int, bat_int))
                ligne.append(bat)
        
            matrice_liste.append(ligne)
        self.batmarice = np.asarray(matrice_liste)

        #Maintenant : la liste des citoyens
        self.ncitoyen = n_citoyen
        self.citoyenliste = []
        for i in range(self.ncitoyen):
            c = Citoyen(random.choice(listemaison))
            self.citoyenliste.append(c)

    

#====================Définition des commandes pour le Kommander====================
    def quit(self):
        self.running = False

    def printmap(self):
        print(self.tilemap.map)
        return
        
    def reset(self):
        self.tilemap.set_zero()
        return

    def vannish(self):
        for i in range(60*60*60):
            self.tilemap.map[random.randint(0, 59)][random.randint(0, 59)] = 0
            pygame.time.wait(1);
            self.tilemap.render()
            self.tilemap.image = pygame.transform.scale(self.tilemap.image, (600, 600))
            self.screen.blit(self.tilemap.image, self.tilemap.rect)
            pygame.display.update()
        return

    def help(self):
        print("""
        Commandes disponibles :
        - quit : quitter le programme
        - reset : remettre la carte à zéro
        - vannish : effacer la carte
        - printmap : afficher la carte
        - help : afficher la liste des commandes
        """)
        return

    def kommander(self, commande):
        commandes = {
            "quit": self.quit,
            "reset": self.reset,
            "vannish": self.vannish,
            "printmap" : self.printmap,
            "help": self.help
        }
        commandes.get(commande)()

        

    #=================== MOTEUR GRAPHIQUE ====================
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                elif event.type == KEYDOWN:
                    if event.key == K_m:
                        print(self.tilemap.map)
                    elif event.key == K_r:
                        self.tilemap.set_random()
                    elif event.key == K_z:
                        self.tilemap.set_zero()
                    elif event.key == K_g:
                        for i in range(60*60*60):
                            self.tilemap.map[random.randint(0, 59)][random.randint(0, 59)] = 0
                            pygame.time.wait(1);
                            self.tilemap.render()
                            self.tilemap.image = pygame.transform.scale(self.tilemap.image, (600, 600))
                            self.screen.blit(self.tilemap.image, self.tilemap.rect)
                            pygame.display.update()
                    elif event.key == K_k:
                        command = input("Commande@PackastanSimulation >$ ")
                        try:
                            self.kommander(command)
                        except:
                            print("Commande inconnue")
                            self.help()
                        
                        
                    #elif event.key == K_s:
                    #    self.save_image()
                            
            self.screen.blit(self.tilemap.image, self.tilemap.rect)
            pygame.display.update()
        pygame.quit()

    #=================== BACKEND ========================
    # coucou