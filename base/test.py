#junkfile pour tester l'état actuel du programme

from batiment import Batiment, TypeBatiment
from citoyen import Citoyen
from numpy import log
import matplotlib.pyplot as plt
from pygame import game

import os
from random import choice

from batiment import TypeBatiment

ville = [
    [TypeBatiment(choice([0, 1, 2, 3, 4, 5, 6, 7, 8])) for _ in range(60)]
    for _ in range(60)
]


