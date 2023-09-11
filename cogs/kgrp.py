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

class kgrp(commands.Cog):
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

class ia(ui.Modal, title='Inactivity Message'):
     instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     reason = ui.TextInput(label='Inactivity Reason', placeholder="", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          user_id = interaction.user.id
          user_mention = f'<@{user_id}>'
          inactive_members = {}
          try:
              with open('inactive_members.json', 'r') as file:
                  inactive_members = json.load(file)
          except FileNotFoundError:
              pass

          inactive_members[user_id] = user_mention
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

async def setup(bot):
    await bot.add_cog(kgrp(bot))