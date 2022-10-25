"""Fichier central, gère la génération du jeu, des villes et leurs exploitation"""

from mapbuilder import MapBuilder
from ville import Ville


class Core():
    def __init__(self, center, population):
        """Initialisation du jeu."""
        self.mb = MapBuilder(center)
        self.mb.LoadFromMemory()
        
        
        self.center = center
        self.population = population
        
        
    def _lancer_simulation(self):
        """Lance une simulation qui s'arrête à l'asymptote. Renvoie la kbien."""
        
        #initialisation de la ville
        V = Ville(self.center, self.mb.GetBatList(), self.population)
        V.start()
        


if __name__ == "__main__":
    C = Core((47.5206, 6.6652), 1)
    C._lancer_simulation()
    
    
    
#   Grande Tailles :
# Strasbourg centré sur la grande île : (48.5825, 7.7477)
# Strasbourg centré sur le Kléber : (48.5944, 7.7540)
# Paris centré sur l'Elysée : (48.86934, 2.31738)