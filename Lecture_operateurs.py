import openpyxl as pyxl

def get_operateurs(path, liste_noeuds):

    #Ouvrir le fichier de données
    wb = pyxl.load_workbook(path, data_only=True)

    #Sélectionner la feuille de travail
    feuille_operateurs = wb["Operateurs"]

    #Sortir les informations par colonnes
    types_operateurs = feuille_operateurs["A"]
    nombre_operateurs = feuille_operateurs["B"]
    capacite_operateurs = feuille_operateurs["C"]
    couts_var = feuille_operateurs["D"]
    couts_fixes = feuille_operateurs["E"]


    #La liste nommée parametres contient plusieurs dictionnaires dont les éléments correspondent aux type de chaque operateur.
    #Ces dictionnaires permettent d'accéder aux différentes informations de chaque types d'operateur
    parametres = []
    for i, type_operateur in enumerate(types_operateurs[1:]):
        parametres.append({})
        parametres[i]["Type"] = type_operateur.value
        parametres[i]["Nombre d'effectifs"] = nombre_operateurs[i+1].value
        parametres[i]["Capacité"] = capacite_operateurs[i+1].value
        parametres[i]["Coûts fixes"] = couts_fixes[i+1].value
        parametres[i]["Coûts variables"] = couts_var[i+1].value


    #Le dictionnaire nommé itinéraires peut être vu comme les variables de décision du problème. Il s'agit d'un dictionnaire dont les clées sont chaque opérateur par type,
    #et la valeur de ces clées est une liste de noeuds traversés par ceux-ci. Dans ce module, ces valeurs seront des listes ayant comme premier et dernier élément le noeud initial
    #En même temps, une liste de ces clées est créée afin de pouvoir choisir un opérateur de façon aléatoire.
    itineraires = {}
    liste_clees = []
    #Calculer le nombre total d'opérateurs (d'entrées dans le dictionnaire)
    n_op_tot = 0
    for n in nombre_operateurs[1:]:
        n_op_tot += n.value
    #Construire le dictionnaire d'itinériares
    for type_operateur in parametres:
        for j in range(type_operateur["Nombre d'effectifs"]):
            clee = (type_operateur["Type"], j+1)
            liste_clees.append(clee)
            #Ajout du point initial et final dans l'itinéraire
            itineraires[clee] = [liste_noeuds[0], liste_noeuds[0]]

    return parametres, itineraires, liste_clees