from numpy import array, where, log2, where, log, exp
from random import choice
from collections import deque

import batiment_r

BESOINS_COEFFS = {0:4, 1:4, 2:4, 3:3, 4:3, 5:3, 6:2, 7:2, 8:1}

# L'uniformisation du kbien est une gaussienne dont la décroissance est gérée
# par ce paramètre. Il faut l'adapter à la taille de la map pour que les kbiens
# soient lisibles.
coeff_uniform = log(.94)


class Citoyen :
    """## Citoyen :
    \nLes instances de Citoyen simulent les déplacement des citoyens de la ville.
    Voir le paragraphe stratégie pour plus d'infos.
    """

    def __init__(self, maison):
        # voir la méthode selectionner_besoin pour plus d'infos
        self.besoins = array([.99 for _ in range(0, 9)])

        # maison est une instance de batiment_r.Maison
        self.maison = maison

        # la position actuelle du citoyen, toujours sur un batiment de la carte.
        self.pos = maison.id

        # 0 : chez lui; 1 : en marche; 2 : là bas; 3 : en retour
        self.tour_state = 0



    def tour(self, batlist, should_print = False):
        """Gère une action du citoyen, est appelée à chaque tour de jeu sur chaque
        citoyen. Renvoie un tuple (kbien, batiment) si le citoyen a terminé son voyage
        vers un batiment, None sinon."""
        # ========= EXPLICATIONS ==============
        # La chronologie du programme est eclatée par la while de Ville.start()
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


        if self.tour_state == 0:
            # J'ai faim !
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


            return
            
            
        elif self.tour_state == 1:
            #On se déplace case par case jusqu'à Esplanade
            self.temps_parcours += 1
            next_step = self.route[0]

            #il faut tester si la route est pleine ou non
            try:
                next_route = batlist[next_step]
            except TypeError:
                return
            
            if next_route.AjouterCitoyen():
                self.route.popleft()
                self.pos = next_step
                self.chemin_retour.append(next_step)
                batlist[ self.pos ].EnleverCitoyen()

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
                print("Bouchon en", next_step)
                return #on ne peut rien faire, la route de devant est saturée

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
            next_step = self.chemin_retour[-1]

            #il faut tester si la route est pleine ou non
            next_route = batlist[next_step]
            if next_route.AjouterCitoyen():
                self.chemin_retour.pop()
                self.pos = next_step
                batlist[ self.pos ].EnleverCitoyen()

                if should_print:
                    print(self.pos)
                if len(self.chemin_retour) == 0:
                    #on est rentrés
                    self.tour_state = 0
                    kbien = exp(- ( coeff_uniform *self.temps_parcours)**2 )

                    if should_print:
                        print("== Etape quatre : Finie ! ==")
                        print(f"\t position actuelle : {self.pos}")
                        print(f"\t temps de parcours total : {self.temps_parcours}")


                    return kbien, self.batiment_cible

                else:
                    return

            
            else:
                print("Bouchon en", next_step)
                return #on ne peut rien faire, la route de devant est saturée
    

    def getbesoins(self):
        return self.besoins


    def getposition(self):
        return self.pos
    

    def getmaison(self):
        return self.maison


    def selectionnerBesoin(self):
        """Renvoie l'indice du besoin le plus urgent, décroit les autres."""
        #on prend les 3 derniers
        besoins_min_list = sorted([self.besoins[t] for t in range(len(self.besoins)) 
                                   if t != 1])
        besoinTt = choice(besoins_min_list[:3])
        besoin_i = where(self.besoins == besoinTt)[0][0]

        #on update tous les autres
        for i_b in range(len(self.besoins)):
            if i_b != besoin_i:
                self.besoins[i_b] *= 1/(BESOINS_COEFFS[i_b]+1)
            else:
                self.besoins[i_b] = 1

        return besoin_i
