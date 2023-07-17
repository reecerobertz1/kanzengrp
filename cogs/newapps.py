import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# slash commands

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

# modals

class testmodal(discord.ui.Modal, title='Testing it'):
     test1 = ui.TextImput(label='Testing modals', placeholder="you're ugly...", style=discord.TextStyle.short)
     test2 = ui.TextImput(label='Testing modals', placeholder="you make me wanna die...", style=discord.TextStyle.long)
     test3 = ui.TextImput(label='Testing modals', placeholder="lol jk....", style=discord.TextStyle.short)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.send_message("lol modal hahahaha")

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Slash(bot))