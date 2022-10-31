from matplotlib.figure import figaspect
import numpy as np
import matplotlib.pyplot as plt
import keyboard
from citoyen import Citoyen
import batiment_r
import time
import os
from random import choice

import mapbuilder as mb

import osmnx.graph as grph
import osmnx.distance as dist


KILL_EPSILON = 1e-4


        
type_to_c = {0:'#ed1c24', 1:'#6ABE30', 2:'#5B6EE1',
                3:'#5FCDE4', 4:'#76428A', 5:'#FBF236', 
                6:'#DF7126', 7:'#D77BBA', 8:'#544406',
                9:'#424258'} #types des batiments en couleurs plt


class Ville:
    def __init__(self, center, batlist, population:int = 1): 
        """# Initialisation de la ville : 
        Permet de créer une ville de taille (height x width), 
        avec éventuellement une map par défaut (fondée uniquement sur les commerces).\n
        S'utilise en instanciation classique : ```city = Ville(h, w)```
        """
        
        self.batlist = batlist
        self.center = center
        
        # ======== On va gérer les dimensions ==========
        self._buildMap()
        
        #affichage. On vise la rapidité.
        self.coos_listx = [bat.coos[0] for bat in self.batlist]
        self.coos_listy = [bat.coos[1] for bat in self.batlist]
        self.coos_list = np.array([bat.coos for bat in self.batlist])
        
        self.color_list = [ type_to_c[bat.type] for bat in self.batlist ]
        self.size_list = [ (1/500) * bat.area for bat in self.batlist ]
        
        
        #Init habitants : Liste des habitants
        self.population = population
        self.habitants = []
        
        print(" --- \tdimensions : ", self.N, self.S, self.E, self.W)

        self._update_list_kbien()
        #self.show_realistic()
        
        
        print(" --- Création des citoyens")
        maisonlist = [m for m in self.batlist if m.type == 1]
        for m in maisonlist:
            self.kbien_list[m.id] = -.5
            
        routeliste = [r for r in self.batlist if r.type == 9]
        for r in routeliste:
            self.kbien_list[r.id] = -.5
            
        for c in range(self.population):
            citoyen = Citoyen(choice(maisonlist))
            self.habitants.append(citoyen)
            
        print(" --- Initialisation terminée")
        
        

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
        
        X = []
        Y = []
        t0 = time.time()
        
        
        #la mettre en false pour terminer le programme
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
                    #print(mean_kbien)
                    self.kbien_list[id_bat] = mean_kbien #mean_kbien
                    #print(self.kbien_list)
                    Y.append(self.kbien_list)
            

            if i % 2 == 0: #la map n'a aucun changements aux tours impairs
               delta = np.mean(self.kbien_list - map_kbien_avant)
               self.derivee.append(delta)

               if i > 100 and np.mean(self.derivee[-5:]) < KILL_EPSILON :
                   self.isRunning = False

        deltat = time.time() - t0
        print(f" --- Simulation fini en {i} tours, soient {deltat//60} min {deltat%60} sec.")
        return self.kbien_list


    def replaceBat(self, x:int, y:int, typeBat:int):
        """# Remplacement :
        Permet de remplacer un batiment en position ```(x, y)```, par un bâtiment de type ```batiment.TypeBatiment```. 
        """
        #TODO
        
        
    def _update_list_kbien(self):
        self.kbien_list = [bat.kbien for bat in self.batlist]
        


    def show_realistic(self):
        plt.style.use('dark_background')
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        
        bbox = (self.W, self.E, self.S, self.N)
        
        print(" --- \tploting", len(self.batlist), "batiments")
        
        # ====== VILLE ==========
        ax_ville = axes[0]
        
        ax_ville.set_box_aspect(1)
        dico = {0:"Commerces", 1:"habitat", 2:"santé", 3:"securité",
                4:"emploi", 5:"moralité", 6:"fete", 7:"physique",
                8:"gestion", 9:"routes"}
        
        ax_ville.scatter(self.coos_listx, self.coos_listy, c=self.color_list, s=self.size_list)
        
        for t in dico:
            ax_ville.scatter([], [], c=type_to_c[t], label=dico[t])


        ax_ville.legend(loc="center left", bbox_transform=fig.transFigure)
        box = ax_ville.get_position()
        ax_ville.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        ax_ville.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=5)
            
        plt.title("Carte des kbiens")
            
        # ====== MAP KBIEN ========
        ax_kbien = axes[1]
        ax_kbien.set_box_aspect(1)    
        
        #cmap = plt.get_cmap('gist_ncar', 1)
        pts = ax_kbien.scatter(self.coos_listx, self.coos_listy, s=self.size_list, c=self.kbien_list, cmap="plasma")
        fig.colorbar(pts)
            
            
            
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



#city = Ville((48.882970, 2.299415))


# 8.25 d'init générale : factoriser

