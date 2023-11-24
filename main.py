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
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


@client.tree.command()
@app_commands.describe(member="Member to describe", 
                       social_points="Add social points (+100/-37.428/+inf)")
async def rep(interaction: discord.Interaction, member: discord.Member=None, social_points: str=""):
    if member is None:
        await interaction.response.send_message("User is not specified", ephemeral=True)
        return
    if social_points == "":
        await interaction.response.send_message("Social points are not specified", ephemeral=True)
        return
    
    responce = database.update_rep(member.id, social_points)
    await interaction.response.send_message(responce, ephemeral=True)


@client.tree.context_menu(name="Завести дело")
async def init(interaction: discord.Interaction, member: discord.Member):
    card: NewCard = NewCard()
    if database.user_exists(member.id):
        user_data: UserData = database.get_data(member.id)
        print(user_data)
        card.initialize_userdata(user_data)
        card.title = "Редактировать дело"
    else:
        card.initialize_id(member.id)
    # TODO: card.social_points.fdsfsdk  --  edit if user exists
    await interaction.response.send_modal(card)


@client.tree.context_menu(name="Получить дело")
async def card(interaction: discord.Interaction, member: discord.Member):
    embed = discord.Embed(title=f"{member.name}#{member.discriminator}", description=f"ID: {member.id}")
    embed.add_field(name="Important info~", value="Info!")
    await interaction.response.send_message(embed=embed)


client.run(Bot.TOKEN)

# TODO: check is user admin
