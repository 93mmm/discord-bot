import discord as ds
import traceback

from helpers import User, credits_for_db
from database import Database
from constants import PATHS


class NewCard(ds.ui.Modal, title="Завести дело"):
    special_signs = ds.ui.TextInput(
        label="Особые приметы",
        style=ds.TextStyle.paragraph,
        placeholder="Укажите приметы пользователя",
        required=True,
        max_length=300
    )

    social_credits = ds.ui.TextInput(
        label="Социальный рейтинг",
        style=ds.TextStyle.short,
        placeholder="0",
        required=True,
        max_length=100
    )

    badges = ds.ui.TextInput(
        label="Награды",
        placeholder="Укажите награды",
        default="HTML JS React"
    )

    def initialize(self, user: User) -> None:
        self.usr = user

    async def on_submit(self, interaction: ds.Interaction):
        social_credits, is_infinity = credits_for_db(self.social_credits.value)

        self.usr.special_signs = self.special_signs.value
        self.usr.social_credits = social_credits
        self.usr.is_infinity = is_infinity
        self.usr.badges = self.badges.value

        Database(PATHS["database"]).add_user(self.usr)
        await interaction.response.send_message("Нормас", ephemeral=True)

    async def on_error(self, interaction: ds.Interaction,
                       ex: Exception) -> None:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        await interaction.response.send_message("Что-то пошло не так",
                                                ephemeral=True)


class ExistingCard(ds.ui.Modal, title="Редактировать дело"):
    special_signs = ds.ui.TextInput(
        label="Особые приметы",
        style=ds.TextStyle.paragraph,
        placeholder="Приметы пользователя",
        required=True,
        max_length=300
    )

    badges = ds.ui.TextInput(
        label="Награды",
        placeholder="Награды",
    )

    def initialize(self, usr: User) -> None:
        self.usr: User = usr

    async def on_submit(self, interaction: ds.Interaction):
        self.usr.special_signs = self.special_signs.value
        self.usr.badges = self.badges.value

        Database(PATHS["database"]).update_user(self.usr)
        await interaction.response.send_message("Нормас", ephemeral=True)

    async def on_error(self, interaction: ds.Interaction,
                       ex: Exception) -> None:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        await interaction.response.send_message("Что-то пошло не так",
                                                ephemeral=True)