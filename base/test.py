#junkfile pour tester l'état actuel du programme

from batiment import Batiment, TypeBatiment
from citoyen import Citoyen
from numpy import log
import matplotlib.pyplot as plt

import os



c = Citoyen()

DATA = [ [.99] for _ in range(9) ]
Legend = []

color = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'orange', 'darkred']

N = 7

Legend.append(0)


for i in range(N):
    Legend.append(i+1)
    c.selectionnerBesoin()
    bs = c.getbesoins()
    for j in range(9):
        DATA[j].append( ( bs[j]))

    pass


for i in range(9):
    plt.plot(Legend, DATA[i], color=color[i], label=str(i))

plt.legend()
plt.show()


