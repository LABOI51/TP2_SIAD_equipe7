import Economies
import Lecture_distances
import Lecture_camions
import Solve

#Setup
path = "C:/Users/Laurent/Documents/Uni/SessionHiver2022/SIAD/ProjetSession/Tests.xlsx"
data, noeuds_1, noeuds_2, distances, liste_noeuds = Lecture_distances.get_data(path)
effectifs, itineraires, liste_clees = Lecture_camions.get_camions(path)
economies, poids = Economies.calcul_econ(data, noeuds_1, noeuds_2, liste_noeuds)

#Solve
print(liste_clees)
Solve.attribution(economies, poids, effectifs, itineraires, liste_clees, liste_noeuds)