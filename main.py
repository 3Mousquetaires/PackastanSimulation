"""Fichier central, gère la génération du jeu, des villes et leurs exploitation"""

from mapbuilder import MapBuilder
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
        
        
        
        
    def Lancer_simulation(self, should_show = False, should_print = False):
        """Lance une simulation qui s'arrête à l'asymptote. Renvoie la kbien."""
        V = Ville(self.center, self.mb.GetBatList(), self.population)
        
        data = V.start()
        
        kbien_moy = self._compute_mean(data)
        print(" --- RESULTAT FINAL :", kbien_moy)
        
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
            newbat = bat.Maison(i, oldbat.coos, props)
        else :
            newbat = bat.Batiment(type_, oldbat.coos, props)
            
        self.mb.batlist[i-1] = newbat
            
        self.mb.ActualiseGraphe(i)
        
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

""""
  liste = C.mb.GetTypeList()
"""

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
    map, map_kbien, kbien_moyen = C.Lancer_simulation()
    pire_bat = np.argmin(map_kbien)
    oldType = map[pire_bat]
    newType = getMaxDeltaKb(oldType)
    C.replaceBat(pire_bat, newType)
    newmap, newmap_kbien, newkbien_moyen = C.Lancer_simulation()
    listeActions.append((oldType, newType, newkbien_moyen - kbien_moyen))
    return newkbien_moyen

def exploration():
    map, map_kbien, kbien_moyen = C.Lancer_simulation()
    pire_bat = np.argmin(map_kbien)
    oldType = map[pire_bat]
    nextType = random.randint(0, 8)
    if(nextType == oldType):
        nextType = 8-nextType
    C.replaceBat(pire_bat, nextType)
    newmap, newmap_kbien, newkbien_moyen = C.Lancer_simulation()
    listeActions.append((oldType, nextType, newkbien_moyen - kbien_moyen))
    return newkbien_moyen


def renforcement():
    map, map_kbien, kbienmoyen = C.Lancer_simulation()
    while(kbienmoyen <= SEUIL):
        rd = random.randint(0, 100)
        if(rd < 20):
            kbmoy = exploration()
        else:
            try:
                kbmoy = exploitation()
            except ValueError:
                kbmoy = exploration()
        print(kbmoy)
    C.Lancer_simulation(True, True)
    
    
    
    


if __name__ == "__main__":
    renforcement()