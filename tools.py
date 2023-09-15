def extract(chaine):
    '''Extrait tout ce qui est dans les () et les return'''
    contenu_entre_parentheses = []
    en_parenthese = False
    mot = ""

    for caractere in chaine:
        if caractere == '(':
            en_parenthese = True
            mot = ""
        elif caractere == ')':
            en_parenthese = False
            if mot:
                contenu_entre_parentheses.append(mot)
            mot = ""
        elif en_parenthese:
            mot += caractere

    return contenu_entre_parentheses
