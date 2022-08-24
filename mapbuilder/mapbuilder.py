import requests as rq
import json
import math
import numpy as np

import igraph as grf


class MapBuilder:
    """Outil intégré de construction de graphe basé sur la zone proche autour d'un point central."""

    def __init__(self, center):
        """Exemple : centre de Stras : (48.58310, 7.74863) (fonctionne sur les coordonées géographiques).\n"""
        self.center = center


    def _calculateCoos(self, liste_sommets):
        """calcul la moyenne de tous les points passés en paramètres.
        Structure : float list list -> float tupple"""
        x = np.mean([pt[0] for pt in liste_sommets])
        y = np.mean([pt[1] for pt in liste_sommets])
        return (x, y)
        


    def CreateGraph(self):
        """Retourne une instance igraph.Graphe. \n
        \tSommets : tous les batiments, routes ou autres.
        \n\tLes arrêtes représentent l'accessibilité entre chaque bâtiment."""

        print(f"Initialisation de {self.center} démarrée. Allez prendre un café.")

        #Il faut tout d'abord récupérer toutes les informations sur les bâtiments.
        batlist_json = self._GetData_batiments()
        print(f"\t { len( batlist_json ) } batiments trouvés")

        G = grf.Graph() #c'est ce truc qu'on va retourner.

        #C'est parti. On extrait chaque bâtiment et ce qui nous intéresse dans une liste de dicos
        batlist = []
        i = 1
        for bat in batlist_json:
            print(f"{i}/{len( batlist_json )}")
            i += 1
            coos = self._calculateCoos(bat["geometry"]["coordinates"])
            batlist.append(
                {
                    "id" : bat["id"],
                    "coos" : coos,
                    "props" : bat["properties"]
                })

            #On ajoute un sommet par dessus le marché
            G.add_vertex(bat["id"])

            #maintenant il faut toutes les routes.
            for i in range(len(batlist)-1):
                route = self._GetItineraire( coos, batlist[i]["coos"] )

                for r in range(len(route)):
                    if not route[r] in G.vs()["name"]:
                        G.add_vertex(route[r])
                        
                        if r == 0:
                            G.add_edge(bat["id"], route[r])
                        else:
                            G.add_edge(route[r-1], route[r])
                
                G.add_edge(route[-1], batlist[i]["id"])
            
        return G


            

        
        






    def _GetItineraire(self, start, finish):
        """
        Prend en argument deux positions, et renvoie la liste des routes pour faire le trajet.\n
        
        les deux arguments sous forme de couple de coordonées longitude puis lattitude.\n
        exemple (6.6609505, 47.5211928), (6.665798, 47.523648)"""
        BASE_URL = "https://routing.openstreetmap.de"
        headers = {
            "Host": "routing.openstreetmap.de",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.openstreetmap.org/",
            "Origin": "https://www.openstreetmap.org",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1"
        }

        url_get = f"{BASE_URL}/routed-car/route/v1/driving/{start[0]},{start[1]};{finish[0]},{finish[1]}?overview=false&geometries=polyline&steps=true"

        route = rq.get(url_get, headers=headers)

        if route.status_code != 200:
            print(f"Erreur : code {route.status_code} renvoyé.")
            return

        json_response = route.json()

        road_list = [r["name"] for r in json_response["routes"][0]["legs"][0]["steps"] if r["name"] != ""]
        #ne pas s'en occuper, faut juste parser la requête de réponse. Appeler dam si ça plante.

        return road_list


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


    def _GetData_batiments(self):
        """Récupère l'intégralité des données sur les batiments contenus dans la zone."""
        #Ca va être un peu le cirque.
        #On déjà récupérer les coos des 4 maps que l'on doit aller chercher.
        center_map_id = self._deg2num(self.center[0], self.center[1], 15)

        #On s'intéresse aux 4 maps autour du centre.
        map_ids = []
        for i in range(2):
            for j in range(2):
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
            print(id)
            response = rq.get(f"https://data.osmbuildings.org/0.2/anonymous/tile/15/{id[0]}/{id[1]}.json", headers=HEADER)

            if response.status_code != 200:
                print("Aie aie aie, internet n'est pas d'accord :(")
                print(response.status_code)
                return

            json_list.append(response.json())
        
        #On va faire l'union de toutes ces données
        json_list[0]["features"] += json_list[1]["features"] + json_list[2]["features"] + json_list[3]["features"]

        json_f  = json_list[0]["features"]
        return json_f


#print(GetItineraire( (2.316068734550804,48.87037435), (-1.2770243425435213,46.1581427) ))
#2.316068734550804,48.87037435;-1.2770243425435213,46.1581427

#print(GetData_batiments((48.58310, 7.74863)))
MB = MapBuilder((48.58310, 7.74863))
g = MB.CreateGraph()

g.write("mapbuilder/graph_stras")



