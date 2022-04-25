class Graph :
    def __init__(self, S):
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

    
