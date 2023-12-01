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

    @discord.ui.button(label="Reviewer")
    async def review(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(review())

    @discord.ui.button(label="Staff")
    async def staff(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(staff())

class staffapps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.emoji = "<:shooky:1121909564799987722>"

    @commands.command()
    async def no(self, ctx):
        if ctx.message.reference is not None:
            try:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                embed = msg.embeds[0]
                user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)

                if not user_id_field:
                    await ctx.send("Invalid embed format. 'Discord ID'.")
                    return

                user_id = user_id_field.value.strip()
                user = self.bot.get_user(int(user_id))

                embed = msg.embeds[0]
                embed.add_field(name="Status", value="Declined ❌")
                await ctx.message.add_reaction("✅")
                await msg.edit(embed=embed)
            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply with the embed you want to process.")

    @commands.command()
    async def yes(self, ctx):
        if ctx.message.reference is not None:
            try:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                embed = msg.embeds[0]
                user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)
                role_field = next((field for field in embed.fields if field.name == 'Role:'), None)

                if not user_id_field or not role_field:
                    await ctx.send("Invalid embed format. 'Discord ID' and 'Role' fields are required.")
                    return

                user_id = user_id_field.value.strip()
                user = ctx.guild.get_member(int(user_id))

                if user:
                    role_name = role_field.value.strip().lower()
                    if role_name == 'staff':
                        role = discord.utils.get(ctx.guild.roles, name='staff')
                    elif role_name == 'mod':
                        role = discord.utils.get(ctx.guild.roles, name='mods')
                    elif role_name == 'reviewer':
                        role = discord.utils.get(ctx.guild.roles, name='judges')
                    else:
                        role = None

                    if role:
                        await user.add_roles(role)

                    accept_message = f"Your application for {role_name} has been accepted!\nPlease go to this channel https://discord.com/channels/1131003330810871979/1131018131813441696 and we will give you more information shortly!\nThank you for wanting to be apart of our team!"
                    await user.send(accept_message)

                    channel = ctx.guild.get_channel(1131006361921130526)
                    if channel:
                        await channel.send(f"{user.mention} was accepted as {role_name}")

                embed.add_field(name="Status", value="Accepted ✅")
                await ctx.message.add_reaction("✅")
                await msg.edit(embed=embed)
            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply with the embed you want to process.")

    @app_commands.command(name='staff', description="Apply for Editors Block's staff")
    @app_commands.guilds(discord.Object(id=1131003330810871979))
    async def staff(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Staff Applications", description="Thank you for wanting to be apart of our team! here is some information about each role before you apply!", color=0x2b2d31)
        embed.add_field(name="moderator", value="as a moderator, you will welcome new members who join the server and help to moderate and keep the chat as active as possible. you can also host events such as movie and game nights!", inline=False)
        embed.add_field(name="reviewer", value="as a reviewer you will review group applications for kanzen, aura and daegu, you will be able to accept or decline applications but remember to judge every app ona non biased perspective", inline=False)
        embed.add_field(name="staff", value="as a staff member, you will help the leads with group activities and managing members of the server", inline=False)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text="Please make sure you fill out each form fully", icon_url=interaction.user.avatar)
        view=roles()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
class staff(ui.Modal, title='Staff Applications'):
    one = ui.TextInput(label='whats your instagram username?', placeholder="enter your instagram username", style=discord.TextStyle.long)
    two = ui.TextInput(label='why do you want to be apart of our staff?', placeholder="i want to become editors block staff because...", style=discord.TextStyle.long)
    three = ui.TextInput(label='what do you bring to the table?', placeholder="list things you want to bring to editors block...", style=discord.TextStyle.long)
    four = ui.TextInput(label="how active are you scale of 1 - 10?", placeholder="enter your activity rate here", style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title='Staff Applications',description=f"**what's their instagram:**\n{self.one.value}\n\n**why do you want to be apart of editors block staff?:**\n{self.two.value}\n\n**what do you bring to the table?:**\n{self.three.value}\n\n**how active are you scale of 1 - 10?:**\n{self.four.value}" ,color=0x2b2d31)
        embed.set_footer(text=f"sent from: {interaction.user.name}", icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
        embed.add_field(name="Role:", value="staff", inline=False)
        channel = interaction.client.get_channel(1178430932416479282)
        await channel.send(embed=embed)
        await interaction.followup.send(f'thank you {interaction.user.display_name} for applying for editors block staff!', ephemeral=True)

class mod(ui.Modal, title='Moderator Applications'):
    one = ui.TextInput(label='whats your instagram username?', placeholder="enter your instagram username", style=discord.TextStyle.long)
    two = ui.TextInput(label='why should we choose you to be a moderator?', placeholder="i want to become editors block staff because...", style=discord.TextStyle.long)
    three = ui.TextInput(label='any experience have in moderating servers?', placeholder="what expirience do you have? list here...", style=discord.TextStyle.long)
    four = ui.TextInput(label='what activities would you like to host?', placeholder="list activities here...", style=discord.TextStyle.long)
    five = ui.TextInput(label="how active are you scale of 1 - 10?", placeholder="enter your activity rate here", style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title='Moderator Applications',description=f"**what's their instagram:**\n{self.one.value}\n\n**why do you want to be apart of the editors block moderator team?:**\n{self.two.value}\n\n**do you have any expirience in moderating servers?:**\n{self.three.value}\n\n**what kind of activities would you like to do in editors block?**\n{self.four.value}\n\n**how active are you scale of 1 - 10?:**\n{self.five.value}" ,color=0x2b2d31)
        embed.set_footer(text=f"sent from: {interaction.user.name}", icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
        embed.add_field(name="Role:", value="mod", inline=False)
        channel = interaction.client.get_channel(1178430932416479282)
        await channel.send(embed=embed)
        await interaction.followup.send(f'thank you {interaction.user.display_name} for applying for editors block staff!', ephemeral=True)

class review(ui.Modal, title='Reviewer Applications'):
    one = ui.TextInput(label='whats your instagram username?', placeholder="enter your instagram username", style=discord.TextStyle.long)
    two = ui.TextInput(label='what do you look for when reviewing?', placeholder="list here...", style=discord.TextStyle.long)
    three = ui.TextInput(label='any experience in reviewing apps?', placeholder="list things you want to bring to editors block...", style=discord.TextStyle.long)
    four = ui.TextInput(label="how active are you scale of 1 - 10?", placeholder="enter your activity rate here", style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title='Reviewer Applications',description=f"**what's their instagram:**\n{self.one.value}\n\n**what do you look for when reviewing?:**\n{self.two.value}\n\n**any experience in reviewing apps?:**\n{self.three.value}\n\n**how active are you scale of 1 - 10?:**\n{self.four.value}" ,color=0x2b2d31)
        embed.set_footer(text=f"sent from: {interaction.user.name}", icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
        embed.add_field(name="Role:", value="reviewer", inline=False)
        channel = interaction.client.get_channel(1178430932416479282)
        await channel.send(embed=embed)
        await interaction.followup.send(f'thank you {interaction.user.display_name} for applying for editors block staff!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(staffapps(bot))