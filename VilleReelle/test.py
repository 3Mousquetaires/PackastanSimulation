import math

import networkx as nx

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

print(deg2num(48.58310, 7.74863, 14))

# ESSAYER DE SERIALISER UN TRUC AVEC JSON.


#   Types des batiments sur stras :
{
  'residential': 573,
  'retail': 9,
   'hotel': 9,
   'None': 2417,
   'hospital': 10,
   'religious': 18,
   'religion': 166,
   'commercial': 261,
   'roof': 3,
   'kindergarten': 2,
   'school': 24,
   'kiosk': 2,
   'office': 9,
   'public': 19,
   'dormitory': 9,
   'administration': 5,
   'chapel': 2,
   'civic': 5,
   'cathedral': 2,
   'service': 5,
   'boat': 1,
   'construction': 4,
   'parking': 2,
   'university': 22,
   'convent': 1,
   'greenhouse': 3,
   'houseboat': 3,
   'steps': 3,
   'industrial': 6,
   'college': 1
  }







#aire moyenne : 471 m², taille moyenne : 14.7 m

#coordonée du centre de strasbourg :
#   (48.58310, 7.74863)

#Paris 17e:
#   (48.882970, 2.299415)

#Montbéliard :
#   (47.505684, 6.803161)

#Arcey :
#  47.522363, 6.660636

#Londres en plein sur Westminster
#   51.500948, -0.124542

#Central Park
#   40.771300, -73.973902
# Je m'amuse comme un fou

def f(x):
  print(.0681*x)
  return 0.0681*x

somme = sum([ f(k) for k in range(0, 3600) ])
print(somme)


