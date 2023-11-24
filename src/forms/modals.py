import discord
import traceback

from src.db_holder import Database
from src.const import Consts, SocCred, UserData


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

    def initialize_id(self, id):
        self.user_id = id
    
    def initialize_userdata(self, data: UserData):
        self.special_signs.default = data.special_signs

        if data.is_infinity == SocCred.GET_FROM_DB:
            self.social_points.default = data.social_points
        elif data.is_infinity == SocCred.PL_INFINITY:
            self.social_points.default = "+inf"
        elif data.is_infinity == SocCred.MIN_INFINITY:
            self.social_points.default = "-inf"
        
        self.photo_cards = " ".join(data.photo_cards)

    async def on_submit(self, interaction: discord.Interaction): # TODO: check is user admin
        if len(self.photo_cards.value.split(" ")) > 3:
            await interaction.response.send_modal(NewCard())

        soc_cr = 0
        is_inf = SocCred.GET_FROM_DB

        if self.social_points.value.startswith("+inf"):
            is_inf = SocCred.PL_INFINITY
        elif self.social_points.value.startswith("-inf"):
            is_inf = SocCred.MIN_INFINITY
        else:
            soc_cr = int(self.social_points.value)

        db: Database = Database(Consts.PATH)
        db.add_user(self.user_id, self.special_signs.value, soc_cr, is_inf, self.photo_cards.value)

        await interaction.response.send_message("User", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        traceback.print_exception(type(error), error, error.__traceback__)