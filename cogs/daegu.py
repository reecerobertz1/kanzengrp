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

    @discord.ui.button(label="Inactivity")
    async def inactive(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(ia())

    @discord.ui.button(label="Feedback")
    async def feedback(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(fb())

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

class fb(ui.Modal, title='Feedback'):
    feedback = ui.TextInput(label='Inactivity Reason', placeholder="", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title='Feedback', description=self.feedback.value, color=0x2b2d31)
        embed.set_footer(text=f"sent from {interaction.user} | {interaction.user.id}", icon_url=interaction.user.display_avatar)
        channel = interaction.client.get_channel(1102977351010222101)
        await channel.send(embed=embed)
        await interaction.followup.send(f'Your feedback has been sent successfully', ephemeral=True)

class daegu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.emoji = "<:tata:1121909389280944169>"

    @commands.command()
    async def daeguinfolmao(self, ctx):
        embed = discord.Embed(title="Welcome to <:DT:1118106614721937408> Daegutowngrp", description="This group is owned by [@dtqwn](https://www.instagram.com/dtqwn) + [@dqrkwld](https://www.instagram.com/dqrkwld)\nThank you so much for joining, we hope you have a great time here\n\nIf you ever feel like you need any help, feel free to ask the leads or staff", color=0x2b2d31)

        embed.set_author(name="Daegutown", icon_url=ctx.guild.icon)
        embed2 = discord.Embed(color=0x2b2d31)
        embed2.set_image(url="https://cdn.discordapp.com/attachments/1121841074512605186/1154928824421728276/banner_welc_00000.png")
        embed2.add_field(name="**✦ GROUP RULES** ***!***", value="<a:inf_redarrow2:1063174893782446130> Follow Discord's Terms of Service and Guidelines at all times.\n<a:inf_redarrow2:1063174893782446130> Watermark logos + use the group hashtag\n<a:inf_redarrow2:1063174893782446130> Never share the logos link to anyone outside of Daegu.\nThis will result in you being kicked from the group\n<a:inf_redarrow2:1063174893782446130> Make sure you are following Dtqwn + Dqrkwld\n<a:inf_redarrow2:1063174893782446130> Also make sure you follow either our TikTok or Instagram or both", inline=False)
        embed2.add_field(name="**✦ CHAT RULES** ***!***", value="<a:inf_redarrow2:1063174893782446130> Please be as active as possible\n<a:inf_redarrow2:1063174893782446130> English chat only (other languages can be hard to moderate)\n<a:inf_redarrow2:1063174893782446130> Please set your discord nickname to “name | username”\n<a:inf_redarrow2:1063174893782446130> No impersonation as other editors\n<a:inf_redarrow2:1063174893782446130> Do spam / promotion in designated channels\n<a:inf_redarrow2:1063174893782446130> Don't say offensive stuff that will make others uncomfortable\n<a:inf_redarrow2:1063174893782446130> No trash talk of other editors / groups\n<a:inf_redarrow2:1063174893782446130> If you move accounts or leave please remember to tell leads", inline=False)
        view = infobuttons()
        message = await ctx.send(embed=embed)
        await ctx.send(embed=embed2, view=view)

async def setup(bot):
    await bot.add_cog(daegu(bot))