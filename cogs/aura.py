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

class infobuttons(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Logos", emoji="<:brazy_milksip:958479364184490075>")
    async def guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = getlogos()
        logos = discord.Embed(title="<:auragrp:1145976005153005620>  Aura Logos!", description="<a:Arrow_1:1145603161701224528> Please make sure you watermark the logos!\n<a:Arrow_1:1145603161701224528> Use the watermark on every edit\n<a:Arrow_1:1145603161701224528> Do not share this link with anyone outside the group!", color=0x2b2d31)
        logos.set_footer(text="Made us some logos? send them to the leads!")
        logos.set_image(url="https://cdn.discordapp.com/attachments/1003438198862659644/1145984912680308786/rules_image_00000.png")
        await interaction.user.send(embed=logos, view=view)

        channel = interaction.client.get_channel(1122994947444973709)
        log = discord.Embed(title="Logo button has been used!", description=f"`{interaction.user.display_name}` has used the logos button", color=0x2b2d31)
        log.set_footer(text=f"id: {interaction.user.id}", icon_url=interaction.user.display_avatar)
        await channel.send(embed=log)
        await interaction.response.send_message(f'I have sent you the logos! Check your DMs', ephemeral=True)

    @discord.ui.button(label="Inactive", emoji="<:HUGGG:1125879413922345000> ")
    async def inactive(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(ia())

class getlogos(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Get logos!")
    async def logos(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Here are the logos!\n[click here](https://mega.nz/folder/SNkySBBb#kNViVZOVnHzEFmFsuhtLOQ)")
        await interaction.followup.send("#𝗮𝘂𝗿𝗮𝗴𝗿𝗽")

class aura(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def rules(self, ctx):
        view=infobuttons()
        embed = discord.Embed(title="<:auragrp:1145976005153005620> Auragrp Rules", description='group rules:\n<a:Arrow_1:1145603161701224528> must be following [remqsi](https://www.instagram.com/remqsi/), [yoongiaeps](https://www.instagram.com/yoongiaeps/), [taedxck](https://www.instagram.com/taedxck/) + [auragrps](https://www.instagram.com/auragrps/)\n<a:Arrow_1:1145603161701224528> watermark your logos with your username if you use it against a mostly plain background (basically make them not steal-able)\n<a:Arrow_1:1145603161701224528> always use the group hashtag #𝐚𝐮𝐫𝐚𝐠𝐫𝐩\n<a:Arrow_1:1145603161701224528> never share our logos or the mega link for our logos to anyone outside of aura\n\nchat rules:\n<a:Arrow_1:1145603161701224528> try to stay as active as possible\n<a:Arrow_1:1145603161701224528> please set your nickname to “name | username” format so we know who you are!\n<a:Arrow_1:1145603161701224528> if you ever decide to move accounts or leave auragrp, pls message us\n<a:Arrow_1:1145603161701224528> do not share the discord invite link to anyone else\n<a:Arrow_1:1145603161701224528> no offensive jokes that will make others uncomfortable\n<a:Arrow_1:1145603161701224528> no impersonation (as other editors)\n<a:Arrow_1:1145603161701224528> only spam in the spam channels\n<a:Arrow_1:1145603161701224528> only self promote in the self promo channel\n<a:Arrow_1:1145603161701224528> be friendly and try to make friends!', color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1003438198862659644/1145984912680308786/rules_image_00000.png")
        await ctx.send(embed=embed, view=view)

class ia(ui.Modal, title='Inactivity Message'):
     instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     reason = ui.TextInput(label='Inactivity Reason', placeholder="", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Inactivity Message',description=f"**instagram:** {self.instagram.value}\n\n**account link:**https://instagram.com/{self.instagram.value}\n\n**inactivity reason:** {self.reason.value}" ,color=0x2b2d31)
          embed.set_footer(text=f"sent from: {interaction.user.name} | {interaction.user.id}", icon_url=interaction.user.avatar)
          embed.set_thumbnail(url=interaction.guild.icon)
          channel = interaction.client.get_channel(1122251494700363868)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your inactive message has been sent successfully', ephemeral=True)

async def setup(bot):
    await bot.add_cog(aura(bot))