import time

import Economies
import Lecture_distances
import Lecture_operateurs
import Clark_Wright
import Fonction_objectif


def main():

    #Setup
    path = "DATA.xlsm"
    data, noeuds_1, noeuds_2, liste_noeuds, temps_gestion_noeuds = Lecture_distances.get_data(path)
    parametres, itineraires, liste_clees = Lecture_operateurs.get_operateurs(path, liste_noeuds)
    economies = Economies.calcul_econ(data, noeuds_1, noeuds_2, liste_noeuds)
    #Puisque la résolution est de nature aléatoire, il y aura plusieurs itérations de celle-ci pendant une période de temps fixe
    # ou sur un nombre d'itérations maximum:
    start = time.time()
    temps = 0
    temps_max = 60

    iteration = 0
    iteration_max = 1000

    #Solutioner le problème une première fois:

    # Solve
    state = False
    while state is False and iteration <= 20:
        iteration += 1
        sol, state, jour = Clark_Wright.solve_probleme(data, economies, parametres, itineraires, liste_clees, liste_noeuds, temps_gestion_noeuds)

    if state is False:
        raise ValueError("Le problème ne peut être solutionné avec les contraintes et les paramètres actuels.")

    # Fonction objectif
    val_sol = Fonction_objectif.eval_solution(sol, liste_clees, parametres, data)

    #Si la valeur de la fonction objectif est plus petite que la précédente, garder seulement cette solution et réitérer
    iteration = 0

    while temps <= temps_max and iteration < iteration_max:
        end = time.time()
        temps = end - start
        iteration += 1

        #Solve
        sol_temp, state, jour_temp = Clark_Wright.solve_probleme(data, economies, parametres, itineraires, liste_clees, liste_noeuds, temps_gestion_noeuds)

        if state is True:
            #Fonction objectif
            val_sol_temp = Fonction_objectif.eval_solution(sol_temp, liste_clees, parametres, data)

            if val_sol_temp < val_sol:
                val_sol = val_sol_temp
                sol = sol_temp
                jour = jour_temp

    print("\nMéthode utilisée : Heuristique de Clark & Wright simplifié")
    print("\n" + str(iteration) + " solutions trouvées en " + str(temps)[:5] + " secondes.")
    print("\nMeilleure solution trouvée: ")
    print("\nTemps total pour faire l'entièreté des livraisons: " + str(jour) + " jours")
    for i, trajet in enumerate(sol):
        print("\nJour " + str(i+1) + ":" + str(trajet))

    print("\nValeur de la fonction objectif de cette solution: " + str(val_sol))

main()
