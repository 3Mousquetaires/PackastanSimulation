import pygame
from pygame.locals import *
import numpy as np
from sympy import arg
import tileset
from tilemap import *
import random

import time

from base.batiment import Maison, Batiment, TypeBatiment
from base.citoyen import Citoyen

file='ressources/tileset.png'

class Game:
    W = 600
    H = 600
    MAX_TOUR = 6000;
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
        self.command_mode = False
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

        print(len(self.citoyenliste))

    

#====================Définition des commandes pour le Kommander====================
    def quit(self, arg1 = None, arg2=None, arg3=None, arg4=None):
        self.running = False

    def printmap(self, arg1 = None, arg2=None, arg3=None, arg4=None):
        print(self.tilemap.map)
        return
        
    def reset(self, arg1 = None, arg2=None, arg3=None, arg4=None):
        self.tilemap.set_zero()
        return

    def vannish(self, arg1 = None, arg2=None, arg3=None, arg4=None):
        for i in range(60*60*60):
            self.tilemap.map[random.randint(0, 59)][random.randint(0, 59)] = 0
            pygame.time.wait(1);
            self.tilemap.render()
            self.tilemap.image = pygame.transform.scale(self.tilemap.image, (600, 600))
            self.screen.blit(self.tilemap.image, self.tilemap.rect)
            pygame.display.update()
        return

    def getBat(self, posx, posy, arg3=None, arg4=None):
        print(self.batmarice[int(posx)][int(posy)].type)
        return

    def exit(self, arg1 = None, arg2=None, arg3=None, arg4=None):
        self.command_mode = False
        return 

    def help(self, arg1 = None, arg2=None, arg3=None, arg4=None):
        print("""
        Commandes disponibles :
        - quit : quitter le programme
        - reset : remettre la carte à zéro
        - vannish : effacer la carte
        - printmap : afficher la carte
        - whichbat : afficher le type de batiment à la position x,y (2 arguments nécessaires !)
        - help : afficher la liste des commandes
        - exit : quitter l'invite de commande Packastan
        """)
        return


    def checkload(self, posx, posy, arg3 = None, arg4 = None):
        print(self.batmarice[int(posx)][int(posy)].type, self.batmarice[int(posx)][int(posy)].capacite)
        return


    def kommander(self, commande, arg1 = None, arg2=None, arg3=None, arg4=None):
        commandes = {
            "quit": self.quit,
            "reset": self.reset,
            "vannish": self.vannish,
            "printmap" : self.printmap,
            "whichbat" : self.getBat,
            "exit" : self.exit,
            "help": self.help,
            "checkroad": self.checkload
        }
        commandes.get(commandes)(arg1, arg2, arg3, arg4)

        

    #=================== MOTEUR GRAPHIQUE ====================
    def run(self):
        i = 0;
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
                        print("hello g")
                        self.tilemap.render()
                        self.tilemap.image = pygame.transform.scale(self.tilemap.image, (600, 600))
                        self.screen.blit(self.tilemap.image, self.tilemap.rect)
                        pygame.display.update()

                    elif event.key == K_t:
                        #test de la méthode Citoyen.tour
                        print("Tour en cours ! Attention les oreilles !")
                        c = self.citoyenliste[0]

                        #======== bloc à tester =====
                        kbien = c.tour( self.batmarice, True)
                        if kbien != None:
                            #on a fini une expérience, Ethan déboule avec ses
                            #algos
                            print("kbien extrait !", kbien)
                            
                        #============================
                        # bloc testé avec réussite

                        
                    elif event.key == K_k:
                        self.command_mode = True
                        while(self.command_mode):
                            command = input("Commande@PackastanSimulation >$ ").split()
                            command.append("");
                            command.append("");
                            command.append("");
                            command.append("");
                            try:
                                self.kommander(command[0], arg1=command[1], arg2 = command[2], arg3 = command[3], arg4 = command[4])
                            except:
                                print("Commande inconnue")
                                
                                self.help()
                        
                        
                    #elif event.key == K_s:
                    #    self.save_image()
                            
            self.screen.blit(self.tilemap.image, self.tilemap.rect)

            #================ GESTION DU TOUR ================================
            
            
            t0 = time.time()
            nb_kbien = 0 #nombre de résultats extraits
            for c in self.citoyenliste:
                kbien = c.tour( self.batmarice )
                if kbien != None:
                    #on a fini une expérience, Ethan déboule avec ses
                    #algos
                    #print("kbien extrait !", kbien)
                    nb_kbien += 1
                    pass
            print("\n\n=================\ntemps d'éxecution :", time.time() - t0)
            print("nombre de résultats :", nb_kbien)
            print("=================\n\n")

            #=================================================================

            pygame.display.update()
            
        pygame.quit()

    #=================== BACKEND ========================
    # coucou