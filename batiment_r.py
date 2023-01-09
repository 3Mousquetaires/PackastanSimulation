# Gère les instances de Batiment et les méthodes associées.
import csv
import os

import numpy as np

from besoin import StrToTypeBesoin

BatimentTToStr = { 0:"commerce", 1:"maison",
    2: "infirmerie", 3:"commissariat",
    4:"usine", 5:"eglise", 6:"bar",
    7:"espace_vert", 8:"mairie", 
    9:"route" }



class Batiment :
    """## Batiment : \nReprésente la classe mère de tous les batiments.
    \n Contient les données urbaines des instances, le résultat du kbien et 
    permet de gérer la quantité de monde dans le batiment."""

    def __init__(self, type_, coos, props):
        """Type_ : int de [0; 9], numéro du besoin auquel répondra l'instance
            \ncoos : float tuple (long, lat), coordonées géographiques
            \nprops : dic contenant les autres propriétés du batiment :
                \n\tid : identifiant du batiment
                \n\tarea : aire du batiment
                \n\tprops_ : autres propriétés du batiment (voir les classes filles)"""

        # on va lire le CSV pour récupérer les données.
        # Fichier CSV : info_batiments.csv
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
            # permet de lancer le programme depuis le dossier VilleReelle, utile en Debug
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
        self.coeff = (str_data[2])
        self.capacite = int(str_data[3])
        self.ressource = str_data[4] #ressource graphique
        
        self.population = 0
        
        self.autre_props = props["props_"]
        self.id = props["id"]
        self.area = props["area"]


    def AjouterCitoyen(self):
        """Gère l'entrée d'un citoyen dans le batiment.
        \nRenvoie True et incrémente l'attribut population si l'entrée est possible, False sinon."""
        if self.population == self.capacite:
            return False
        else :
            self.population += 1
            return True


    def EnleverCitoyen(self):
        """Décrémente l'attribut population, à utiliser lors de la sortie d'un citoyen du batiment."""
        self.population -= 1

    
    def ActualiseKbien(self, kbien):
        """Renvoie la nouvelle moyenne du kbien du batiment, actualisée avec la valeur 
        passée en argument."""
        self.kbien = kbien
        self.historique_kbien.append(self.kbien)
        
        return sum(self.historique_kbien)/len(self.historique_kbien)
        



class Maison(Batiment):
    """## Maison : \nFille de Batiment, représente une maison, contient un annuaire des batiments auxquels elle est reliée.
    En effet, le pathfinding dans la ville est factorisé au niveau \"maison\" : elles contiennent
    les positions des batiments les plus proches de chaque type et un chemin vers chacun d'entre eux."""

    def __init__(self, coos, props):
        super().__init__(1, coos, props)

        # annuaire des batiments auxquels la maison est reliée
        self.memoire_batiments = { k:None for k in range(9) }
        self.memoire_batiments[1] = [self.coos]


    def GetBatiment(self, besoin):
        try:
            route = self.memoire_batiments[str(besoin)]
        except KeyError:
            # Un bug inconnu créé certaines instances avec des keys de type int, d'autres de types string.
            # On gère les deux cas.
            return self.memoire_batiments[besoin]

        return route
    
    
    def IsRelated(self, i):
        """Renvoie [k] si l'annuaire de la maison pointe sur le batiment i pour le besoin k.
        Renvoie [-1] sinon.
        \n La méthode renvoie bien une liste, utile en debug et si le MapBuilder, dans ses imprécisions, 
        créé des maisons reliées à plusieurs batiments pour un même besoin."""
        a = []
        for k in self.memoire_batiments:
            if int(k) != 1 and i in self.memoire_batiments[k]:
                a.append(k)
        
        if a == []:
            return [-1]
        return a


    def Update_Bats(self, type_, chemin):
        """Assesseur de l'annuaire de la maison, permet de mettre à jour le chemin vers un batiment."""
        self.memoire_batiments[type_] = chemin
        
        
ROAD_AREA = 50
        
class Road(Batiment):
    """## Road : \nFille de Batiment, ne contient pas de méthodes additionnelles. 
    \nContient l'attribut node, permet de croiser les données avec OPENSTREETMAP lors
    des pathfindings."""
    def __init__(self, coos, id, node):
        props = {"props_":None, "id":id, "area":ROAD_AREA}
        self.node = node
        super().__init__(9, coos, props)