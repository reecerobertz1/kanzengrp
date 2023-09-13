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

class trickortreat(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Join", emoji="<a:pumpkin:1151485353585295475>")
    async def Join(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(tt())

class tt(ui.Modal, title='Trick or Treat'):
    instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
    biases = ui.TextInput(label='Who do you want your partner to edit?', placeholder="", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            with open('biases.json', 'r') as file:
                biases_data = json.load(file)
        except FileNotFoundError:
            biases_data = []
        user_data = {
            'instagram': self.instagram.value,
            'reason': self.biases.value
        }
        biases_data.append(user_data)
        with open('biases.json', 'w') as file:
            json.dump(biases_data, file, indent=4)
        await interaction.followup.send(f'You have joined the tick or treat event!', ephemeral=True)

class infobuttons(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Logos", emoji="<:tata:1121909389280944169>")
    async def guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = getlogos()
        logos = discord.Embed(title="<a:kanzenflower:1128154723262943282>  Kanzen Logos!", description="<a:Arrow_1:1145603161701224528> Please make sure you watermark the logos!\n<a:Arrow_1:1145603161701224528> Use the watermark on every edit\n<a:Arrow_1:1145603161701224528> Do not share this link with anyone outside the group!", color=0x2b2d31)
        logos.set_footer(text="Made us some logos? send them to Reece!")
        logos.set_image(url="https://cdn.discordapp.com/attachments/849724031723634688/1145605654539669565/new_banner_00000.png")
        await interaction.user.send(embed=logos, view=view)

        channel = interaction.client.get_channel(1122627075682078720)
        log = discord.Embed(title="Logo button has been used!", description=f"`{interaction.user.display_name}` has used the logos button", color=0x2b2d31)
        log.set_footer(text=f"id: {interaction.user.id}", icon_url=interaction.user.display_avatar)
        await channel.send(embed=log)
        await interaction.response.send_message(f'I have sent you the logos! Check your DMs', ephemeral=True)

    @discord.ui.button(label="Inactive", emoji="<:mang:1121909428866793582>")
    async def inactive(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(ia())

    @discord.ui.button(label="Suggest", emoji="<:rj:1121909526300479658>")
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
    instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
    reason = ui.TextInput(label='Inactivity Reason', placeholder="", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        user_id = interaction.user.id
        user_mention = f'<@{user_id}>'
        inactive_members = []

        # Try to load existing data from the JSON file
        try:
            with open('inactive_members.json', 'r') as file:
                inactive_members = json.load(file)
        except FileNotFoundError:
            pass

        # Append the current user's data to the list
        user_data = {
            'instagram': self.instagram.value,
            'reason': self.reason.value
        }
        inactive_members.append(user_data)

        # Save the updated data to the JSON file
        with open('inactive_members.json', 'w') as file:
            json.dump(inactive_members, file)

        embed = discord.Embed(title='Inactivity Message', color=0x2b2d31)
        embed.add_field(name='Instagram Name:', value=f'{self.instagram.value}', inline=False)
        embed.add_field(name='Instagram Account Link:', value=f'https://instagram.com/{self.instagram.value}', inline=False)
        embed.add_field(name='Inactivity Reason:', value=f'{self.reason.value}', inline=False)
        embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
        channel = interaction.client.get_channel(1121913672822968330)
        await channel.send(embed=embed)
        await interaction.followup.send(f'Your inactive message has been sent successfully', ephemeral=True)



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

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def info(self, ctx):
        embed = discord.Embed(description="## Welcome *!*\nThank you for joining Kanzengrp! We hope you have a good time!  ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏\nIf you ever need any help feel free to ping @lead or @staff\n\nTo get the logos press the `logos` button below! And if you need\nto send an inactivity message, you can click the `inactive` button!", color=0x2b2d31)
        view = infobuttons()
        embed2 = discord.Embed(title="<a:kanzenflower:1128154723262943282> Kanzen rules ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏ ͏ ͏ ͏ ͏", description='✦ Group Rules :\n<a:Arrow_1:1145603161701224528> always watermark the logos\n<a:Arrow_1:1145603161701224528> do not share the logos link outside the server!\n<a:Arrow_1:1145603161701224528> make sure you are following [@remqsi](https://www.instagram.com/remqsi/) + [@kanzengrp!](https://www.instagram.com/kanzengrp/)\n<a:Arrow_1:1145603161701224528> if you do ever decide to leave the grp, or move accounts. please let lead or staff know!\n\n✦ Chat Rules :\n<a:Arrow_1:1145603161701224528> please be as active as possible!\n<a:Arrow_1:1145603161701224528> no using any slurs / words that can be offensive!\n<a:Arrow_1:1145603161701224528> please set your nickname as "your name | username"\n<a:Arrow_1:1145603161701224528> no impersonation as other editors\n<a:Arrow_1:1145603161701224528> no trash talking other editors and groups!', color=0x2b2d31)
        embed2.set_image(url="https://cdn.discordapp.com/attachments/1121841074512605186/1148046433858113536/kgrp_00000_00000.png")
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
    async def halloweentot(self, ctx):
        view=trickortreat()
        await ctx.send("🎃 **HALLOWEEN TRICK OR TREAT**\nThis year, instead of Secret Santa, we're doing a Halloween twist!\n\n**HOW IT WORKS:**\n- Everyone gets paired up randomly.\n- Click the ''join'' button below and share your Instagram username and a list of your favorite things (if you have a long list, just send your top favorites).\n- Now, you can either make your partner's day by sharing something they love or play a little trick by sharing something related to someone else.\n- Don't forget to use __**#kanzentrickortreat**__ when you share your post.\n- If you join, you'll get a message from <@849682093575372841> on October 1st with your partner's details.\n\n**EXTRA INFO:**\n- Participating in this event earns you **3500xp**.\n- You can post your edit anytime in October.\n@everyone", view=view)

    @commands.command()
    async def totpartners(self, ctx):
        try:
            with open('biases.json', 'r') as file:
                biases_data = json.load(file)
        except FileNotFoundError:
            biases_data = []
        random.shuffle(biases_data)
        pairs = []
        for i in range(0, len(biases_data), 2):
            user1_data = biases_data[i]
            user2_data = biases_data[i + 1] if i + 1 < len(biases_data) else None

            user1_instagram = user1_data.get('instagram', 'No Instagram')
            user2_instagram = user2_data.get('instagram', 'No Instagram') if user2_data else "No partner"

            user1_reason = user1_data.get('reason', 'No Reason')
            user2_reason = user2_data.get('reason', 'No Reason') if user2_data else "No Reason"

            pairs.append(f"**Partners**\n\"{user1_instagram}\" - \"{user1_reason}\"\n\"{user2_instagram}\" - \"{user2_reason}\"")
        await ctx.send('\n'.join(pairs))

    @commands.command()
    async def dmpartner(self, ctx, user: discord.Member, *, message: str):
        embed = discord.Embed(title="**Halloween Trick or Treat**", description=message, color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(text="Have fun Trick or Treating!", icon_url=user.avatar)
        await user.send(embed=embed)

async def setup(bot):
    await bot.add_cog(kanzen(bot))