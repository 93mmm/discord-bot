import discord
import traceback

from src.db_holder import Database, soc_rating_in_form, get_soc_rating_for_db
from src.const import Consts, UserData


class NewCard(discord.ui.Modal, title="Дело"):
    special_signs = discord.ui.TextInput(
        label="Signs",
        style=discord.TextStyle.paragraph,
        placeholder="Specify the signs of the user",
        required=True,
        max_length=300
    )

    social_points = discord.ui.TextInput(
        label="Social credits",
        style=discord.TextStyle.short,
        placeholder="0",
        required=True,
        max_length=100
    )

    photo_cards = discord.ui.TextInput(
        label="Awards",
        placeholder="Insert rewards (maximum 3) separated by a space",
        default="HTML JS React"
    )

    def initialize_id(self, user_id):
        self.user_id = user_id
    
    def initialize_userdata(self, user_id: int, data: UserData):
        self.user_id = user_id
        self.special_signs.default = data.special_signs

        self.social_points.default = soc_rating_in_form(data.is_infinity, data.social_points)

        self.photo_cards.default = " ".join(data.photo_cards)

    async def on_submit(self, interaction: discord.Interaction): # TODO: check is user admin
        if len(self.photo_cards.value.split(" ")) > 3:
            await interaction.response.send_modal(NewCard())

        social_points, is_infinity = get_soc_rating_for_db(self.social_points.value)

        db: Database = Database(Consts.PATH)
        if not db.user_exists(self.user_id):
            db.add_user(self.user_id, self.special_signs.value, social_points, is_infinity, self.photo_cards.value)
        else:
            db.edit_user(self.user_id, self.special_signs.value, social_points, is_infinity, self.photo_cards.value)

        await interaction.response.send_message("User", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)
