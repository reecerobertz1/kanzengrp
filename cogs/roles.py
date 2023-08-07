from discord import ui, Embed
from discord.interactions import Interaction
from collections import deque
from typing import List
from discord.ui import View, Select
import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        await ctx.send("Please select your pronouns:", view=self.get_pronouns_menu())

    def get_pronouns_menu(self):
        pronouns_menu = discord.ui.Select(placeholder="Please select your pronouns:")
        pronouns_options = {
            "She/Her": 1122635691487137884,
            "He/Him": 1121852424353755137,
            "They/Them": 1122635724559241317
        }
        for label, role_id in pronouns_options.items():
            pronouns_menu.add_option(label=label, value=label, description="Select this option.", emoji="👍", id=role_id)
        return pronouns_menu

    @commands.Cog.listener()
    async def on_select_option(self, interaction: discord.Interaction):
        role_id = None
        if interaction.custom_id == "pronouns_menu":
            selected_option = interaction.data["values"][0]
            role_id = selected_option.get("role_id")

        if role_id:
            role = discord.utils.get(interaction.guild.roles, id=role_id)
            if role:
                await interaction.user.add_roles(role)

async def setup(bot):
    await bot.add_cog(Roles(bot))