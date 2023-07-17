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

    @app_commands.command(name='kanzen', description='Get Kanzen logos')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def kanzenlogos(self, interaction: discord.Interaction):
        await interaction.response.send_message('https://mega.nz/folder/J40zCTYY#L73pTeQKWpCh15wpuQaIFA', ephemeral=True)

    @app_commands.command(name='aura', description='Get Aura logos')
    @app_commands.guilds(discord.Object(id=957987670787764224))
    async def auralogos(self, interaction: discord.Interaction):
        await interaction.response.send_message('https://mega.nz/folder/SNkySBBb#kNViVZOVnHzEFmFsuhtLOQ', ephemeral=True)


    @app_commands.command(name='modal', description='open testing modal')
    async def testmodal(self, interaction: discord.Interaction):
         await interaction.response.send_modal(testmodal())

# modals

class testmodal(ui.Modal, title='Testing it'):
     test1 = ui.TextInput(label='Testing modals', placeholder="you're ugly...", style=discord.TextStyle.short)
     test2 = ui.TextInput(label='Testing modals', placeholder="you make me wanna die...", style=discord.TextStyle.long)
     test3 = ui.TextInput(label='Testing modals', placeholder="lol jk....", style=discord.TextStyle.short)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.send_message(f"{self.test1} {self.test2} {self.test3}", ephemeral=True)

class ia(ui.Modal, title='Inactivity Message'):
     test1 = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     test2 = ui.TextInput(label='Inactivity Reason', placeholder="", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.send_message(f"{self.test1} {self.test2} {self.test3}", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Slash(bot))