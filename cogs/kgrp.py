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

    @discord.ui.button(label="Server Guide", emoji="<:guide:1136757467943022685>")
    async def guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="<:guide:1136757467943022685> Server Guide", color=0x2b2d31)
        embed.add_field(name="Get Started", value="<#1131007362895970414> - Server announcements are made here!\n<#1131005271502753812> - Server information\n<#1133730290221715487> - Get your roles here", inline=False)
        embed.add_field(name="Boost", value="<#1133772140915732511> - Boost messages are sent here\n<#1133772155499327538> - Claim the booster perks here", inline=False)
        embed.add_field(name="Events", value="<#1135594840739041380> - Server events and information is sent here\n<#1135594856106959032> - Giveaways are hosted here", inline=False)
        embed.add_field(name="Applications", value="<#1133771634793250847> - You can apply for the groups here\n<#1133771722659741877> - Ask questions about the applications\n<#1133771757816393839> - Answers from the qna", inline=False)
        embed.add_field(name="Main", value="<#1133767338588639323> - Start a converstion here with other members!\n<#1133767363339223110> - Speak other languages here!\n<#1133771941619191913> - Send self promotion here\n<#1134559895480442951> - Support the server with `/bump`", inline=False)
        embed.add_field(name="Editing", value="<#1133770895593324664> - Get opinions on your edits! \n<#1133770809366814890> - Get edit help with <@&1131127084379549757>\n<#1133770828882903141> - Ping <@&1131130102328078336> to get dts for your next post!\n<#1133770844817080360> - Ping <@&1131130157160206396> to collab with other server members\n<#1136756099710730331> - Talk in vc while editing", inline=False)
        embed.add_field(name="Bots", value="<#1133772583813263422> - Use our custom bot <@849682093575372841> here! `+help` for commands\n<#1133772598979866774> - Count as high as you can (can't count twice in a row)\n<#1133772609222361270> - Use other bots here other than hoshi\n<#1133772621666844813> - Another spam channel for you to use other bots\n<#1133772650695626882> - Use music commands here\n<#1133772672631836754> - Listen to music here", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Role Info", emoji="<:roles_00000:1136752067277504633>")
    async def roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="<:roles_00000:1136752067277504633> Role Info",description="<@&1131006052209541212> - Editors block owners\n<@&1131006067564875806> - Editors block staff\n<@&1136803676854431745> - our amazing supporters\n<@&1131016215754715166> - Accepted members from recruit\n<@&1131016147282710679> - Default Role from verification " ,color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True)   

    @discord.ui.button(label="Affiliate Info", emoji="<:partners:1137446533994909766>")
    async def affinfo(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="<:partners:1137446533994909766> Affiliate Information", color=0x2b2d31)
        embed.add_field(name="Advert with ping", value="<a:arrowpink:1134860720777990224> Follow Discord's [tos](https://discord.com/terms) and [guidelines](https://discord.com/guidelines)\n<a:arrowpink:1134860720777990224> Must have 100+ members\nIf you meet our requirements, please message one of our owners", inline=False)
        embed.add_field(name="Advert without ping", value="<a:arrowpink:1134860720777990224> Follow Discord's [tos](https://discord.com/terms) and [guidelines](https://discord.com/guidelines)\n<a:arrowpink:1134860720777990224> Must have 75+ members\nIf you meet our requirements, please message one of our owners", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class kgrp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def info1(self, ctx):
        embed = discord.Embed(title="Welcome *!*", description="Thank you for joining Kanzengrp! We hope you have a good time!  ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏\nIf you ever need any help feel free to ping @lead or @staff\n\nTo get the logos press the `logos` button below! And if you need\nto send an inactivity message, you can click the `inactive` button!", color=0x2b2d31)
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