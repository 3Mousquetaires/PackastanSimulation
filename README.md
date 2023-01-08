# PackastanSimulation : Optimisation de la disposition des bâtiments dans une ville

Ce repo contient les fichiers sources du projet TIPE 2022-2023 du groupe des 3 mousquetaires :

* Paul-Henri Andrieu [@phandrieu](https://github.com/phandrieu)
* Damien Maître [@DobbyOff](https://github.com/DobbyOff)
* Ethan Petitjean [@Slordeee](https://github.com/Slordeee)

## Introduction

PackastanSimulation est un programme mesurant puis optimisant la disposition des bâtiments dans une ville donnée en fonction des besoins répondus par ces derniers. Face aux nombreux modèles mathématiques déterminant l'évolution d'une ville, nous avons opté pour une démarche empirique visant à calculer la vertue du positionnement des bâtiments. Nous appliquons ensuite des méthodes d'apprentissage renforcé pour tendre, simulation après simulation, vers une ville idéale.

## Fonctionnement

### Les Citoyens

Les briques atomiques de notre projet sont les Citoyens : nous simulons la vie des habitants de la ville.
Leurs activités sont simples : répondre à un besoin. La pyramide développée par le sociologue Maslow donne une énumération hiérarchisée des besoins de l'être. Tour après tour, nos citoyens voient leurs besoins devenir de plus en plus pressants.

 > Techniquement, les besoins des citoyens sont des suites géométriques décroissantes. A chaque tour, l'indacteur de chaque besoin est multiplié par une constante dépendant de l'importance du besoin : 
 <img src="https://latex.codecogs.com/svg.image?K_{n&plus;1}&space;&space;=&space;\frac{1}{b_k&space;&plus;&space;1}&space;\cdot&space;K_n\\&space;\\\forall&space;n,&space;K_{n}&space;=&space;.99&space;\cdot&space;\frac{1}{(b_k&space;&plus;&space;1)^n}" title="https://latex.codecogs.com/svg.image?K_{n+1} = \frac{1}{b_k + 1} \cdot K_n\\ \\\forall n, K_{n} = .99 \cdot \frac{1}{(b_k + 1)^n}" />


### Les Batiments : premier étage de la simulation

Chaque Citoyens qui n'est pas déjà occupé sélectionne donc un de ses trois besoins les plus pressants. Ce citoyen va ensuite se rendre dans le batiment le plus proche correspondant au besoin en question.

 > Le déplacement s'effectue en tours par tours, comme au Monopoly. Ainsi, tous les citoyens bougent en même temps, et nous pouvons simuler des bouchons ou des magasins saturés. Les tours sont en fait les tours de la boucle while qui fait jouer chaque citoyens. Soyons sûrs des termes : en un tour, chaque citoyen effectue une action, comme au Mille Bornes.

Pour chacun de ces voyages, nous mesurons le nombre de tours qu'il a nécessité : combien de tours entre la sortie de la maison et le retour sur son canapé. Ce résultat est assimilable au temps qu'il a fallu au citoyen pour répondre à son besoin. C'est la disposition des routes et des batiments qui détermine ce coefficient : plus le batiment recherché est loin de la maison du Citoyen, plus la route pour y accéder est longue, plus il faut de tours pour la parcourir en aller/retour, et plus le coefficient est grand.

 > Nous passons ensuite ce résultat dans une gaussienne pour uniformiser les variations  : 
 <img src="https://latex.codecogs.com/svg.image?k_{bien}&space;=&space;e^{-(A&space;\cdot&space;t)^2}" title="https://latex.codecogs.com/svg.image?k_{bien} = e^{-(A \cdot t)^2}" />

 > La gaussienne est décroissante : plus le temps de parcours est grand, plus le coefficient bien est petit. Le temps de parcours dépend aussi de la taille de la ville. Notre simulation fut testée sur différentes échelles, et il faut choisir la constante A pour que les fluctuations du kbien, sur l'intervalle [0, 1], soient visibles à l'affichage. Le programme pourrait se passer de ce confort, puisqu'il ne s'occupe que de faire des moyennes et des recherches de minima, mais l'affichage serait bien moins impressionnant.

A partir d'une densité de population suffisante (nous pouvons choisir la population de notre ville), chaque batiment est assez visité pour que l'on puisse faire la moyenne, pour chaque batiment, du coefficient bien obtenu lorsqu'un citoyen voulait s'y rendre. Ce kbien moyen est une mesure de la facilité qu'on les Citoyens pour se rendre dans ce batiment. Ce coefficient bien mesure donc la vertue du positionnement du batiment dans la ville. S'il est plus bas que les autres, c'est que le batiment est plus loin des habitants que les autres. Le résultat du premier étage de simulations est ce coefficient bien par batiment.

Nos résultats furent encourageants : Quelque soit la ville utilisée, la moyenne des kbiens converge, et la répétition de ces simulations donnait toujours, avec l'imprécision d'un observateur humain, un même résultat. Ceci nous convainc donc que nous mesurons bien une variable qui dépend du positionnement des bâtiments de la ville.


Pour que les différent fichiers fonctionnent correctement, il faut que les bibliothèques suivantes soient installées :

* numpy
* matplotlib
* pynput
* csv
* collections
* keyboard
* requests
* json
* osmnx

### Apprentissage par renforcement

Pour plus d'informations sur l'apprentissage par renforcement, consultez [etape_renforcement.md](https://github.com/3Mousquetaires/PackastanSimulation/blob/main/etape_apprentissage.md)



#coordonée du centre de strasbourg :
#   (48.58310, 7.74863)

#Paris 17e:
#   (48.882970, 2.299415)

#Montbéliard :
#   (47.505684, 6.803161)

#Arcey :
#  47.522363, 6.660636

#Londres en plein sur Westminster
#   51.500948, -0.124542

#Central Park
#   40.771300, -73.973902
# Je m'amuse comme un fou
