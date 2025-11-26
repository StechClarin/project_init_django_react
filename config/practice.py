def compteurmot(expression):
    compteur = {}                # 1. Dictionnaire vide
    mots = expression.split()    # 2. Transformer en liste
    
    # Boucle sur chaque mot dans la liste
    for mot in mots:
        # 4. Vérifier si le mot est DÉJÀ une clé dans le dictionnaire
        if mot in compteur:
            # 5. Si oui, incrémenter sa valeur
            compteur[mot] += 1
        else:
            # 6. Si non, créer la clé avec la valeur 1
            compteur[mot] = 1
            
    return compteur # Retourner le dictionnaire final

if __name__ == "__main__":
    expression = "bonjour bonjour tout le monde"
    
    # 1. Appeler la fonction UNE SEULE FOIS
    resultats = compteurmot(expression)
    
    # 2. Boucler sur le DICTIONNAIRE résultat (pas sur la liste de mots)
    # .items() te donne la clé (mot) et la valeur (compte)
    for mot, compte in resultats.items():
        print(f"{mot} : {compte}")