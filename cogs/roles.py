from discord import ui, Embed
from discord.interactions import Interaction
from collections import deque
from typing import List
from discord.ui import View, Select
import discord
from discord.ext import commands
from discord.utils import get


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        select = Select(
            placeholder="Select a role",
            options=[
                discord.SelectOption(label="he/hom", value=str(1121852424353755137)),
                discord.SelectOption(label="she/her", value=str(1122635691487137884)),
                discord.SelectOption(label="they/them", value=str(1122635724559241317))
            ]
        )
        async def add_role(interaction: discord.Interaction):
            await interaction.response.send_message(f"You selected {select.values[0]}")
        select.callback = add_role
        view = View()
        view.add_item(select)

        embed = discord.Embed(title="Roles", description="Roles", color=0x2b2d31)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Roles(bot))