import asyncio
import datetime
import json
import random
import re
from typing import Any
import discord
from discord.ext import commands
from discord import app_commands
from discord.interactions import Interaction
from discord.ui import View, Select
from typing import List, Optional
from discord import ui

class confessbutton(discord.ui.View):
    async def __init__(self):
        super().__init__(timeout=30)
        self.value = None

    @discord.ui.button(label="Click to confess", style=discord.ButtonStyle.red)
    async def confess(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(confessmodal())

class confessmodal(ui.Modal, title='Kanzen Confessions'):
    confession = ui.TextInput(label='Whats your confession', placeholder="Enter confession here...", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = interaction.client.get_channel(1140186620121841735)
        embed = discord.Embed(title="New confession", description=f"{self.confession.value}", color=0x2b2d31)
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Use /confess to send a confession!")
        await channel.send(embed=embed)
        await interaction.followup.send(f"Your confession has been sent to <#1140186620121841735>", ephemeral=True)

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