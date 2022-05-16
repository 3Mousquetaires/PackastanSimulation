from enum import Enum

import csv
from mailbox import MaildirMessage
import os
from turtle import update

from sympy import memoize_property

import game
import pygame

from base.besoin import StrToTypeBesoin, TypeBesoin

#Variables globales  ------------------------------------------------------
LISTE_BATIMENT_STR = ["commerce", "maison", "infirmerie", 
    "commissariat", "usine", "eglise", "bar", "espace vert",
    "mairie"]


CSV_FILE = "base\info_batiments.csv"

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


BatimentTToStr = { TypeBatiment.COMMERCE:"commerce", TypeBatiment.MAISON:"maison",
    TypeBatiment.INFIRMERIE:"infirmerie", TypeBatiment.COMMISSARIAT:"commissariat",
    TypeBatiment.USINE:"usine", TypeBatiment.EGLISE:"eglise", TypeBatiment.BAR:"bar",
    TypeBatiment.ESPACE_VERT:"espace_vert", TypeBatiment.MAIRIE:"mairie", 
    TypeBatiment.ROUTE:"route" }


def RENDER_BATMATRICE(array, taillex, tailley):
    """convention : taillex = nb de batiments sur une ligne, \n
    tailley = nb batiments sur une colonne.\n
    Attention, c'est une liste de TypeBatiments, il faut 
    instancer les classes Batiments !"""
    return [
        [TypeBatiment( array[i, j] ) for j in range(taillex)]
        for i in range(tailley)
    ]



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
        



class Maison(Batiment):
    def __init__(self, type, adresse):
        super().__init__(type, adresse)

        self.memoire_batiments = { k:None for k in range(9) }
        self.Update_Bats()


    def GetBatiment(self, besoin):
        if self.memoire_batiments[besoin] == None:
            self.Update_Bats()

        return self.memoire_batiments[besoin]


    def Update_Bats(self):
        """Renvoie un dico avec tous les batiments les plus proches en fonctions de
        tous les besoins\n
        Permet d'avoir un appel commun par maison.
        Pour chercher juste certains batiments, il suffit de passer un dico partiellement
        rempli dans Retour0, le prg fill le reste."""

        File = [self.adresse]
        deja_vus = []

        map = game.Game().tilemap.get_map()
        while (len(File) != 0) and (None in self.memoire_batiments.values()):
            #Il reste des bouts de route à parcourir et 
            # le dico n'est pas encore rempli
            x, y = File.pop()
            deja_vus.append((x, y))
            #il faut explorer le carré autour
            for i in [x-1, x, x+1]:
                for j in [y-1, y, y+1]:
                    if (i, j) in deja_vus:
                        continue
                    try:
                        if self.memoire_batiments[ map[i, j] ] == None:
                            self.memoire_batiments[ map[i, j] ] = (i, j) #on a trouvé une adresse
                    except IndexError:
                        #on est hors de la map, inutile de continuer
                        continue

                    if map[i, j] == 9: #une route
                        File.append( (i, j) )
