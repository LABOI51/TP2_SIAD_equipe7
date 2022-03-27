from random import randint

###Attribution d'un itinéraire à un camion au hasard###
#Retourne le dicitonnaire d'itinéraires modifié et la liste des noeuds à traverser
def attribution(economies, poids, effectifs, itineraires, liste_clees, liste_noeuds):
    #Choix aléatoire du camion: (ON POURRAIT LE FAIRE DE FAÇON EXHAUSTIVE, MAIS CA SERAIT LONG - branch and bound)
    alea = randint(0, len(liste_clees)-1)
    clee_camion = liste_clees[alea]
    #Ajout d'une condition ne permettant pas d'ajouter des points à un camion déjà 
    compteur = 0
    while len(itineraires[clee_camion]) != 2 or compteur <= 100000:
        alea = randint(0, len(liste_clees)-1)
        clee_camion = liste_clees[alea]
        compteur += 1

    #Ajout du premier noeud dans l'itinéraire du camion choisi:
    






#def check_capacite(noeuds_visites, charge, capacite):

def solve(economies, poids, effectifs, itineraires, liste_clees, liste_noeuds):
    solution = attribution(economies, poids, effectifs, itineraires, liste_clees, liste_noeuds)
    #etc....
