import numpy as np
import matplotlib.pyplot as plt
import keyboard
import batiment_r
import citoyen
import time
import os

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
        self.size_list = [ (1/200) * bat.area for bat in self.batlist ]
        
        
        #Init habitants : Liste des habitants
        self.population = population
        self.habitants = []
        
        print(" --- \tdimensions : ", self.N, self.S, self.E, self.W)

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


    def replaceBat(self, x:int, y:int, typeBat:int):
        """# Remplacement :
        Permet de remplacer un batiment en position ```(x, y)```, par un bâtiment de type ```batiment.TypeBatiment```. 
        """
        #TODO
        
        

        


    def show_realistic(self):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(7.8, 7))
        
        
        #imgpath = self.get_background()
        #bck = plt.imread(imgpath)
        
        
        bbox = (self.W, self.E, self.S, self.N)
        #ax.imshow(bck, zorder=0, extent=bbox, aspect='equal')
        
        print(" --- \tploting", len(self.batlist), "batiments")
        
        dico = {0:"Commerces", 1:"habitat", 2:"santé", 3:"securité",
                4:"emploi", 5:"moralité", 6:"fete", 7:"physique",
                8:"gestion"}
        
        sc = ax.scatter(self.coos_listx, self.coos_listy, c=self.color_list, s=self.size_list)
        
        for t in dico:
            ax.scatter([], [], c=type_to_c[t], label=dico[t])

        fig.subplots_adjust(right=0.8)
        ax.legend(loc="center left",     bbox_to_anchor=(0.8, 0.5), bbox_transform=fig.transFigure)
            
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
