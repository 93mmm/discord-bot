import discord as ds

from database import Database
from helpers import User
from constants import PATHS, CONFIG
from forms.modals import NewCard, ExistingCard
from forms.client import Client


client: Client = Client(intents=ds.Intents.all())
db: Database = Database(PATHS["database"])


@client.event
async def on_ready():
    print(f"Logged in as {client.user} "
          f"(ID: {client.user.id})\n---------")


@client.tree.command()
@ds.app_commands.describe(member="Пользователь",
                          social_points="Очки рейтинга (+100/-37/etc)")
async def rep(interaction: ds.Interaction,
              member: ds.Member=None,
              social_points: str=""):
    errmsg: str = ""

    if interaction.user.id not in CONFIG["administrators"]:
        errmsg = "Вы не админ"

    if member is None:
        errmsg = "Пользователь не указан"

    if social_points == "":
        errmsg = "Социальный рейтинг не указан"

    if social_points.startswith("+inf") or social_points.startswith("-inf"):
        errmsg = "Нельзя указать бесконечный рейтинг"

    if not db.user_exists(member.id):
        errmsg = "Сначала добавьте пользователя"

    if errmsg != "":
        await interaction.response.send_message(errmsg, ephemeral=True)
        return

    db.update_rep(member.id, int(social_points))
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


client.run(CONFIG["token"])
