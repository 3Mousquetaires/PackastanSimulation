import main
import copy
import random

def LetsDanceTonight(self):
    """Shuffle les batiments. Boogie Wonderland !"""
    C = main.C
    countlist = [0 for k in range(9)]
    
    typeset = [0, 2, 3, 4, 5, 6, 7, 8]
    newbatlist = []
    
    for b in C.mb.batlist:
        newb =  copy.deepcopy(b)
        if newb.type != 1 and newb.type != 9 :
            newb.type = random.choice(typeset)
        newbatlist.append(newb)
    
    
    
        
       