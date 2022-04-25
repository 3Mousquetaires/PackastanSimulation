from batiment import Batiment
from numpy import array, where, log2, where


from random import choice, uniform

from besoin import TypeBesoin


BESOINS_COEFFS = {0:16, 1:16, 2:16, 3:8, 4:8, 5:8, 6:4, 7:4, 8:2}


class Citoyen :
    def __init__(self):
        self.age = 0
        self.besoins = array([.99 for _ in range(0, 9)]) #array([uniform(.5, 1) for _ in range(0, 9)])


    def tour(self):
        besoin = self.selectionnerBesoin()

        #selection du batiment
        #navigation vers le batiment

        #interface batiment

        return
    

    def getbesoins(self):
        return self.besoins


    def selectionnerBesoin(self):
        #on prend les 3 derniers
        besoins_min_list = sorted(self.besoins)
        besoinTt = choice(besoins_min_list[:3])
        besoin_i = where(self.besoins == besoinTt)[0][0]

        print(besoin_i, "selectionné !")
        #on update tous les autres
        for i_b in range(len(self.besoins)):
            if i_b != besoin_i:
                self.besoins[i_b] *= 1/(log2(BESOINS_COEFFS[i_b])+1) #self.besoins[i_b]

        return TypeBesoin(besoin_i) #on le retourne sous forme d'un Besoin (version enum)

        

                



