import openpyxl as pyxl


def append_distance(noeud, object_to_append):
    """Fonction permettant d'ajouter à un liste les valeurs extraites d'un fichier Excel."""
    if noeud.value is not None:
        object_to_append.append(noeud.value)


def get_distance_data(path):
    """Fonction permettant d'extraire les données de distances d'un fichier Excel."""

    #Ouvrir le fichier de données
    wb = pyxl.load_workbook(path, data_only=True)
    #Sélectionner la feuille de travail
    feuille = wb["Temps"]
    #Extraire les colonnes de distances entre les noeuds
    noeuds_1 = []
    for noeud in feuille["G"]:
        append_distance(noeud, noeuds_1)

    noeuds_2 = []
    for noeud in feuille["H"]:
        append_distance(noeud, noeuds_2)

    distances = []
    for dist in feuille["P"]:
        append_distance(dist, distances)

    #Créer une matrice de distances sous forme de dictionnaire, où la distance entre le noeud 1 et 2 est la valeur
    #de la clée "1;2".
    data = {}
    for i, dist in enumerate(distances[1:]):
        data[noeuds_1[i+1],noeuds_2[i+1]] = distances[i+1]

    #Créer une liste exhaustive des noeuds du problème:
    liste_noeuds = []
    for cell in feuille["A"]:
        if cell.value != None:
            liste_noeuds.append(cell.value)

    #Créer un dictionnaire de temps de gestion de chaque noeud, où chaque noeud est une clée, et la valeur est le temps
    #Total de gestion du noeud
    temps_gestion = feuille["D"]
    temps_gestion_noeuds = {}
    for i, nd in enumerate(liste_noeuds[1:]):
        temps_gestion_noeuds[nd] = temps_gestion[i+1].value

    return data, noeuds_1[1:], noeuds_2[1:], liste_noeuds[1:], temps_gestion_noeuds

