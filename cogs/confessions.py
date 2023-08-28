import discord
from discord.ext import commands
from discord import app_commands
from discord.interactions import Interaction
from discord.ui import View, Select
from typing import List, Optional
from discord import ui
import datetime

class confessbutton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.value = None
        self.start_time = datetime.datetime.utcnow()

    @discord.ui.button(label="Click to confess", style=discord.ButtonStyle.red)
    async def confess(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(confessmodal())

class confessmodal(ui.Modal, title='Kanzen Confessions'):
    confession = ui.TextInput(label='Whats your confession', placeholder="Enter confession here...", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = interaction.client.get_channel(1145568957345054751)
        embed = discord.Embed(title="New confession", description=f"{self.confession.value}", color=0x2b2d31)
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Use /confess to send a confession!")
        confessions = await channel.send(embed=embed)
        await interaction.followup.send(f"Your confession has been sent to <#1145568957345054751>", ephemeral=True)
        await confessions.add_reaction("<:breaths:1128463455993741352>")
        await confessions.add_reaction("<:pause:1132212249621184634>")
        await confessions.add_reaction("<:__:1132210032822456411>")
        await confessions.add_reaction("<a:crysad:1132210059233988678>")
        await confessions.add_reaction("<a:wAHhh:1128463952423174164>")

class confessions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='confess', description='Drop your juiciest secrets!')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def confess(self, interaction: discord.Interaction):
        view = confessbutton()
        await interaction.response.send_message('Your confessions are sent anonymously! Do not be scared to tell us anything', view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(confessions(bot))