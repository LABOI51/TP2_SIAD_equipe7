from operator import itemgetter

def calcul_econ(data, noeuds_1, noeuds_2, liste_noeuds):
    #Créer deux vecteurs dont les éléments ont une contrepartie à la même positions;
    #ils représentent des arcs potentiels à lier au point initial
    arc_potentiel_1 = noeuds_1[(len(liste_noeuds)-1):]
    arc_potentiel_2 = noeuds_2[(len(liste_noeuds)-1):]

    #Calculer les économies de la liaison des arcs dans les listes précédentes:
    economies = []
    for i, nd_1 in enumerate(arc_potentiel_1):
        nd_2 = arc_potentiel_2[i]
        #Trouver les clées du dictionnaire afin de pouvoir calculer l'économie associée à chaque arc
        key_1 = (liste_noeuds[0],nd_1)
        key_2 = (liste_noeuds[0],nd_2)
        key_3 = (nd_1,nd_2)
        #Calculer l'économie selon l'heuristique de Clark et Wright
        econ_arc = round(data[key_1] + data[key_2] - data[key_3],5)
        economies.append((key_3, econ_arc))

    #Réaranger la liste afin qu'elle soit en ordre décroissant d'économies
    economies.sort(key=itemgetter(1), reverse=True)
    
    
    return economies



