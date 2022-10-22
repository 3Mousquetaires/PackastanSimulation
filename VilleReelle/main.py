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
        
        


if __name__ == "__main__":
    C = Core((48.5804, 7.7488), 1)
    C._lancer_simulation()