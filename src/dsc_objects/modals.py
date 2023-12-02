import discord
import traceback

from src.db_holder import Database, soc_rating_in_form, get_soc_rating_for_db
from src.helpers.const import UserData, Bot


class NewCard(discord.ui.Modal, title="Дело"):
    special_signs = discord.ui.TextInput(
        label="Особые приметы",
        style=discord.TextStyle.paragraph,
        placeholder="Укажите приметы пользователя",
        required=True,
        max_length=300
    )

    social_points = discord.ui.TextInput(
        label="Социальный рейтинг",
        style=discord.TextStyle.short,
        placeholder="0",
        required=True,
        max_length=100
    )

    photo_cards = discord.ui.TextInput(
        label="Награды",
        placeholder="Укажите награды",
        default="HTML JS React"
    )

    def initialize_id(self, user_id):
        self.user_id = user_id
    
    def initialize_userdata(self, user_id: int, data: UserData, submit_message: str):
        self.user_id = user_id
        self.special_signs.default = data.special_signs

        self.social_points.default = soc_rating_in_form(data.social_points, data.is_infinity)

        self.photo_cards.default = " ".join(data.photo_cards)

    async def on_submit(self, interaction: discord.Interaction): # TODO: check is user admin
        social_points, is_infinity = get_soc_rating_for_db(self.social_points.value)

        db: Database = Database(Bot.DB_PATH)
        if not db.user_exists(self.user_id):
            db.add_user(self.user_id, self.special_signs.value, social_points, is_infinity, self.photo_cards.value)
        else:
            db.edit_user(self.user_id, self.special_signs.value, social_points, is_infinity, self.photo_cards.value)

        await interaction.response.send_message("Нормас", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, ex: Exception) -> None:
        await interaction.response.send_message("Что-то пошло не так", ephemeral=True)
        traceback.print_exception(type(ex), ex, ex.__traceback__)
