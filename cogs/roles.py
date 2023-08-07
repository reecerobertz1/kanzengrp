from discord import ui, Embed
from discord.interactions import Interaction
from collections import deque
from typing import List
from discord.ui import View, Select
import discord
from discord.ext import commands
from discord.utils import get

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [

            discord.SelectOption(label="he/hom", value=str(1121852424353755137) ,description="Крутая роль", emoji=""),
            discord.SelectOption(label="she/her", value=str(1122635691487137884), description="Богатая роль", emoji="🤳"),
            discord.SelectOption(label="they/them", value=str(1122635724559241317), description="Игровая роль", emoji="🎮"),
        ]

        super().__init__(placeholder="Меню",options=options)
    
    async def callback(self, inter: discord.Interaction):
        await inter.user.add_roles(get(inter.guild.roles, id=int(self.values[0])))
        await inter.response.send_message(f"Вы выбрали роль <@&{self.values[0]}>")


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        view = DropdownView()
        await ctx.send(view=view)

async def setup(bot):
    await bot.add_cog(Roles(bot))