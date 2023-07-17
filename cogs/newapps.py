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

    @app_commands.command(name='lol', description='testing slash commands')
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('testing')


    @app_commands.command(name='modal', description='open testing modal')
    async def test(self, interaction: discord.Interaction):
         await interaction.response.send_modal(testmodal())


class testmodal(discord.ui.Modal, title='Testing it'):
     test1 = discord.ui.TextImput(label='Testing modals', placeholder="you're ugly...", style=discord.TextStyle.short)
     test2 = discord.ui.TextImput(label='Testing modals', placeholder="you make me wanna die...", style=discord.TextStyle.long)
     test3 = discord.ui.TextImput(label='Testing modals', placeholder="lol jk....", style=discord.TextStyle.short)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.send_message('testing modals')

          

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Slash(bot))