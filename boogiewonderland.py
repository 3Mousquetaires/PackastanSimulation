import main
import re

def LetsDanceTonight(self):
    """Shuffle les batiments. Boogie Wonderland !"""
    C = main.C
    countlist = [0 for k in range(9)]
    
    for b in C.mb.batlist:
        if not b.type in [1, 9] :
            countlist[b.type] += 1
            
    
        
        