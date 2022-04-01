import openpyxl as pyxl

def get_data(path):

    #Ouvrir le fichier de données
    wb = pyxl.load_workbook(path, data_only=True)
    #Sélectionner la feuille de travail
    feuille = wb["Temps"]
    #Extraire les colonnes de distances entre les noeuds
    noeuds_1 = []
    for noeud in feuille["G"]:
        if noeud.value is not None:
            noeuds_1.append(noeud.value)
    noeuds_2 = []
    for noeud in feuille["H"]:
        if noeud.value is not None:
            noeuds_2.append(noeud.value)
    distances = []
    for dist in feuille["P"]:
        if dist.value is not None:
            distances.append(dist.value)
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

