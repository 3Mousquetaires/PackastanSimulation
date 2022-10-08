
from email.header import Header
import hashlib
from re import M
from tokenize import Double
import numpy as np
import matplotlib.pyplot as plt
import keyboard
import batiment_r
import citoyen
import time
import random
import defaultMap
import requests
import shutil
import os

import mapbuilder as mb

import osmnx.graph as grph
import osmnx.distance as dist


        
type_to_c = {0:'#ed1c24', 1:'#6ABE30', 2:'#5B6EE1',
                3:'#5FCDE4', 4:'#76428A', 5:'#FBF236', 
                6:'#DF7126', 7:'#D77BBA', 8:'#544406',
                9:'#424258'} #types des batiments en couleurs plt


class Ville:
    def __init__(self, center, population:int = 1, kill_epsilon=0): 
        """# Initialisation de la ville : 
        Permet de créer une ville de taille (height x width), 
        avec éventuellement une map par défaut (fondée uniquement sur les commerces).\n
        S'utilise en instanciation classique : ```city = Ville(h, w)```
        \nkill_epsilon conseillé : 1e-4. Laisser à 0 pour que le tour ne s'arrête pas. 
        """
        
        self.kill_epsilon = 1e-4 #si la dérivée moyenne des 5 derniers tours descend sous 10^-6, le tour est fini
        self.center = center

        # ======== On va initialiser la ville ===========
        MB = mb.MapBuilder(center)
        print(" --- initialisation des bâtiments")
        self.batlist = MB.CreateBatListe()
            
        
        
        # ======== On va gérer les dimensions ==========
        self._buildMap()
        print("\n --- initialisation de la carte")
        self.imgpath = self.get_background()
        
        #affichage. On vise la rapidité.
        self.coos_listx = [bat.coos[0] for bat in self.batlist]
        self.coos_listy = [bat.coos[1] for bat in self.batlist]
        self.coos_list = np.array([bat.coos for bat in self.batlist])
        
        self.color_list = [ type_to_c[bat.type] for bat in self.batlist ]
        self.size_list = [ (1/50) * bat.area for bat in self.batlist ]
        
        
        #Init habitants : Liste des habitants
        self.population = population
        self.habitants = []
        
        print(" --- \tdimensions : ", self.N, self.S, self.E, self.W)
        
        
        # on initialise toutes les maisons
        print(" --- Initialisation de l'annuaire des maisons")
        maisonlist = [m for m in self.batlist if m.type == 1]
        
        t0 = time.time()
        G = grph.graph_from_bbox(self.N, self.S, self.E, self.W, network_type="all")
        print(" --- \tCréation du graphe : ", time.time()-t0)
        
        t0 = time.time()
        print(" --- \tCréation de l'annuaire")
        
        roadlist = []
        
        print(len(maisonlist))
        
        i = 0
        for m in maisonlist:
            print(i)
            i += 1
            coos = m.coos
            node0 = dist.nearest_nodes(G, coos[0], coos[1])
            
            for k in range(9):
                if k != 1:
                    batf = self.find_closer(coos, k)
                    nodef = dist.nearest_nodes(G, batf.coos[0], batf.coos[1])
                    
                    chemin = dist.shortest_path(G, node0, nodef)
                    roadlist.append(chemin)
                    m.Update_Bats(k, chemin)
                    
        print("Finito !", time.time()-t0)
        

        self.show_realistic()
        
        

    def highlightMaps(self):
        self.highlightedMaps = []
        for i in range(10):
            tmp = np.zeros((self.height, self.width))
            tmp.fill(-1)
            for j in range(self.height):
                for k in range(self.width):
                    if self.nummap[j][k] == i:
                        tmp[j][k] = i

            self.highlightedMaps.append(tmp)
            
            
    def _buildMap(self):
        #Le côté NW et SE :
        coos_list = [bat.coos for bat in self.batlist]
        print(" --- \t ecart-type des batiments :", np.std(coos_list))
        
        self.E = max([x[0] for x in coos_list])
        self.W = min(x[0] for x in coos_list)
        
        self.N = max([y[1] for y in coos_list])
        self.S = min([y[1] for y in coos_list])
        
        self.height = int(self.N-self.S)
        self.width = int(self.E-self.W)
        
        print(" --- \tdimensions :", self.N-self.S, "x", self.E-self.W)
            
            

    def start(self):
        """# Simulation de de la ville:
        Ne prend aucun paramètre, lance la simulation et renvoie la map des ```kbien```
        """
        self.batToShow = 0
        self.highlightMaps()
        i = 0
        def affichage():
            if keyboard.is_pressed("1"):
                self.batToShow =1
            if keyboard.is_pressed("2"):
                self.batToShow = 2
            if keyboard.is_pressed("3"):
                self.batToShow = 3
            if keyboard.is_pressed("4"):
                self.batToShow = 4
            if keyboard.is_pressed("5"):
                self.batToShow = 5
            if keyboard.is_pressed("6"):
                self.batToShow = 6
            if keyboard.is_pressed("7"):
                self.batToShow = 7
            if keyboard.is_pressed("8"):
                self.batToShow = 8
            if keyboard.is_pressed("9"):
                self.batToShow = 9
            if keyboard.is_pressed("0"):
                self.batToShow = 0
            if keyboard.is_pressed("esc"):
                self.isRunning = False
            self.show_extended2(self.map_kbien, self.highlightedMaps[self.batToShow], "Tour : "+str(i))


        
        # =================== Gestion du tour : jeu et actualisation ===============================
        self.isRunning = True
        self.derivee = []
        
        
        #la mettre en false pour terminer le programme
        while self.isRunning:
            i+=1
            map_kbien_avant = np.copy(self.map_kbien)

            #appel au jeu de chaque citoyen.
            for c in self.habitants:
                resultat = c.tour(self.map, should_print = False)
                if type(resultat) != type(None):
                    #Si la méthode tour renvoie un truc, c'est qu'un kbien a été extrait.
                    coord_bat = resultat[1]

                    mean_kbien = self.map[coord_bat[0]][coord_bat[1]].ActualiseKbien(resultat[0])
                    self.map_kbien[coord_bat] = mean_kbien
            

            if i % 2 == 0: #la map n'a aucun changements aux tours impairs
                delta = np.mean(self.map_kbien - map_kbien_avant)
                self.derivee.append(delta)

                if i > 10 and np.mean(self.derivee[-5:]) < self.kill_epsilon :
                    self.isRunning = False


        plt.close(self.fig)
        plt.ioff()
        return self.map_kbien


    def replaceBat(self, x:int, y:int, typeBat: batiment_r.TypeBatiment):
        """# Remplacement :
        Permet de remplacer un batiment en position ```(x, y)```, par un bâtiment de type ```batiment.TypeBatiment```. 
        """
        #TODO
        
        

        


    def show_realistic(self):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(7, 7))
        
        bck = plt.imread(self.imgpath)
        
        
        bbox = (self.W, self.E, self.S, self.N)
        ax.imshow(bck, zorder=0, extent=bbox, aspect='equal')
        
        print(" --- \tploting", len(self.batlist), "batiments")
        
        ax.scatter(self.coos_listx, self.coos_listy, c=self.color_list, s=self.size_list)
            
        plt.show()
        
        
    def get_background(self):
        imgpath = f"./VilleReelle/maps/{self.center}.png"
        
        if os.path.isfile(imgpath):
            print(" --- \tmap trouvée en cache")
            return imgpath
        
        print(" --- \trecherche de la map de background en cours")
        
        print(" --- \t sommets W-N-E-S :", self.W, self.N, self.E, self.S)
        
        URL = f"https://render.openstreetmap.org/cgi-bin/export?bbox={self.W},{self.S},{self.E},{self.N}&scale=10000&format=png"
        
        #https://render.openstreetmap.org/cgi-bin/export?bbox=7.7193546295166025,48.58103633431289,7.767333984375001,48.588389089026066&scale=11447&format=png
        #https://render.openstreetmap.org/cgi-bin/export?bbox=2.2958973333333335,48.8716851 99 99 99 95,2.3184674615384613,48.88672527272727&scale=10000&format=png
        print(" --- map inexistante, cliquer sur ce lien : \n")
        print(URL)
        print(f"merci de la renommer en {self.center}.png")
        
        raise Exception("map inconnue :(")


    def exportBatmatrice(self) -> np.ndarray:
        """# Exportation de la matrice de bâtiments : 
        Permet d'exporter la matrice de bâtiments sous forme d'un ```np.ndarray``` de dimension ```(w, h)```.
        """
        array = np.zeros((self.height, self.width), dtype=batiment_r.TypeBatiment)
        for i in range(self.height):
            for j in range(self.width):
                array[i][j] = batiment_r.TypeBatiment(self.nummap[i][j])
        return array


city = Ville((48.58310, 7.74863))
#city = Ville((48.882970, 2.299415))


# 8.25 d'init générale : factoriser

# TODO : 
#   Faire la couche d'au dessus, 
#       ammener la gestion des jeux à la chaîne
#   Factoriser l'init générale
#   Serialiser : créer un graphe

