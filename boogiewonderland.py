import main
import copy
import random
import os
import json

def LetsDanceTonight():
    """Shuffle les batiments. Boogie Wonderland !"""
    C = main.C
    
    typeset = [0, 2, 3, 4, 5, 6, 7, 8]
    newbatlist = []
    
    for b in C.mb.batlist:
        newb =  copy.deepcopy(b)
        if newb.type != 1 and newb.type != 9:
            newb.type = random.choice(typeset)
        newbatlist.append(newb.__dict__)
        
    path = os.path.join(os.getcwd(), "data",  "mapshuffled")
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    if os.name == "nt":
        with open(os.path.join(f"{path}\\map.json"), 'w') as file:
            file.write(json.dumps(newbatlist, sort_keys=True, indent=4 ))

    else:
        with open(os.path.join(f"{path}/map.json"), 'w') as file:
            file.write(json.dumps(self._dumpsBatList(), sort_keys=True, indent=4 ))
        

from PIL import Image
from numpy import asarray, vectorize

    
def VoulezVous():
    """Sort la map d'une image"""
    ctotype = {
        (88, 209, 43, 255): 1,
        (91, 206, 47, 255):1,
        (205, 92, 17, 255) : 0,
        (235, 64, 7, 255): 0,
        (226, 112, 121, 255): 2,
        (61, 7, 235, 255): 3,
        (7, 235, 235, 255): 4,
        (168, 7, 235, 255): 5,
        (0, 0, 0, 255): 6,
        (8, 19, 1, 255) : 6,
        (255, 255, 255, 255): 7,
        (179, 94, 173, 255) : 8
    }
    
    img = Image.open("VilleType-Centrique.png")
    data = asarray(img)
    
    map = []
    for l in data:
        ll = []
        for e in l:
            ll.append(ctotype[tuple(e)])
        map.append(ll)
        
    print(map)
    
    
    
    
    
    
if __name__ == "__main__":
    VoulezVous()
        
       