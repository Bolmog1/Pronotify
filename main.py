# COPYRIGHT BOLMOG
# FICHIER CREER LE 14 SEPTEMBRE 2023

# ------------------------------------ INITIALIZATION ------------------------------------

import discord
from discord.ext import tasks, commands
from config import token_bot, path_user_files
from texts import *
from tools import *
from pronote import *
import time

version_bot = 'En Dévleppoment pour 1.0'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


# ------------------------------------ CLASS(s) ------------------------------------


class SigninView(discord.ui.View):
    def __init__(self, message_id: int, message_content: str):
        super().__init__()
        self.message_id = message_id
        self.message_content = message_content
        self.add_item(discord.ui.Button(label="RGPD", url='https://bolmog1.github.io/Pronotify/#RGPD'))  # Bouton RGPD

    # Bouton Accepter
    @discord.ui.button(label="Accepter", style=discord.ButtonStyle.green)  # Bouton 'Accepter'
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):  # L'utilisateur a appuyer
        await interaction.message.delete()
        await interaction.user.send(f"Ok ! Tu as accèpter le RGPD ! \n"
                                    f"maintenant on va vérifier que ton compte fonctionne !")
        detail = extract(self.message_content)
        result = user_test_account(detail[0], detail[1], detail[2])
        if result[0]:
            create_user_file(interaction.user.id, {"ID":  interaction.user.id, "moyenne": result[2],
                                                   "idMessageMdP": self.message_id,
                                                   "PreviousConnectionNotFailed": True,
                                                   "NotificationMoyenne": True, "NotificationAbsence": True,
                                                   "NotificationNotes": True, "NotificationsDevoirs": True,
                                                   "NotificationsInfos":  True})
            await interaction.user.send(f"Ton compte fonctionne ! Bonjour **{result[1]}** !\n{bienvenue_text}")
            log(f"{interaction.user.id} ({interaction.user.display_name}) a désormais les notifications Discord")
        else:  # Il y'a une erreur
            if result[2] == 404:  # L'utilisateur à probablement donné un mauvais mdp/id
                await interaction.user.send(f"C'est génant :sweat_smile:, il y'a une erreur !"
                                            f"\nEs-tu sûr de ne pas avoir fait d'erreur ?"
                                            f"\nSi cela recommence a nouveaux, contact le programmeur.")
            else:  # Le module Pronotepy a eu un problème (mauvais signe)
                await interaction.user.send(f"C'est génant :sweat_smile:, il y'a une erreur !"
                                            f"\nElle ne provient surement pas de toi !"
                                            f"\nLe serveur rencontre un problème. Les gestionnaires ont-été notifié.")

    # Bouton Refuser
    @discord.ui.button(label="Refuser", style=discord.ButtonStyle.red)  # Bouton 'Refuser'
    async def refuse(self, interaction: discord.Interaction, button: discord.ui.Button):  # L'utilisateur a appuyer
        await interaction.message.delete()
        await interaction.user.send("Tu as refusé, ok ! Je comprend ! Au revoir (j'imagine)")


class PreferenceView(discord.ui.View):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    @discord.ui.button(label="Notif Moy", style=discord.ButtonStyle.blurple)
    async def moyenne(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = get_user_json(str(interaction.user.id))
        if data['NotificationMoyenne']:
            change_user_json(interaction.user.id, 'NotificationMoyenne', False)
            await interaction.response.send_message("Notification de moyenne **Désactiver**", ephemeral=True, delete_after=5)
        else:
            change_user_json(interaction.user.id, 'NotificationMoyenne', True)
            await interaction.response.send_message("Notification de moyenne **Activée**", ephemeral=True, delete_after=5)
        data = get_user_json(str(interaction.user.id))
        await interaction.message.edit(content=preference_text(data))

    @discord.ui.button(label="Notif Abs", style=discord.ButtonStyle.blurple)
    async def absence(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = get_user_json(str(interaction.user.id))
        if data['NotificationAbsence']:
            change_user_json(interaction.user.id, 'NotificationAbsence', False)
            await interaction.response.send_message("Notification d'absence **Désactiver**", ephemeral=True, delete_after=5)
        else:
            change_user_json(interaction.user.id, 'NotificationAbsence', True)
            await interaction.response.send_message("Notification d'absence **Activée**", ephemeral=True, delete_after=5)
        data = get_user_json(str(interaction.user.id))
        await interaction.message.edit(content=preference_text(data))

    @discord.ui.button(label="Notif Note", style=discord.ButtonStyle.blurple)
    async def notes(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = get_user_json(str(interaction.user.id))
        if data['NotificationNotes']:
            change_user_json(interaction.user.id, 'NotificationNotes', False)
            await interaction.response.send_message("Notification de Note **Désactiver**", ephemeral=True, delete_after=5)
        else:
            change_user_json(interaction.user.id, 'NotificationNotes', True)
            await interaction.response.send_message("Notification de Note **Activée**", ephemeral=True, delete_after=5)
        data = get_user_json(str(interaction.user.id))
        await interaction.message.edit(content=preference_text(data))

    @discord.ui.button(label="Notif Devoir", style=discord.ButtonStyle.blurple)
    async def note(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = get_user_json(str(interaction.user.id))
        if data['NotificationsDevoirs']:
            change_user_json(interaction.user.id, 'NotificationsDevoirs', False)
            await interaction.response.send_message("Notification des devoirs **Désactiver**", ephemeral=True, delete_after=5)
        else:
            change_user_json(interaction.user.id, 'NotificationsDevoirs', True)
            await interaction.response.send_message("Notification des devoirs **Activée**", ephemeral=True, delete_after=5)
        data = get_user_json(str(interaction.user.id))
        await interaction.message.edit(content=preference_text(data))

    @discord.ui.button(label="Notif info", style=discord.ButtonStyle.blurple)
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = get_user_json(str(interaction.user.id))
        if data['NotificationsInfos']:
            change_user_json(interaction.user.id, 'NotificationsInfos', False)
            await interaction.response.send_message("Notification d'info **Désactiver**", ephemeral=True, delete_after=5)
        else:
            change_user_json(interaction.user.id, 'NotificationsInfos', True)
            await interaction.response.send_message("Notification d'info **Activée**", ephemeral=True, delete_after=5)
        data = get_user_json(str(interaction.user.id))
        await interaction.message.edit(content=preference_text(data))


class RGPDview(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Politique des donnèes", url='https://bolmog1.github.io/Pronotify/#RGPD'))

    @discord.ui.button(label="Télécharger mes données", style=discord.ButtonStyle.grey)
    async def download(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message(file=discord.File(f"{interaction.user.id}.json"))
        except Exception as e:
            log(f"Erreur RGPD de {interaction.user.id} lors d'envoie du fichier : {e}")
            await interaction.response.send_message("Une erreur est survenue pendant l'envoie de ton fichier.\n"
                                           "es-tu inscrit aux notifications ?")

    @discord.ui.button(label="Supprimer mes données", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            from os import remove
            remove(f"{interaction.user.id}.json")
            await interaction.response.send_message("T'es données ont était supprimer. bye :wave: !")
        except Exception as e:
            log(e)
            await interaction.response.send_message("Quelque chose à mal tournée ici...")

# ------------------------------------ FONCTIONS ------------------------------------


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()  # Synchronise les commandes
        print(len(synced))
        log("Bot lancé !")
    except Exception as e:
        print(e)
        log(e)
    my_task.start()


@bot.event
async def on_error(event):
    print('error', event)


@tasks.loop(minutes=20)  # Lance des automatisation, s'éxecute toute les 20 minutes
async def my_task():
    utilisateurs = fichiers_user()
    for utilisateur in utilisateurs:
        data = get_user_json(utilisateur)
        user = await bot.fetch_user(data['ID'])  # Rechercher l'objet user
        msg = await user.fetch_message(data["idMessageMdP"])  # Rechercher le message Mdp/id
        detail = extract(msg.content)
        etab, id, mdp = detail[0], detail[1], detail[2]
        if etab[0] == '<':
            etab = etab[1:-1]
        try:
            client = pronotepy.Client(etab, username=id, password=mdp)
            if client.logged_in:
                if data["NotificationMoyenne"]: # ----- MOYENNE -----
                    notes = client.current_period  # Récupération des notes du Trimestre
                    moyennes_notes = notes.averages  # Récupérations des moyennes des notes
                    moyenne_eleve = []
                    for moyenne in moyennes_notes:
                        moyenne_eleve.append(float(moyenne.student.replace(',', '.')))
                    moyenne_general = None
                    if len(moyenne_eleve) != 0:
                        moyenne_general = round(sum(moyenne_eleve) / len(moyenne_eleve), 2)
                    if data['moyenne'] == None and moyenne_general != None:
                        change_user_json(user.id, 'moyenne', moyenne_general)
                    if moyenne_general != None and moyenne_general > data['moyenne']:
                        change_user_json(user.id, 'moyenne', moyenne_general)
                        deco = discord.Embed(title=':bell: Notification Moyenne Général !',
                                             description=f":arrow_up_small: de {data['moyenne']} à {moyenne_general}",
                                             colour=0x3498db)
                        await user.send(embed=deco)
                    elif data['moyenne'] != None and moyenne_general < data['moyenne']:
                        change_user_json(user.id, 'moyenne', moyenne_general)
                        deco = discord.Embed(title=':bell: Notification Moyenne Général !',
                                             description=f":arrow_down_small: de {data['moyenne']} à {moyenne_general}",
                                             colour=0x3498db)
                        await user.send(embed=deco)
                if data["NotificationNotes"]:  # ----- NOTES -----
                    t = time.localtime()
                    if t.tm_hour == 18 and t.tm_min < 20:  # S'il est 18h
                        nouvelles_notes = []
                        periods = client.periods  # Obtenir les Notes
                        for period in periods:
                            for grade in period.grades:
                                if grade.date == f'{t.tm_year}-{t.tm_mon}-{t.tm_mday}':
                                    nouvelles_notes.append(f'__Nouvelle note__: {grade.grade}/{grade.out_of} en '
                                                           f'{grade.subject} *(Coeff {grade.coefficient})*')
                        if len(nouvelles_notes) > 0:
                            display = ""
                            for info in nouvelles_notes:
                                display += f"{info}\n"
                            deco = discord.Embed(title=':bell: Notification Notes !',
                                                 description=display, colour=0x27ae60)
                            await user.send(embed=deco)
                if data["NotificationsInfos"]:  # ----- Infos -----
                    t = time.localtime()
                    if t.tm_mon < 10:
                        mois = f'0{t.tm_mon}'
                    else:
                        mois = t.tm_mon
                    if t.tm_min > 40:
                        nouvelles_infos = []
                        infos = client.information_and_surveys()  # Checks les infos
                        for info in infos:
                            if str(info.creation_date) == f"{t.tm_year}-{mois}-{t.tm_mday} {t.tm_hour}":
                                if info.read:
                                    nouvelles_infos.append(f'*(info déjà lu)*~~{info.title} par {info.author}~~ le '
                                                           f'{info.start_date}')
                                else:
                                    nouvelles_infos.append(f'**Nouvelle Info:**{info.title} par {info.author}')
                        disc_s = client.discussions()  # Check les disscussions (no jugement sur l'ortho)
                        if t.tm_hour == 18 and t.tm_min < 20:
                            for disc in disc_s:
                                if str(disc.date)[0:10] == f"{t.tm_year}-{mois}-{t.tm_mday}":
                                    if disc.unread:
                                        nouvelles_infos.append(f'__Nouvelle disscussion__: {disc.subject} '
                                                               f'*par {disc.creator}*')
                                    else:
                                        nouvelles_infos.append(f'*(disscussion déjà lu)*: {disc.subject} '
                                                               f'*par {disc.creator}*')
                        if len(nouvelles_infos) > 0:
                            display = ""
                            for info in nouvelles_infos:
                                display += f"{info}\n"
                            deco = discord.Embed(title=':bell: Notification Infos/Sondages !',
                                                 description=display, colour=0x9b59b6)
                            await user.send(embed=deco)
                if data['NotificationAbsence']:
                    nouvelles_infos = []
                    t = time.localtime()
                    if t.tm_hour == 18 and t.tm_min < 20:
                        import datetime
                        trimestre = client.current_period
                        absences = trimestre.absences
                        for absence in absences:
                            if absence.from_date == datetime.date.today():
                                nouvelles_infos.append(f"Absence aujourd'hui pendant {absence.hours}")
                    if len(nouvelles_infos) > 0:
                        display = ""
                        for info in nouvelles_infos:
                            display += f"{info}\n"
                        deco = discord.Embed(title=':bell: Notification Absences !',
                                             description=display, colour=0xe74c3c)
                        await user.send(embed=deco)
                if data['NotificationsDevoirs']:
                    nouvelles_infos = []
                    t = time.localtime()
                    if t.tm_hour == 18 and t.tm_min < 20:
                        import datetime
                        devoirs = client.homework(datetime.date.today())
                        for devoir in devoirs:
                            if str(devoir.date) == f"{t.tm_year}-{mois}-{t.tm_wday}":
                                if devoir.done:
                                    nouvelles_infos.append(f"~~*{devoir.description}* en **{devoir.subject.name}**~~"
                                                           f":heavy_check_mark:")
                                else:
                                    nouvelles_infos.append(f"*{devoir.description}* en **{devoir.subject.name}**")
                    if len(nouvelles_infos) > 0:
                        display = ""
                        for info in nouvelles_infos:
                            display += f"{info}\n"
                        deco = discord.Embed(title=':bell: Notification des Devoirs pour demain !',
                                             description=display, colour=0xf1c40f)
                        await user.send(embed=deco)
                change_user_json(user.id, 'PreviousConnectionNotFailed', True)
        except Exception as e:
            if data["PreviousConnectionNotFailed"]:
                log(f"Une erreur est survenue avec {user.id} ({user.id}), pronote : {e}")
                await user.send('Une erreur est survenu durant la connexion a ton compte !')
                change_user_json(user.id, 'PreviousConnectionNotFailed', False)


@commands.dm_only()
@bot.event
async def on_message(msg):
    if msg.channel.type is discord.ChannelType.private:  # Verifier d'être en DM
        if msg.content[0:15] == "Etablissement:(":
            if f"{msg.author.id}.json" in fichiers_user():
                await msg.author.send("Evite de mettre t'es MdP en double... Apres, fait ce que tu veut !")
            else:
                await msg.author.send(RGPD_text, view=SigninView(int(msg.id), str(msg.content)))
        elif msg.author.id == 696633499305771028:
            if msg.content == "shutdown":
                await msg.author.send("Arret du bot")
                print("Bot Shutdown by user")
                log(f"Bot arrêter par {msg.author.id}")
                await bot.close()


# ------------------------------------ COMMANDS ------------------------------------


@bot.tree.command(name='parametres', description="Te permet de modifier t'es préférences")
async def parametres(interaction: discord.Interaction):
    if f"{interaction.user.id}.json" in fichiers_user():
        await interaction.response.send_message(preference_text(get_user_json(interaction.user.id)), view=PreferenceView(interaction))
    else:
        await interaction.response.send_message("Pour changer t'es préférence en matière de Notifications il faudrait"
                                                "d'abord y être inscrit pas vrai ? -> `/signin` pour en savoir + !")


@bot.tree.command(name='credit', description="credit")
async def credit(interaction: discord.Interaction):
    await interaction.response.send_message(Credit_text)


@bot.tree.command(name='rgpd', description="Te permet d'acceder au réglage concernant le RGPD")
async def rgpd(interaction: discord.Interaction):
    if f"{interaction.user.id}.json" in fichiers_user():
        await interaction.response.send_message(RGPD_view_text, view=RGPDview())
    else:
        await interaction.response.send_message("Pour changer t'es préférence en matière de données personnel il "
                                                "faudrait d'abord y être inscrit pas vrai ? -> "
                                                "`/signin` pour en savoir + !")


@bot.tree.command(name='version', description='Renvoie la version du bot !')
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(f"Actuellement en version : __{version_bot}__ !")


@bot.tree.command(name='signin', description='Inscrit toi au notifications')
async def signin(interaction: discord.Interaction):
    if interaction.channel.type is discord.ChannelType.private:  # Vérifie d'être en DM
        if f"{interaction.user.id}.json" in fichiers_user():
            await interaction.response.send_message("Je te connais toi !")
        else:
            await interaction.response.send_message(signin_text)
            await interaction.user.send(template_text)
    else:
        await interaction.response.send_message("Continuons cette discussion en privé ?\n"
                                                "*Tu ne veux pas montrer t'es secrets à tous le monde ?*",
                                                ephemeral=True)


# ------------------------------------ RUN ------------------------------------


bot.run(token_bot)
