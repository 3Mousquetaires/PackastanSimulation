from numpy import array, where, log2, where 

#from pygame.locals import *
import numpy as np

from random import choice

from collections import deque

import batiment

BESOINS_COEFFS = {0:16, 1:16, 2:16, 3:8, 4:8, 5:8, 6:4, 7:4, 8:2}

coeff_uniform = np.log(1.2)


class Citoyen :
    def __init__(self, maison:batiment.TypeBatiment):
        self.age = 0
        self.besoins = array([.99 for _ in range(0, 9)]) #array([uniform(.5, 1) for _ in range(0, 9)])
        self.maison = maison
        self.pos = maison.adresse
        #0 : chez lui; 1 : en marche; 2 : là bas; 3 : en retour
        self.tour_state = 0



    def tour(self, batmatrice, should_print = False):
        """Il faut transmettre l'instance de batiment de position 
        Citoyen.pos à la méthode."""
        #========= EXPLICATIONS ==============
        # méthode de fou furieux
        # La chronologie du programme est eclatée par la while de game.run
        # Je peux pas faire jouer un citoyen puis celui d'après : il
        # faut que tout le monde fasse tout en même temps.

        # On joue sur le membre tour_state, voir 10 lignes au dessus

        #  -> Si tour_state = 0:
        #     le citoyen choisit un besoin, il trouve
        #     une route vers un batiment qui correspond, 
        #     on initialise la route de retour et le temps de parcours.

        #  -> si tour_state = 1:
        #     On vient de passer un autre tick. On va chercher
        #     dans la liste route la prochaine adresse où se dépalcer
        #     Si il y a de la place, on y va : on update la liste route, 
        #     on update la route de retour, on update la pos actuelle
        #     Sinon : on fait rien.

        #  -> si tour_state = 2 : on est arrivé
        #     Pas grand chose à faire actuellement, on renseigne le 
        #     batiment qu'on était parti chercher à la base

        #  -> si tour_state = 3:
        #     Chemin du retour : on utilise la liste chemin_route, qu'on
        #     parcours à l'envers. Quand on arrive, on renvoie cette fois
        #     un kbien et l'adresse du bat qu'on était allé chercher.



        #J'ai faim !
        if self.tour_state == 0:
            besoin = self.selectionnerBesoin()

            #on cherche l'adresse du o'Tacos dans le GPS
            route = self.maison.GetBatiment(besoin)
            self.route = deque( route )
            self.tour_state += 1

            self.temps_parcours = 0

            self.chemin_retour = []

            if should_print :
                print(" == Étape une : == ")
                print(f"\t besoin : {besoin}")
                print(f"\t route : {self.route}")
                print("======================\n")


            return # TESTS : jusqu'ici tout s'passe bien
            
            
        elif self.tour_state == 1:
            #On vroum vroum jusqu'à Esplanade
            self.temps_parcours += 1
            next_pos = self.route[0]

            #il faut tester si la route est pleine ou non
            next_route = batmatrice[next_pos[0]][next_pos[1]] 
            if next_route.AjouterCitoyen():
                self.route.popleft()
                self.pos = next_pos
                self.chemin_retour.append(next_pos)
                batmatrice[ self.pos[0] ][self.pos[1]].EnleverCitoyen()

                if len(self.route) == 0:
                    #on est arrivé
                    self.tour_state += 1

                    if should_print:
                        print("\n== Etape deux : ==")
                        print(f"\t position actuelle : {self.pos}")
                        print(f"\t temps de parcours : {self.temps_parcours}")
                        print(f"\t chemin de retour : {self.chemin_retour}")
                        print("================")

                if should_print:
                    print(self.pos)
                return
    
            
            else:
                print("Bouchon en", next_pos)
                return #on ne peut rien faire, la route de devant
                #est bloquée

        elif self.tour_state == 2:
            self.batiment_cible = self.pos
            self.tour_state += 1
            #On est arrivé !  
            if should_print:
                print("== Etape trois : Arrivé ! ==\n")
            return


        elif self.tour_state == 3:
            #gestion de la route de retour
            self.temps_parcours += 1
            next_pos = self.chemin_retour[-1]

            #il faut tester si la route est pleine ou non
            next_route = batmatrice[next_pos[0]][next_pos[1]] 
            if next_route.AjouterCitoyen():
                self.chemin_retour.pop()
                self.pos = next_pos
                batmatrice[ self.pos[0] ][ self.pos[1]] .EnleverCitoyen()

                if should_print:
                    print(self.pos)
                if len(self.chemin_retour) == 0:
                    #on est rentrés
                    self.tour_state = 0
                    kbien = np.exp(- ( coeff_uniform *self.temps_parcours)**2 )

                    if should_print:
                        print("== Etape quatre : Finie ! ==")
                        print(f"\t position actuelle : {self.pos}")
                        print(f"\t temps de parcours total : {self.temps_parcours}")


                    return kbien, self.batiment_cible

                else:
                    return

            
            else:
                print("Bouchon en", next_pos)
                return #on ne peut rien faire, la route de devant
                #est bloquée
    

    def getbesoins(self):
        return self.besoins


    def getposition(self):
        return self.pos
    

    def getmaison(self):
        return self.maison


    def selectionnerBesoin(self):
        #on prend les 3 derniers
        besoins_min_list = sorted(self.besoins)
        besoinTt = choice(besoins_min_list[:3])
        besoin_i = where(self.besoins == besoinTt)[0][0]

        #on update tous les autres
        for i_b in range(len(self.besoins)):
            self.besoins[1] = 1
            if i_b != besoin_i:
                self.besoins[i_b] *= 1/(log2(BESOINS_COEFFS[i_b])+1)
            else:
                self.besoins[i_b] = 1

        return besoin_i
            

        
    def _rechercherBatiments(self):
        """renvoie l'adresse du premier batiment trouvé répondant
        à *besoin*."""
        pass
