import random

def ajouter ( map , type_bat ) :
    colonne = random.randint(0 , 59)
    ligne = random.randint(0 , 59)
    if map[colonne , ligne] != 9 :
        if map[colonne , ligne] != type_bat :
            map[colonne , ligne] = type_bat
            return map
    return ajouter(map , type_bat)



def retirer ( map , type_bat) :
    colonne = random.randint(0 , 59)
    ligne = random.randint(0 , 59)
    if map[colonne , ligne] != 9 :
        new_type = random.randint(0 , 8)
        if new_type != type_bat :
            if map[colonne , ligne] != type_bat :
                map[colonne , ligne] = new_type
                return map
    return retirer(map , type_bat)




def max_recompense ( l_recompense , etat_precedent) :
    recompense_max = 0
    j = 0
    for i in range(len(l_recompense)) :
        if etat_precedent-5<=l_recompense[i][1] and l_recompense[i][1]<= etat_precedent+5 :
            if recompense_max < l_recompense[i][0] :
                recompense_max = l_recompense[i][0]
                j = i
    return l_recompense[j][2]




def renforcement(type_bat , etats , etat_moyen , etat_precedent , l_recompense , l_etat_vu , l_action , map) :
    while etat_moyen <= 90 :
        if random.randint(0 , 10) < 3 :
            action = random.choice(l_action)
            etat_precedent = etat_moyen
            action(map , type_bat)
            # lancer la simu un peu 
            recompense = etat_moyen - etat_precedent
            l_recompense.append([recompense , etat_precedent , action])
            l_etat_vu.append(etat_precedent)
        else :
            if etat_moyen in l_etat_vu :
                action = max_recompense(l_recompense , etat_precedent)
                action(map , type_bat)
        #changement des valeurs dans la liste etats

        type_bat = etats.index(min(etats))
        etat_moyen += 0.1
    return True