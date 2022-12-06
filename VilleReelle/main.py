"""Fichier central, gère la génération du jeu, des villes et leurs exploitation"""

from mapbuilder import MapBuilder
from ville import Ville

import numpy as np
import matplotlib.pyplot as plt

import batiment_r as bat

import time


class Core():
    def __init__(self, center, population):
        """Initialisation du jeu."""
        self.mb = MapBuilder(center)
        self.mb.LoadFromMemory()
        
        
        self.center = center
        self.population = population
        
        
        
        
    def _lancer_simulation(self):
        """Lance une simulation qui s'arrête à l'asymptote. Renvoie la kbien."""
        V = Ville(self.center, self.mb.GetBatList(), self.population)
        
        data = V.start()
        
        kbien = self._compute_mean(data)
        print(" --- RESULTAT FINAL :", kbien)
        
        V.show_realistic()
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
            
        self.mb.SetBat(i, newbat)
            
        self.mb.ActualiseGraphe(i)
        
        
    def _compute_mean(self, data):
        """En attendant de faire marcher np.nonzero..."""
        k = data.count(-.5)
        n = len(data)-data.count(0)-k
        return (sum(data) + k*.5)/n
    
    
    def _mean_kbien(self, k):
        """Renvoie la moyenne bien calculée de tous les batiments du type k"""
        
        for i in range(len(self.MB.batlist)):
            pass
        

maps = {
    "Paris centre 2": (48.86934, 2.31739),
    "Paris centre 3": (),
    "Strasbourg centre 2": (48.5825, 7.7477)
}


if __name__ == "__main__":
    C = Core((47.2737, 4.8264), 1000)
    #C = Core((48.86934, 2.31738), 500_000)
    C._lancer_simulation()
    #C.ReplaceBat(1, 4)
    
    print("fin")



    
    
    
#   Grande Tailles :
# Strasbourg centré sur la grande île : (48.5825, 7.7477)
# Strasbourg centré sur le Kléber : (48.5944, 7.7540)
# Paris centré sur l'Elysée : (48.86934, 2.31738)