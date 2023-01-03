"""Fichier central, gère la génération du jeu, des villes et leurs exploitation"""

from mapbuilder import MapBuilder
from ville import Ville

import numpy as np
import matplotlib.pyplot as plt

import batiment_r as bat

import time
import random
import sys

np.set_printoptions(threshold=sys.maxsize)

SEUIL = 0.5

class Core():
    def __init__(self, center, population):
        """Initialisation du jeu."""
        self.mb = MapBuilder(center)
        self.mb.LoadFromMemory()
        
        
        self.center = center
        self.population = population
        
        
        
        
    def _lancer_simulation(self, should_show = True):
        """Lance une simulation qui s'arrête à l'asymptote. Renvoie la kbien."""
        V = Ville(self.center, self.mb.GetBatList(), self.population)
        
        data = V.start()
        
        kbien = self._compute_mean(data)
        print(" --- RESULTAT FINAL :", kbien)
        
        if should_show:
            V.show_realistic()
        
        print(" -- Tableau des catégories :")
        for k in range(9):
            print(f"--\t {k} : {self._mean_kbien(data, k)}")
            
        
        # return kbien
        
        
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

def renforcement():
    listeActions = []
    C = Core((47.5042, 6.8252), 1000)
    lkbien, kbienmoyen = C.Lancer_simulation(False)
    while(kbienmoyen <= SEUIL):
        rd = random.randint(0, 100)
        if rd < 20:
            
        else:
            


if __name__ == "__main__":
    

