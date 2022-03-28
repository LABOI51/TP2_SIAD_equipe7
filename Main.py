import Economies
import Lecture_distances
import Lecture_camions
import Solve

#Setup
path = "C:/Users/Laurent/Documents/Uni/SessionHiver2022/SIAD/TP2_SIAD_equipe7/Tests.xlsx"
data, noeuds_1, noeuds_2, distances, liste_noeuds = Lecture_distances.get_data(path)
effectifs, itineraires, liste_clees = Lecture_camions.get_camions(path, liste_noeuds)
economies = Economies.calcul_econ(data, noeuds_1, noeuds_2, liste_noeuds)

#Solve
sol = Solve.solve(data, economies, effectifs, itineraires, liste_clees, liste_noeuds)

#Fonction objectif
