def choix_methode():
    """Fonction permettant le choix de la méthode à utiliser pour résoudre le problème"""
    check = False
    while check is False:
        print("\nMéthodes ou heuristiques disponibles : ")
        print("1: Méthode aléatoire")
        print("2: Heuristique de Clarke & Wright modifié")
        methode = input("\nEntrer le numéro de la méthode à utiliser: ")
        if methode in ["1", "2"]:
            return methode
        else:
            print("\nVeuillez entrer un numéro de méthode valide.")
