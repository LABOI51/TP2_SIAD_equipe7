def choix_methode():
    """Fonction permettant le choix de la méthode à utiliser pour résoudre le problème et le temps de résolution."""
    check = False
    while check is False:
        print("\nMéthodes ou heuristiques disponibles : ")
        print("1: Méthode aléatoire")
        print("2: Heuristique de Clarke & Wright modifié")
        methode = input("\nEntrer le numéro de la méthode à utiliser: ")
        if methode in ["1", "2"]:
             check = True
        else:
            print("\nVeuillez entrer un numéro de méthode valide.")

    check = False
    while check is False:
        temps_max = input("\nVeuillez entrer le temps de résolution (en secondes) à utiliser: ")
        try:
            if float(temps_max) <= 28800 and float(temps_max) >= 0:
                return methode, float(temps_max)
            else:
                print("\nLe temps entré dépasse le maximum de 8h (28 800 secondes) ou est négatif. S'il vous-plaît "
                      "entrer une valeur entre 0 et 28 800 secondes.")

        except TypeError:
            print("\n L'entrée n'est pas valide. S'il vous plait réessayer.")

