"""Fichier central, gère la génération du jeu, des villes et leurs exploitation"""

from mapbuilder import MapBuilder, Bug
from ville import Ville
from json import dumps

from copy import copy

import numpy as np
import matplotlib.pyplot as plt

import batiment_r as bat

import random
import sys

np.set_printoptions(threshold=sys.maxsize)

SEUIL = 0.5
listeActions = []


        
type_to_c = {0:'#ed1c24', 1:'#6ABE30', 2:'#5B6EE1',
                3:'#5FCDE4', 4:'#76428A', 5:'#FBF236', 
                6:'#DF7126', 7:'#D77BBA', 8:'#544406',
                9:'#424258'} #types des batiments en couleurs plt


SHOULD_FLEX = False

ARCHIVE = None


class Core():
    def __init__(self, center, population):
        """Initialisation du jeu."""
        self.mb = MapBuilder(center)
        self.mb.LoadFromMemory()
        
        self.center = center
        self.population = population
        self.needToGraph = False
        global ARCHIVE
        ARCHIVE = copy(self.mb)

        self.lastV = None
        self.firstV = None

        if SHOULD_FLEX:
            self.flex()


    def start_graphing(self):
        self.needToGraph = True
        plt.style.use('dark_background')
        self.fig, self.axes = plt.subplots(1, 2, figsize=(12, 6))
        self.ax_ville = self.axes[0]
        self.ax_ville.set_box_aspect(1)
        self.dico = {0:"Commerces", 1:"habitat", 2:"santé", 3:"securité",
                4:"emploi", 5:"moralité", 6:"fete", 7:"physique",
                8:"gestion", 9:"routes"}
        self.ax_ville.legend(loc="center left", bbox_transform=self.fig.transFigure)
        self.box = self.ax_ville.get_position()

        box = self.ax_ville.get_position()
        self.ax_ville.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9])
        plt.title("Carte des kbiens")
        self.ax_kbien = self.axes[1]
        self.ax_kbien.set_box_aspect(1)
        self.ax_kbien = self.axes[1]
        self.ax_kbien.set_box_aspect(1)
        self.inistializingGraph = True


    def show_realistic(self, ville):
        self.ax_ville.clear()
        self.ax_kbien.clear()
        
        bbox = (ville.W, ville.E, ville.S, ville.N)
        
        print(" --- \tploting", len(ville.batlist), "batiments")
        
        # ====== VILLE ==========
        
        self.ax_ville.scatter(ville.coos_listx, ville.coos_listy, c= ville.color_list, s= ville.size_list)
        
        for t in self.dico:
            self.ax_ville.scatter([], [], c=type_to_c[t], label=self.dico[t])

        self.ax_ville.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=True, ncol=4)
        title = f"Carte des kbiens {self._compute_mean(ville.kbien_list)}"
        plt.title(title)
            
        # ====== MAP KBIEN ========
        
        #cmap = plt.get_cmap('gist_ncar', 1)
        self.pts = self.ax_kbien.scatter(ville.coos_listx, ville.coos_listy, s=ville.size_list, c=ville.kbien_list, cmap="plasma")
        if self.inistializingGraph :
            self.fig.colorbar(self.pts)
            self.inistializingGraph = False
        plt.pause(0.01)


    def flex(self):
        V = Ville(self.center, self.mb.GetBatList(), self.population)
        V.start()
        self.show_realistic(V)
        
        
        
        
    def Lancer_simulation(self, should_show = False, should_print = False, should_init = True):
        """Lance une simulation qui s'arrête à l'asymptote. Renvoie la kbien."""
        V = Ville(self.center, self.mb.GetBatList(), self.population)
        self.lastV = V

        if should_init:
            self.firstV = V
        
        data = V.start()
        
        kbien_moy = self._compute_mean(data)
        print(" --- RESULTAT FINAL :", kbien_moy)
        print("\n\n")
        
        if should_show:
            self.show_realistic(V)
        
        if should_print:
            print(" -- Tableau des catégories :")
            for k in range(9):
                print(f"--\t {k} : {self._mean_kbien(data, k)}")
            
        return data, kbien_moy
    
        
        
    def ReplaceBat(self, i, type_):
        """Cette méthode écrase le batiment en position i et le remplace un autre
        avec les mêmes caractéristiques si ce n'est son type"""
        oldbat = self.mb.GetBat(i)
        props = {"props_":oldbat.autre_props,
                 "id":oldbat.id,
                 "area":oldbat.area}
        
        if type_ == 1:
            #maison
            newbat = bat.Maison(oldbat.coos, props)
        else :
            newbat = bat.Batiment(type_, oldbat.coos, props)
            
        self.mb.batlist[i-1] = newbat
            
        try:
            self.mb.ActualiseGraphe(i)
        except Bug:
            self.show_realistic(self.lastV)
        
        print(" -- Echange réalisé.")
        
        
    def _compute_mean(self, data):
        """En attendant de faire marcher np.nonzero..."""
        k = data.count(-.5)
        n = len(data)-data.count(0)-k
        return (sum(data) + k*.5)/n
    
    
    def _mean_kbien(self, data, k):
        """Renvoie la moyenne bien calculée de tous les batiments du type k"""
        somme = 0
        n = 0
        
        l = [b.id for b in self.mb.batlist if b.type == k]
        for i in l:
            somme += data[i]
            n += 1
            
        try:    
            return somme/n
        except ZeroDivisionError:
            return 0 #Si le type n'existe pas : 0. TODO : Vérifier la stratégie
                
            
        

maps = {
    "Paris centre 2": (48.86934, 2.31739),
    "Paris centre 3": (),
    "Strasbourg centre 2": (48.5825, 7.7477)
}

### Renforcement

C = Core(((48.5825, 7.748)), 25_000)


def getMaxDeltaKb(oldbat):
    maxdelta = -1
    maxbat = -1
    for (old, new, delta)in listeActions:
        if(old == oldbat):
            if delta > maxdelta:
                maxbat = new
    if(maxdelta < 0 or maxbat == -1):
        raise ValueError
    else:
        return maxbat

    

def exploitation():
    map = C.mb.GetTypeList()
    map_kbien, kbien_moyen = C.Lancer_simulation(False, False)
    pire_bat = np.argmin(map_kbien)
    oldType = map[pire_bat]
    newType = getMaxDeltaKb(oldType)
    C.ReplaceBat(pire_bat, newType)
    newmap = C.mb.GetTypeList()
    newmap_kbien, newkbien_moyen = C.Lancer_simulation(False, False)
    listeActions.append((oldType, newType, newkbien_moyen - kbien_moyen))
    return newkbien_moyen

def exploration():
    map = C.mb.GetTypeList()
    map_kbien, kbien_moyen = C.Lancer_simulation(False, False)
    pire_bat = np.argmin(map_kbien)
    oldType = map[pire_bat]
    nextType = random.randint(0, 8)
    if(nextType == oldType):
        nextType = 8-nextType
    C.ReplaceBat(pire_bat, nextType)
    newmap = C.mb.GetTypeList()
    newmap_kbien, newkbien_moyen = C.Lancer_simulation(False, False)
    listeActions.append((oldType, nextType, newkbien_moyen - kbien_moyen))
    return newkbien_moyen


def renforcement(nb_tours = 200):
    plt.ion()

    newmap = C.mb.GetTypeList()
    map_kbien, kbienmoyen = C.Lancer_simulation(False, False, should_init=True)

    i = 0
    while(kbienmoyen <= SEUIL) or (i < nb_tours):
        print(f"tour numéro {i}")
        i += 1
        try:
            rd = random.randint(0, 100)
            if(rd < 20):
                kbmoy = exploration()
            else:
                try:
                    kbmoy = exploitation()
                except ValueError:
                    kbmoy = exploration()
        except KeyboardInterrupt:
            #C.show_realistic(C.lastV)
            #C.show_realistic(C.firstV)
            break
    C.start_graphing()
    C.Lancer_simulation(True, True)
    
    
    
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        renforcement()
    elif int(sys.argv[1]) == 1:
        #StrasbourgComp()
        print("coucou les petits loups")
    elif int(sys.argv[1]) == 2:
        print("...There's not a soul out there...")
        
        with open(os.path.join(os.getcwd(), "data", "map1.json"), "w") as f:
            f.write(dumps(C.mb._dumpsBatList(), sort_keys=True, indent=4 ))

        renforcement(nb_tours=50)
        
        with open(os.path.join(os.getcwd(), "data", "map2.json"), "w") as f:
            f.write(dumps(C.mb._dumpsBatList(), sort_keys=True, indent=4 ))
        
        #renforcement()
        
    else:
        print("bah chef qu'est ce que tu fais ?")