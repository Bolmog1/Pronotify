import pronotepy


def user_test_account(etab, id, mdp):
    if etab[0] == '<':
        etab = etab[1:-1]
    try:
        client = pronotepy.Client(etab, username=id, password=mdp)
        if client.logged_in:
            notes = client.current_period  # Récupération des notes du Trimestre
            moyennes_notes = notes.averages  # Récupérations des moyennes des notes
            moyenne_eleve = []
            for moyenne in moyennes_notes:
                moyenne_eleve.append(float(moyenne.student.replace(',', '.')))
            moyenne_general = round(sum(moyenne_eleve) / len(moyenne_eleve), 2)  # Calcul de la moyennes général

            nom_utilisateur = client.info.name
            return True, nom_utilisateur, moyenne_general
        else:
            return False, 'Error', 500
    except:
        return False, 'Error', 404