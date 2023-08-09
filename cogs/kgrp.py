import asyncio
import datetime
import json
import random
import re
from typing import Any
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import View, Select
from typing import List, Optional
from discord import ui

class infobuttons(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Logos", emoji="<a:kanzenflower:1128154723262943282>")
    async def guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = getlogos()
        embed = discord.Embed(title=f"{interaction.user.name} has got the logos!", color=0x2b2d31)
        logos = discord.Embed(title="<a:kanzenflower:1128154723262943282>  Kanzen Logos!", description="<a:bounceyarrow:1128155233437106187> Please make sure you watermark the logos!\n<a:bounceyarrow:1128155233437106187> Use the watermark on every edit\n<a:bounceyarrow:1128155233437106187> Do not share this link with anyone outside the group!", color=0x2b2d31)
        logos.set_footer(text="Made us some logos? send them to Reece!")
        logos.set_image(url="https://cdn.discordapp.com/attachments/1121841074512605186/1128394231115948072/theme_3_00000.png")
        await interaction.user.send(embed=logos, view=view)
        channel = interaction.client.get_channel(1122627075682078720)
        await channel.send(embed=embed)
        await interaction.followup.send("I have sent you the logos! check DMs", ephemeral=True)

    @discord.ui.button(label="Role Info", emoji="<:roles_00000:1136752067277504633>")
    async def roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="<:roles_00000:1136752067277504633> Role Info",description="<@&1131006052209541212> - Editors block owners\n<@&1131006067564875806> - Editors block staff\n<@&1136803676854431745> - our amazing supporters\n<@&1131016215754715166> - Accepted members from recruit\n<@&1131016147282710679> - Default Role from verification " ,color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True)   

class getlogos(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Get logos!")
    async def logos(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Here are the logos!\n(link)")
        await interaction.followup.send("#𝗞𝗮𝗻𝘇𝗲𝗻𝗴𝗿𝗽")

class kgrp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def info1(self, ctx):
        embed = discord.Embed(description="## Welcome *!*\nThank you for joining Kanzengrp! We hope you have a good time!  ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏\nIf you ever need any help feel free to ping @lead or @staff\n\nTo get the logos press the `logos` button below! And if you need\nto send an inactivity message, you can click the `inactive` button!", color=0x2b2d31)
        embed.set_footer(text="Follow the groups below!", icon_url="https://images-ext-2.discordapp.net/external/eVpj5e3hkU4cFDmIU8KnoGkfnfyDbbJPVs1xJWmUNQg/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1131003330810871979/128ca9e19d2f0aa0e41c99310673dfac.png")
        view = infobuttons()
        await ctx.send("https://cdn.discordapp.com/attachments/1121841074512605186/1138673275665399818/kanzen_rules_00000.png")
        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def info2(self, ctx):
        embed = discord.Embed(title="<a:kanzenflower:1128154723262943282> Kanzen rules ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏ ͏ ͏ ͏ ͏", description='✦ Group Rules :\n<a:bounceyarrow:1128155233437106187> always watermark the logos\n<a:bounceyarrow:1128155233437106187> do not share the logos link outside the server!\n<a:bounceyarrow:1128155233437106187> make sure you are following [@remqsi](https://www.instagram.com/remqsi/) + [@kanzengrp!](https://www.instagram.com/kanzengrp/)\n<a:bounceyarrow:1128155233437106187> if you do ever decide to leave the grp, or move accounts. please let lead or staff know!\n\n✦ Chat Rules :\n<a:bounceyarrow:1128155233437106187> please be as active as possible!\n<a:bounceyarrow:1128155233437106187> no using any slurs / words that can be offensive!\n<a:bounceyarrow:1128155233437106187> please set your nickname as "your name | username"\n<a:bounceyarrow:1128155233437106187> no impersonation as other editors\n<a:bounceyarrow:1128155233437106187> no trash talking other editors and groups!', color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1121841074512605186/1138674299033624786/kgrp_00000.png")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(kgrp(bot))