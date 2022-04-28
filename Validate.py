from Clark_Wright import check_capacite

def validate(solution, parametres, liste_clees, liste_noeuds, data, temps_gestion_noeuds):
    """Validation de solutions"""

    ###Vérification que tous les employés sont présent dans chacun des dictionnaires, et qu'aucun nouvel employé est ajouté
    for op in liste_clees:
        for jour in solution:
            if op not in jour:
                return False
            if len(liste_clees) != len(jour):
                return False

    ###Vérification que tous les noeuds sont là, pas de doubles, pas de nouveaux:
    #Liste des noeuds visités
    nd_visites = [liste_noeuds[0]]
    for jour in solution:
        for chemin in jour.keys():
            #Vérification que tous les itinéraires comprennent le noeud initial au début et à la fin
            if jour[chemin][0] != liste_noeuds[0] or jour[chemin][-1] != liste_noeuds[0]:
                return False
            #Ajout de tous les noeuds visités à une liste continue (sauf le noeud initial)
            nd_visites += jour[chemin][1:-1]
    #Vérification qu'une liste ne contient pas plus de noeuds que l'autre
    if len(nd_visites) != len(liste_noeuds):
        return False
    #Vérification que chaque noeuds visitié se retrouve dans la liste de noeuds à visiter
    for nd in nd_visites:
        if nd not in liste_noeuds:
            return False
    #Vérification que chaque noeud est visité une seule fois:
    if len(nd_visites) > len(set(nd_visites)):
        return False

    ###Vérification que le nombre de jours de la solution ne dépasse pas 15: (limite supérieure)
    if len(solution) > 15:
        return False

    ###Vérification que les capacités des opérateurs est respectée, et ce pour tous les jours:
    for jour in solution:
        for op in jour.keys():
            if check_capacite(data, parametres, jour[op], op, temps_gestion_noeuds) is False:
                return False

    #Si toutes les vérifications sont passées, la solution est considérée comme acceptable:
    return True


