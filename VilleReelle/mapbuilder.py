from fileinput import close
import requests as rq
import json
import math
import numpy as np

import time

#import igraph as grf
import networkx as nx
import os
# Vocabulaire anglais : Edges sont les arètes, Nodes sont les sommets

import batiment_r

import osmnx.graph as grph
import osmnx.distance as dist

from osmnx import save_graphml, load_graphml





def _deg2rad(angle):
    return angle* np.pi * _EARTH_RADIUS / 180


#CONSTANTES (tout est converti en m/m²)
_LVL_HEIGHT = 2.875
_POP_DENSITY = 0.08333
_EARTH_RADIUS = 6_371.009 * 10**3
_SHAB_AREA_RATIO = .91

_TYPE_TO_TYPE = {
    'retail' : 0,
    'commercial' : 0,
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
    'civic' : 8
}



class MapBuilder:
    """Outil intégré de construction de graphe urbain basé sur la zone proche autour d'un point central."""
    
    def __init__(self, center):
        """Exemple : centre de Strasbourg : (48.58310, 7.74863) (fonctionne sur les coordonées géographiques).\n"""
        self.center = center
        
        self.batlist = []
        self.maisonliste = []
        self.pfGraph = nx.MultiDiGraph()
        
        self.route_dico = {}
        
       
        
    
    def Initialise(self, size):
        """Faut s'y frotter...\n
            Préférer la déserialisation depuis le cache avec MapBuilder.LoadFromMemory\n
            Temps d'exécution : 10 15 minutes."""
            
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
        
        
        print(" --- \tCréation du graphe de déplacement.")
        self.pfGraph = grph.graph_from_bbox(self.N, self.S, self.E, self.W, network_type="all")
        
        
        t0 = time.time()
        print(f" --- \tInitialisation des maisons : {len(self.maisonliste)} trouvées.")
        
        #print(json.dumps(self.maisonliste[0].__dict__))
        # deuxième traitement : init des maisons
        self.route_dico = {}
        
        i = -1
        self.i_route = len(self.batlist)
        for m in self.maisonliste:
            print(i)
            i += 1
            for k in range(9):
                if k != 1:
                    batf = self.find_closer(m.coos, k)
                    
                    chemin = [m.id]
                    chemin += self._get_itineraire(m.coos, batf.coos)          
                    chemin.append(batf.id)
                    m.Update_Bats(k, chemin)
                    
        deltat = time.time()-t0
        print(f" --- \tMaisons générées en {deltat//60} min {deltat%60} s.")
        
        print(" --- Initialisation terminée !")
        
        print(" --- Serialisation rapide")
        self.SelfSerialize()
        
        print(" --- \tterminé !")
                    
                    
                    
    def ActualiseGraphe(self, i):
        """Actualise le graphe de déplacement, en supposant
        que seul le ie batiment ait été changé."""
        print(" --- Actualisation de l'annuaire des maisons concernées.")
        for m in self.maisonliste:
            k = m.IsRelated(i)
            if k != [-1] :
                print(m)
                for t in k:
                    if t == 1:
                        continue
                    batf = self.find_closer(m.coos, t)
                    print("hello ?")
                    chemin = [m.id]
                    chemin += self._get_itineraire(m.coos, batf.coos)          
                    chemin.append(batf.id)
                    m.Update_Bats(t, chemin) 
        print(" --- \tFini")                                   
        
        
        
    def _dumpsBatList(self):
        """Les objets maisons ne sont pas sérialisables, """
        D = []
        
        for b in self.batlist:
            D.append(b.__dict__)
            
        return D
    
    
    def _loadsBatList(self, data):
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
            path = os.path.join(os.getcwd(), "VilleReelle", "memoire",  f"{self.center}")

            with open(f"{path}\\map.json", "r") as file:
                print(f" --- \tTrouvé dans la mémoire !")
                data = file.read()
                batlist_raw = json.loads(data)
                self._loadsBatList(batlist_raw)
                
            self.pfGraph(f"{path}\\graph.xml")
            
            
        print(" --- Fin du chargement de la map")
        return
    
        

    def SelfSerialize(self):
        """Ecrit l'instance actuelle dans [self.center]\map.json et [self.center]\graph.json\n
        Appel automatique depuis Initialise, éviter de toucher."""
        path = os.path.join(os.getcwd(), "memoire",  f"{self.center}")
        
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        
        with open(os.path.join(f"{path}\\map.json"), 'w') as file:
            file.write(json.dumps(self._dumpsBatList(), sort_keys=True, indent=4 ))
            
        save_graphml(self.pfGraph, f"{path}\\graph.xml")
        
        
    def GetBat(self, i):
        """get"""
        return self.batlist[i-1]

 
    def _calculateCoos(self, liste_sommets):
        """calcul la moyenne de tous les points passés en paramètres.
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
        
        #1/2 Somme de i = 0 à (n-1) des |x_i y_i+1 - x_i+1 y_i|
        somme = 0
        for i in range(len(liste_points)-1):
            somme += liste_points[i][0]*liste_points[i+1][1] - liste_points[i+1][0]*liste_points[i][1] 
        return abs(somme) /2
    
    
    
    def find_closer(self, coos0, type2find):
        """# Cherche le batiment le plus proche du coos0 correspondant au type en question"""
        min_ =  -1
        bmin_ = None
        
        for bat in self.batlist:
            if bat.type != type2find or bat.coos == coos0:
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
        #Il faut tout d'abord récupérer toutes les informations sur les bâtiments.
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
            except KeyError:
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
        #Ca va être un peu le cirque.
        #On déjà récupérer les coos des 4 maps que l'on doit aller chercher.
        center_map_id = self._deg2num(self.center[0], self.center[1], 15)

        if self.size == 1:
            map_ids = [(center_map_id[0], center_map_id[1])]
        else:
            #On s'intéresse aux 4 maps autour du centre.
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

            if response.status_code != 200:
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
        


#print(_get_itineraire( (2.316068734550804,48.87037435), (-1.2770243425435213,46.1581427) ))
#2.316068734550804,48.87037435;-1.2770243425435213,46.1581427

#print(__getdata_batiments((48.58310, 7.74863))

#MB = MapBuilder((48.58310, 7.74863))


import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Erreur : il manque des arguments\nSynthaxe : mapbuilder.py latitude longitude")
    else:    
        try: 
            size = int(sys.argv[3])
        except IndexError:
            size = 1
        MB = MapBuilder( (float(sys.argv[1]), float(sys.argv[2])))
        MB.Initialise(size=size)
