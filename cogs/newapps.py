import discord
from discord.ext import commands
from discord import app_commands
import traceback
from typing import Optional
from io import BytesIO


		
class Slash(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot: commands.Bot = bot
		super().__init__()

	@app_commands.command(description="im dying")
	@app_commands.guilds(discord.Object(id=1121841073673736215))
	async def sumn(self, interaction: discord.Interaction):
		await interaction.response.defer(ephemeral=True)
		channel = self.bot.get_channel(1122627075682078720)
		await channel.send(f"{interaction.user.mention} used the `logos` command!")
		await interaction.followup.send(content=f"yay", ephemeral=True)
		

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Slash(bot))