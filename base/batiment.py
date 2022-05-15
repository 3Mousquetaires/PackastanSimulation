from enum import Enum

import csv
from mailbox import MaildirMessage
import os

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
        



    

    


