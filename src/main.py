import discord
from discord import app_commands
from PIL import Image

from image import ImageProcessor
from db_holder import Database
from helpers.const import UserData
from dsc_objects.modals import NewCard
from dsc_objects.client import Client
from config import get_config

config = get_config()
intents = discord.Intents.all()
client = Client(intents=intents)

database = Database(config['db_path'])
database.create_table()
image = ImageProcessor()

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})\n" + "=" * 47)

@client.tree.command()
@app_commands.describe(member="Пользователь", 
                       social_credits="Укажите очки рейтинга (+100/-37/+inf)")
async def csc(interaction: discord.Interaction, member: discord.Member=None, social_credits: str=""):
    if member is None:
        await interaction.response.send_message("Пользователь не указан", ephemeral=True)
        return
    if social_credits == "":
        await interaction.response.send_message("Социальный рейтинг не указан", ephemeral=True)
        return
    
    response = database.update_rep(member.id, social_credits)
    await interaction.response.send_message(response, ephemeral=True)


@client.tree.context_menu(name="Завести дело")
async def init_case(interaction: discord.Interaction, member: discord.Member):
    card: NewCard = NewCard()
    if database.user_exists(member.id):
        user_data: UserData = database.get_user_data(member.id, "")
        card.initialize_userdata(member.id, user_data, "Личное дело изменено")
        card.title = "Редактировать дело"
    else:
        card.initialize_id(member.id)
    await interaction.response.send_modal(card)


@client.tree.context_menu(name="Получить дело")
async def get_card(interaction: discord.Interaction, member: discord.Member):
    if not database.user_exists(member.id):
        await interaction.response.send_message("У пользователя пока что нет карточки", ephemeral=True)
        return
    data: UserData = database.get_user_data(member.id, f"{member.name}#{member.discriminator}")
    
    print("username:", data.name)
    file = image.draw_assets(data)
    f = discord.File(fp=file.filename())
    file.close()

    await interaction.response.send_message(file=f)

client.run(config['token'])

# TODO: check is user admin