def recherche_params(parametres, operateur):
    """Fonction permettant d'identifier et de retourner les paramètres concernant un type d'opérateur donné, ceux-ci
    se trouvant dans une liste de dicitonnaires (parametres)"""
    for params in parametres:
        # Si le type d'opérateur concorde avec celui de la liste de paramètres:
        if operateur[0] == params["Type"]:
            c_fixe = params["Coûts fixes"]
            c_var = params["Coûts variables"]
            return c_fixe, c_var

    raise ValueError("Le type d'opérateur ne se retrouve pas dans les paramètres.")


def calcul_distance(solution, data, operateur):
    """Fonction permettant de calculer la distance associée à un itinéraire donné"""
    # Retrouver la solution de l'operateur à l'étude:
    chemin = solution[operateur]

    # Calculer la distance parcourue par cet operateur:
    c_dist = 0
    #Si le chemin comporte seulement 2 noeuds (si l'opérateur ne fait aucun déplacement), la distance retournée est simplement 0
    if len(chemin) == 2:
        return c_dist
    else:
        for j, arret in enumerate(chemin[:-1]):
            clee_arc = (arret,chemin[j + 1])
            try:
                c_dist += data[clee_arc]
            # Si la clee est inconnue, il s'agit en fait qu'elle est inversée dans la liste
            except KeyError:
                clee_arc = (chemin[j + 1],arret)
                c_dist += data[clee_arc]
        return c_dist


def evaluation_operateur(solution, parametres, data, operateur):
    """Fonction permettant d'évaluer le coût associé au trajet de chaque opérateur pour un jour donné."""

    #Recherche dans les paramètres pour trouver les informations nécessaires:
    c_fixe, c_var = recherche_params(parametres, operateur)

    #Calcul de la distance parcourue par l'operateur à l'étude:
    distance = calcul_distance(solution, data, operateur)

    #Calcul du coût total de l'operateur
    if distance == 0:
        return 0
    else:
        c_operateur = c_fixe + (c_var * distance)
    return c_operateur


def eval_solution(solution_globale, liste_clees, parametres, data):
    """Fonction permettant d'évaluer le coût d'une solution donnée."""

    #Évaluation de la valeur totale de la solution de la journée:
    val_solution = 0
    for sol_jour in solution_globale:
        for operateur in liste_clees:
            val_solution += evaluation_operateur(sol_jour, parametres, data, operateur)
    return val_solution


