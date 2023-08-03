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

    @discord.ui.button(label="Server Guide", emoji="<:guide:1136757467943022685>")
    async def guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="<:guide:1136757467943022685> Server Guide", color=0x2b2d31)
        embed.add_field(name="Get Started", value="<#1131007362895970414> - Server announcements are made here!\n<#1131005271502753812> - Server information\n<#1133730290221715487> - Get your roles here", inline=False)
        embed.add_field(name="Boost", value="<#1133772140915732511> - Boost messages are sent here\n<#1133772155499327538> - Claim the booster perks here", inline=False)
        embed.add_field(name="Events", value="<#1135594840739041380> - Server events and information is sent here\n<#1135594856106959032> - Giveaways are hosted here", inline=False)
        embed.add_field(name="Applications", value="<#1133771634793250847> - You can apply for the groups here\n<#1133771722659741877> - Ask questions about the applications\n<#1133771757816393839> - Answers from the qna", inline=False)
        embed.add_field(name="Main", value="<#1133767338588639323> - Start a converstion here with other members!\n<#1133767363339223110> - Speak other languages here!\n<#1133771941619191913> - Send self promotion here\n<#1134559895480442951> - Support the server with `/bump`", inline=False)
        embed.add_field(name="Editing", value="<#1133770895593324664> - Get opinions on your edits! \n<#1133770809366814890> - Get edit help with <@&1131127084379549757>\n<#1133770828882903141> - Ping <@&1131130102328078336> to get dts for your next post!\n<#1133770844817080360> - Ping <@&1131130157160206396> to collab with other server members\n<#1136756099710730331> - Talk in vc while editing", inline=False)
        embed.add_field(name="Bots", value="<#1133772583813263422> - Use our custom bot <@849682093575372841> here! `+help` for commands\n<#1133772598979866774> - Count as high as you can (can't count twice in a row)\n<#1133772609222361270> - Use other bots here other than hoshi\n<#1133772621666844813> - Another spam channel for you to use other bots\n<#1133772650695626882> - Use music commands here\n<#1133772672631836754> - Listen to music here", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Role Info", emoji="<:roles_00000:1136752067277504633>")
    async def roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        timeout = None
        embed = discord.Embed(title="<:roles_00000:1136752067277504633> Role Info",description="some shit" ,color=0x2b2d31)
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
        view = appbuttons(timeout=None)
        embed = discord.Embed(title="Apply Here *!*", description="some shit about applying n whatever", color=0x2b2d31)
        embed.set_footer(text="If you have any issues with applying, please contact staff or owners!")
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def lol(self, ctx):
        embed = discord.Embed(title="Welcome *!*", 
                              description="> Thank you for joining Editors Block!\n> This is a community server made for all types of editors.\n> Feel free to ping @owners or @staff if you need any help.\n\nAlso, we will do group recruits for the groups Kanzen, Aura, and Daegu!", 
                              color=0x2b2d31)
        embed.set_footer(text="Follow the groups below!", 
                         icon_url="https://images-ext-2.discordapp.net/external/eVpj5e3hkU4cFDmIU8KnoGkfnfyDbbJPVs1xJWmUNQg/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1131003330810871979/128ca9e19d2f0aa0e41c99310673dfac.png")

        button = discord.ui.Button(label="Kanzen", url="https://www.instagram.com/kanzengrp/", emoji="<:kanzen:1136701626799886366>")
        button2 = discord.ui.Button(label="Aura", url="https://www.instagram.com/auragrps/", emoji="<:aura:1136701593018978415>")
        button3 = discord.ui.Button(label="Daegu", url="https://www.instagram.com/daegutowngrp/", emoji="<:daegu:1136701608026185879>")

        view = discord.ui.View(timeout=None)
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def lol2(self, ctx):
        view = infobuttons(timeout=None)
        embed = discord.Embed(title="<:rules:1136761913972359178> Server Rules", 
                                description="<a:arrowpink:1134860720777990224> Follow Discord's [tos](https://discord.com/terms) and [guidelines](https://discord.com/guidelines)\n<a:arrowpink:1134860720777990224> Be nice and respectful to everyone in the server!\n<a:arrowpink:1134860720777990224> No impersonation of other editors (you will be banned)\n<a:arrowpink:1134860720777990224> Use channels for their intended purpose\n<a:arrowpink:1134860720777990224> No spamming pings, you will be warned and then kicked\n<a:arrowpink:1134860720777990224>  No trash talk of other people", 
                                color=0xee518f)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ebmessages(bot))