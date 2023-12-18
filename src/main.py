import discord as ds

from database import Database
from helpers import User, get_errmsg_rep
from image import ImgProcessor
from constants import PATHS, CONFIG
from forms.modals import NewCard, ExistingCard
from forms.dropdown import DropdownView
from forms.client import Client


client: Client = Client(intents=ds.Intents.all())
db: Database = Database(PATHS["database"])
imgage_processor: ImgProcessor = ImgProcessor()


@client.event
async def on_ready():
    print(f"Logged in as {client.user} "
          f"(ID: {client.user.id})\n---------")


@client.tree.command()
@ds.app_commands.describe(member="Пользователь",
                          social_credits="Очки рейтинга (+100/-37/etc)")
async def rep(interaction: ds.Interaction,
              member: ds.Member=None,
              social_credits: str=""):
    errmsg: str = get_errmsg_rep(interaction.user.id,
                                 member,
                                 social_credits,
                                 db)
    if errmsg != "":
        await interaction.response.send_message(errmsg, ephemeral=True)
        return

    db.update_rep(member.id, int(social_credits))
    responce: str = f"Эээ, {member.mention}, тебе " \
                    f"{interaction.user.mention} репутацию повысил"
    await interaction.response.send_message(responce)


@client.tree.context_menu(name="Дело")
async def init(interaction: ds.Interaction, member: ds.Member):
    usr: User = db.get_user(member.id)
    if db.user_exists(member.id):
        card: ExistingCard = ExistingCard()
    else:
        card: NewCard = NewCard()
    card.initialize(usr)

    await interaction.response.send_modal(card)


@client.tree.context_menu(name="Получить дело")
async def get(interaction: ds.Interaction, member: ds.Member):
    if not db.user_exists(member.id):
        await interaction.response.send_message("У пользователя "
                                                "пока что нет карточки",
                                                ephemeral=True)
        return
    data: User = db.get_user(member.id)

    processed = imgage_processor.draw_assets(data,
                                             f"{member.name}#"
                                             f"{member.discriminator}")
    uploaded_file = ds.File(fp=processed.filename())
    processed.close()
    await interaction.response.send_message(file=uploaded_file)


@client.tree.command()
@ds.app_commands.describe(member="Пользователь")
async def badges(interaction: ds.Interaction, member: ds.Member):
    await interaction.response.send_message(view=DropdownView())


client.run(CONFIG["token"])
