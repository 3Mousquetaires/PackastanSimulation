"""Fichier central, gère la génération du jeu, des villes et leurs exploitation"""

from mapbuilder import MapBuilder
from ville import Ville

import numpy as np
import matplotlib.pyplot as plt

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
        return kbien
        
        
    def _compute_mean(self, data):
        """En attendant de faire marcher np.nonzero..."""
        n = len(data)-data.count(0)
        return sum(data)/n
        

if __name__ == "__main__":
    C = Core((48.5825, 7.7477), 10_000)
    C._lancer_simulation()
    
    
    
#   Grande Tailles :
# Strasbourg centré sur la grande île : (48.5825, 7.7477)
# Strasbourg centré sur le Kléber : (48.5944, 7.7540)
# Paris centré sur l'Elysée : (48.86934, 2.31738)