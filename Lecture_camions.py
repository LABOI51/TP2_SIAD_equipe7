from importlib.metadata import distribution
import openpyxl as pyxl

def get_camions(path):

    #Ouvrir le fichier de données
    wb = pyxl.load_workbook(path, data_only=True)

    #Sélectionner la feuille de travail
    feuille_camions = wb["Camions"]

    #Sortir les informations par colonnes
    types_camions = feuille_camions["A"]
    nombre_camions = feuille_camions["B"]
    capacite_camions = feuille_camions["C"]

    #La liste nommée effectifs contient plusieurs tuples dont les éléments correspondent aux type de chaque camion.
    #La première position indique le type du camion, la seconde le nombre de camions de ce type et la troisième la capacité de chaque camion de ce type
    effectifs = []
    for i, type in enumerate(types_camions[1:]):
        effectifs.append((type.value, nombre_camions[i+1].value, capacite_camions[i+1].value))

    #Le dictionnaire nommé itinéraires peut être vu comme les variables de décision du problème. Il s'agit d'un dictionnaire dont les clées sont chaque camion par type,
    #et la valeur de ces clées est une liste de noeuds traversés par ceux-ci. Dans ce module, ces valeurs seront des listes vides, évidemment.
    #En même temps, une liste de ces clées est créée afin de pouvoir choisir un camion de façon aléatoire.
    itineraires = {}
    liste_clees = []
    #Calculer le nombre total de camions (d'entrées dans le dictionnaire)
    n_camions_tot = 0
    for n in nombre_camions[1:]:
        n_camions_tot += n.value
    #Construire le dictionnaire
    for i in effectifs:
        for j in range(i[1]):
            clee = (i[0], j+1)
            liste_clees.append(clee)
            itineraires[clee] = []

    return effectifs, itineraires, liste_clees