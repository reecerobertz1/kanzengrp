import traceback
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

    @app_commands.command(name='ia', description='Send an inactivity message!')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def ia(self, interaction: discord.Interaction):
         await interaction.response.send_modal(ia())

    @app_commands.command(name='apply', description='Apply for kanzen!')
    @app_commands.guilds(discord.Object(id=1122181605591621692))
    async def apps(self, interaction: discord.Interaction):
         await interaction.response.send_modal(apps())

# modals

class testmodal(ui.Modal, title='Testing it'):
     test1 = ui.TextInput(label='Testing modals', placeholder="you're ugly...", style=discord.TextStyle.short)
     test2 = ui.TextInput(label='Testing modals', placeholder="you make me wanna die...", style=discord.TextStyle.long)
     test3 = ui.TextInput(label='Testing modals', placeholder="lol jk....", style=discord.TextStyle.short)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.send_message(f"https://instagram.com/{self.test1}")

class ia(ui.Modal, title='Inactivity Message'):
     instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     reason = ui.TextInput(label='Inactivity Reason', placeholder="", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Inactivity Message', color=0x2b2d31)
          embed.add_field(name='Instagram Name:', value=f'{self.instagram.value}', inline=False)
          embed.add_field(name='Instagram Account Link:', value=f'https://instagram.com/{self.instagram.value}', inline=False)
          embed.add_field(name='Inactivity Reason:', value=f'{self.reason.value}', inline=False)
          embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
          channel = interaction.client.get_channel(1121913672822968330)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your inactive message has been sent successfully', ephemeral=True)

class apps(ui.Modal, title='Kanzengrp Applications'):
     instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     dcname = ui.TextInput(label='Discord username', placeholder="Enter your Discord username here...", style=discord.TextStyle.short)
     edit = ui.TextInput(label='Edit link (Instagran or Streamable)', placeholder="Paste link here...", style=discord.TextStyle.short)
     app = ui.TextInput(label='What app do you use for editing', placeholder="Editing app name...", style=discord.TextStyle.short)
     extra = ui.TextInput(label='Anything else you would like us to know?', placeholder="Extra info here...", style=discord.TextStyle.paragraph, required=False)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Kanzen Forms', color=0x2b2d31)
          embed.add_field(name='Instagram Name:', value=f'{self.instagram.value}', inline=False)
          embed.add_field(name='Instagram Account Link:', value=f'https://instagram.com/{self.instagram.value}', inline=False)
          embed.add_field(name='Discord Username:', value=f'{self.dcname.value}', inline=False)
          embed.add_field(name='Edit:', value=f'{self.edit.value}', inline=False)
          embed.add_field(name='Editing app:', value=f'{self.app.value}', inline=False)
          embed.add_field(name='Anything else:', value=f'{self.extra.value}', inline=False)
          embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
          channel = interaction.client.get_channel(1122183100038905908)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your application has been sent successfully', ephemeral=True)

    # normal commands

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Slash(bot))