# PackastanSimulation : Optimisation de la disposition des bâtiments dans une ville

Ce repo contient les fichiers sources du projet TIPE 2022-2023 du groupe des 3 mousquetaires :

* Paul-Henri Andrieu [@phandrieu](https://github.com/phandrieu)
* Damien Maître [@DobbyOff](https://github.com/DobbyOff)
* Ethan Petitjean [@Slordeee](https://github.com/Slordeee)

$$\int_0^{+\infty} \frac{sh(t)}{ch(t+ln(1+\frac{1}{t}} dt$$

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

Nos résultats furent encourageants : Quelque soit la ville utilisée, la moyenne des kbiens converge, et la répétition de ces simulations donnait toujours, avec l'imprécision d'un observateur humain, un même résultat. Nous sommes donc convaincus que nous mesurons bien une variable qui dépend du positionnement des bâtiments de la ville, dont les variations sont pertinentes.


### Apprentissage renforcé : deuxième étage de simulations

Tout ce qui précède est fonctionnel. Mais ça ne suffit pas. Le deuxième étage de PackastanSimulation permet d'optimiser le kbien moyen d'une ville grâce à l'intelligence artificielle. Nous répetons la génération du kbien de la ville encore et encore, en changeant à chaque fois le type du pire batiment. 

> Nous utilisons la technique de l'apprentissage renforcé. Le deuxième étage a deux types d'actions : l'exploitation et l'exploration. En exploration, le programme tente une nouvelle stratégie, et inscrit le résultat dans sa mémoire. En exploitation, il utilise cette mémoire pour agir de la façon la plus efficace sur la carte.

Ce deuxième étage produit une suite de villes dont le kbien est croissant et convergeant. L'asymptote est donc, selon nos termes, la disposition optimale des batiments dans la ville suivant le besoin auquels ils répondent.


### Serialisation et factorisation

Après compilé un programme fonctionnel sur une ville inventée de toute pièce et faite pour que les simulations soient simples, il a fallu implémenter nos méthodes sur une vraie ville. Nous sommes en moyen de récupérer tous les batiments d'une aire urbaine d'une taille donnée, de créer un graphe de déplacement qui relie tous les batiments type 'habitation' aux autres batiments répondant aux besoins des citoyens.

 > Nous utilisons la base de données d'OpenStreetMap, qui contient une quantité gigantesque de données en accès libre. Nous dialoguons avec OPM pour obtenir les données brutes contenant tous les batiments présents sur une tile vectorielle. Les tiles vectorielles sont les 'pixels' des cartes en lignes, ce sont des images rectangulaires d'une précision donnée qui couvrent le globe.
 > Les données sont récupérées sous format JSON, il suffit alors de traiter ces données pour créer des instances de Batiments qui correspondent à ceux existant dans la réalité. Nous avons extrait la surface, la position géographique, la hauteur et le type de tous les batiments référencés par OPM sur les aires urbaines que nous avons testées.

Le temps d'exécution de ce programme est très long. La plus grande surface sur laquelle nous nous soyons aventurée réferençait 26 000 batiments sur Strasbourg centre. La création des batiments est relativement rapide et en complexité linéaire O(n). Le problème est la création du graphe de déplacement. Il faut en effet parcourir chaque maison, et pour chaque besoin il faut trouver le batiment y répondant le plus proche, et calculer un chemin y menant. Le calcul de chemin est géré par la bibliothèque `networkx`, reste trop lent. Trop lent pour que les citoyens calculent à chaque tour le batiment intéressant le plus proche et l'itinéraire pour y parvenir. Nous avons donc factorisé cette partie et donné à chaque maison un annuaire où tous les batiments et les chemins vers eux sont remplis. Ces annuaires constituent la partie la plus chronophage du programme. La génération de la carte taille 3 de Strasbourg centre (soit environ 15 km² centré sur la grande île) a pris 1h 40. Nous tombons sur 20 petites minutes pour des cartes de Montbéliard (25) de quelque km² (taille 2).



## Visite du repo 

 > Pour que les différent fichiers fonctionnent correctement, il faut que les bibliothèques suivantes soient installées : numpy, matplotlib, csv, collections, requests, json, osmnx. D'autres peuvent s'ajouter pour les versions précédentes.


 * `main.py` : C'est d'ici qu'est exécuté le programme. Il contient la classe Core qui gère le deuxième étage de simulations et les procédures utilisées par l'algorithme d'apprentissage renforcé. Il désérialise la mémoire du programme, créé les villes et les modifie. Il est actuellement paramétré pour lancer Strasbourg centre en taille 3 à son exécution. Pour le lancer en simulation : `python main.py`.

 * `ville.py` : contient la classe Ville qui gère le premier étage des simulations à l'échelle d'une ville entière. Créé les citoyens et les fait jouer.

 * `mapbuilder.py` : contient la classe MapBuilder, c'est le programme qui construit les cartes, les serialises et les déserialise. Pour le lancer en construction : `python mapbuilder.py latitude longitude [taille = 1]`.

 * `batiment_r.py` : classe Batiment, Maison et Road.

 * `citoyen.py` : classe Citoyen.

 * `info_batiments.csv` : contient les informations sur les besoins primaires.

 * `map.txt` : Il s'agit de la carte originelle en 60x60 sur laquelle nous avons créé le programme avant d'implémenter MapBuilder.

 * `VilleRelle, base et OLD` : anciens dossiers qui où nous expérimentions avec les différents étages du programme avant de tout brancher.

 * `memoire` : mémoire du programme, contient les cartes déjà serialisées. Ce dossier est dans le .gitignore, il n'est donc pas à jour. Les cartes sont en effet trop volumineuses pour être transférées à Github lors des commit sans que ce dernier de râle. On parle en effet d'un JSON de 2 millions de lignes et d'un XAML de 230 000 lignes pour notre carte de Strasbourg centre en taille 3, soit environ 50 Mo.

 * `étude` : contient des fichiers JSONs récupérés en sortie de MapBuilder, les requêtes renvoyées par OpenStreetMap et d'autres fichiers tests. Nous étudions ces gros fichiers à la main pour en comprendre la synthaxe et ensuite créer des programmes qui traitent ces grosses quantités d'informations automatiquement.

 * `cache` : dossier utilisé par l'une de nos bibliothèques importées sans que l'on ne sache vraiment pourquoi.

## Showcase : Strasbourg

Nous montrons dans les détails le premier résultat fonctionnel de PackastanSimulation : l'implémentation de la ville de Strasbourg dans le programme.

### Création de la carte 

> Le fichier `mapbuilder` fut appelé, centré sur la Grande île de Strasbourg, au sud ouest de la cathédrale. Voici le résultat, affiché sur matplotlib :

![Alt text](readme/Stras%203%20map.png)

### Premier étage de la simulation

 > Une fois que la ville est récupérée et instanciée, 1000 citoyens sont créés et vont se déplacer dans la ville pour lancer le calcul du kbien. Voici le résultat :

 ![Alt text](readme/Stras%203%20premier%20tour.png)

 ### Asymptote et Strasbourg optimal :

 > Laissons tourner la simulation quelque temps :

![Alt text](readme/Stras%203%20asymptote%20tour.png)


## Banque de coordonnées

* coordonnées du centre de strasbourg : 48.58310, 7.748)

* Paris 17e: (48.882970, 2.299415)

* Montbéliard : (47.505684, 6.803161)

* Arcey : (47.522363, 6.660636)

* Londres en plein sur Westminster : (51.500948, -0.124542)

* Central Park : (40.771300, -73.973902)
