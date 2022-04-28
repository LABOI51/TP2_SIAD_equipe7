import unittest

from Validate import validate
from Fonction_objectif import eval_solution


class Test_solver(unittest.TestCase):

    def setUp(self):

        #Instance du problème:
        self.liste_noeuds = ["A", "B", "C", "D", "E", "F", "G"]
        self.liste_clees = [("Gestionnaire", 1), ("Livreur", 1), ("Livreur", 2)]
        self.data = {("A", "B"): 11, ("A", "C"): 15, ("A", "D"): 4, ("A", "E"): 5, ("A", "F"): 6,
                ("A", "G"): 7, ("B", "C"): 5, ("B", "D"): 2, ("B", "E"): 8, ("B", "F"): 3,
                ("B", "G"): 10, ("C", "D"): 12, ("C", "E"): 2, ("C", "F"): 6, ("C", "G"): 8,
                ("D", "E"): 3, ("D", "F"): 11,("D", "G"): 5, ("E", "F"): 17, ("E", "G"): 15,
                ("F", "G"): 9}

        self.parametres = [{'Type': 'Gestionnaire', "Nombre d'effectifs": 1, 'Capacité': 30, 'Coûts fixes': 60, 'Coûts variables': 10},
                       {'Type': 'Livreur', "Nombre d'effectifs": 2, 'Capacité': 50, 'Coûts fixes': 60, 'Coûts variables': 5}]

        self.temps_gestion_noeuds = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 2, "F": 3, "G": 1}


        #Solution réalisable 1
        self.sol_res_1 = [{("Gestionnaire", 1): ["A", "B", "A"], ("Livreur", 1): ["A", "C", "D", "A"], ("Livreur", 2): ["A", "E", "F", "A"]},
                     {("Gestionnaire", 1): ["A", "A"], ("Livreur", 1): ["A", "G", "A"], ("Livreur", 2): ["A", "A"]}]

        self.val_sol_res_1 = 890

        #Solution réalisable 2:
        self.sol_res_2 = [{("Gestionnaire", 1): ["A", "B", "A"], ("Livreur", 1): ["A", "C", "A"], ("Livreur", 2): ["A", "D", "A"]},
                     {("Gestionnaire", 1): ["A", "E", "A"], ("Livreur", 1): ["A", "F", "A"], ("Livreur", 2): ["A", "G", "A"]}]

        self.val_sol_res_2 = 1075

        #Solution irréalisable 1:
        #Solution ne respectant pas la capacité d'un employé:
        self.sol_irr_1 = [{("Gestionnaire", 1): ["A", "B", "C", "D", "E", "F", "G", "A"], ("Livreur", 1): ["A", "A"], ("Livreur", 2): ["A", "A"]}]

        #Solution irréalisable 2:
        #Solution ne passant pas par tous les points (manque le point C):
        self.sol_irr_2 = [{("Gestionnaire", 1): ["A", "B", "A"], ("Livreur", 1): ["A", "D", "A"], ("Livreur", 2): ["A", "E", "F", "A"]},
                     {("Gestionnaire", 1): ["A", "A"], ("Livreur", 1): ["A", "G", "A"], ("Livreur", 2): ["A", "A"]}]

        # Solution irréalisable 3:
        # Noeud ajouté (noeud H):
        self.sol_irr_3 = [{("Gestionnaire", 1): ["A", "B", "A"], ("Livreur", 1): ["A", "C", "D", "A"], ("Livreur", 2): ["A", "E", "F", "A"]},
                     {("Gestionnaire", 1): ["A", "A"], ("Livreur", 1): ["A", "G", "A"], ("Livreur", 2): ["A", "H", "A"]}]

        # Solution irréalisable 4:
        # Noeud doublé (noeud C):
        self.sol_irr_4 = [{("Gestionnaire", 1): ["A", "B", "A"], ("Livreur", 1): ["A", "C", "D", "A"], ("Livreur", 2): ["A", "E", "F", "A"]},
                     {("Gestionnaire", 1): ["A", "C", "A"], ("Livreur", 1): ["A", "G", "A"], ("Livreur", 2): ["A", "H", "A"]}]

        # Solution irréalisable 4:
        # Manque un opérateur:
        self.sol_irr_5 = [{("Gestionnaire", 1): ["A", "B", "A"], ("Livreur", 1): ["A", "C", "D", "A"], ("Livreur", 2): ["A", "E", "F", "A"]},
                     {("Gestionnaire", 1): ["A", "A"], ("Livreur", 1): ["A", "G", "A"]}]

        # Solution irréalisable 5:
        # Opérateur ajouté:
        self.sol_irr_6 = [{("Gestionnaire", 1): ["A", "B", "A"], ("Livreur", 1): ["A", "D", "A"], ("Livreur", 2): ["A", "E", "F", "A"]},
                     {("Gestionnaire", 1): ["A", "A"], ("Livreur", 1): ["A", "G", "A"], ("Livreur", 2): ["A", "A"],  ("Livreur", 3): ["A", "A"]}]


    def test_validate(self):
        liste_sol_valider = [self.sol_res_1, self.sol_res_2, self.sol_irr_1, self.sol_irr_2,
                             self.sol_irr_3, self.sol_irr_4, self.sol_irr_5, self.sol_irr_6]

        liste_validations_theo = [True, True, False, False, False, False, False, False]

        for i, sol in enumerate(liste_sol_valider):
            self.assertEqual(validate(sol, self.parametres, self.liste_clees, self.liste_noeuds, self.data, self.temps_gestion_noeuds), liste_validations_theo[i])

    def test_evaluate(self):
        liste_sol_evaluer = [self.sol_res_1, self.sol_res_2]

        liste_evaluations_theo = [self.val_sol_res_1, self.val_sol_res_2]

        for i, sol in enumerate(liste_sol_evaluer):
            self.assertEqual(eval_solution(sol, self.liste_clees, self.parametres, self.data,
                                      self.temps_gestion_noeuds), liste_evaluations_theo[i])