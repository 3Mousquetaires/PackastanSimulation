import numpy as np
import matplotlib.pyplot as plt
import batiment
import citoyen
import random

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
        for i in range(height):
            for j in range(width):
                self.map_kbien[i][j]=1

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
                self.map.append(bat)
        
        #Init habitants : Liste des habitants
        self.habitants = []
        for i in range(self.population):
            hab = citoyen.Citoyen(self.annuaire[random.randint(0, len(self.annuaire))])
            self.habitants.append(hab)

        self.fig = plt.figure()




        # =================== Gestion du tour : jeu et actualisation =================================
        self.isRunning = True
        #la mettre en false pour terminer le programme

        while self.isRunning:
            #appel au jeu de chaque citoyen.
            for c in self.habitants:
                resultat = c.tour(self.map, should_print = True)

                if type(resultat) == type(None):
                    #Si la méthode tour renvoie un truc, c'est qu'un kbien a été extrait.
                    self.map_kbien[resultat[1]] = resultat[0]






    def print(self):
        """# Impression de la map : 
        Permet d'afficher dans la console la map (sous forme de ```np-array```).
        """
        print(self.map)
    
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
    
    def show_extended(self, m1:np.ndarray, m2:np.ndarray):
        """# Affichage étendu : 
        Permet d'afficher avec ```Matplotlib``` la ville, ainsi qu'une légende sous la forme d'une barre de couleur, ainsi
        que deux matrices complémentaires ```m1``` et ```m2```. 
        """
        plt.subplot(131)
        cmap1 = plt.get_cmap('RdPu', np.max(self.nummap) - np.min(self.nummap) + 1)
        mat1 = plt.imshow(self.nummap, cmap = cmap1, vmin = np.min(self.nummap)-0.5, vmax = np.max(self.nummap)+0.5)
        cax1 = plt.colorbar(mat1, ticks = np.arange(np.min(self.nummap), np.max(self.nummap)+1), orientation="horizontal")

        plt.subplot(132)
        #cmap2 = plt.get_cmap('RdBu', np.max(m1) - np.min(m1) + 1)
        mat2 = plt.imshow(m1)
        cax2 = plt.colorbar(mat2, orientation="horizontal")
        #self.fig.add_subplot(113)
        plt.subplot(133)
        mat3 = plt.imshow(m2)
        cax3 = plt.colorbar(mat3, orientation="horizontal")
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


#Tests : 
city = Ville(100, 100, 300, np.random.randint(0, 9, size=(100, 100)))
city.show_extended(np.random.uniform(low=0.0, high=1.0, size=(50,50)), np.random.randint(0, 10000, size=(500, 500)))
print(city.exportBatmatrice())