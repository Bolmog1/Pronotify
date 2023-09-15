# COPYRIGHT BOLMOG
# FICHIER CREER LE 14 SEPTEMBRE 2023

# ------------------------------------ INITIALIZATION ------------------------------------

import discord
from discord.ext import tasks, commands
from texts import *
from tools import *
from config import token_bot

version_bot = 'En Dévleppoment pour 1.0'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


# ------------------------------------ CLASS(s) ------------------------------------


class SigninView(discord.ui.View):
    def __init__(self, message_id: int):
        super().__init__()
        self.message_id = message_id
        self.add_item(discord.ui.Button(label="RGPD", url='https://CNIL.fr'))

    # Bouton Accepter
    @discord.ui.button(label="Accepter", style=discord.ButtonStyle.green)  # Bouton 'Accepter'
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):  # L'utilisateur a appuyer
        await interaction.message.delete()
        await interaction.user.send(f"Ok ! Tu as accèpter le RGPD ! \n"
                                    f"maintenant on va vérifier que ton compte fonctionne !")

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


@tasks.loop(minutes=20)  # Lance des automatisation, s'éxecute toute les 20 minutes
async def my_task():
    pass


@commands.dm_only()
@bot.event
async def on_message(msg):
    if msg.channel.type is discord.ChannelType.private:  # Verifier d'être en DM
        if msg.content[0:15] == "Etablissement:(":
            # await msg.author.send("yo")
            await msg.author.send(RGPD_text, view=SigninView(int(msg.id)))


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
