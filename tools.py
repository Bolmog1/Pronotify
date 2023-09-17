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


def get_user_json(fichier):
    import json
    with open(fichier, 'r') as f:
        data = json.load(f)
    return data


def change_user_json(id, para, value):
    import json
    with open(f'{id}.json', 'r') as f:
        data = json.load(f)
    f.close()
    data[para] = value
    with open(f'{id}.json', 'w') as f:
        json.dump(data, f)
    f.close()


def fichiers_user():
    import os
    from config import path_user_files
    fichiers_json = []
    for dossier_racine, sous_dossiers, fichiers in os.walk(path_user_files):
        for fichier in fichiers:
            if fichier.endswith(".json"):
                print(fichier)
                chemin_complet = os.path.join(dossier_racine, fichier)
                fichiers_json.append(chemin_complet)

    return fichiers_json


# Fonction pour créer un fichier JSON avec un ID donné
def create_user_file(id, contenu):
    import json
    try:
        donnees = contenu

        with open(f'{id}.json', 'w') as fichier:
            json.dump(donnees, fichier)

        print(f"Fichier JSON '{id}' créé avec succès avec l'ID {id}.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
