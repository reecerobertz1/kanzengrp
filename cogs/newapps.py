import discord
from discord.ext import commands
from discord import app_commands
import traceback
from typing import Optional
from io import BytesIO
from discord_slash import cog_ext

class newapps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='test', description='testing')
    async def test(self, interaction: discord.Interaction, name: str, age: int) -> None:
         await interaction.response.send_message(f'My name is {name} and i am {age} years old!')

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(newapps(bot))