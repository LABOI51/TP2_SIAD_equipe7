import openpyxl as pyxl

def get_camions(path, liste_noeuds):

    #Ouvrir le fichier de données
    wb = pyxl.load_workbook(path, data_only=True)

    #Sélectionner la feuille de travail
    feuille_camions = wb["Camions"]

    #Sortir les informations par colonnes
    types_camions = feuille_camions["A"]
    nombre_camions = feuille_camions["B"]
    capacite_camions = feuille_camions["C"]
    couts_var = feuille_camions["D"]
    couts_fixes = feuille_camions["E"]


    #La liste nommée parametres contient plusieurs dictionnaires dont les éléments correspondent aux type de chaque camion.
    #Ces dictionnaires permettent d'accéder aux différentes informations de chaque types de camion
    parametres = []
    for i, type_camion in enumerate(types_camions[1:]):
        parametres.append({})
        parametres[i]["Type"] = type_camion.value
        parametres[i]["Nombre d'effectifs"] = nombre_camions[i+1].value
        parametres[i]["Capacité"] = capacite_camions[i+1].value
        parametres[i]["Coûts fixes"] = couts_fixes[i+1].value
        parametres[i]["Coûts variables"] = couts_var[i+1].value


    #Le dictionnaire nommé itinéraires peut être vu comme les variables de décision du problème. Il s'agit d'un dictionnaire dont les clées sont chaque camion par type,
    #et la valeur de ces clées est une liste de noeuds traversés par ceux-ci. Dans ce module, ces valeurs seront des listes ayant comme premier et dernier élément le noeud initial
    #En même temps, une liste de ces clées est créée afin de pouvoir choisir un camion de façon aléatoire.
    itineraires = {}
    liste_clees = []
    #Calculer le nombre total de camions (d'entrées dans le dictionnaire)
    n_camions_tot = 0
    for n in nombre_camions[1:]:
        n_camions_tot += n.value
    #Construire le dictionnaire d'itinériares
    for type_camion in parametres:
        for j in range(type_camion["Nombre d'effectifs"]):
            clee = (type_camion["Type"], j+1)
            liste_clees.append(clee)
            #Ajout du point initial et final dans l'itinéraire
            itineraires[clee] = [liste_noeuds[0], liste_noeuds[0]]

    #Construire un dictionnaire dont la clée est le type de camion de coûts fixes et variables
    return parametres, itineraires, liste_clees