from typing import Any
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import View, Select
from typing import List, Optional
from discord import ui

class infobuttons(discord.ui.View):
    def __init__ (self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Server Rules")
    async def rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Rules", color=0x2b2d31)
        embed.add_field(name="Chat Rules", value="GFHDJSKHGSDFGFDGJKFGKJJKGFKGHJKG")
        await interaction.response.send_message(embed=embed, ephemeral=True)    

    @discord.ui.button(label="Role Info")
    async def roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Rules", color=0x2b2d31)
        embed.add_field(name="Chat Rules", value="GFHDJSKHGSDFGFDGJKFGKJJKGFKGHJKG")
        await interaction.response.send_message(embed=embed, ephemeral=True)  

class appbuttons(discord.ui.View):
    def __init__ (self):
        super().__init__()
        self.value = None
        
    @discord.ui.button(label="Apply!")
    async def roles(self, interaction: discord.Interaction, button: discord.ui.Button):
         await interaction.response.send_modal(grprctkda())

class grprctkda(ui.Modal, title='Applications'):
     instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     edit = ui.TextInput(label='Edit link (Instagran or Streamable)', placeholder="Paste link here...", style=discord.TextStyle.short)
     grps = ui.TextInput(label='What group(s) do you want to join?', placeholder="Kanzen, Aura, Daegu...", style=discord.TextStyle.short)
     app = ui.TextInput(label='What app do you use for editing', placeholder="Editing app name...", style=discord.TextStyle.short)
     extra = ui.TextInput(label='Anything else you would like us to know?', placeholder="Extra info here...", style=discord.TextStyle.paragraph, required=False)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Forms', color=0x2b2d31)
          embed.add_field(name='Instagram Name:', value=f'{self.instagram.value}', inline=False)
          embed.add_field(name='Instagram Account Link:', value=f'https://instagram.com/{self.instagram.value}', inline=False)
          embed.add_field(name='Edit:', value=f'{self.edit.value}', inline=False)
          embed.add_field(name='Editing app:', value=f'{self.app.value}', inline=False)
          embed.add_field(name='Group(s) they want to be in:', value=f'{self.grps.value}', inline=False)
          embed.add_field(name='Anything else:', value=f'{self.extra.value}', inline=False)
          embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
          channel = interaction.client.get_channel(1131006328207327294)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your application has been sent successfully', ephemeral=True)

class ebmessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def applylol(self, ctx):
         view = appbuttons
         embed = discord.Embed(title="Apply Here *!*", description="some shit about applying n whatever", color=0x2b2d31)
         embed.set_footer(text="If you have any issues with applying, please contact staff or owners!")
         await ctx.send(embed=embed, view=view)

    @commands.command()
    async def lol(self, ctx):
        embed = discord.Embed(title="Welcome *!*", description="> Thank you for joining Editors Block! This is a community server made for all types of editors.\n> Feel free to ping @owners or @staff if you need any help.\n\nAlso, we will do group recruits for the groups Kanzen, Aura, and Daegu!", color=0x2b2d31)
        embed.set_footer(text="Follow the groups below!", icon_url="https://images-ext-2.discordapp.net/external/eVpj5e3hkU4cFDmIU8KnoGkfnfyDbbJPVs1xJWmUNQg/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1131003330810871979/128ca9e19d2f0aa0e41c99310673dfac.png")

        button = discord.ui.Button(label="Kanzen", url="https://www.instagram.com/kanzengrp/")
        button2 = discord.ui.Button(label="Aura", url="https://www.instagram.com/auragrps/")
        button3 = discord.ui.Button(label="Daegu", url="https://www.instagram.com/daegutowngrp/")

        view = discord.ui.View()
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def lol2(self, ctx):
        view = infobuttons()
        embed = discord.Embed(title="Owner Info", description="Editors Block is owned by @remqsi, @yoongiaeps, and @taedxck", color=0x2b2d31)
        embed.set_author(name="Hoshi#3105", icon_url=f'https://cdn.discordapp.com/avatars/849682093575372841/f04c5815341216fdafe736a2564a4d09.png?size=1024')
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ebmessages(bot))