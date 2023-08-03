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

    @app_commands.command(name='kanzen', description='Get Kanzen logos')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def kanzenlogos(self, interaction: discord.Interaction):
        await interaction.response.send_message('https://mega.nz/folder/J40zCTYY#L73pTeQKWpCh15wpuQaIFA', ephemeral=True)

    @app_commands.command(name='aura', description='Get Aura logos')
    @app_commands.guilds(discord.Object(id=957987670787764224))
    async def auralogos(self, interaction: discord.Interaction):
        await interaction.response.send_message('https://mega.nz/folder/SNkySBBb#kNViVZOVnHzEFmFsuhtLOQ', ephemeral=True)

    @app_commands.command(name='ia', description='Send an inactivity message!')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def ia(self, interaction: discord.Interaction):
         await interaction.response.send_modal(ia())

    @app_commands.command(name='apps', description='Apply for kanzen!')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guilds(discord.Object(id=1122181605591621692))
    async def apps(self, interaction: discord.Interaction):
         await interaction.response.send_modal(apps())

    @app_commands.command(name='app', description='Apply for aura!')
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guilds(discord.Object(id=1123347338841313331))
    async def auraapps(self, interaction: discord.Interaction):
         await interaction.response.send_modal(auraapps())

    @app_commands.command(name='staff', description='Apply for Kanzen staff!')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def staff(self, interaction: discord.Interaction):
         await interaction.response.send_modal(staff())

# modals

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

# kanzen staff

class staff(ui.Modal, title='Kanzen Staff Apps'):
     instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     reason = ui.TextInput(label='why should you be chosen?', placeholder="Put your reason here...", style=discord.TextStyle.long)
     exp = ui.TextInput(label='what kind of expirience do you have?', placeholder="Expirience list here..", style=discord.TextStyle.long)
     contribute = ui.TextInput(label='what will you contribute with?', placeholder="E.g. Events you would like to host, To help improve Kanzen etc...", style=discord.TextStyle.long)
     extra = ui.TextInput(label='anything else you would like to add?', placeholder="Expirience list here..", style=discord.TextStyle.long, required=False)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Kanzen Staff Apps', color=0x2b2d31)
          embed.add_field(name='Instagram Name:', value=f'{self.instagram.value}', inline=False)
          embed.add_field(name='Instagram Account Link:', value=f'https://instagram.com/{self.instagram.value}', inline=False)
          embed.add_field(name='why should you be chosen?:', value=f'{self.reason.value}', inline=False)
          embed.add_field(name='what kind of expirience do you have?:', value=f'{self.exp.value}', inline=False)
          embed.add_field(name='what will you contribute with?:', value=f'{self.contribute.value}', inline=False)
          embed.add_field(name='anything else you would like to say?', value=f'{self.extra.value}')
          embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
          channel = interaction.client.get_channel(1135238365902553158)
          await channel.send(embed=embed)
          await interaction.followup.send(f'You have sent your staff app successfully', ephemeral=True)

# kanzen apps

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

    # aura apps

class auraapps(ui.Modal, title='Auragrp Applications'):
     instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     dcname = ui.TextInput(label='Discord username', placeholder="Enter your Discord username here...", style=discord.TextStyle.short)
     edit = ui.TextInput(label='Edit link (Instagran or Streamable)', placeholder="Paste link here...", style=discord.TextStyle.short)
     app = ui.TextInput(label='What app do you use for editing', placeholder="Editing app name...", style=discord.TextStyle.short)
     extra = ui.TextInput(label='Anything else you would like us to know?', placeholder="Extra info here...", style=discord.TextStyle.paragraph, required=False)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Aura Forms', color=0x2b2d31)
          embed.add_field(name='Instagram Name:', value=f'{self.instagram.value}', inline=False)
          embed.add_field(name='Instagram Account Link:', value=f'https://instagram.com/{self.instagram.value}', inline=False)
          embed.add_field(name='Discord Username:', value=f'{self.dcname.value}', inline=False)
          embed.add_field(name='Edit:', value=f'{self.edit.value}', inline=False)
          embed.add_field(name='Editing app:', value=f'{self.app.value}', inline=False)
          embed.add_field(name='Anything else:', value=f'{self.extra.value}', inline=False)
          embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
          channel = interaction.client.get_channel(1123353889228468305)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your application has been sent successfully', ephemeral=True)

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Slash(bot))