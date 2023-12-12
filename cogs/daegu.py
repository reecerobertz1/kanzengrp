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

    @discord.ui.button(label="Inactive", emoji="<:DT:1118106614721937408>")
    async def inactive(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(ia())

    @discord.ui.button(label="Suggest", emoji="<:DT:1118106614721937408>")
    async def suggest(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(suggest())

    @discord.ui.button(label="Feedback", emoji="<:DT:1118106614721937408>")
    async def feedback(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(feedback())

class daegu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def info1(self, ctx):
        embed = discord.Embed(title="Welcome to <:DT:1118106614721937408> Daegutown Grp!", description="This group is owned by [@dtqwn](https://instagram.com/dtqwn) + [@dqrkwld](https://instagram.com/dqrkwld)\nThank you so much for joining, we hope you have a great time here\n\nIf you ever feel like you need any help, feel free to ask the leads or staffㅤ", color=0x2b2d31)
        view = infobuttons()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def info2(self, ctx):
        view = infobuttons()
        embed = discord.Embed(description='Introduce yourself here and remember to get your roles and biases!\nYou can find our group logos and hashtag [here](https://discord.com/channels/896619762354892821/897239740665974784) ㅤㅤㅤㅤㅤㅤ ㅤㅤㅤㅤㅤ', color=0x2b2d31)
        embed.add_field(name="** **", value="**✦ GROUP RULES** ***!***\n\n- Follow Discord's Terms of Service and Guidelines at all times.\n- Watermark logos + use the group hashtag\n- Never share the logos link to anyone outside of Daegu.\nThis will result in you being kicked from the group\n- Make sure you are following Remqsi + Dtqwn\n- Also make sure you follow either our TikTok or Instagram or both\n\n**✦ CHAT RULES** ***!***\n\n- Please be as active as possible\n- English chat only (other languages can be hard to moderate)\n- Please set your discord nickname to “name | username”\n- No impersonation as other editors\n- Do spam / promotion in designated channels\n- Don't say offensive stuff that will make others uncomfortable\n- No trash talk of other editors / groups\n- If you move accounts or leave please remember to tell leads")
        embed.set_footer(text="- Use the buttons below to view our server Information and rules")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1121841074512605186/1145605533974401104/kgrp_00000_00000.png")
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name='ia', description='Send an inactive message!')
    @app_commands.guilds(discord.Object(id=896619762354892821))
    async def daegulogos(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ia())

class ia(ui.Modal, title='Inactivity Message'):
     instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     reason = ui.TextInput(label='Inactivity Reason', placeholder="", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Inactivity Message', color=0x2b2d31)
          embed.add_field(name='Instagram Name:', value=f'{self.instagram.value}', inline=False)
          embed.add_field(name='Instagram Account Link:', value=f'https://instagram.com/{self.instagram.value}', inline=False)
          embed.add_field(name='Inactivity Reason:', value=f'{self.reason.value}', inline=False)
          embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
          channel = interaction.client.get_channel(1058814073380274326)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your inactive message has been sent successfully', ephemeral=True)

class feedback(ui.Modal, title='Feedback'):
     improve = ui.TextInput(label='Has daegu improved?', placeholder="Yes/No", style=discord.TextStyle.short)
     feedback = ui.TextInput(label='What is your feedback', placeholder="", style=discord.TextStyle.long)
     suggestions = ui.TextInput(label='Any suggestions?', placeholder="", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Member Feedback', color=0x2b2d31)
          embed.add_field(name='Has daegu improved?', value=f'{self.improve.value}', inline=False)
          embed.add_field(name='Members feedback:', value=f'{self.feedback.value}', inline=False)
          embed.add_field(name='Members suggestions:', value=f'{self.suggestions.value}', inline=False)
          embed.set_footer(text=f"{interaction.user.name} | {interaction.user.id}", icon_url=interaction.user.avatar)
          channel = interaction.client.get_channel(1102977351010222101)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your inactive message has been sent successfully', ephemeral=True)

class suggest(ui.Modal, title='Suggestions'):
     suggestion = ui.TextInput(label='What would you like to suggest?', placeholder="Put suggestion here...", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(description=f'suggestion: {self.suggestion.value}', color=0x2b2d31)
          embed.set_author(name=f"sent by {interaction.user.name}", icon_url=interaction.user.avatar)
          channel = interaction.client.get_channel(1150023727082373160)
          suggestion = await channel.send(embed=embed)
          await interaction.followup.send(f'Your suggestion has been sent successfully', ephemeral=True)
          await suggestion.add_reaction("<:LIKE:1146004608154607627>")
          await suggestion.add_reaction("<:DISLIKE:1146004603834478602>")

async def setup(bot):
    await bot.add_cog(daegu(bot))