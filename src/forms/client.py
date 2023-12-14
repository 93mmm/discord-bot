import discord as ds
from constants import CONFIG


class Client(ds.Client):
    def __init__(self, *, intents: ds.Intents):
        super().__init__(intents=intents)
        self.tree = ds.app_commands.CommandTree(self)

    async def setup_hook(self):
        GUILD_OBJ = ds.Object(id=CONFIG["guild-id"])
        self.tree.copy_global_to(guild=GUILD_OBJ)

        await self.tree.sync(guild=GUILD_OBJ)
