import discord
from discord.ext import commands
from discord import app_commands
import traceback
from typing import Optional
from io import BytesIO

class newapps(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot: commands.Bot = bot
		super().__init__()
		
@app_commands.command()
async def hello(interaction: discord.Interaction):
	await interaction.responce.send_message('hello')
		

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(newapps(bot))