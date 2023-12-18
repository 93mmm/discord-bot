import discord as ds
from constants import KEY_CONFIG


class Badges(ds.ui.Select):
    def __init__(self):
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

    async def callback(self, interaction: ds.Interaction):
        print(self.values)
        await interaction.response.send_message("Your favourite colour is "
                                                f"{self.values[0]}")


class DropdownView(ds.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Badges())

