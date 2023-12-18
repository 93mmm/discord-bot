import discord as ds
from constants import KEY_CONFIG, PATHS
from database import Database
from helpers import get_keys


class Badges(ds.ui.Select):
    def __init__(self, user_id: int):
        self.user_id = user_id
        options: list[ds.SelectOption] = list()
        i = 0
        for key, val in KEY_CONFIG["badges"].items():
            i += 1
            opt: ds.SelectOption = ds.SelectOption(label=val[0],
                                                   description="bdg")
            options.append(opt)
            if i == 10:
                break

        super().__init__(placeholder='Choose your favourite colour...',
                         min_values=0,
                         max_values=4,
                         options=options)
        # TODO: select already selected badges

    async def callback(self, interaction: ds.Interaction):
        db: Database = Database(PATHS["database"])
        if not db.user_exists(self.user_id):
            await interaction.responce.send_message("Сначала добавьте пользователя",
                                                    ephemeral=True)
            return
        usr: User = db.get_user(self.user_id)
        proper_badges, wrong_badges = get_keys(" ".join(self.values))

        usr.badges = " ".join(proper_badges)
        db.update_user(usr)
        await interaction.response.send_message("Награды пользователя обновлены", ephemeral=True)
