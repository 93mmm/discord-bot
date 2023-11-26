import discord
from discord import app_commands

from src.db_holder import *
from src.const import Bot 
from src.forms.modals import NewCard
from src.forms.client import Client


intents = discord.Intents.all()
client = Client(intents=intents)

database = Database(Consts.PATH)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})\n---------")


@client.tree.command()
@app_commands.describe(member="Пользователь", 
                       social_points="Укажите очки рейтинга (+100/-37/+inf)")
async def rep(interaction: discord.Interaction, member: discord.Member=None, social_points: str=""):
    if member is None:
        await interaction.response.send_message("Пользователь не указан", ephemeral=True)
        return
    if social_points == "":
        await interaction.response.send_message("Социальный рейтинг не указан", ephemeral=True)
        return
    
    responce = database.update_rep(member.id, social_points)
    await interaction.response.send_message(responce, ephemeral=True)


@client.tree.context_menu(name="Завести дело")
async def init(interaction: discord.Interaction, member: discord.Member):
    card: NewCard = NewCard()
    if database.user_exists(member.id):
        user_data: UserData = database.get_user_data(member.id)
        card.initialize_userdata(member.id, user_data, "Личное дело изменено")
        card.title = "Редактировать дело"
    else:
        card.initialize_id(member.id)
    await interaction.response.send_modal(card)


@client.tree.context_menu(name="Получить дело")
async def card(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=f"{member.name}#{member.discriminator}", description=f"ID: {member.id}")
    embed.add_field(name="Important info~", value="Info!")
    await interaction.response.send_message(embed=embed)


client.run(Bot.TOKEN)

# TODO: check is user admin
# TODO: localize answers in russian language