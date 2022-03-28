from random import randint
import copy
import time

###Attribution d'un itinéraire à un camion au hasard###
# Choix aléatoire d'un camion:
def alea_camion(liste_clees):
    # Choix aléatoire du camion: (ON POURRAIT LE FAIRE DE FAÇON EXHAUSTIVE, MAIS CA SERAIT LONG - branch and bound)
    alea = randint(0, len(liste_clees) - 1)
    clee_camion = liste_clees[alea]
    return clee_camion


# Retourne le dicitonnaire d'itinéraires modifié et la liste des noeuds à traverser
def attribution(economies, itineraires, clee_camion, noeuds, nombre_noeuds):
    # Création d'un itinéraire temporaire pour le camion et d'une liste temporaire de noeuds visités:
    temp = copy.deepcopy(itineraires)
    noeuds_temp = copy.deepcopy(noeuds)
    # Ajout de la première paire de noeuds dans l'itinéraire temporaire si l'itinéraire est vide
    if len(temp[clee_camion]) == 2 and len(noeuds_temp) >= 3:
        for i in range(nombre_noeuds):
            noeud1 = economies[i][0][0]
            noeud2 = economies[i][0][2]
            if noeud1 in noeuds_temp and noeud2 in noeuds_temp:
                temp[clee_camion].insert(1, noeud1)
                noeuds_temp.remove(noeud1)
                temp[clee_camion].insert(2, noeud2)
                noeuds_temp.remove(noeud2)
                return temp, noeuds_temp, clee_camion

    elif len(temp[clee_camion]) == 2 and len(noeuds_temp) == 2:
        temp[clee_camion].insert(1, noeuds_temp[1])
        noeuds_temp.remove(noeuds_temp[1])
        return temp, noeuds_temp, clee_camion

    # Ajout d'un noeud dans l'itinéraire s'il y a déjà un noeud présent
    else:
        # Choix du noeud le plus avantageux à lier au premier noeud ou au dernier noeud de la chaine
        noeud_ouvert1 = temp[clee_camion][1]
        noeud_ouvert2 = temp[clee_camion][-2]

        for i in range(len(economies)):

            # Vérifie si le noeud ouvert 1 constitue l'un des deux noeuds de l'arc étudié
            if noeud_ouvert1 in economies[i][0]:
                # Si le noeud ouvert est le premier noeud de l'arc et que le second est disponible:
                # Ajout de l'autre noeud dans l'itinéraire temporaire afin qu'il soit testé
                if noeud_ouvert1 == economies[i][0][0] and economies[i][0][2] in noeuds_temp:
                    temp[clee_camion].insert(1, economies[i][0][2])
                    noeuds_temp.remove(economies[i][0][2])
                    return temp, noeuds_temp, clee_camion
                # Si le noeud ouvert est le second noeud de l'arc et que le premier est disponible:
                # Ajout de l'autre noeud dans l'itinéraire temporaire afin qu'il soit testé
                elif noeud_ouvert1 == economies[i][0][2] and economies[i][0][0] in noeuds_temp:
                    temp[clee_camion].insert(1, economies[i][0][0])
                    noeuds_temp.remove(economies[i][0][0])
                    return temp, noeuds_temp, clee_camion

            # Même chose mais avec le noeud final du chemin
            elif noeud_ouvert2 in economies[i][0]:
                # Si le noeud ouvert est le premier noeud de l'arc et que le second est disponible:
                # Ajout de l'autre noeud dans l'itinéraire temporaire afin qu'il soit testé
                if noeud_ouvert2 == economies[i][0][0] and economies[i][0][2] in noeuds_temp:
                    temp[clee_camion].insert(-2, economies[i][0][2])
                    noeuds_temp.remove(economies[i][0][2])
                    return temp, noeuds_temp, clee_camion
                # Si le noeud ouvert est le second noeud de l'arc et que le premier est disponible:
                # Ajout de l'autre noeud dans l'itinéraire temporaire afin qu'il soit testé
                elif noeud_ouvert2 == economies[i][0][2] and economies[i][0][0] in noeuds_temp:
                    temp[clee_camion].insert(-2, economies[i][0][0])
                    noeuds_temp.remove(economies[i][0][0])
                    return temp, noeuds_temp, clee_camion


def check_capacite(data, effectifs, chemin_a_verifier, camion_a_verifier):
    # Calculer d'abord la charge du chemin à vérifier:
    charge = 0
    for i, arret in enumerate(chemin_a_verifier[:-1]):
        clee_arc = arret + ";" + str(chemin_a_verifier[i + 1])
        try:
            charge += data[clee_arc]
        except KeyError:
            clee_arc = str(chemin_a_verifier[i + 1]) + ";" + arret
            charge += data[clee_arc]

    # Trouver la capacité du type de camion utilisé pour ce chemin:
    type_camion = camion_a_verifier[0]
    for camion in effectifs:
        if type_camion == camion[0]:
            cap = camion[2]
            break
        else:
            continue
    # Vérifier si la solution temporaire est faisable avec la capacité du camion choisi
    if cap >= charge and cap is not None:
        return True
    else:
        return False


def solve(data, economies, effectifs, itineraires, liste_clees, liste_noeuds):
    # Choix d'un camion initial au hasard:
    liste_utilises = []
    clee_camion = alea_camion(liste_clees)
    n_noeuds_tot = len(liste_clees)
    resolu = False

    start = time.time()
    temps = 0
    while resolu is False and temps <= 10:
        end = time.time()
        temps = end-start
        solution_temp, liste_noeuds_temp, camion_a_verifier = attribution(
            economies,
            itineraires,
            clee_camion,
            liste_noeuds,
            n_noeuds_tot
        )
        chemin_a_verifier = solution_temp[camion_a_verifier]

        if check_capacite(data, effectifs, chemin_a_verifier, camion_a_verifier) is True:
            itineraires = copy.deepcopy(solution_temp)
            liste_noeuds = copy.deepcopy(liste_noeuds_temp)
            if len(liste_noeuds) == 1:
                resolu = True
                return itineraires
            else:
                resolu = False
                continue
        else:
            if len(itineraires[clee_camion]) != 2:
                liste_utilises.append(clee_camion)
            # Changement de camion
            clee_camion = alea_camion(liste_clees)
            while clee_camion in liste_utilises and len(liste_utilises) != len(liste_clees):
                clee_camion = alea_camion(liste_clees)
            if len(liste_utilises) == len(liste_clees):
                print("Tous les camions sont utilisés, mais tous les noeuds ne furent pas visités")
                return itineraires
    print("Il est impossible de résoudre ce problème avec la capacité actuelle de la flotte")
    return itineraires