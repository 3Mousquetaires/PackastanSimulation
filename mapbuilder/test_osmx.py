import networkx as nx
import osmnx as ox

import numpy as np
import time
import json


def print_json(json_file, nom):
    """Ecrit le JSON en para dans le fichier \"nom\"."""
    with open(f"mapbuilder/{nom}", 'w') as print_file :
        print_file.write(json.dumps(json_file, indent=4, sort_keys=True))
        print_file.close()

t0 = time.time()
G = ox.graph_from_place("Arcey, Doubs, France", network_type = "all_private")

Gp = ox.utils_graph.get_undirected(G)
print(time.time() - t0)

routes = Gp.nodes._nodes

for r in routes:
    if routes[r]['y'] == 47.521304 and routes[r]['x'] == 6.660986:
        print(r)
print(routes)

#fig, ax = ox.plot_graph(G)


