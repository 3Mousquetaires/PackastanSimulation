from enum import Enum

class TypeBesoin (Enum) :
    ALIMENTATION = 0
    HABITATION = 1
    SANTE = 2
    SECURITE = 3
    EMPLOI = 4
    MORALITE = 5
    FETE = 6
    PHYSIQUE = 7
    GESTION = 8
    DEPLACEMENT = 9

StrToTypeBesoin = {"alimentation":TypeBesoin.ALIMENTATION, "habitation":TypeBesoin.HABITATION,
    "sante":TypeBesoin.SANTE, "securite":TypeBesoin.SECURITE, "emploi":TypeBesoin.EMPLOI,
    "moralite":TypeBesoin.MORALITE, "fete":TypeBesoin.FETE, "physique":TypeBesoin.PHYSIQUE,
    "gestion":TypeBesoin.GESTION, "deplacement":TypeBesoin.DEPLACEMENT}