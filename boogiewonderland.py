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
        
    
    
    
if __name__ == "__main__":
    LetsDanceTonight()
        
       