def choix_methode():
    """Fonction permettant le choix de la méthode à utiliser pour résoudre le problème"""
    check = False
    while check is False:
        print("Méthodes ou heuristiques disponibles : ")
        print("1: Méthode aléatoire")
        print("2: Heuristique de Clarke & Wright modifié")
        methode = input("Entrer le numéro de la méthode à utiliser: ")
        if methode in ["1", "2"]:
            return methode
        else:
            print("S'il vous plaît entrer un numéro de méthode valide.")
