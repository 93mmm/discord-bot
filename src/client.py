import discord
from src.const import Bot
from discord import app_commands


class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        GUILD_OBJ = discord.Object(id=Bot.GUILD_ID)
        self.tree.copy_global_to(guild=GUILD_OBJ)
        await self.tree.sync(guild=GUILD_OBJ)
