# COPYRIGHT BOLMOG
# FICHIER CREER LE 26 SEPTEMBRE 2023

import discord
from pronote import *
from config import token_bot, path_user_files
from discord.ext import commands
from tools import *
import time

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    t = time.localtime()
    if t.tm_mon < 10:
        mois = f'0{t.tm_mon}'
    else:
        mois = t.tm_mon
    channel = bot.get_channel(1155904681671925840)
    await channel.send(f"{t.tm_year}-{mois}-{t.tm_mday} / Executution quotidienne")
    utilisateurs = fichiers_user()
    for utilisateur in utilisateurs:
        utilisateur = utilisateur[:-5]
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
                if data["NotificationMoyenne"]:  # ----- MOYENNE -----
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
                    nouvelles_notes = []
                    periods = client.periods  # Obtenir les Notes
                    for period in periods:
                        for grade in period.grades:
                            if grade.date == f'{t.tm_year}-{mois}-{t.tm_mday}':
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
                    nouvelles_infos = []
                    infos = client.information_and_surveys()  # Checks les infos
                    for info in infos:
                        print(info.creation_date, info.title, info.start_date)
                        print(str(info.creation_date)[:10] == f"{t.tm_year}-{mois}-{t.tm_mday}")
                        if str(info.creation_date)[:10] == f"{t.tm_year}-{mois}-{t.tm_mday}":
                            if info.read:
                                nouvelles_infos.append(f'*(info déjà lu)*~~ {info.title} par {info.author}~~ \nle '
                                                       f'{info.start_date}')
                            else:
                                nouvelles_infos.append(f'**Nouvelle Info:**{info.title} \npar {info.author}')
                    disc_s = client.discussions()  # Check les disscussions (no jugement sur l'ortho)
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
                    import datetime
                    devoirs = client.homework(datetime.date.today())
                    for devoir in devoirs:
                        if str(devoir.date) == f"{t.tm_year}-{mois}-{t.tm_mday + 1}":
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
            print(e)
            if data["PreviousConnectionNotFailed"]:
                log(f"Une erreur est survenue avec {user.id} ({user.id}), pronote : {e}")
                await user.send('Une erreur est survenu durant la connexion a ton compte !')
                change_user_json(user.id, 'PreviousConnectionNotFailed', False)
        await bot.close()

bot.run(token_bot)