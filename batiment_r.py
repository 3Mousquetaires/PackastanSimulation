
import csv
import os

import numpy as np

from besoin import StrToTypeBesoin

#Variables globales  ------------------------------------------------------
LISTE_BATIMENT_STR = ["commerce", "maison", "infirmerie", 
    "commissariat", "usine", "eglise", "bar", "espace vert",
    "mairie", "route"]



#  ------------------------------------------------------------------------



BatimentTToStr = { 0:"commerce", 1:"maison",
    2: "infirmerie", 3:"commissariat",
    4:"usine", 5:"eglise", 6:"bar",
    7:"espace_vert", 8:"mairie", 
    9:"route" }



class Batiment :
    def __init__(self, type_, coos, props):
        # == TESTEE ==
        #on va lire le CSV pour récupérer les données.
        str_data = []
        self.kbien = 0 # 0 <= kbien <= 1
        self.historique_kbien = [self.kbien]

        self.coos = coos

        CSV_FILE = os.path.join(os.getcwd(), "info_batiments.csv")

        try:
            with open(CSV_FILE, 'r') as file:
                reader = csv.reader(file)

                for row in reader:
                    if row[0] == BatimentTToStr[  type_]:
                        str_data = row
                        break
        except FileNotFoundError:
            CSV_FILE = CSV_FILE = os.path.join(os.getcwd(), "VilleReelle", "info_batiments.csv")
            
            with open(CSV_FILE, 'r') as file:
                reader = csv.reader(file)

                for row in reader:
                    if row[0] == BatimentTToStr[  type_]:
                        str_data = row
                        break

        #exploitation de str_data :
        self.type = type_
        self.besoin =  StrToTypeBesoin[ str_data[1] ] 
        #traduction de "alimentation" -> TypeBesoin.ALIMENTATION
        self.coeff = int(str_data[2])
        self.capacite = int(str_data[3])
        self.ressource = str_data[4] #ressource graphique
        
        self.population = 0
        
        
        self.autre_props = props["props_"]
        self.id = props["id"]
        self.area = props["area"]


    def AjouterCitoyen(self):
        """renvoie un bool : false si le batiment est plein"""
        if self.population == self.capacite:
            return False
        else :
            self.population += 1
            return True


    def EnleverCitoyen(self):
        self.population -= 1

    
    def ActualiseKbien(self, kbien):
        self.kbien = kbien
        self.historique_kbien.append(self.kbien)
        
        return sum(self.historique_kbien)/len(self.historique_kbien)
        



class Maison(Batiment):
    def __init__(self, coos, props):
        super().__init__(1, coos, props)

        self.memoire_batiments = { k:None for k in range(9) }
        self.memoire_batiments[1] = [self.coos]
        #self.Update_Bats()


    def GetBatiment(self, besoin):
        route = self.memoire_batiments[str(besoin)]

        return route
    
    
    def IsRelated(self, i):
        """Renvoie k si l'annuaire de la maison pointe sur le batiment i pour le besoin k.
        Renvoie -1 sinon."""
        a = []
        for k in self.memoire_batiments:
            if int(k) != 1 and i in self.memoire_batiments[k]:
                a.append(k)
        
        if a == []:
            return [-1]
        return a


    def Update_Bats(self, type_, chemin):
        """SET : update l'annuaire de la maison"""
        self.memoire_batiments[type_] = chemin
        
        
ROAD_AREA = 50

        
class Road(Batiment):
    """Plus un shortcut qu'autre chose, ne contient pas de méthodes additionnelles."""
    def __init__(self, coos, id, node):
        props = {"props_":None, "id":id, "area":ROAD_AREA}
        self.node = node
        super().__init__(9, coos, props)