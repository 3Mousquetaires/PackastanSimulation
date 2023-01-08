# La classe Ville gère le premier étage de simulations.
from matplotlib.figure import figaspect
import numpy as np
import matplotlib.pyplot as plt

from citoyen import Citoyen
import batiment_r
import mapbuilder as mb

import time
import os
from random import choice


import osmnx.graph as grph
import osmnx.distance as dist


# constante qui arrête le premier étage de simulations à 
# l'approche de l'asymptote.
KILL_EPSILON = 1e-4


# Dictionnaire de couleurs pour les types de batiments
type_to_c = {0:'#ed1c24', 1:'#6ABE30', 2:'#5B6EE1',
                3:'#5FCDE4', 4:'#76428A', 5:'#FBF236', 
                6:'#DF7126', 7:'#D77BBA', 8:'#544406',
                9:'#424258'} 


class Ville:
    """## VILLE :\n
    C'est ici qu'est géré le premier étage de simulations. Créé les citoyens 
    et organise leur déplacement. Calcule le coefficient kbien pour chaque batiment
    et s'arrête toute seule à l'approche de l'asymptote.
    """

    def __init__(self, center, batlist, population:int = 1): 
        """\n\tCenter : (long, lat) le centre géographique de la carte
        \n\tbatlist : liste des batiments
        \n\tpopulation : nombre de citoyens à créer
        """
        
        # ========= Premières factorisations pour l'affichage =========
        self.batlist = batlist
        self.center = center
        
        self.coos_listx = [bat.coos[0] for bat in self.batlist]
        self.coos_listy = [bat.coos[1] for bat in self.batlist]
        coos_list = [bat.coos for bat in self.batlist]
        
        self.E = max([x[0] for x in coos_list])
        self.W = min(x[0] for x in coos_list)
        
        self.N = max([y[1] for y in coos_list])
        self.S = min([y[1] for y in coos_list])
        
        self.height = int(self.N-self.S)
        self.width = int(self.E-self.W)
        
        print(" --- \tdimensions :", self.N-self.S, "x", self.E-self.W)
        
        self.color_list = [ type_to_c[bat.type] for bat in self.batlist ]
        self.size_list = [ (1/10000) * bat.area for bat in self.batlist ]

        
        # ======== Création divine des citoyens ==========
        self.population = population
        self.habitants = []

        self._update_list_kbien()
        
        print(" --- Création des citoyens")

        # Le kbien des maisons est impertinent. Nous 
        # les fixons à -0.5 pour les mettre en évidence lors de l'affichage.
        maisonlist = [m for m in self.batlist if m.type == 1]
        for m in maisonlist:
            self.kbien_list[m.id] = -.5
            
        # Idem.
        routeliste = [r for r in self.batlist if r.type == 9]
        for r in routeliste:
            self.kbien_list[r.id] = -.5
            
        # Création des citoyens
        for c in range(self.population):
            citoyen = Citoyen(choice(maisonlist))
            self.habitants.append(citoyen)
            

        print(" --- Initialisation terminée")
        
        

    def highlightMaps(self):
        """???"""
        self.highlightedMaps = []
        for i in range(10):
            tmp = np.zeros((self.height, self.width))
            tmp.fill(-1)
            for j in range(self.height):
                for k in range(self.width):
                    if self.nummap[j][k] == i:
                        tmp[j][k] = i

            self.highlightedMaps.append(tmp)

            

    def start(self):
        """Simulation de de la ville:
        Ne prend aucun paramètre, lance la simulation et renvoie la map des ```kbien```
        """
        self.batToShow = 0
        self.highlightMaps()
        i = 0
        
        # =================== Gestion du tour : jeu et actualisation ===============================
        self.isRunning = True
        self.derivee = []
        
        X = []
        Y = []
        t0 = time.time()
        
        # La durée de convergence est de l'ordre de 170 tours, soient environ 40 secondes
        # sur Strasbourg, taille 3 et 1000 habitants.
        while self.isRunning:
            i+=1
            X.append(i)
            map_kbien_avant = np.copy(self.kbien_list)

            #appel au jeu de chaque citoyen.
            for c in self.habitants:
                resultat = c.tour(self.batlist, should_print = False)
                if type(resultat) != type(None):
                    #Si la méthode tour renvoie un truc, c'est qu'un kbien a été extrait.
                    id_bat = resultat[1]
                    mean_kbien = self.batlist[id_bat].ActualiseKbien(resultat[0])
                    self.kbien_list[id_bat] = mean_kbien 
                    Y.append(self.kbien_list)
            

            if i % 2 == 0: #la map n'a aucun changements aux tours impairs, les citoyens font des aller-retours.
               delta = np.mean(self.kbien_list - map_kbien_avant)
               self.derivee.append(delta)

               if i > 100 and np.mean(self.derivee[-5:]) < KILL_EPSILON :
                    # On affine le calcul sur les 5 derniers tours éviter un pic trop proche de 
                    # l'asymptote qui terminerait la simulation.
                   self.isRunning = False

        deltat = time.time() - t0
        print(f" --- Simulation fini en {i} tours, soient {deltat//60} min {deltat%60} sec.")
        # étrangement, le temps de tour est légèrement croissant.
        return self.kbien_list

        
        
    def _update_list_kbien(self):
        """Met à jour l'attribut self.kbien_list."""
        self.kbien_list = [bat.kbien for bat in self.batlist]
        
        
        
    def get_background(self):
        """N'est plus utilisée, l'affichage de la map d'arrière plan ralentit tout."""
        imgpath = f"./VilleReelle/maps/{self.center}.png"
        
        if os.path.isfile(imgpath):
            print(" --- \tmap trouvée en cache")
            return imgpath
        
        print(" --- \trecherche de la map de background en cours")
        
        print(" --- \t sommets W-N-E-S :", self.W, self.N, self.E, self.S)
        
        URL = f"https://render.openstreetmap.org/cgi-bin/export?bbox={self.W},{self.S},{self.E},{self.N}&scale=10000&format=png"
        
        # Nous n'avons pas réussi à télécharger directement l'image depuis OPENSTREETMAP, 
        # qui est plus sécurisé que ce que nous pensions sur ce genre d'opérations.
        print(" --- map inexistante, cliquer sur ce lien : \n")
        print(URL)
        print(f"merci de la renommer en {self.center}.png")
        
        raise Exception("map inconnue :(")