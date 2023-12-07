import discord
from discord import app_commands

from PIL import Image

from src.image import ImageProcessor
from src.db_holder import Database
from src.helpers.const import Bot, UserData
from src.helpers.helpers import soc_rating_in_form
from src.dsc_objects.modals import NewCard
from src.dsc_objects.client import Client


intents = discord.Intents.all()
client = Client(intents=intents)

database = Database(Bot.DB_PATH)
image = ImageProcessor()

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
    if not database.user_exists(member.id):
        await interaction.response.send_message("У пользователя пока что нет карточки", ephemeral=True)
        return
    data: UserData = database.get_user_data(member.id, f"{member.name}#{member.discriminator}")

    embed = discord.Embed(title=f"{member.name}#{member.discriminator}", description=f"ID: {member.id}")
    embed.add_field(name="Очки социального рейтинга:", value=soc_rating_in_form(data.social_points, data.is_infinity))
    embed.add_field(name="Важные приметы:", value=data.special_signs)
    embed.add_field(name="Награды:", value=" ".join(data.photo_paths))
    
    file = image.draw_assets("User!")
    f = discord.File(fp=file.filename())
    file.close()
    await interaction.response.send_message(embed=embed, file=f)


client.run(Bot.TOKEN)

# TODO: check is user admin