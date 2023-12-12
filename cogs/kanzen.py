import json
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
        embed2.set_image(url="https://cdn.discordapp.com/attachments/849724031723634688/1184214617791135764/banner_welc_00000.png?ex=658b28ce&is=6578b3ce&hm=ced47c472a4fa18f179bbb7d836ed5873001ccfebb47f3d79d0b5f51df743ff0&")
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

async def setup(bot):
    await bot.add_cog(kanzen(bot))