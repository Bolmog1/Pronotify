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
        self.add_item(discord.ui.Button(label="RGPD", url='https://CNIL.fr'))  # Bouton RGPD

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


# ------------------------------------ FONCTIONS ------------------------------------


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()  # Synchronise les commandes
        print(len(synced))
    except Exception as e:
        print(e)
    await my_task()


@tasks.loop(minutes=20)  # Lance des automatisation, s'éxecute toute les 20 minutes
async def my_task():
    utilisateurs = fichiers_user()
    for utilisateur in utilisateurs:
        data = get_user_json(utilisateur)
        user = await bot.fetch_user(data['ID'])  # Rechercher l'objet user
        msg = await user.fetch_message(data["idMessageMdP"])  # Rechercher le message Mdp/id
        detail = extract(msg.content)
        actualisation_pronote(detail[0], detail[1], detail[2], data)
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
                    moyenne_general = round(sum(moyenne_eleve) / len(moyenne_eleve), 2)  # Calcul de la moyennes général
                    if moyenne_general > data['moyenne']:
                        deco = discord.Embed(title=':bell: Notification Moyenne Général !',
                                             description=f":arrow_up_small: de {data['moyenne']} à {moyenne_general}",
                                             colour=0x3498db)
                        await user.send(embed=deco)
                    elif moyenne_general < data['moyenne']:
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
                if data["NotificationsInfos"]:
                    t = time.localtime()
                    if t.tm_min > 40:
                        nouvelles_infos = []
                        infos = client.information_and_surveys()  # Checks les infos
                        for info in infos:
                            if str(info.creation_date) == f"{t.tm_year}-{t.tm_mon}-{t.tm_mday} {t.tm_hour}":
                                if info.read:
                                    nouvelles_infos.append(f'*(info déjà lu)*~~{info.title} par {info.author}~~ le '
                                                           f'{info.start_date}')
                                else:
                                    nouvelles_infos.append(f'**Nouvelle Info:**{info.title} par {info.author}')
                        disc_s = client.discussions()  # Check les disscussions (no jugement sur l'ortho)
                        if t.tm_hour == 18 and t.tm_min < 20:
                            for disc in disc_s:
                                if str(disc.date)[0:10] == f"{t.tm_year}-{t.tm_mon}-{t.tm_mday}":
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
                if data['']:  # CONTINUER ICI
                    pass
        except:
            pass


@commands.dm_only()
@bot.event
async def on_message(msg):
    if msg.channel.type is discord.ChannelType.private:  # Verifier d'être en DM
        if msg.content[0:15] == "Etablissement:(":
            # await msg.author.send("yo")
            await msg.author.send(RGPD_text, view=SigninView(int(msg.id), str(msg.content)))


# ------------------------------------ COMMANDS ------------------------------------


@bot.tree.command(name='version', description='Renvoie la version du bot !')
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(f"Actuellement en version : __{version_bot}__ !")


@bot.tree.command(name='signin', description='Inscrit toi au notifications')
async def signin(interaction: discord.Interaction):
    if interaction.channel.type is discord.ChannelType.private:  # Vérifie d'être en DM
        await interaction.response.send_message(signin_text)
        await interaction.user.send(template_text)
    else:
        await interaction.response.send_message("Continuons cette discussion en privé ?\n"
                                                "*Tu ne veux pas montrer t'es secrets à tous le monde ?*",
                                                ephemeral=True)


# ------------------------------------ RUN ------------------------------------


bot.run(token_bot)
