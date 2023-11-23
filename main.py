import discord
from discord import app_commands
from src.db_holder import *
from src.const import Bot 

intents = discord.Intents.all()
GUILD_OBJ = discord.Object(id=Bot.GUILD_ID)

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD_OBJ)
        await self.tree.sync(guild=GUILD_OBJ)


client = MyClient(intents=intents)

database = Database("files/database/database.db")


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
@app_commands.describe(member="Member to describe", 
                       social_points="Social points of member", 
                       special_signs="Special signs of member")
async def add_card(interaction: discord.Interaction, member: discord.Member=None, social_points: int=0, special_signs: str=""):
    if member is None:
        print("user does not specified")
    userID: int = member.id
    userTag: str = f"{member.name}#{member.discriminator}"

    database.add_user(userID, userTag, special_signs, social_points)
    await interaction.response.send_message(f"User successfully added")


client.run(Bot.TOKEN)


# TODO: remove Username from database