from enum import Enum

import csv

import numpy as np

from besoin import StrToTypeBesoin, TypeBesoin

from numba import jit

#Variables globales  ------------------------------------------------------
LISTE_BATIMENT_STR = ["commerce", "maison", "infirmerie", 
    "commissariat", "usine", "eglise", "bar", "espace vert",
    "mairie"]


CSV_FILE = "base/info_batiments.csv"

#  ------------------------------------------------------------------------

class TypeBatiment (Enum):
    """Nécessaire pour sauver de l'espace : 
    stock un type de batiment comme un int au lieu 
    d'une string.\n
    Utiliser le dico BatimentTToStr pour convertir TypeBatiment -> string."""
    COMMERCE = 0
    MAISON = 1
    INFIRMERIE = 2
    COMMISSARIAT = 3
    USINE = 4
    EGLISE = 5
    BAR = 6
    ESPACE_VERT = 7
    MAIRIE = 8
    ROUTE = 9

    def int(self):
        return self.value


BatimentTToStr = { TypeBatiment.COMMERCE:"commerce", TypeBatiment.MAISON:"maison",
    TypeBatiment.INFIRMERIE:"infirmerie", TypeBatiment.COMMISSARIAT:"commissariat",
    TypeBatiment.USINE:"usine", TypeBatiment.EGLISE:"eglise", TypeBatiment.BAR:"bar",
    TypeBatiment.ESPACE_VERT:"espace_vert", TypeBatiment.MAIRIE:"mairie", 
    TypeBatiment.ROUTE:"route" }



class Batiment :
    def __init__(self, type, adresse):
        # == TESTEE ==
        #on va lire le CSV pour récupérer les données.
        str_data = []
        self.kbien = 1 # 0 <= kbien <= 1
        self.adresse = adresse

        with open(CSV_FILE, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                if row[0] == BatimentTToStr[type]:
                    str_data = row
                    break

        #exploitation de str_data :
        self.type = type
        self.besoin =  StrToTypeBesoin[ str_data[1] ] 
        #traduction de "alimentation" -> TypeBesoin.ALIMENTATION
        self.coeff = int(str_data[2])
        self.capacite = int(str_data[3])
        self.ressource = str_data[4] #ressource graphique
        
        self.population = 0


    def AjouterCitoyen(self):
        """renvoie un bool : false si le batiment est plein"""
        if self.population == self.capacite:
            return False
        else :
            self.population += 1
            return True


    def EnleverCitoyen(self):
        self.population -= 1
        



class Maison(Batiment):
    def __init__(self, adresse, map):
        """Chaque maison a une carte, le tilemap.Getmap()"""
        super().__init__(TypeBatiment.MAISON, adresse)

        self.memoire_batiments = { k:None for k in range(9) }
        self.memoire_batiments[1] = [self.adresse]
        self.map = map
        self.Update_Bats()


    def GetBatiment(self, besoin):
        route = self.memoire_batiments[besoin]

        if route == None:
            self.Update_Bats()
        elif self.map[route[-1]] != besoin:
            self.Update_Bats()

        route = self.memoire_batiments[besoin]

        return route

    def Update_Bats(self):
        """Renvoie un dico avec tous les batiments les plus proches en fonctions de
        tous les besoins\n
        Permet d'avoir un appel commun par maison.
        Pour chercher juste certains batiments, il suffit de passer un dico partiellement
        rempli dans Retour0, le prg fill le reste."""

        File = [(self.adresse[0], self.adresse[1], [])]
        deja_vus = []

        while (len(File) != 0) and (None in self.memoire_batiments.values()):
            #Il reste des bouts de route à parcourir et 
            # le dico n'est pas encore rempli
            x, y, accumulateur = File.pop()
            deja_vus.append((x, y))
            #il faut explorer le carré autour
            for i in [x-1, x, x+1]:
                for j in [y-1, y, y+1]:
                    if (i, j) in deja_vus:
                        continue
                    try:
                        if self.map[i, j] == 9: #une route                            
                            # explications accumulateur :
                            # l'acc garde en mémoire la généalogie du point
                            File.append( (i, j, accumulateur + [(x, y)]) )
                            continue
                    except IndexError:
                        #on est hors de la map, inutile de continuer
                        continue

                    if self.memoire_batiments[ self.map[i, j] ] == None:
                        self.memoire_batiments[ self.map[i, j] ] = accumulateur + [(x, y), (i, j)] #(i, j) #on a trouvé une adresse
