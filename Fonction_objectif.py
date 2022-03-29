

def recherche_params(parametres, liste_clees, camion):
    for params in parametres:
        # Si le type du camion concorde avec celui de la liste de paramètres:
        if camion[0] == params["Type"]:
            c_fixe = params["Coûts fixes"]
            c_var = params["Coûts variables"]
            return c_fixe, c_var

    raise ValueError("Le type de camion ne se retrouve pas dans les paramètres.")



def calcul_distance(solution, data, camion):
    # Retrouver la solution du camion à l'étude:
    chemin = solution[camion]

    # Calculer la distance parcourue par ce camion:
    dist = 0
    #Si le chemin comporte seulement 2 noeuds (si le camion ne fait aucun déplacement), la distance retournée est simplement 0
    if len(chemin) == 2:
        return dist
    else:
        for j, arret in enumerate(chemin[:-1]):
            clee_arc = arret + ";" + str(chemin[j + 1])
            try:
                dist += data[clee_arc]
            # Si la clee est inconnue, il s'agit en fait qu'elle est inversée dans la liste
            except KeyError:
                clee_arc = str(chemin[j + 1]) + ";" + arret
                dist += data[clee_arc]
        return dist


def evaluation_camion(solution, parametres, data, liste_clees, camion):

        #Recherche dans les paramètres pour trouver les informations nécessaires:
        c_fixe, c_var = recherche_params(parametres, liste_clees, camion)

        #Calcul de la distance parcourue par le camion à l'étude:
        distance = calcul_distance(solution, data, camion)

        #Calcul du coût total du camion
        c_camion = c_fixe + (c_var * distance)

        return c_camion


def eval_solution(solution, liste_clees, parametres, data):
    #Évaluation de la valeur totale de la solution:
    val_solution = 0

    for camion in liste_clees:

        val_solution += evaluation_camion(solution, parametres, data, liste_clees, camion)

    return val_solution