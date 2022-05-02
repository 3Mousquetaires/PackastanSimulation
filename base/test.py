#junkfile pour tester l'état actuel du programme

from batiment import Batiment, TypeBatiment
from citoyen import Citoyen
import numpy as np
import matplotlib.pyplot as plt
#from pygame import game

import os
from random import choice

from batiment import TypeBatiment

ville = [
    [TypeBatiment(choice([0, 1, 2, 3, 4, 5, 6, 7, 8])) for _ in range(60)]
    for _ in range(60)
]



def faire_batville():
    lenx, leny = 60, 60

    batville = []
    for i in range(leny//2):
        j = 0
        batligne = []
        while j < lenx:
            bat = choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
            batligne.append(9)
            batligne += [bat]*3
            j += 4
        batville.append(batligne)
        batville.append(batligne)
        batville.append([9 for _ in range(lenx)])
    
    return np.array(batville)

#question : comment apposer un graphe sur les routes

print(faire_batville())


    

