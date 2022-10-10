from email.policy import default
from os import kill
from typing import NewType, final
from batiment import TypeBatiment
from ville import *
from re import M
from tokenize import Double
import numpy as np
import matplotlib.pyplot as plt
import keyboard
import batiment
import citoyen
import time
import random
import defaultMap as dm
import map_test
import csv
import sys

np.set_printoptions(threshold=sys.maxsize)
defaultMap = dm.defaultMap

valeurs = []

file = open("history.csv", "w", newline="")
writer = csv.writer(file)

listeActions = []

def remplacement(map, x, y, newType):
    map[x][y] = newType;
    return map

def remplacementAleatoire(map, x,y):
    old_type = map[x][y]
    nextype = random.randint(0, 8)
    if(nextype == old_type):
        nextype = 8-nextype
    return remplacement(map, x, y, nextype)

def minkbien(map, mapkb):
    localmin = 1
    x, y = 0, 0
    for i in range(len(mapkb)):
        for j in range(len(mapkb[i])):
            if (mapkb[i][j] < localmin and map[i][j] != 9):
                localmin = mapkb[i][j]
                x, y = i, j
    return x, y

def etape_exploration(map, mapkb):
    kbienmoyen = np.mean(mapkb)
    x, y = minkbien(map, mapkb)
    oldtype = map[x][y]
    map = remplacementAleatoire(map, x, y)
    newtype = map[x][y]
    return kbienmoyen, map, oldtype, newtype

def exploration(map, mapkb):
    city = Ville(len(map), len(map[1]), len(map)*len(map[1]), map)
    map, mapbk = city.start()
    oldkbmoy, newmap, oldtype, newtype = etape_exploration(map, mapkb)
    city = Ville(len(newmap), len(newmap[1]), len(newmap)*len(newmap[1]), newmap)
    map, mapkb = city.start()
    newkb = np.mean(mapkb)
    listeActions.append((oldtype, newtype, (newkb-oldkbmoy)))
    return map, mapkb

def getMaxBatDeltaKb(oldbat):
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


def etape_exploitation(map, mapkb):
    kbmoyen = np.mean(mapkb)
    x, y = minkbien(map, mapkb)
    oldtype = map[x][y]
    newtype = getMaxBatDeltaKb(oldtype)
    map[x][y] = newtype
    return kbmoyen, map, oldtype, newtype

def exploitation(map, mapkb):
    city = Ville(len(map), len(map[1]), len(map)*len(map[1]), map)
    map, mapkb = city.start()
    oldkbmoy, newmap, oldtype, newtype = etape_exploitation(map, mapkb)
    city = Ville(len(newmap), len(newmap[1]), len(newmap)*len(newmap[1]), newmap)
    map, mapkb = city.start()
    newkb = np.mean(mapkb)
    listeActions.append((oldtype, newtype, (newkb-oldkbmoy)))
    return map, mapkb

def renforcement():
    city = Ville(len(defaultMap), len(defaultMap[0]), len(defaultMap)*len(defaultMap[0]), defaultMap)
    map, map_kbien = city.start(affichageLive=False)
    kbmoy = np.mean(map_kbien)
    while(kbmoy < 0.240):
        rd = random.randint(0, 100)
        if rd < 20:
            map, map_kbien = exploration(map, map_kbien)
        else:
            try:
                map, map_kbien = exploitation(map, map_kbien)
            except ValueError:
                map, map_kbien = exploration(map, map_kbien)
        kbmoy = np.mean(map_kbien)
        writer.writerow([kbmoy])
        print(kbmoy)
    with open('map.txt', 'w') as f:
        print(map.tolist(), file=f)
    city = Ville(len(map), len(map[0]), len(map)*len(map[0]), map, kill_epsilon=0)
    map, map_kbien = city.start(affichageLive=True)

renforcement()
