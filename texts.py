signin_text = "Premièrement, hello :wave: \n\n"\
        "Ensuite pour recevoir des notifications, il faut ton mot de passe Pronote /:\n"\
        "Donc, pour la sécurité de ton compte, on n'enregistrera JAMAIS ton mot de passe.\n\n"\
        "**Mais donc on fait comment?**\n\n"\
        "En mettant ton Mot de passe ici ! (oui ça paraît stupide au début...) mais ici ton MdP est à l'abris des " \
        "regards, accesible pour le programme t'envoyer des notification et pour toi le supprimer si tu ne veux plus " \
        "que ton MdP ne soit afficher quelque part !\n\n"\
        "Si tu est toujours partant (car ça peut être sujet à réfléxion) suis l'exemple envoyer ci-joint et remplace " \
        "le à ta sauce avant de le renvoyer ! (Tips: Tu peux copier/coller le templates qu'est le message " \
        "ci-joint avec '...'>'Copier le texte':arrow_down:)"

template_text = "Etablissement:(<https://demo.index-education.net/pronote/eleve.html>)\n"\
                "Identifiant:(demonstration)\n"\
                "MotDePasse:||(pronotevs)||\n"

RGPD_text = "**On y est presque ! (Vraiment)**\n\n"\
        "> Cependant, pour faire fonctionner correctement le bot et fournir un service optimal, nous avons besoin " \
        "d'enregistrer quelques infos\n"\
        "> *(qui sont ton ID Discord pour que le programme sache qui il a a notifier, t'as moyennes afin de te la " \
        "comparer au cours du temps et te notifier de son évolution et enfin de t'es préférences en terme de " \
        "notifications)*\n" \
        "> tu peux en savoir plus en cliquant plus bas sur 'RGPD' !\n\n"\
        "> Par la suite fait `/rgpd` afin d'accéder a différentes options lié au [RGPD](<https://fr.wikipedia.org/" \
        "wiki/Règlement_général_sur_la_protection_des_données>) dont la suppression des " \
        "'données personnel' *(c'est juste t'a moyennes mais c'est pas moi qui fait les lois :man_shrugging:‍️)*\n\n"\
        "- La question est donc accepte tu qu'on enregistre ces quelques données ?"

bienvenue_text = "Super !\n**Tu sera désormais notifier des dernières actualité de ton compte Pronote !**" \
                 "\nTu peux modifier t'es préférences en termes de notifications avec `/parametre` !"


def preference_text(data):

        text = ":bell: Tu peut modifier t'es préférences ici ! \n " \
               "voici t'es préférences actuellement :point_down: :\n\n> :bar_chart: "

        if data["NotificationMoyenne"]:
                text += "Notification de moyenne : **Activée**"
        else:
                text += "Notification de moyenne : **Désactivée**"

        text += "\n> *Tu recevra une notification à chaque modification de ta moyenne !*\n\n> :no_pedestrians: "

        if data["NotificationAbsence"]:
                text += "Notification d'absence : **Activée**"
        else:
                text += "Notification d'absence : **Désactivée**"

        text += "\n> *Tu recevra une notification à chaque fois qu'une absence sera renseigner*\n\n> :pencil: "

        if data["NotificationNotes"]:
                text += "Notification de Note : **Activée**"
        else:
                text += "Notification de Note : **Désactivée**"

        text += "\n> *Tu recevra une notifications à chaque fois qu'une nouvelle note sera renseigner !*\n\n> :books: "

        if data["NotificationsDevoirs"]:
                text += "Notification de devoirs : **Activée**"
        else:
                text += "Notification de devoirs : **Désactivée**"

        text += "\n> *Tu recevra tous les soirs un résumé des devoirs pour le lendemain !*\n\n> :loudspeaker: "

        if data["NotificationsInfos"]:
                text += "Notification Infos/Sondages : **Activée**"
        else:
                text += "Notification Infos/Sondages : **Désactivée**"

        text += "\n> *Tu recevra tous les soirs un résumé des informations et sondages de la journée*\n"

        return text


RGPD_view_text = "C'est ici que tu gère t'es données personnel :point_down: !\n\n" \
                 "- Tu peut télécharger t'es données !\n*Tu auras alors un aperçu de tous ce qu'on sait sur toi" \
                 "(pas grand chose je te rassure)*\n\n" \
                 "- Tu peut supprimer t'es données !\n*On effacera alors toutes les informations a ton propos !*\n\n" \
                 "- Tu peut aller voir (ou revoir) notre site avec notre politiques de confidentialité !"

Credit_text = "Merci c'est très gentil de penser aux gens qui fabrique et code ce que tu utilise au quotidien !\n"\
              "D'abord quelque remerciement aux personnes qui ont codées les modules que j'utilise !\n"\
              "- Merci au module **[PronotePy](<https://github.com/bain3/pronotepy>)**\n" \
              "- Merci au module **[DiscordPy](<https://discordpy.readthedocs.io>)**\n" \
              "Et enfin, moi ! *[Bolmog](https://github.com/Bolmog1)*, pour vous servir !\n" \
              "Mais surtout merci a vous d'utiliser le bot !"
