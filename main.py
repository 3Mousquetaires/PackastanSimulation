"""Fichier central, gère la génération du jeu, des villes et leurs exploitation"""

from mapbuilder import MapBuilder, Bug
from ville import Ville

from copy import copy

import numpy as np
import matplotlib.pyplot as plt

import batiment_r as bat

import time
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
        
        global ARCHIVE
        ARCHIVE = copy(self.mb)

        self.lastV = None

        if SHOULD_FLEX:
            self.flex()

    def show_realistic(self, ville):
        plt.style.use('dark_background')
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        
        bbox = (ville.W, ville.E, ville.S, ville.N)
        
        print(" --- \tploting", len(ville.batlist), "batiments")
        
        # ====== VILLE ==========
        ax_ville = axes[0]
        
        ax_ville.set_box_aspect(1)
        dico = {0:"Commerces", 1:"habitat", 2:"santé", 3:"securité",
                4:"emploi", 5:"moralité", 6:"fete", 7:"physique",
                8:"gestion", 9:"routes"}
        
        ax_ville.scatter(ville.coos_listx, ville.coos_listy, c=ville.color_list, s=ville.size_list)
        
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
        pts = ax_kbien.scatter(ville.coos_listx, ville.coos_listy, s=ville.size_list, c=ville.kbien_list, cmap="plasma")
        fig.colorbar(pts)
        plt.draw()

    def flex(self):
        V = Ville(self.center, self.mb.GetBatList(), self.population)
        V.start()
        self.show_realistic(V)
        
        
        
        
    def Lancer_simulation(self, should_show = False, should_print = False):
        """Lance une simulation qui s'arrête à l'asymptote. Renvoie la kbien."""
        V = Ville(self.center, self.mb.GetBatList(), self.population)
        self.lastV = V
        
        data = V.start()
        
        kbien_moy = self._compute_mean(data)
        print(" --- RESULTAT FINAL :", kbien_moy)
        print("\n\n")
        
        if should_show:
            V.show_realistic()
        
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
            self.lastV.show_realistic()
        
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

C = Core((47.5042, 6.8252), 1000)


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
    map_kbien, kbien_moyen = C.Lancer_simulation(True, True)
    pire_bat = np.argmin(map_kbien)
    oldType = map[pire_bat]
    newType = getMaxDeltaKb(oldType)
    C.ReplaceBat(pire_bat, newType)
    newmap = C.mb.GetTypeList()
    newmap_kbien, newkbien_moyen = C.Lancer_simulation(True, True)
    listeActions.append((oldType, newType, newkbien_moyen - kbien_moyen))
    return newkbien_moyen

def exploration():
    map = C.mb.GetTypeList()
    map_kbien, kbien_moyen = C.Lancer_simulation(True, True)
    pire_bat = np.argmin(map_kbien)
    oldType = map[pire_bat]
    nextType = random.randint(0, 8)
    if(nextType == oldType):
        nextType = 8-nextType
    C.ReplaceBat(pire_bat, nextType)
    newmap = C.mb.GetTypeList()
    newmap_kbien, newkbien_moyen = C.Lancer_simulation(True, True)
    listeActions.append((oldType, nextType, newkbien_moyen - kbien_moyen))
    return newkbien_moyen


def renforcement():
    plt.ion()
    newmap = C.mb.GetTypeList()
    map_kbien, kbienmoyen = C.Lancer_simulation(True, True)
    while(kbienmoyen <= SEUIL):
        rd = random.randint(0, 100)
        if(rd < 20):
            kbmoy = exploration()
        else:
            try:
                kbmoy = exploitation()
            except ValueError:
                kbmoy = exploration()
    C.Lancer_simulation(True, True)
    
    
    



if __name__ == "__main__":
    renforcement()