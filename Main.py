import time

import Lecture_distances
import Lecture_operateurs
import Approche_alea
import Clark_Wright
import Economies
import Fonction_objectif
import UI
import Validate

def main():
    """Fonction permettant de lancer la résolution du problème par l'heuristique de Clarke & Wright simplifié."""

    #Setup
    path = "DATA.xlsm"
    data, noeuds_1, noeuds_2, liste_noeuds, temps_gestion_noeuds = Lecture_distances.get_distance_data(path)
    parametres, itineraires, liste_clees = Lecture_operateurs.get_operateurs(path, liste_noeuds)
    economies = Economies.calcul_econ(data, noeuds_1, noeuds_2, liste_noeuds)

    #Choix de la méthode
    methode, temps_max = UI.choix_methode()
    if methode == "1":
        txt_methode = "la méthode aléatoire"
    else:
        txt_methode = "l'heuristique de Clarke & Wright"

    print("\nÉvaluation de la solution à l'aide de " + txt_methode + "...")

    #Puisque la résolution est de nature aléatoire, il y aura plusieurs itérations de celle-ci pendant une période de temps fixe
    # ou sur un nombre d'itérations maximum:
    start = time.time()
    temps = 0
    iteration = 0

    #Solutioner le problème une première fois:

    # Solve
    state = False
    while state is False and iteration <= 50:
        iteration += 1

        if methode == "1":
            sol, state, jour = Approche_alea.solve_probleme(data,
                                                           parametres,
                                                           itineraires,
                                                           liste_clees,
                                                           liste_noeuds,
                                                           temps_gestion_noeuds
                                                           )


        elif methode == "2":
            sol, state, jour = Clark_Wright.solve_probleme(data,
                                                           economies,
                                                           parametres,
                                                           itineraires,
                                                           liste_clees,
                                                           liste_noeuds,
                                                           temps_gestion_noeuds
                                                           )

        else:
            raise ValueError("Erreur inconnue.")

        #Validation de la solution initiale
        if Validate.validate(sol, parametres, liste_clees, liste_noeuds, data, temps_gestion_noeuds) is False:
            state = False

    if state is False:
        raise ValueError("Le problème ne peut être solutionné avec les contraintes et les paramètres actuels.")

    # Fonction objectif
    val_sol = Fonction_objectif.eval_solution(sol, liste_clees, parametres,
                                              data, temps_gestion_noeuds)

    #Si la valeur de la fonction objectif est plus petite que la précédente, garder seulement cette solution et réitérer
    iteration = 0

    while temps <= temps_max:

        end = time.time()
        temps = end - start
        iteration += 1

        #Solve
        if methode == "1":
            sol_temp, state, jour_temp = Approche_alea.solve_probleme(data,
                                                           parametres,
                                                           itineraires,
                                                           liste_clees,
                                                           liste_noeuds,
                                                           temps_gestion_noeuds
                                                           )

        elif methode == "2":
            sol_temp, state, jour_temp = Clark_Wright.solve_probleme(data,
                                                           economies,
                                                           parametres,
                                                           itineraires,
                                                           liste_clees,
                                                           liste_noeuds,
                                                           temps_gestion_noeuds
                                                           )
        else:
            raise ValueError("Erreur inconnue.")

        if state is True:

            #Fonction objectif
            val_sol_temp = Fonction_objectif.eval_solution(sol_temp, liste_clees, parametres,
                                                           data, temps_gestion_noeuds)
            if val_sol_temp < val_sol and Validate.validate(sol_temp, parametres,
                                                            liste_clees, liste_noeuds,
                                                            data, temps_gestion_noeuds) is True:
                val_sol = val_sol_temp
                sol = sol_temp
                jour = jour_temp

    #Sortie utilisateur
    print("\n" + str(iteration) + " solutions trouvées en " + str(temps)[:5] + " secondes.")
    print("\nTemps total pour faire l'entièreté des livraisons: " + str(jour) + " jours")
    print("\nMeilleure solution trouvée: ")
    for i, trajet in enumerate(sol):
        print("\nJour " + str(i+1) + ":" + str(trajet))
    print("\nValeur de la fonction objectif de cette solution: " + str(round(val_sol, 2)))

main()
