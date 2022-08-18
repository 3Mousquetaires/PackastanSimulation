
from re import M
import numpy as np
import matplotlib.pyplot as plt
import keyboard
import batiment
import citoyen
import time
import random
import defaultMap

class Ville:
    def __init__(self, height:int, width:int, population:int = 1,map:np.ndarray=np.array([[]])): 
        """# Initialisation de la ville : 
        Permet de créer une ville de taille (height x width), 
        avec éventuellement une map par défaut (fondée uniquement sur les commerces).\n
        S'utilise en instanciation classique : ```city = Ville(h, w)``` 
        """
        #Init W/H/nb_cit : 

        self.width = width
        self.height = height
        self.population = population
        #Init nummap : Map en int
        if np.shape(map) == (height, width):
            self.nummap = map
        else:
            self.nummap = np.zeros((height, width))
        
        #Init map_kbien : Map des kbien
        self.map_kbien = np.zeros((height, width))

        self.map_saturation = np.zeros((height, width)) 

        #Init map : Map des instances
        self.map = []
        self.annuaire = []
        for i in range(height):
            temp = []
            for j in range(width):
                if self.nummap[i][j] == 1 :
                    bat = batiment.Maison((i, j), self.nummap)
                    self.annuaire.append(bat)
                else:
                    bat = batiment.Batiment(type = batiment.TypeBatiment(self.nummap[i][j]), adresse = (i, j))
                temp.append(bat)
            self.map.append(temp)
        
        #Init habitants : Liste des habitants
        self.habitants = []
        for i in range(self.population):
            hab = citoyen.Citoyen(self.annuaire[random.randint(0, len(self.annuaire)-1)])
            self.habitants.append(hab)

        self.fig = plt.figure()

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
            affichage()
        plt.close(self.fig)
        plt.ioff()
        return self.map_kbien, self.derivee
                    

    def print(self):
        """# Impression de la map : 
        Permet d'afficher dans la console la map (sous forme de ```np-array```).
        """
        print(self.nummap)
    

    def replaceBat(self, x:int, y:int, typeBat: batiment.TypeBatiment):
        """# Remplacement :
        Permet de remplacer un batiment en position ```(x, y)```, par un bâtiment de type ```batiment.TypeBatiment```. 
        """
        self.map[x][y] = typeBat.int()


    def show(self):
        """# Affichage : 
        Permet d'afficher avec ```Matplotlib``` la ville, ainsi qu'une légende sous la forme d'une barre de couleur. 
        """
        def discrete_matshow(data):
            self.fig.add_subplot(111)
            # get discrete colormap
            cmap = plt.get_cmap('RdBu', np.max(data) - np.min(data) + 1)
            # set limits .5 outside true range
            mat = plt.imshow(data, cmap=cmap, vmin=np.min(data) - 0.5, 
                            vmax=np.max(data) + 0.5)
            # tell the colorbar to tick at integers
            cax = plt.colorbar(mat, ticks=np.arange(np.min(data), np.max(data) + 1))
        discrete_matshow(self.nummap)
        plt.show()
    

    def show_extended1( self, m1:np.ndarray, title:str = ""):
        """# Affichage étendu : 
        Permet d'afficher avec ```Matplotlib``` la ville, ainsi qu'une légende sous la forme d'une barre de couleur, ainsi
        qu'une matrice complémentaire ```m1```. 
        """
        plt.ion()
        
        plt.subplot(121)
        cmap1 = plt.get_cmap('RdPu', np.max(self.nummap) - np.min(self.nummap) + 1)
        mat1 = plt.imshow(self.nummap, cmap = cmap1, vmin = np.min(self.nummap)-0.5, vmax = np.max(self.nummap)+0.5)
        cax1 = plt.colorbar(mat1, ticks = np.arange(np.min(self.nummap), np.max(self.nummap)+1), orientation="horizontal")

        plt.subplot(122)
        mat2 = plt.imshow(m1)
        cax2 = plt.colorbar(mat2, orientation="horizontal")
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.suptitle(title)
        plt.show()
    

    def show_extended2(self, m1:np.ndarray, m2:np.ndarray, title:str=""):
        """# Affichage étendu : 
        Permet d'afficher avec ```Matplotlib``` la ville, ainsi qu'une légende sous la forme d'une barre de couleur, ainsi
        que deux matrices complémentaires ```m1``` et ```m2```. 
        """
        plt.ion()
        plt.subplot(131)
        plt.title("Carte")
        cmap1 = plt.get_cmap('gist_ncar', np.max(self.nummap) - np.min(self.nummap) + 1)
        mat1 = plt.imshow(self.nummap, cmap = cmap1, vmin = np.min(self.nummap)-0.5, vmax = np.max(self.nummap)+0.5)
        cax1 = plt.colorbar(mat1, ticks = np.arange(np.min(self.nummap), np.max(self.nummap)+1), orientation="horizontal")
        plt.subplot(132)
        plt.title("Carte des kbien")
        mat2 = plt.imshow(m1)
        cax2 = plt.colorbar(mat2, orientation="horizontal")
        plt.subplot(133)
        plt.title("Carte des " + batiment.LISTE_BATIMENT_STR[self.batToShow] + "s")
        mat3 = plt.imshow(m2)
        cax3 = plt.colorbar(mat3, orientation="horizontal")
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.suptitle(title)
        plt.show()


    def exportBatmatrice(self) -> np.ndarray:
        """# Exportation de la matrice de bâtiments : 
        Permet d'exporter la matrice de bâtiments sous forme d'un ```np.ndarray``` de dimension ```(w, h)```.
        """
        array = np.zeros((self.height, self.width), dtype=batiment.TypeBatiment)
        for i in range(self.height):
            for j in range(self.width):
                array[i][j] = batiment.TypeBatiment(self.nummap[i][j])
        return array



city = Ville(90, 60, 5400, defaultMap.defaultMap)
_, b = city.start()

plt.figure()
plt.plot(b)
plt.show()
