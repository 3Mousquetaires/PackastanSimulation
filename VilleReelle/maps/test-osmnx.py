import osmnx.graph as grph
import osmnx.distance as dist

import json

import time


N = 48.58947147619048
S = 48.57449032075472
E = 7.76752771428572
W = 7.74480095555556

print(" pif paf pouf")
t0 = time.time()
G = grph.graph_from_bbox(N, S, E, W, network_type="all")
print(f"\t -- temps pour générer le graphe {time.time() - t0}")



node_cat = dist.nearest_nodes(G, 7.7511494661017, 48.58193883050848)
node_tns = dist.nearest_nodes(G, 7.75523548780488, 48.58642051219512)

t0 = time.time()
print(dist.shortest_path(G, node_cat, node_tns))
print(f"\t -- temps pour générer l'itinéraire {time.time() - t0}")

print(node_cat, node_tns)

#(7.7511494661017, 48.58193883050848)

#dic = json.dumps(G)
#print(dic)