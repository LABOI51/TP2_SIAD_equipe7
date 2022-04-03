from random import randint
import copy


###Attribution d'un itinéraire à un opérateur au hasard###
# Choix aléatoire d'un opérateur:
def alea_op(liste_clees):
    # Choix aléatoire du opérateur:
    alea = randint(0, len(liste_clees) - 1)
    clee_op = liste_clees[alea]
    return clee_op


def compute_cas_assignation(temp, clee_op, econ, noeuds_temp, insert_position):
    temp[clee_op].insert(insert_position, econ)
    noeuds_temp.remove(econ)
    return temp, noeuds_temp, clee_op


# Retourne le dicitonnaire d'itinéraires modifié et la liste des noeuds à traverser
def attribution(economies, itineraires, clee_op, noeuds):

    # Création d'un itinéraire temporaire pour l'opérateur et d'une liste temporaire de noeuds visités:
    temp = copy.deepcopy(itineraires)
    noeuds_temp = copy.deepcopy(noeuds)

    # Ajout de la première paire de noeuds dans l'itinéraire temporaire si celui-ci est vide
    if len(temp[clee_op]) == 2 and len(noeuds_temp) >= 3:
        for econ in economies:
            noeud1 = econ[0][0]
            noeud2 = econ[0][-1]
            if noeud1 in noeuds_temp and noeud2 in noeuds_temp:
                temp[clee_op].insert(1, noeud1)
                noeuds_temp.remove(noeud1)
                temp[clee_op].insert(2, noeud2)
                noeuds_temp.remove(noeud2)
                return temp, noeuds_temp, clee_op


    #Cas où il ne reste qu'un noeud à ajouter et il s'agit d'un nouvel opérateur
    elif len(temp[clee_op]) == 2 and len(noeuds_temp) == 2:
        temp[clee_op].insert(1, noeuds_temp[1])
        noeuds_temp.remove(noeuds_temp[1])
        return temp, noeuds_temp, clee_op

    # Ajout d'un noeud dans l'itinéraire s'il y a déjà un noeud présent
    else:
        # Choix du noeud le plus avantageux à lier au premier noeud ou au dernier noeud de la chaine
        noeud_ouvert1 = temp[clee_op][1]
        noeud_ouvert2 = temp[clee_op][-2]

        for i in range(len(economies)):

            # Vérifie si le noeud ouvert 1 constitue l'un des deux noeuds de l'arc étudié
            if noeud_ouvert1 in economies[i][0]:
                # Si le noeud ouvert est le premier noeud de l'arc et que le second est disponible:
                # Ajout de l'autre noeud dans l'itinéraire temporaire afin qu'il soit testé
                
                if noeud_ouvert1 == economies[i][0][0] and economies[i][0][-1] in noeuds_temp:
                    return compute_cas_assignation(temp, clee_op, economies[i][0][-1], noeuds_temp, 1)

                # Si le noeud ouvert est le second noeud de l'arc et que le premier est disponible:
                # Ajout de l'autre noeud dans l'itinéraire temporaire afin qu'il soit testé
                elif noeud_ouvert1 == economies[i][0][-1] and economies[i][0][0] in noeuds_temp:
                    return compute_cas_assignation(temp, clee_op, economies[i][0][0], noeuds_temp, 1)

            # Même chose mais avec le noeud final du chemin
            elif noeud_ouvert2 in economies[i][0]:
                # Si le noeud ouvert est le premier noeud de l'arc et que le second est disponible:
                # Ajout de l'autre noeud dans l'itinéraire temporaire afin qu'il soit testé
                if noeud_ouvert2 == economies[i][0][0] and economies[i][0][-1] in noeuds_temp:
                    return compute_cas_assignation(temp, clee_op, economies[i][0][-1], noeuds_temp, -2)

                # Si le noeud ouvert est le second noeud de l'arc et que le premier est disponible:
                # Ajout de l'autre noeud dans l'itinéraire temporaire afin qu'il soit testé
                elif noeud_ouvert2 == economies[i][0][-1] and economies[i][0][0] in noeuds_temp:
                    return compute_cas_assignation(temp, clee_op, economies[i][0][0], noeuds_temp, -2)


def check_capacite(data, parametres, chemin_a_verifier, op_a_verifier, temps_gestion_noeuds):

    # Calculer d'abord la charge du chemin à vérifier:
    charge = 0

    for i, arret in enumerate(chemin_a_verifier[:-1]):
        clee_arc = (arret, chemin_a_verifier[i + 1])
        try:
            charge += data[clee_arc]
        except KeyError:
            clee_arc = (chemin_a_verifier[i + 1],arret)
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


def solve_jour(data, economies, parametres, itineraires, liste_clees, liste_noeuds, temps_gestion_noeuds):

    # Choix d'un opérateur initial au hasard:
    liste_utilises = []
    clee_op = alea_op(liste_clees)
    state = False

    iteration = 0
    while state is False and iteration <= 1000:
        solution_temp, liste_noeuds_temp, op_a_verifier = attribution(
            economies,
            itineraires,
            clee_op,
            liste_noeuds,
        )
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
            if len(liste_utilises) == len(liste_clees):
                return itineraires, state, liste_noeuds
    return itineraires, state, liste_noeuds

#Résolution du problème sur plusieurs jours
def solve_probleme(data, economies, parametres, itineraires, liste_clees, noeuds_restants, temps_gestion_noeuds):
    solution = []
    jour = 0
    state = False
    while state is False and jour <= 15:
        itineraires_jour, state, noeuds_restants = solve_jour(data,
                                                              economies,
                                                              parametres,
                                                              itineraires,
                                                              liste_clees,
                                                              noeuds_restants,
                                                              temps_gestion_noeuds
                                                              )
        solution.append(itineraires_jour)
        jour += 1
    return solution, state, jour
