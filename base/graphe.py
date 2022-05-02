from cmath import inf
import queue


class Graph :
    def __init__(self, S):
        #graphes via listes d'adjacences avec pondération
        #sous forme de ('a * float) list ????
        self.sommets = S

        self.tab = { s:[] for s in S}
        
        return


    def addSommet(self, x, A):
        self.tab[x] = A

    
    def addArc(self, x, list_y):
        """x -> y"""
        if type(list_y) != type([]):
            list_y = [list_y]

        for y in list_y:
            self.tab[x].append(y)

        return


    def findPath(self, x, y, s0):
        """via Djikstra"""
        F = queue()
        Dists = {s : +inf for s in self.sommets}
        Vus = {s:False for s in self.sommets}
        Parents = {s:None for s in self.sommets}

        Dists[s0]

    
