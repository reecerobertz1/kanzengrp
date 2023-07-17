import discord
from discord.ext import commands
from discord import app_commands

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='test', description='testing slash commands')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('testing')

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Slash(bot))