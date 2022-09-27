import numpy as np
import random

def testmap(n):
    map = []
    for i in range(n):
        ligne_actuelle = []
        if i%3 == 0:
            for j in range(n):
                ligne_actuelle.append(9)
            map.append(ligne_actuelle)
        else:
            for j in range(n):
                if j%3 ==0:
                    ligne_actuelle.append(9)
                else:
                    ligne_actuelle.append(random.randint(0, 8))
            map.append(ligne_actuelle)

    return np.asarray(map)