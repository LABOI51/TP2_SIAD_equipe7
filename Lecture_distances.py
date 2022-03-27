import openpyxl as pyxl

def get_data(path):

    #Ouvrir le fichier de données
    wb = pyxl.load_workbook(path, data_only=True)
    #Sélectionner la feuille de travail
    feuille = wb["Temps"]
    #Extraire les colonnes de distances entre les noeuds
    noeuds_1 = []
    for noeud in feuille["A"]:
        noeuds_1.append(noeud.value)
    noeuds_2 = []
    for noeud in feuille["B"]:
        noeuds_2.append(noeud.value)
    distances = []
    for dist in feuille["C"]:
        distances.append(dist.value)
    #Créer une matrice de distances sous forme d'une liste, où chaque élément est un tuple de trois éléments
    #1: noeud de départ, #2: noeud d'arrivé, #3: distance entre ces noeuds
    data = {}
    for i, dist in enumerate(distances[1:]):
        data[str(noeuds_1[i+1])+";"+str(noeuds_2[i+1])] = distances[i+1]

    #Créer une liste exhaustive des noeuds du problème:
    liste_noeuds = []
    for cell in feuille["E"]:
        if cell.value != None:
            liste_noeuds.append(cell.value)

    return data, noeuds_1[1:], noeuds_2[1:], distances[1:], liste_noeuds[1:]

