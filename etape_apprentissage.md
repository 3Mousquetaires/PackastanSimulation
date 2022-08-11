# Etape pour apprentissage par renforcement:

Quelques définitions :

- état : niveau actuel d'avancement dans la mission
- environnement : ici la caractérisation de la ville ( disposition des bâtiments, leurs caractéristiques... )
- récompense : amélioration ou régression de l'avancement de la mission ( on réajuste l'état en fonction de la récompense )
- action : action faite sur la ville ( ex: supprimer un bâtiment ), l'action appartient à un ensemble d'action prédéfinit par l'utilisateur
- état maximale : mission terminée, ville parfaite
- ratio d'exploration : taux ici fixé d'action aléatoires pour voir comment l'état va évoluer

1) prendre en compte l'état "s" à l'environnement "E" :

- faire tourner la simulation dans la ville d'environnement E ( un certain temps à définir )

- récupérer le K_bien ( ce qui sera ici l'état )

2) 1) ( si on est en dessous du ratio d'exploration ) faire une action "act" aux hasard dans la liste des actions possible "ensemble_act":

- définir un ensemble d'actions possible
- prendre une action aléatoirement 
- appliquer l'action sur l'environnement ( l'environnement change ) 

2) 2) ( hors ratio d'exploration ) action qui maximise la récompense :

- comparer l'état actuel aux différents états déjà rencontré dans le tableau des récompenses 
- appliquer l'action la plus adapté 

3) regarder le changement de l'état "s'" :

- faire tourner la simulation dans la nouvelle ville 
- récupérer le K_bien

4) évaluer la récompense de ce nouvel état

- comparer K_bien et K_bien2
- en déduire la récompense ( positive ou négative )

5) ajouter la récompense dans un tableau récompense "tab_r" :

- créer un tableau des différentes récompenses par rapport à l'action appliquée et de l'état

6) mettre à jour l'état en fonction
7) répéter jusqu'à avoir état maximale