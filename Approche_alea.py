from random import randint
import copy



def alea_op(liste_clees):
    """Fonction permettant d'obtenir un opérateur au hasard.'"""

    alea = randint(0, len(liste_clees) - 1)
    clee_op = liste_clees[alea]
    return clee_op


# Retourne le dicitonnaire d'itinéraires modifié et la liste des noeuds à traverser
def attribution_alea(itineraires, clee_op, noeuds):
    """Fonction attribuant un noeud à l'itinéraire d'opérateurs."""

    # Création d'un itinéraire temporaire pour l'opérateur et d'une liste temporaire de noeuds visités:
    temp = copy.deepcopy(itineraires)
    noeuds_temp = copy.deepcopy(noeuds)

    #Attribution d'un noeud aléatoire à l'itinéraire temporaire, sauf le noeud initial
    rand = randint(1, len(noeuds_temp)-1)
    noeud_alea = noeuds_temp[rand]
    temp[clee_op].insert(-1, noeud_alea)
    noeuds_temp.remove(noeud_alea)

    return temp, noeuds_temp, clee_op

def check_capacite(data, parametres, chemin_a_verifier, op_a_verifier, temps_gestion_noeuds):
    """Fonction vérifiant si l'itinéraire temporaire à évaluer est possible selon la capacité de l'opérateur."""


    # Si le chemin est de seulement de 2 noeuds, cela implique qu'il s'agit seulement du noeud initial. La charge est
    # donc nulle et il est établi que la charge respecte la capacité. Cela est seulement réellement applicable à la
    # validation, mais est une mesure de prévention intéressante.
    if len(chemin_a_verifier) == 2:
        return True

    # Calculer d'abord la charge du chemin à vérifier:
    charge = 0

    for i, arret in enumerate(chemin_a_verifier[:-1]):
        clee_arc = (arret, chemin_a_verifier[i + 1])
        try:
            charge += data[clee_arc]
        except KeyError:
            clee_arc = (chemin_a_verifier[i + 1], arret)
            charge += data[clee_arc]
        charge += temps_gestion_noeuds[arret]

    # Trouver la capacité du type de l'opérateur utilisé pour ce chemin:
    type_op = op_a_verifier[0]
    for op in parametres:
        if type_op == op["Type"]:
            cap = op["Capacité"]
            break
        else:
            continue

    # Vérifier si la solution temporaire est faisable avec la capacité du livreur choisi
    if cap >= charge and cap is not None:
        return True

    else:
        return False


def solve_jour(data, parametres, itineraires, liste_clees, liste_noeuds, temps_gestion_noeuds):
    """Fonction permettant d'assigner les tâches aux opérateurs pour un jour donné."""

    # Choix d'un opérateur initial au hasard:
    liste_utilises = []
    clee_op = alea_op(liste_clees)
    state = False

    iteration = 0
    while state is False and iteration <= 50:
        solution_temp, liste_noeuds_temp, op_a_verifier = attribution_alea(itineraires, clee_op, liste_noeuds)

        iteration += 1
        chemin_a_verifier = solution_temp[op_a_verifier]

        #Si la capacité (en temps) du livreur est supérieure à la charge associée au chemin, le nouveau chemin est considéré comme
        #valide et un nouveau point est ajouté. S'il s'agissait du dernier noeud, le problème est considéré comme résolu

        if check_capacite(data, parametres, chemin_a_verifier, op_a_verifier, temps_gestion_noeuds) is True:
            itineraires = copy.deepcopy(solution_temp)
            liste_noeuds = copy.deepcopy(liste_noeuds_temp)
            if len(liste_noeuds) == 1:
                state = True
                return itineraires, state, liste_noeuds
            else:
                continue

        # Si la capacité de l'opérateur est inférieure à la charge associée au chemin, le ou les nouveaux points sont retirés
        # et l'opérateur est changé:
        else:
            if len(itineraires[clee_op]) != 2:
                liste_utilises.append(clee_op)
            # Changement d'opérateur
            clee_op = alea_op(liste_clees)
            # Si l'opérateur a déja été traité, un différent est choisi. Si tous les opérateurs ont déjà été choisis
            # et utilisés, le problème est considéré comme non_résolu, et le jour suivant est débuté
            while clee_op in liste_utilises and len(liste_utilises) != len(liste_clees):
                clee_op = alea_op(liste_clees)
            #Si les opérateurs sont tous utilisés, la journée est considérée comme terminée
            if len(liste_utilises) == len(liste_clees):
                return itineraires, state, liste_noeuds
    return itineraires, state, liste_noeuds


def solve_probleme(data, parametres, itineraires, liste_clees, noeuds_restants, temps_gestion_noeuds):
    """Fonction englobant toutes les autres de ce module. Permet de résoudre le problème sur plusieurs jours."""

    solution = []
    jour = 0
    state = False
    while state is False and jour <= 15:
        itineraires_jour, state, noeuds_restants = solve_jour(data,
                                                              parametres,
                                                              itineraires,
                                                              liste_clees,
                                                              noeuds_restants,
                                                              temps_gestion_noeuds
                                                              )
        solution.append(itineraires_jour)
        jour += 1
    return solution, state, jour
