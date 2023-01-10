import requests as rq
import json
import math
import numpy as np

import time

import networkx as nx
import os
# Vocabulaire anglais : Edges sont les arètes, Nodes sont les sommets

import batiment_r

import osmnx.graph as grph
import osmnx.distance as dist
from osmnx import save_graphml, load_graphml



class Bug (Exception):
    pass



def _deg2rad(angle):
    return angle* np.pi * _EARTH_RADIUS / 180


#CONSTANTES (tout est converti en m/m²)
_LVL_HEIGHT = 2.875
_POP_DENSITY = 0.08333
_EARTH_RADIUS = 6_371.009 * 10**3


_TYPE_TO_TYPE = {
    """Dictionnaire de conversion des types d'OSM en types de batiments.
    Obtenu empiriquement en testant les limites du programme en terme de surface
    urbaine."""

    'retail' : 0,
    'commercial' : 6,
    'greenhouse' : 0, # ?
    'residential' : 1,
    'hotel' : 1,
    'houseboat' : 1,
    'dormitory' : 1,
    'hospital' : 2,
    'kindergarten' : 4,
    'school' : 4,
    'service' : 4,
    'construction' : 4,
    'university' : 4, # :(
    'office' : 4,
    'industrial' : 4,
    'agricultural' : 4,
    'college' : 4,
    'religious': 5,
    'religion' : 5,
    'cathedral' : 5,
    'convent' : 5,
    'chapel' : 5,
    'roof' : 7,
    'kiosk' : 7,
    'public' : 8,
    'administration' : 8,
    'civic' : 3
}



class MapBuilder:
    """ ## MapBuilder :
    Outil intégré de construction de graphe urbain basé sur la zone proche autour d'un point central.
    Contient deux attributs principaux :
    \n\t - batlist : liste des instances batiments de la zone
    \n\t - pfGraph : graphe routier de la zone, utilisé pour le pathfinding."""
    
    def __init__(self, center):
        """Exemple : centre de Strasbourg : (48.58310, 7.74863) (fonctionne sur les coordonées géographiques).\n"""
        self.center = center
        
        self.batlist = []
        self.maisonliste = []
        self.pfGraph = nx.MultiDiGraph()
        
        # Cet attribut sert à répertorier les routes déjà connues avec leur "NodeID"
        self.route_dico = {}
        
       
        
    
    def Initialise(self, size):
        """Faut s'y frotter...\n
        Démarre la construction de l'instance.\n
        Il existe des méthodes pour sérialiser et déserialiser les instances MapBuilders.
        Préférer la déserialisation depuis le cache avec MapBuilder.LoadFromMemory\n
            Temps d'exécution : Strasbourg taille 3, 1h40"""
            
        self.size = size
            
        print(f" --- Initialisation de {self.center} lancée, allez prendre un café.")
        print(" --- \tPremier traitement des bâtiments.")
        self._create_bat_list()
        
        #calcul de la bbox
        coos_list = [bat.coos for bat in self.batlist]
        self.E = max([x[0] for x in coos_list])
        self.W = min(x[0] for x in coos_list)
        
        self.N = max([y[1] for y in coos_list])
        self.S = min([y[1] for y in coos_list])
        
        self.bbox = (self.N, self.S, self.E, self.W)
        
        print(" --- Checkup dénombrement :")
        for k in range(9):
            print(f" --- \t{k} : {len([b for b in self.batlist if b.type == k])}")
        
        
        print(" --- \tCréation du graphe de déplacement.")
        self.pfGraph = grph.graph_from_bbox(self.N, self.S, self.E, self.W, network_type="all")
        
        
        t0 = time.time()
        print(f" --- \tInitialisation des maisons : {len(self.maisonliste)} trouvées.")
        
        # deuxième traitement : init des maisons. Nous les relions toutes 
        # batiments les plus proches pour chaque type de besoin.
        # En même temps, on crée le graphe de déplacement, et on enregistre les routes
        # qu'on emprunte. Elles deviennent des nouvelles instances de batiment_r.Road, ajoutée
        # à la liste des batiments.
        self.route_dico = {}
        
        i = -1
        self.i_route = len(self.batlist)
        for m in self.maisonliste:
            i += 1
            print(i) # Quand ce compteur atteint len(self.maisonliste), la création de l'objet est terminée.
            
            for k in range(9): # Pour chaque type de besoin :
                if k != 1:
                    batf = self.find_closer(m.coos, k)
                    
                    chemin = [m.id]
                    
                    if batf != None:
                        chemin += self._get_itineraire(m.coos, batf.coos)          
                        chemin.append(batf.id)
                        
                    m.Update_Bats(k, chemin)
                    
        deltat = time.time()-t0
        print(f" --- \tMaisons générées en {deltat//60} min {deltat%60} s.")
        
        print(" --- Initialisation terminée !")
        
        print(" --- Serialisation rapide")
        self.SelfSerialize()
        
        print(" --- \tterminé !")
        

        
    def GetTypeList(self):
        return [b.type for b in self.batlist]
                    
                    
                    
    def ActualiseGraphe(self, i):
        """Actualise le graphe de déplacement, en supposant
        que seul le ie batiment ait été changé."""
        print(" --- Actualisation de l'annuaire des maisons concernées.")
        self.maisonliste = [b for b in self.batlist if b.type == 1]

        # Il faut parcourir toutes les maisons et mettre à jour 
        # celles qui pointent sur le ie batiment.
        for m in self.maisonliste:
            try:
                k = m.IsRelated(i)
            except TypeError:
                # Un bug inconnu se propage à mesure que le deuxième étage de simulations 
                # progresse. Des maisons ont tout leur annuaire à None. Ce bug ne survient qu'après 
                # la convergence, même sur des grandes maps.
                raise Bug("Y'a du None")

            if k != [-1] :
                for tP in k:
                    t = int(tP)
                    if t == 1:
                        continue
                    
                    #Le plus proche batiment du type k :
                    batf = self.find_closer(m.coos, t)

                    chemin = [m.id]
                    if batf != None:
                        chemin += self._get_itineraire(m.coos, batf.coos)          
                        chemin.append(batf.id)
                    
                    self.batlist[m.id-1].Update_Bats(str(t), chemin)

        print(" --- \tFini")                                   
        
        
        
    def _dumpsBatList(self):
        """Renvoie une liste contenant les attributs __dict__ des batiments.
        Python est incapable de séraliser toute la liste, les objets maisons ne sont pas sérialisables."""
        D = []
        
        for b in self.batlist:
            D.append(b.__dict__)
            
        return D
    
    
    def _loadsBatList(self, data):
        """Charge une liste de dictionnaires, et crée une liste de batiments."""
        self.batlist = []
        
        for b in data:
            props_dico = {
                "id" : b["id"],
                "props_" : b["autre_props"],
                "area" : b["area"],
                "capacite": b["capacite"]
            }
            
            
            if b["type"] == 1:
                bat = batiment_r.Maison(b["coos"], props_dico)
                self.maisonliste.append(bat)
                bat.memoire_batiments = b["memoire_batiments"]

            elif b["type"] == 9:
                bat = batiment_r.Road((b["coos"][1], b["coos"][0]), b["id"], b["node"])
                self.route_dico[b["node"]] =b["id"]

            else:
                bat = batiment_r.Batiment(b["type"], b["coos"], props_dico)
                
            self.batlist.append(bat)
    
    
    
    def LoadFromMemory(self):
        """Initialise l'instance à partir d'une sauvegarde sur le disque.\n
        La mémoire du programme est dans le dossier memoire."""
        print(f" --- Initialisation de {self.center} commencée")

        try:
            path = os.path.join(os.getcwd(), "memoire",  f"{self.center}")

            with open(f"{path}\\map.json", "r") as file:
                print(f" --- \tTrouvé dans la mémoire !")
                data = file.read()
                batlist_raw = json.loads(data)
                self._loadsBatList(batlist_raw)
            
            self.pfGraph = load_graphml(f"{path}\\graph.xml")
            
            

        except FileNotFoundError:
            # On va voir dans \memoire, puis dans \VilleReelle\memoire. Cette
            # tolérance permet de lancer le programme depuis VilleReelle ou depuis la racine.
            path = os.path.join(os.getcwd(), "VilleReelle", "memoire",  f"{self.center}")

            with open(f"{path}\\map.json", "r") as file:
                print(f" --- \tTrouvé dans la mémoire !")
                data = file.read()
                batlist_raw = json.loads(data)
                self._loadsBatList(batlist_raw)
                
            self.pfGraph = load_graphml(f"{path}\\graph.xml")
            
            
        
        print(" --- Checkup dénombrement :")
        for k in range(9):
            print(f" --- \t{k} : {len([b for b in self.batlist if b.type == k])}")    
            
        print(" --- Fin du chargement de la map")
        return
    
        

    def SelfSerialize(self):
        """Ecrit l'instance actuelle dans [self.center]\map.json et [self.center]\graph.json\n
        Appel automatique depuis Initialise, éviter de toucher depuis l'extérieur."""
        path = os.path.join(os.getcwd(), "memoire",  f"{self.center}")
        
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        
        with open(os.path.join(f"{path}\\map.json"), 'w') as file:
            file.write(json.dumps(self._dumpsBatList(), sort_keys=True, indent=4 ))
            
        save_graphml(self.pfGraph, f"{path}\\graph.xml")
        
        
    def GetBat(self, i):
        """Renvoie le batiment d'id i. Les id commencent à 1."""
        return self.batlist[i-1]

 
    def _calculateCoos(self, liste_sommets):
        """calcule la moyenne de tous les points passés en paramètres.
        Très concrètement, cette méthode calcule la valeur coos d'un batiment.\n
        Structure : float list list -> float tupple"""
        x = np.mean([pt[0] for pt in liste_sommets])
        y = np.mean([pt[1] for pt in liste_sommets])
        return  (round(x, 14), round(y, 14))



    def _deg2rad(self, angle):
        return angle* np.pi * _EARTH_RADIUS / 180



    def _calculateArea(self, liste_sommets):
        """Calcule l'aire du polygone associé.\n
        Signature : float list list -> float"""
        # Il faut d'abord convertir toutes ces coordonées en sommets de R². 
        # On prend l'angle en radians entre le point et le centre.
        liste_points =  [] 
        for s in liste_sommets:
            diff = (s[0] - self.center[1], s[1] - self.center[0])
            liste_points.append(( self._deg2rad(diff[0]), self._deg2rad(diff[1]) ))
        
        # 1/2 Somme de i = 0 à (n-1) des |x_i y_i+1 - x_i+1 y_i|
        somme = 0
        for i in range(len(liste_points)-1):
            somme += liste_points[i][0]*liste_points[i+1][1] - liste_points[i+1][0]*liste_points[i][1] 
        return abs(somme) /2
    
    
    
    def find_closer(self, coos0, type2find):
        """# Cherche le batiment le plus proche du coos0 correspondant au type en question"""
        # C'est une simple recherche de minimum.
        min_ =  -1
        bmin_ = None
        
        i = 0
        for bat in self.batlist:
            if bat.type != type2find:
                i += 1
                continue
            else:
                nnorm = np.linalg.norm( np.array(bat.coos) - np.array(coos0), 2)
                if nnorm < min_ or min_ == -1:
                    min_ = nnorm
                    bmin_ = bat
                    
        return bmin_    


    def _create_bat_list(self):
        """Utilise self._getdata_batiments pour renvoyer une liste de 
        Bâtiments formatés et avec les bonnes données."""
        # Il faut tout d'abord récupérer toutes les informations sur les bâtiments.
        # Ne pas hésiter à aller voir le dossier étude pour voir la tête des données envoyées par OPENSTREETMAP
        batlist_json = self._getdata_batiments()
        print(f" --- \t{ len( batlist_json ) } batiments trouvés.")

        #C'est parti. On extrait chaque bâtiment et ce qui nous intéresse dans une liste de dicos
        i = 0

        #premier traitement général
        for bat in batlist_json:
            # =================== Traitement des donnes du batiment ===================
            i += 1
            coos = self._calculateCoos(bat["geometry"]["coordinates"][0])
            area = self._calculateArea(bat["geometry"]["coordinates"][0])

            try:
                type_str = bat["properties"]["type"]
            except KeyError:
                type_int = 1
                #cas des None à gérer

            types_inconnus_liste = []
            try:
                type_int = _TYPE_TO_TYPE[type_str]
            except KeyError:
                type_int = 1
                types_inconnus_liste.append(type_str)
            except UnboundLocalError:
                pass

            
            capacite = (( bat["properties"]["height"]//_LVL_HEIGHT )+1) * _POP_DENSITY * area

            dist_origine = (
                _deg2rad(coos[1]-self.center[0]), 
                _deg2rad(coos[0]-self.center[1]) 
            )

            props_dico = {
                    "id" : i,
                    "dist_origine" : dist_origine,
                    "props_" : bat["properties"],
                    "area" : area,
                    "capacite" : capacite
            }
            
            
            if type_int == 1:
                newbat = batiment_r.Maison(coos, props_dico)
                self.maisonliste.append(newbat)
            else:
                newbat = batiment_r.Batiment(type_int, coos, props_dico)
                
            self.batlist.append(newbat)



    def _get_itineraire(self, start, finish):
        """
        Prend en argument deux positions, et renvoie la liste des routes pour faire le trajet.\n
        
        les deux arguments sous forme de couple de coordonées longitude puis lattitude.\n
        exemple (6.6609505, 47.5211928), (6.665798, 47.523648)"""
        node0 = dist.nearest_nodes(self.pfGraph, start[0], start[1])
        node1 = dist.nearest_nodes(self.pfGraph, finish[0], finish[1])
        
        itineraire = dist.shortest_path(self.pfGraph, node0, node1)
        chemin = []
        
        if itineraire == None:
            return []

        for r in itineraire:
            try:
                chemin.append(self.batlist[ self.route_dico[r]].id)
            except KeyError: # Si la route n'est pas dans self.route_dico
                #il faut créer la route.
                coos = (self.pfGraph.nodes[r]['y'], self.pfGraph.nodes[r]['x'])
                id_ = self.i_route
                self.i_route += 1
                newr = batiment_r.Road(coos, id_, node=r)
                self.route_dico[r] = id_
                self.batlist.append(newr)
                
                chemin.append(newr.id)
                
        
        return chemin
        
        

    def print_json(self, json_file, nom):
        """Ecrit le JSON en para dans le fichier \"nom\"."""
        with open(f"mapbuilder/{nom}", 'w') as print_file :
            print_file.write(json.dumps(json_file, indent=4, sort_keys=True))
            print_file.close()


    def _deg2num(self, lat_deg, lon_deg, zoom):
        """convertit la position géographique en coordoné de tile"""
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (xtile, ytile)


    def _getdata_batiments(self):
        """Récupère l'intégralité des données sur les batiments contenus dans la zone."""
        # Ca va être un peu le bazar.
        # On va déjà récupérer les coos des size² maps que l'on doit aller chercher.
        center_map_id = self._deg2num(self.center[0], self.center[1], 15)

        if self.size == 1:
            map_ids = [(center_map_id[0], center_map_id[1])]
        else:
            map_ids = []
            for i in range(-self.size+1, self.size):
                for j in range(-self.size+1, self.size):
                    map_ids.append( (center_map_id[0]+i, center_map_id[1]+j) )

        #maintenant les requêtes.
        HEADER = {
            "Host": "data.osmbuildings.org",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Alt-Used": "data.osmbuildings.org",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "If-Modified-Since": "Tue, 23 Aug 2022 16:17:02 GMT",
            "TE": "trailers"
        } #je me fais passer pour Firefox parce que sinon je me prends des 403 :( 


        json_list = []
        for id in map_ids:
            print(" -- \t tile id", id)
            response = rq.get(f"https://data.osmbuildings.org/0.2/anonymous/tile/15/{id[0]}/{id[1]}.json", headers=HEADER)

            if not response.status_code in [200, 201, 202, 203]:
                print("Aie aie aie, internet n'est pas d'accord :(")
                print(response.status_code)
                return

            json_list.append(response.json())
        
        #On va faire l'union de toutes ces données
        for i in range(len(map_ids)):
            json_list[0]["features"] += json_list[i]["features"]

        json_f  = json_list[0]["features"]
        return json_f
    
    
    def GetBatList(self):
        return self.batlist
    
    
    def SetBat(self, i, bat):
        self.batlist[i-1] = bat
        

import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Erreur : il manque des arguments\nSynthaxe : mapbuilder.py latitude longitude [size]")
    else:    
        try: 
            size = int(sys.argv[3])
        except IndexError:
            size = 1
        MB = MapBuilder( (float(sys.argv[1]), float(sys.argv[2])))
        MB.Initialise(size=size)