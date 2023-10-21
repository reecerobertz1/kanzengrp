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

    @discord.ui.button(label="Logos")
    async def logos(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = getlogos()
        logos = discord.Embed(title="<a:kanzenflower:1128154723262943282> Kanzen Logos!", description="<a:Arrow_1:1145603161701224528> Please make sure you watermark the logos!\n<a:Arrow_1:1145603161701224528> Use the watermark on every edit\n<a:Arrow_1:1145603161701224528> Do not share this link with anyone outside the group!", color=0x2b2d31)
        logos.set_footer(text="Made us some logos? send them to Reece!")
        logos.set_image(url="https://cdn.discordapp.com/attachments/849724031723634688/1145605654539669565/new_banner_00000.png")
        await interaction.user.send(embed=logos, view=view)
        channel = interaction.client.get_channel(1122627075682078720)
        log = discord.Embed(title="Logo button has been used!", description=f"`{interaction.user.display_name}` has used the logos button", color=0x2b2d31)
        log.set_footer(text=f"id: {interaction.user.id}", icon_url=interaction.user.display_avatar)
        await channel.send(embed=log)
        await interaction.response.send_message(f'I have sent you the logos! Check your DMs', ephemeral=True)

    @discord.ui.button(label="Booster Perks")
    async def bp(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Kanzen Perks", description="<a:Arrow_1:1145603161701224528> Remqsi's colouring packs 1 & 2\n<a:Arrow_1:1145603161701224528> BTS Photos\n<a:Arrow_1:1145603161701224528> Enhypen Photos\n<a:Arrow_1:1145603161701224528> Blackpink Photos\n<a:Arrow_1:1145603161701224528> Break your heart project file\n<a:Arrow_1:1145603161701224528> Lisa candy project file", color=0x2b2d31)
        embed.set_footer(text="This is just a preview, only boosters get the link")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Inactivity")
    async def inactive(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(ia())

    @discord.ui.button(label="Suggest")
    async def suggest(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(suggest())

class getlogos(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Get logos!")
    async def logos(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Here are the logos!\n[click here](https://mega.nz/folder/J40zCTYY#L73pTeQKWpCh15wpuQaIFA)")
        await interaction.followup.send("#𝗞𝗮𝗻𝘇𝗲𝗻𝗴𝗿𝗽")

class ia(ui.Modal, title='Inactivity Message'):
     instagram = ui.TextInput(label='What is your instagram username?', placeholder="Put username here...", style=discord.TextStyle.short)
     reason = ui.TextInput(label='What is your reason?', placeholder="Put reason here...", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Inactivity Message', color=0x2b2d31)
          embed.add_field(name="Instagram Username", value=self.instagram.value)
          embed.add_field(name="Instagram Link", value=f"https://instagram.com/{self.instagram.value}")
          embed.add_field(name="Reason", value=self.reason.value)
          embed.set_author(name=f"sent by {interaction.user.name}", icon_url=interaction.user.avatar)
          embed.set_footer(text=interaction.user.id, icon_url=interaction.guild.icon)
          channel = interaction.client.get_channel(1121913672822968330)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your suggestion has been sent successfully', ephemeral=True)

class suggest(ui.Modal, title='Suggestions'):
     suggestion = ui.TextInput(label='What would you like to suggest?', placeholder="Put suggestion here...", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(description=f'suggestion: {self.suggestion.value}', color=0x2b2d31)
          embed.set_author(name=f"sent by {interaction.user.name}", icon_url=interaction.user.avatar)
          channel = interaction.client.get_channel(1145568921987059802)
          suggestion = await channel.send(embed=embed)
          await interaction.followup.send(f'Your suggestion has been sent successfully', ephemeral=True)
          await suggestion.add_reaction("<:LIKE:1146004608154607627>")
          await suggestion.add_reaction("<:DISLIKE:1146004603834478602>")

class pronouns(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(emoji="<:one:1146003619750105168>")
    async def he_him(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1121852424353755137
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1121852424353755137>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1121852424353755137>", ephemeral=True)


    @discord.ui.button(emoji="<:two:1146003617942351902>")
    async def she_her(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122635691487137884
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122635691487137884>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122635691487137884>", ephemeral=True)

    @discord.ui.button(emoji="<:three:1146003614691753994>")
    async def they_them(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122635724559241317
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122635724559241317>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122635724559241317>", ephemeral=True)

    @discord.ui.button(emoji="<:four:1146003611227263047>")
    async def he_they(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122635760445706321
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122635760445706321>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122635760445706321>", ephemeral=True)

    @discord.ui.button(emoji="<:five:1146003609125916712>")
    async def she_they(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122635742229835897
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122635742229835897>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122635742229835897>", ephemeral=True)

    @discord.ui.button(emoji="<:six:1146003606835834951>")
    async def any(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122635791844266064
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122635791844266064>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122635791844266064>", ephemeral=True)

class Programs(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(emoji="<:aftereffects:1139953449954447380>")
    async def ae(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122921620047147131
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122921620047147131>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122921620047147131>", ephemeral=True)


    @discord.ui.button(emoji="<:alightmotion:1139953459303546940>")
    async def am(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122921640288850025
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122921640288850025>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122921640288850025>", ephemeral=True)

    @discord.ui.button(emoji="<:sonyvegas:1139953453813223444>")
    async def svp(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1139954079506911303
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1139954079506911303>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1139954079506911303>", ephemeral=True)

    @discord.ui.button(emoji="<:videostar:1139953847784194119>")
    async def vs(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122921660320858274
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122921660320858274>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122921660320858274>", ephemeral=True)

    @discord.ui.button(emoji="<:funimate:1139953446552879156>")
    async def fnm(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1139954125560365116
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1139954125560365116>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1139954125560365116>", ephemeral=True)

    @discord.ui.button(emoji="<:cutecut:1139953845057896549>")
    async def ccp(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1139954104383324240
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1139954104383324240>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1139954104383324240>", ephemeral=True)

    @discord.ui.button(emoji="<:capcut:1139953436058722436>")
    async def cc(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1139954142215942255
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1139954142215942255>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1139954142215942255>", ephemeral=True)

class games(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(emoji="<:fortnite:1123259326006571090>")
    async def fn(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122921698367389756
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122921698367389756>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122921698367389756>", ephemeral=True)

    @discord.ui.button(emoji="<:MCicon:1123259350522282025>")
    async def mc(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122979205324480553
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122979205324480553>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122979205324480553>", ephemeral=True)


    @discord.ui.button(emoji="<:ROBLOXicon:1123259382063443968>")
    async def roblox(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122921713823395851
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122921713823395851>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122921713823395851>", ephemeral=True)

    @discord.ui.button(emoji="<:Valoranticon:1123259406092611654>")
    async def valo(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122921729384271963
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122921729384271963>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122921729384271963>", ephemeral=True)

    @discord.ui.button(emoji="<:gtaV:1123259437637980183>")
    async def gta(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122921800502878259
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122921800502878259>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122921800502878259>", ephemeral=True)

    @discord.ui.button(emoji="<:honkai:1139958684324216934>")
    async def honkai(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1139957904712142932
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1139957904712142932>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1139957904712142932>", ephemeral=True)

    @discord.ui.button(emoji="<:genshin:1139958246526951464>")
    async def genshin(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122921755216973854
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122921755216973854>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122921755216973854>", ephemeral=True)

    @discord.ui.button(emoji="<:phasmophobia:1139962251453927556>")
    async def phasmo(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1139962329950343208
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1139962329950343208>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1139962329950343208>", ephemeral=True)

class other(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(emoji="<:hoshistar:1148103083021320293>")
    async def fn(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122655473368314017
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122655473368314017>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122655473368314017>", ephemeral=True)

    @discord.ui.button(emoji="<:one:1146003619750105168>")
    async def mc(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122927309813461143
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122927309813461143>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122927309813461143>", ephemeral=True)


    @discord.ui.button(emoji="<:two:1146003617942351902>")
    async def roblox(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122928933575335936
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122928933575335936>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122928933575335936>", ephemeral=True)

    @discord.ui.button(emoji="<:three:1146003614691753994>")
    async def valo(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122926819553841162
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122926819553841162>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122926819553841162>", ephemeral=True)

    @discord.ui.button(emoji="<:four:1146003611227263047>")
    async def gta(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122926767192154142
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122926767192154142>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122926767192154142>", ephemeral=True)

    @discord.ui.button(emoji="<:five:1146003609125916712>")
    async def honkai(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1122926835936809090
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1122926835936809090>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1122926835936809090>", ephemeral=True)

    @discord.ui.button(emoji="<:six:1146003606835834951>")
    async def genshin(self, interaction: discord.Interaction, button: discord.Button):
        role_id = 1129219295310794874
        role = interaction.guild.get_role(role_id)
        
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"You have removed <@&1129219295310794874>", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You have selected <@&1129219295310794874>", ephemeral=True)

class kanzen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def info(self, ctx):
        embed = discord.Embed(description="### Welcome!\n> Thank you for joining Kanzengrp! We hope you have a good time!\n> If you ever need any help feel free to ping @lead or @staff\n> \n> To get the logos press the logos button below! And if you need\n> to send an inactivity message, you can click the inactive button!", color=0x2b2d31)
        view = infobuttons()
        embed2 = discord.Embed(description='### Group Rules:\n<a:Arrow_1:1145603161701224528> always watermark the logos\n<a:Arrow_1:1145603161701224528> do not share the logos link outside the server!\n<a:Arrow_1:1145603161701224528> make sure you are following [@remqsi](https://www.instagram.com/kanzengrp/) + [@kanzengrp](https://www.instagram.com/kanzengrp/)\n<a:Arrow_1:1145603161701224528> if you do ever decide to leave the grp, or move accounts. please let lead or staff know!\n\n### Chat Rules:\n<a:Arrow_1:1145603161701224528> please be as active as possible!\n<a:Arrow_1:1145603161701224528> no using any slurs / words that can be offensive!\n<a:Arrow_1:1145603161701224528> please set your nickname as "your name | username"\n<a:Arrow_1:1145603161701224528> no impersonation as other editors\n<a:Arrow_1:1145603161701224528> no trash talking other editors and groups!', color=0x2b2d31)
        embed2.set_image(url="https://cdn.discordapp.com/attachments/1121841074512605186/1154928824421728276/banner_welc_00000.png")
        embed.set_author(name="Kanzengrp", icon_url="https://cdn.discordapp.com/icons/1121841073673736215/a_2589a17d1463e51248bd02fd9af3e01a.gif?size=1024")
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2, view=view)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def iamembers(self, ctx):
        try:
            with open('inactive_members.json', 'r') as file:
                inactive_members = json.load(file)

            member_list = '\n'.join(inactive_members.values())
            if member_list:
                await ctx.send(f'Inactive Members:\n{member_list}')
            else:
                await ctx.send('No inactive members found.')

        except FileNotFoundError:
            await ctx.send('No inactive members found.')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def iawipe(self, ctx):
        try:
            with open('inactive_members.json', 'w') as file:
                json.dump({}, file)
            
            await ctx.send('Inactive members list has been wiped.')

        except Exception as e:
            await ctx.send(f'An error occurred: {str(e)}')

    @app_commands.command(name='ia', description='Send an inactive message!')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def auralogos(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ia())

    @commands.command()
    async def rroles(self, ctx):
        select = Select(
            placeholder="Select a role",
            options=[
                discord.SelectOption(label="red", value="red", emoji="<:red:1123256597167231076>"),
                discord.SelectOption(label="peach", value="peach", emoji="<:peach:1123256601365725247>"),
                discord.SelectOption(label="orange", value="orange", emoji="<:orange:1123256593316855962>"),
                discord.SelectOption(label="yellow", value="yellow", emoji="<:yellow:1123256589160304712>"),
                discord.SelectOption(label="light green", value="light green", emoji="<:lightgreen:1123256587981693018>"),
                discord.SelectOption(label="green", value="green", emoji="<:green:1123260467721277634>"),
                discord.SelectOption(label="teal", value="teal", emoji="<:teal:1123256594654830673>"),
                discord.SelectOption(label="light teal", value="light teal", emoji="<:lightteal:1123256585326702703>"),
                discord.SelectOption(label="light blue", value="light blue", emoji="<:lightblue:1123256581417615390>"),
                discord.SelectOption(label="blue", value="blue", emoji="<:blue:1123256591819481150>"),
                discord.SelectOption(label="purple", value="purple", emoji="<:purple:1123256504741527652>"),
                discord.SelectOption(label="lavender", value="lavender", emoji="<:lavender:1123256583917420545>"),
                discord.SelectOption(label="pink", value="pink", emoji="<:pink:1123256905289191484>"),
                discord.SelectOption(label="light pink", value="light pink", emoji="<:lightpink:1123256598496813127>"),
                discord.SelectOption(label="white", value="white", emoji="<:white:1123256528602927154>"),
                discord.SelectOption(label="black", value="black", emoji="<:black:1123256580100587681>")
            ]
        )
        async def add_role(interaction: discord.Interaction):
            await interaction.response.defer()
            role_ids = {
                "red": 1122919355273986138,
                "peach": 1122920134223335524,
                "orange": 1122920245267542106,
                "yellow": 1122920319557046413,
                "light green": 1122920394735763526,
                "green": 1122920478194028646,
                "teal": 1122920653876633670,
                "light teal": 1122920539766407178,
                "light blue": 1122920731529973841,
                "blue": 1122920821216792617,
                "purple": 1122920986086477964,
                "lavender": 1122920902858899456,
                "pink": 1122921065744707634,
                "light pink": 1122921134174769304,
                "white": 1122921232145338480,
                "black": 1122921204630696009,
            }
            
            member = interaction.user
            selected_value = interaction.data["values"][0]
            selected_role_id = role_ids.get(selected_value)
            
            for role_id in role_ids.values():
                role = interaction.guild.get_role(role_id)
                if role and role in member.roles:
                    await member.remove_roles(role)
            
            if selected_role_id:
                role = interaction.guild.get_role(selected_role_id)
                if role:
                    await member.add_roles(role)
                    await interaction.followup.send(f"You selected {selected_value}", ephemeral=True)
                else:
                    await interaction.followup.send("Role not found. Please contact a server admin.", ephemeral=True)
            else:
                await interaction.followup.send("Invalid role selection. Please try again.", ephemeral=True)

        select.callback = add_role
        view = View(timeout=None)
        view.add_item(select)

        embed = discord.Embed(title="<a:kanzenflower:1128154723262943282> Colours", description="<:red:1123256597167231076><@&1122919355273986138> \n<:peach:1123256601365725247><@&1122920134223335524> \n<:orange:1123256593316855962><@&1122920245267542106> \n<:yellow:1123256589160304712><@&1122920319557046413> \n<:lightgreen:1123256587981693018><@&1122920394735763526> \n<:green:1123260467721277634><@&1122920478194028646> \n<:teal:1123256594654830673><@&1122920653876633670> \n<:lightteal:1123256585326702703><@&1122920539766407178> \n<:lightblue:1123256581417615390><@&1122920731529973841> \n<:blue:1123256591819481150><@&1122920821216792617> \n<:purple:1123256504741527652><@&1122920986086477964> \n<:lavender:1123256583917420545><@&1122920902858899456> \n<:pink:1123256905289191484><@&1122921065744707634> \n<:lightpink:1123256598496813127><@&1122921134174769304> \n<:white:1123256528602927154><@&1122921232145338480> \n<:black:1123256580100587681><@&1122921204630696009>", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text="Use the drop down menu to select/deselect a role!")
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def rroles3(self, ctx):
        embed = discord.Embed(title="<a:kanzenflower:1128154723262943282> Pronouns", description="<:one:1146003619750105168><@&1121852424353755137> \n<:two:1146003617942351902><@&1122635691487137884> \n<:three:1146003614691753994><@&1122635724559241317> \n<:four:1146003611227263047><@&1122635760445706321> \n<:five:1146003609125916712><@&1122635742229835897> \n<:six:1146003606835834951><@&1122635791844266064>", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text="Use the buttons to select/deselect a role!")
        view=pronouns()
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def rroles2(self, ctx):
        embed = discord.Embed(title="<a:kanzenflower:1128154723262943282> Programs", description="<:aftereffects:1139953449954447380> <@&1122921620047147131> \n<:alightmotion:1139953459303546940> <@&1122921640288850025>\n<:sonyvegas:1139953453813223444> <@&1139954079506911303> \n<:videostar:1139953847784194119> <@&1122921660320858274> \n<:funimate:1139953446552879156> <@&1139954125560365116> \n<:cutecut:1139953845057896549> <@&1139954104383324240> \n<:capcut:1139953436058722436> <@&1139954142215942255>", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text="Use the buttons to select/deselect a role!")
        view=Programs()
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def rroles4(self, ctx):
        embed = discord.Embed(title="<a:kanzenflower:1128154723262943282> Games", description="<:fortnite:1123259326006571090> <@&1122921698367389756> \n<:MCicon:1123259350522282025> <@&1122979205324480553> \n<:ROBLOXicon:1123259382063443968> <@&1122921713823395851> \n<:Valoranticon:1123259406092611654> <@&1122921729384271963> \n<:gtaV:1123259437637980183> <@&1122921800502878259> \n<:honkai:1139958684324216934> <@&1139957904712142932> \n<:genshin:1139958246526951464> <@&1122921755216973854> \n<:phasmophobia:1139962251453927556> <@&1139962329950343208>", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text="Use the buttons to select/deselect a role!")
        view=games()
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def rroles5(self, ctx):
        embed = discord.Embed(title="<a:kanzenflower:1128154723262943282> Other", description="<:hoshistar:1148103083021320293> <@&1122655473368314017> \n<:one:1146003619750105168> <@&1122927309813461143> \n<:two:1146003617942351902> <@&1122928933575335936> \n<:three:1146003614691753994> <@&1122926819553841162> \n<:four:1146003611227263047> <@&1122926767192154142> \n<:five:1146003609125916712> <@&1122926835936809090> \n<:six:1146003606835834951> <@&1129219295310794874>", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text="Use the buttons to select/deselect a role!")
        view=other()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(kanzen(bot))