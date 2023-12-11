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

class roles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Moderator")
    async def mod(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(mod())

    @discord.ui.button(label="Staff")
    async def staff(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(staff())

class mod(ui.Modal, title='Moderator Applications'):
    one = ui.TextInput(label='whats your instagram username?', placeholder="enter your instagram username", style=discord.TextStyle.long)
    two = ui.TextInput(label='why do you want to be apart of our staff?', placeholder="i want to become kanzens staff because...", style=discord.TextStyle.long)
    three = ui.TextInput(label='what do you bring to the table?', placeholder="list things you want to bring to kanzens...", style=discord.TextStyle.long)
    four = ui.TextInput(label="how active are you scale of 1 - 10?", placeholder="enter your activity rate here", style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title='Moderator Applications',description=f"**what's their instagram:**\n{self.one.value}\n\n**why do you want to be apart of kanzens staff?:**\n{self.two.value}\n\n**what do you bring to the table?:**\n{self.three.value}\n\n**how active are you scale of 1 - 10?:**\n{self.four.value}" ,color=0x2b2d31)
        embed.set_footer(text=f"sent from: {interaction.user.name}", icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
        embed.add_field(name="Role:", value="mod", inline=False)
        channel = interaction.client.get_channel(1178976893861646366)
        await channel.send(embed=embed)
        await interaction.followup.send(f'thank you {interaction.user.display_name} for applying for kanzens staff!', ephemeral=True)

class staff(ui.Modal, title='Staff Applications'):
    one = ui.TextInput(label='whats your instagram username?', placeholder="enter your instagram username", style=discord.TextStyle.long)
    two = ui.TextInput(label='why should we choose you to be a staff?', placeholder="i want to become kanzens staff because...", style=discord.TextStyle.long)
    three = ui.TextInput(label='any experience have being staff?', placeholder="what expirience do you have? list here...", style=discord.TextStyle.long)
    four = ui.TextInput(label='what activities would you like to host?', placeholder="list activities here...", style=discord.TextStyle.long)
    five = ui.TextInput(label="how active are you scale of 1 - 10?", placeholder="enter your activity rate here", style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title='Staff Applications',description=f"**what's their instagram:**\n{self.one.value}\n\n**why do you want to be apart of the kanzens staff team?:**\n{self.two.value}\n\n**do you have any expirience being staff?:**\n{self.three.value}\n\n**what kind of activities would you like to do in kanzens?**\n{self.four.value}\n\n**how active are you scale of 1 - 10?:**\n{self.five.value}" ,color=0x2b2d31)
        embed.set_footer(text=f"sent from: {interaction.user.name}", icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
        embed.add_field(name="Role:", value="staff", inline=False)
        channel = interaction.client.get_channel(1178976893861646366)
        await channel.send(embed=embed)
        await interaction.followup.send(f'thank you {interaction.user.display_name} for applying for kanzens staff!', ephemeral=True)

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

    @discord.ui.button(label="Server Roles")
    async def roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Kanzen Roles", description="<:lead:1181429630029275136> - is for the kanzen lead\n<:headstaff:1181430061333745724> - is for head staff\n<:mods:1181430661588987944> - is for moderators\n<:staff:1181429748191199244> - is for staff\n<:trainee:1181430659902885929> - is for trainee staff\n<:devs:1181430657520504882> - is for hoshi developers\n<:boosters:1181430064584347729> - is for kanzen boosters\n<:top20:1181430063397339136> - is for the top 20 active members\n<:zennie:1181430664415948870> - is for everyone", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.user.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Booster Perks")
    async def bp(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Kanzen Perks", description="<a:Arrow_1:1145603161701224528> Remqsi's colouring packs 1 & 2\n<a:Arrow_1:1145603161701224528> BTS Photos\n<a:Arrow_1:1145603161701224528> Enhypen Photos\n<a:Arrow_1:1145603161701224528> Blackpink Photos\n<a:Arrow_1:1145603161701224528> Break your heart project file\n<a:Arrow_1:1145603161701224528> Lisa candy project file", color=0x2b2d31)
        embed.set_footer(text="This is just a preview, only boosters get the link")
        embed.set_thumbnail(url=interaction.user.display_avatar)
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
    instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
    reason = ui.TextInput(label='Inactivity Reason', placeholder="", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        user_id = interaction.user.id
        user_mention = f'<@{user_id}>'
        inactive_members = []
        try:
            with open('inactive_members.json', 'r') as file:
                inactive_members = json.load(file)
        except FileNotFoundError:
            pass
        user_data = {
            'instagram': self.instagram.value,
            'reason': self.reason.value
        }
        inactive_members.append(user_data)
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

    @discord.ui.button(emoji="<:fn:1173123421123645471>")
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
        self.emoji = "<:shooky:1121909564799987722>"

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def info(self, ctx):
        embed = discord.Embed(title="Welcome!", description="> Thank you for joining Kanzengrp! We hope you have a good time!\n> If you ever need any help feel free to ping @lead or @staff\n> \n> To get the logos press the logos button below! And if you need\n> to send an inactivity message, you can click the inactive button!", color=0x2b2d31)

        embed.set_author(name="Kanzengrp", icon_url=ctx.guild.icon)
        embed2 = discord.Embed(description='**Group Rules**\n<a:Arrow_1:1145603161701224528> always watermark the logos\n<a:Arrow_1:1145603161701224528> do not share the logos link outside the server!\n<a:Arrow_1:1145603161701224528> make sure you are following [@remqsi](https://www.instagram.com/remqsi/) + [@kanzengrp](https://www.instagram.com/kanzengrp/)\n<a:Arrow_1:1145603161701224528> if you do ever decide to leave the grp, or move accounts. please let lead or staff know!\n\n**Chat Rules**\n<a:Arrow_1:1145603161701224528> please be as active as possible!\n<a:Arrow_1:1145603161701224528> no using any slurs / words that can be offensive!\n<a:Arrow_1:1145603161701224528> please set your nickname as "your name | username"\n<a:Arrow_1:1145603161701224528> no impersonation as other editors\n<a:Arrow_1:1145603161701224528> no trash talking other editors and groups!\n<a:Arrow_1:1145603161701224528> any rules above broken, you will receive a warning/get kicked', color=0x2b2d31)
        embed2.set_image(url="https://cdn.discordapp.com/attachments/1121841074512605186/1183779211601784862/banner_welc_00000.png?ex=6589934d&is=65771e4d&hm=e90a438ad4160e550252f72311044a4f69f20dd7817f13f2fa102c7fb1ce6aec&")
        view = infobuttons()
        ttbutton = discord.ui.Button(label=f"Tiktok", url=f"https://www.tiktok.com/@kanzengrp?_t=8hBEO47Fw37&_r=1", emoji="<:tiktok:1171995663890911273>")
        igbutton = discord.ui.Button(label=f"Instagram", url=f"https://www.instagram.com/kanzengrp/", emoji="<:insta:1171995666382336040>")
        card = discord.ui.Button(label=f"Carrd", url=f"https://kanzengrp.carrd.co", emoji="<:carrd:1173159791988838430>")
        button_view = discord.ui.View()
        button_view.add_item(ttbutton)
        button_view.add_item(igbutton)
        button_view.add_item(card)

        message = await ctx.send(embed=embed, view=button_view)
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
                discord.SelectOption(label="red", value="red", emoji="<:red:1173122695479701534>"),
                discord.SelectOption(label="peach", value="peach", emoji="<:peach:1173122698155671673>"),
                discord.SelectOption(label="orange", value="orange", emoji="<:orange:1173122699497840721>"),
                discord.SelectOption(label="yellow", value="yellow", emoji="<:yellow:1173122700953264158>"),
                discord.SelectOption(label="light green", value="light green", emoji="<:lightgreen:1173122703239163974>"),
                discord.SelectOption(label="green", value="green", emoji="<:green:1173122704870748170>"),
                discord.SelectOption(label="teal", value="teal", emoji="<:teal:1173122709127962674>"),
                discord.SelectOption(label="light teal", value="light teal", emoji="<:lightteal:1173122707211169842>"),
                discord.SelectOption(label="light blue", value="light blue", emoji="<:lightblue:1173122711682289674>"),
                discord.SelectOption(label="blue", value="blue", emoji="<:lightblue:1173122711682289674>"),
                discord.SelectOption(label="purple", value="purple", emoji="<:purple:1173122714433757294>"),
                discord.SelectOption(label="lavender", value="lavender", emoji="<:lavander:1173122716694478868>"),
                discord.SelectOption(label="pink", value="pink", emoji="<:pink:1173122763796529283>"),
                discord.SelectOption(label="light pink", value="light pink", emoji="<:lightpink:1173122766225014854>"),
                discord.SelectOption(label="white", value="white", emoji="<:white:1173122767747547147>"),
                discord.SelectOption(label="black", value="black", emoji="<:black:1173122722675568730>")
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

        embed = discord.Embed(title="<a:kanzenflower:1128154723262943282> Colours", description="<:red:1173122695479701534><@&1122919355273986138> \n<:peach:1173122698155671673><@&1122920134223335524> \n<:orange:1173122699497840721><@&1122920245267542106> \n<:yellow:1173122700953264158><@&1122920319557046413> \n<:lightgreen:1173122703239163974><@&1122920394735763526> \n<:green:1173122704870748170><@&1122920478194028646> \n<:teal:1173122709127962674><@&1122920653876633670> \n<:lightteal:1173122707211169842><@&1122920539766407178> \n<:lightblue:1173122711682289674><@&1122920731529973841> \n<:lightblue:1173122711682289674><@&1122920821216792617> \n<:purple:1173122714433757294><@&1122920986086477964> \n<:lavander:1173122716694478868><@&1122920902858899456> \n<:pink:1173122763796529283><@&1122921065744707634> \n<:lightpink:1173122766225014854><@&1122921134174769304> \n<:white:1173122767747547147><@&1122921232145338480> \n<:black:1173122722675568730><@&1122921204630696009>", color=0x2b2d31)
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
        embed = discord.Embed(title="<a:kanzenflower:1128154723262943282> Games", description="<:fn:1173123421123645471> <@&1122921698367389756> \n<:MCicon:1123259350522282025> <@&1122979205324480553> \n<:ROBLOXicon:1123259382063443968> <@&1122921713823395851> \n<:Valoranticon:1123259406092611654> <@&1122921729384271963> \n<:gtaV:1123259437637980183> <@&1122921800502878259> \n<:honkai:1139958684324216934> <@&1139957904712142932> \n<:genshin:1139958246526951464> <@&1122921755216973854> \n<:phasmophobia:1139962251453927556> <@&1139962329950343208>", color=0x2b2d31)
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

    @commands.command()
    async def halloweentot(self, ctx):
        view=trickortreat()
        await ctx.send("🎃 **HALLOWEEN TRICK OR TREAT**\nThis year, instead of Secret Santa, we're doing a Halloween twist!\n\n**HOW IT WORKS:**\n- Everyone gets paired up randomly.\n- Click the ''join'' button below and share your Instagram username and a list of your favorite things (if you have a long list, just send your top favorites).\n- Now, you can either make your partner's day by sharing something they love or play a little trick by sharing something related to someone else.\n- Don't forget to use __**#kanzentrickortreat**__ when you share your post.\n- If you join, you'll get a message from <@849682093575372841> on October 1st with your partner's details.\n\n**EXTRA INFO:**\n- Participating in this event earns you **3500xp**.\n- You can post your edit anytime in October.", view=view)

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

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def staffapps(self, ctx):
        embed = discord.Embed(title="Kanzen Staff Apps", description="Thank you for wanting to apply to be apart of Kanzen's staff team! Here is some info for each role\n\n**Moderator**:\nHelp moderate the chat, delete messages and time-out members when needed! Use the warn commands with Hoshi as well, each member will have 3 warnings before being kicked, each warning will go after a month unless the receive another one. If you are abusing your power as an moderator, you will be removed and never added back as any type of staff\n\n**Staff**:\nStaff will help the lead and head staff out with group events, you can also host your own events too like watch parties and game nights. You cant host any collabs unless you have multiple going at once. You will also help out with server stuff, like making/deleting channels", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_footer(icon_url=ctx.author.avatar, text="Click the buttons below to apply! (only one)")
        view=roles()
        await ctx.reply(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(kanzen(bot))