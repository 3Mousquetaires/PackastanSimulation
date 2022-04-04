from enum import Enum

import csv
from mailbox import MaildirMessage
import os

#Variables globales  ------------------------------------------------------
LISTE_BATIMENT_STR = ["commerce", "maison", "infirmerie", 
    "commissariat", "usine", "eglise", "bar", "espace vert",
    "mairie"]


CSV_FILE = "info_batiments.csv"

#  ------------------------------------------------------------------------





class TypeBatiment (Enum):
    """Nécessaire pour sauver de l'espace : 
    stock un type de batiment comme un int au lieu 
    d'une string.\n
    Utiliser le dico TypeToStr pour convertir TypeBatiment -> string."""
    COMMERCE = 0
    MAISON = 1
    INFIRMERIE = 2
    COMMISSARIAT = 3
    USINE = 4
    EGLISE = 5
    BAR = 6
    ESPACE_VERT = 7
    MAIRIE = 8


TypeToStr = { TypeBatiment.COMMERCE:"commerce", TypeBatiment.MAISON:"maison",
    TypeBatiment.INFIRMERIE:"infirmerie", TypeBatiment.COMMISSARIAT:"commissariat",
    TypeBatiment.USINE:"usine", TypeBatiment.EGLISE:"eglise", TypeBatiment.BAR:"bar",
    TypeBatiment.ESPACE_VERT:"espace_vert", TypeBatiment.MAIRIE:"mairie" }






def CreerBatiment(type):
    """Paramètres :
        type : un TypeBatiment, penser à importer l'enum"""
    return Batiment()


class Batiment :
    def __init__(self, type):
        #on va lire le CSV pour récupérer les données.
        str_data = []

        with open(CSV_FILE, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                if row[0] == TypeToStr[type]:
                    str_data = row
                    break

        #exploitation de str_data :
        self.type = type
        self.besoin = str_data[1]
        self.coeff = int(str_data[2])
        self.capacite = int(str_data[3])
        self.ressource = str_data[4] #ressource graphique
        
        


    

    


