import random
import base.batiment as bat
import tilemap
import game

map = game.tilemap.get_map()

def ajouter ( map , type ) :
    colonne = random.randint(0 , 59)
    ligne = random.randint(0 , 59)
    if map[colonne][ligne] != 9 :
        if map[colonne][ligne] != type :
            map[colonne][ligne] = type
            return map
    return ajouter(map , type)

def retirer ( map , type) :
    colonne = random.randint(0 , 59)
    ligne = random.randint(0 , 59)
    if map[colonne][ligne] != 9 :
        new_type = random.randint(0 , 8)
        if new_type != type :
            if map[colonne][ligne] != type :
                map[colonne][ligne] = new_type
                return map
    return retirer(map , type)

def max_recompense ( l_recompense , etat_precedent) :
    recompense_max = 0
    j = 0
    for i in len(l_recompense) :
        if etat_precedent-5<=l_recompense[i][1] and l_recompense[i][1]<= etat_precedent+5 :
            if recompense_max < l_recompense[i][0] :
                recompense_max = l_recompense[i][0]
                j = i
    return l_recompense[j][2]

l_action = [ajouter , retirer ]

etat0 = 50 ; etat1 = 50 ; etat2 = 50 ; etat3 = 50 ; etat4 = 50
etat5 = 50 ; etat6 = 50 ; etat7 = 50 ; etat8 = 50

etats = [ etat0 , etat1 , etat2 , etat3 , etat4 ,etat5 , etat6 , etat7 , etat8 ]

etat_moyen = (etat0 + etat1 + etat2 + etat3 + etat4 + etat5 + etat6 + etat7 + etat8) / 9
etat_precedent = (etat0 + etat1 + etat2 + etat3 + etat4 + etat5 + etat6 + etat7 + etat8) / 9

l_recompense = []
l_etat_vu = []

type = bat.TypeBatiment(random.randint(0 , 8))

while etat_moyen <= 90 :
    if random(0 , 10) < 3 :
        action = random.choice(l_action)
        action() #sur la ville en affectant que le type 
        # lancer la simu un peu 
        recompense = etat_moyen - etat_precedent
        l_recompense.append([recompense , etat_precedent , action])
        l_etat_vu.append(etat_precedent)
    else :
        if etat_moyen in l_etat_vu :
            action = max_recompense(l_recompense , etat_precedent)
            action()
    #faire tourner simulation
    #changement des valeurs dans la liste etats
    type = min(etats)
    etat_moyen