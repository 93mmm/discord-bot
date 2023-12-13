import discord
from discord import app_commands
from config import get_config_value

class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        GUILD_OBJ = discord.Object(id=int(get_config_value('guild_id')))
        self.tree.copy_global_to(guild=GUILD_OBJ)
        await self.tree.sync(guild=GUILD_OBJ)