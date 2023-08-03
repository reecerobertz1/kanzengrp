from typing import Any
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import View, Select
from typing import List, Optional

class infobuttons(discord.ui.View):
    def __init__ (self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Server Rules")
    async def rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Rules", color=0x2b2d31)
        embed.add_field(name="Chat Rules", value="GFHDJSKHGSDFGFDGJKFGKJJKGFKGHJKG")
        await interaction.response.send_message(embed=embed, ephermal=True)    


    @commands.command()
    async def lol(self, ctx):
        embed = discord.Embed(title="Welcome *!*", description="> Thank you for joining Editors Block! This is a community server made for all types of editors.\n> Feel free to ping @owners or @staff if you need any help.\n\nAlso, we will do group recruits for the groups Kanzen, Aura, and Daegu!", color=0x2b2d31)
        embed.set_footer(text="Follow the groups below!", icon_url="https://images-ext-2.discordapp.net/external/eVpj5e3hkU4cFDmIU8KnoGkfnfyDbbJPVs1xJWmUNQg/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1131003330810871979/128ca9e19d2f0aa0e41c99310673dfac.png")

        button = discord.ui.Button(label="Kanzen", url="https://www.instagram.com/kanzengrp/")
        button2 = discord.ui.Button(label="Aura", url="https://www.instagram.com/auragrps/")
        button3 = discord.ui.Button(label="Daegu", url="https://www.instagram.com/daegutowngrp/")

        view = discord.ui.View()
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)
        await ctx.send(embed=embed)

    @commands.command()
    async def lol2(self, ctx):
        embed = discord.Embed(title="Owner Info", description="Editors Block is owned by @remqsi, @yoongiaeps, and @taedxck", color=0x2b2d31)
        embed.set_author(name="Hoshi#3105", icon_url=f'https://cdn.discordapp.com/avatars/849682093575372841/f04c5815341216fdafe736a2564a4d09.png?size=1024')
        view = infobuttons
        await ctx.send(embed=embed, view=view)