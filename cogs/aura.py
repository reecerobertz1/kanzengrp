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

class gamenight(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Interested", emoji="<a:rocknroll:1125872006538199121>")
    async def he_him(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1151053389413765141
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You will no longer receive a reminder", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You will now receive reminders for the game night!\nWe will ping you with the role <@&1151053389413765141>", ephemeral=True)

    @discord.ui.button(label="Suggest a date an time", emoji="<a:mm_hug_tight:1122277098887848028>")
    async def date(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(date())

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
        self.hidden = True

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def rules(self, ctx):
        view=infobuttons()
        embed = discord.Embed(title="<:auragrp:1145976005153005620> Auragrp Rules", description='group rules:\n<a:Arrow_1:1145603161701224528> must be following [remqsi](https://www.instagram.com/remqsi/), [yoongiaeps](https://www.instagram.com/yoongiaeps/), [taedxck](https://www.instagram.com/taedxck/) + [auragrps](https://www.instagram.com/auragrps/)\n<a:Arrow_1:1145603161701224528> watermark your logos with your username if you use it against a mostly plain background (basically make them not steal-able)\n<a:Arrow_1:1145603161701224528> always use the group hashtag #𝐚𝐮𝐫𝐚𝐠𝐫𝐩\n<a:Arrow_1:1145603161701224528> never share our logos or the mega link for our logos to anyone outside of aura\n\nchat rules:\n<a:Arrow_1:1145603161701224528> try to stay as active as possible\n<a:Arrow_1:1145603161701224528> please set your nickname to “name | username” format so we know who you are!\n<a:Arrow_1:1145603161701224528> if you ever decide to move accounts or leave auragrp, pls message us\n<a:Arrow_1:1145603161701224528> do not share the discord invite link to anyone else\n<a:Arrow_1:1145603161701224528> no offensive jokes that will make others uncomfortable\n<a:Arrow_1:1145603161701224528> no impersonation (as other editors)\n<a:Arrow_1:1145603161701224528> only spam in the spam channels\n<a:Arrow_1:1145603161701224528> only self promote in the self promo channel\n<a:Arrow_1:1145603161701224528> be friendly and try to make friends!', color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1003438198862659644/1145984912680308786/rules_image_00000.png")
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def rolesa(self, ctx):
        embed1 = discord.Embed(title="・₊˚ name colours", description="<:colours_00000:1146895379879694446><@&1122261109886439495>\n<:colours_00001:1146895383155445801><@&1122261261934133420>\n<:colours_00002:1146895385806262313><@&1122261348420690021>\n<:yellow:1146895815755968612><@&1122261454331052074>\n<:colours_00004:1146895394895310898><@&1122261541539033088>\n<:colours_00005:1146895398393368677><@&1122261624695312505>\n<:colours_00006:1146895400691830855><@&1122261781285445815>\n<:colours_00007:1146895403715928095><@&1122261688826208339>\n<:colours_00008:1146895407260114995><@&1122261866312376370>\n<:blue:1146896528531787997><@&1122261959161683998>\n<:colours_00010:1146895414331715614><@&1122262098546794578>\n<:colours_00011:1146895417469042810><@&1122262010097319976>\n<:colours_00012:1146895419863998585><@&1122262238095495295>\n<:colours_00013:1146895423089410088><@&1122262166188327022>\n<:colours_00014:1146895425727647794><@&1122262320584851536>\n<:colours_00015:1146895427615076492><@&1122262350209224864>", color=0x2b2d31)
        embed1.set_footer(text="React with the emojis below to select a role!", icon_url="https://cdn.discordapp.com/icons/957987670787764224/5e22eb11a922cda86efb326de2498ded.png?size=1024")
        embed2 = discord.Embed(title="・₊˚ editing programs", description="<:ae:1146896850511724544> <@&1122999279439581274>\n<:am:1146896878487740446> <@&1122999333516742676>\n<:vs:1146896935123427531> <@&1122999355121606676>\n<:cc:1146896904744095875> <@&1146897567381209169>\n<:ccp:1146896977175519273> <@&1122999375078109194>\n<:fm:958457116186791977> <@&1146897584934375574>", color=0x2b2d31)
        embed2.set_footer(text="React with the emojis below to select a role!", icon_url="https://cdn.discordapp.com/icons/957987670787764224/5e22eb11a922cda86efb326de2498ded.png?size=1024")
        embed3 = discord.Embed(title="・₊˚ pronouns", description="<:1:1146898248498425886><@&1122253597539831930>\n<:2:1146898257935618071><@&1122253575469404180>\n<:3:1146898252311035924><@&1122253613725663283>\n<:4:1146898256438243390><@&1122253656033611956>\n<:5:1146898250884993134><@&1122253630725181530>\n<:6:1146898260657717400><@&1122253671871283401>", color=0x2b2d31)
        embed3.set_footer(text="React with the emojis below to select a role!", icon_url="https://cdn.discordapp.com/icons/957987670787764224/5e22eb11a922cda86efb326de2498ded.png?size=1024")
        embed4 = discord.Embed(title="・₊˚ games", description="<:1:1146898248498425886> <@&1122999400306851922>\n<:2:1146898257935618071> <@&1122999436289785997>\n<:3:1146898252311035924> <@&1122999419642597446>\n<:4:1146898256438243390> <@&1122999670550048888>", color=0x2b2d31)
        embed4.set_footer(text="React with the emojis below to select a role!", icon_url="https://cdn.discordapp.com/icons/957987670787764224/5e22eb11a922cda86efb326de2498ded.png?size=1024")
        embed5 = discord.Embed(title="・₊˚ extra", description="<:1:1146898248498425886><@&1122999466438438962>\n<:2:1146898257935618071><@&1125515778582659122>", color=0x2b2d31)
        embed5.set_footer(text="React with the emojis below to select a role!", icon_url="https://cdn.discordapp.com/icons/957987670787764224/5e22eb11a922cda86efb326de2498ded.png?size=1024")
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)
        await ctx.send(embed=embed4)
        await ctx.send(embed=embed5)
    
    @commands.command()
    async def gamenight(self, ctx):
        view = gamenight()
        await ctx.send("hey aromies \nnani is planning on having a game night sometime around the end of the month, we will be playing among us! \n\nif you’re interested click the `interested` button below to get the game night role so you can be ping for the reminder\nand also click the `suggest a time` button to tell us what date and time is most suitable for you, but include you timezone too! so we can work out what it is in our timezones!\n@everyone", view=view)

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
        
class date(ui.Modal, title='Game Night'):
     instagram = ui.TextInput(label='What date and time is best for you?', placeholder="Enter your date and time here...", style=discord.TextStyle.short)
     reason = ui.TextInput(label='What timezone are you in?', placeholder="Enter timezone...", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Game Night time suggestions',description=f"**Date & Time:** {self.instagram.value}\n\n**timezone:** {self.reason.value}" ,color=0x2b2d31)
          embed.set_footer(text=f"sent from: {interaction.user.name} | {interaction.user.id}", icon_url=interaction.user.avatar)
          embed.set_thumbnail(url=interaction.guild.icon)
          channel = interaction.client.get_channel(1151070008848429056)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your time and date suggestion has been sent!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(aura(bot))