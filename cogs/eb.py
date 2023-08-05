import asyncio
import json
import random
import re
from typing import Any
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import View, Select
from typing import List, Optional
from discord import ui

class infobuttons(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
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
        embed = discord.Embed(title="<:roles_00000:1136752067277504633> Role Info",description="<@&1131006052209541212> - Editors block owners\n<@&1131006067564875806> - Editors block staff\n<@&1136803676854431745> - our amazing supporters\n<@&1131016215754715166> - Accepted members from recruit\n<@&1131016147282710679> - Default Role from verification " ,color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True)   

class appbuttons(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None
        
    @discord.ui.button(label="Click to apply!")
    async def roles(self, interaction: discord.Interaction, button: discord.ui.Button):
         await interaction.response.send_modal(grprctkda())

class verifycode(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Verify")
    async def verify(self, interaction: discord.Interaction, button: discord.Button):
        view = answer
        embed = discord.Embed(title="Hello! Are you human? Let's find out!", description="`Please type the code below to be able to access this server!`\n**Code:** FBGKDHS", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, view=view ,ephemeral=True)

class answer(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Answer", style=discord.ButtonStyle.green)
    async def vmo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(verifymodal())

class verifymodal(ui.Modal, title='Verification'):
     code = ui.TextInput(label='What was the code?', placeholder="Enter code here...", style=discord.TextStyle.short)
     async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Thank you! You're all verified, enjoy your time here in Editors Block", ephemeral=True)

class qnabutton(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Click to ask a question!")
    async def qnabutton(self, interaction: discord.Interaction, button: discord.ui.Button):
         await interaction.response.send_modal(qnamodal())

class qnamodal(ui.Modal, title="Editor's Block Q&A"):
     dmyesno = ui.TextInput(label='Do you want us to answer privately?', placeholder="Enter your answer here...", style=discord.TextStyle.short)
     question = ui.TextInput(label='What is your question?', placeholder="Ask question here...", style=discord.TextStyle.short)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title="Editor's Block Q&A", color=0x2b2d31)
          embed.add_field(name='Answer in dm (yes or no)', value=f'{self.dmyesno.value}', inline=False)
          embed.add_field(name='Question', value=f'{self.question.value}', inline=False)
          embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
          channel = interaction.client.get_channel(1133771810714951732)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your question was sent successfully', ephemeral=True)

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
        self.giveaway_data = {}
        self.load_giveaway_data()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, duration: int, *, args):
        """Start a giveaway."""
        if duration <= 0:
            return await ctx.send("The duration must be greater than 0.")
        
        duration_hours = duration
        duration_seconds = duration_hours * 3600  # Convert hours to seconds

        args = args.split()
        prize = " ".join(args)
        host_mention = None

        if len(args) > 1:
            # Check if the last argument starts with "@" to determine if it's a host mention
            last_arg = args[-1]
            if last_arg.startswith("<@") and last_arg.endswith(">"):
                host_mention = last_arg
                prize = " ".join(args[:-1])
        
        giveaway_message = f"React with 🎉 to enter the giveaway for **{prize}**!\nDuration: {duration_hours} hours"
        giveaway_embed = discord.Embed(title="Giveaway", description=giveaway_message, color=0x2b2d31)

        if host_mention:
            giveaway_embed.add_field(name="Host", value=host_mention, inline=False)

        giveaway_msg = await ctx.send('<@&1131127104226992208>', embed=giveaway_embed)

        await giveaway_msg.add_reaction("🎉")
        self.giveaway_data[giveaway_msg.id] = {"prize": prize, "duration": duration_seconds, "entries": []}
        await self.save_giveaway_data()

        await asyncio.sleep(duration_seconds)
        await self.pick_winner(giveaway_msg)

    async def pick_winner(self, message):
        data = self.giveaway_data.get(message.id)
        if not data:
            return
        
        if not data["entries"]:
            return await message.channel.send("No one entered the giveaway. The prize will go unclaimed.")

        winner_id = random.choice(data["entries"])
        winner = self.bot.get_user(winner_id)

        if winner:
            prize = data["prize"]
            await message.channel.send(f"Congratulations to {winner.mention} for winning the giveaway for **{prize}**! Please message a lead, staff/host for your prize")
        else:
            await message.channel.send("The giveaway winner could not be determined.")

        del self.giveaway_data[message.id]
        await self.save_giveaway_data()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot and str(reaction.emoji) == "🎉":
            data = self.giveaway_data.get(reaction.message.id)
            if data:
                data["entries"].append(user.id)
                await self.save_giveaway_data()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gapick(self, ctx, message_id: int):
        """Pick a winner for a specific giveaway."""
        message = await ctx.fetch_message(message_id)
        await self.pick_winner(message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gaclear(self, ctx):
        """Clear the giveaway data."""
        self.giveaway_data.clear()
        await self.save_giveaway_data()
        await ctx.send("Giveaway data has been cleared.")

    async def save_giveaway_data(self):
        with open("giveaway_data.json", "w") as f:
            json.dump(self.giveaway_data, f, indent=4)

    async def load_giveaway_data(self):
        try:
            with open("giveaway_data.json", "r") as f:
                self.giveaway_data = json.load(f)
        except FileNotFoundError:
            self.giveaway_data = {}

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def openapps(self, ctx):
        application_channel_id = 1133771634793250847
        application_channel = self.bot.get_channel(application_channel_id)
        view = appbuttons()
        embed = discord.Embed(title="Apply Here *!*", 
                              description="information:\n<a:arroworange:1134860722757713980> This reacruit is for the groups Kanzengrp, Auragrps and Daegutowngrp\n<a:arroworange:1134860722757713980> You will receive a dm from our bot Hoshi with your application results\n<a:arroworange:1134860722757713980>  You do not need to use a certain editing app to apply\n<a:arroworange:1134860722757713980> All fandoms and styles are accepted here!\n<a:arroworange:1134860722757713980> We mostly look for unique edits with smooth transitions\n<a:arroworange:1134860722757713980> Velocity edits ARE NOT accepted\n<a:arroworange:1134860722757713980> You can apply for any group, just be specific in your application what groups\n\napplication rules:\n<a:arroworange:1134860722757713980> Follow the rules on the recruit posts posted by the group you want to join\n<a:arroworange:1134860722757713980> Be patient with apps! staff are not active 24/7\n<a:arroworange:1134860722757713980> Only apply once, unless we decide to reapps", 
                              color=0x2b2d31)
        application_channel = await application_channel.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def lol(self, ctx):
        embed = discord.Embed(title="Welcome *!*", 
                              description="> Thank you for joining Editors Block!\n> This is a community server made for all types of editors.\n> Feel free to ping @owners or @staff if you need any help.\n\nWe will do group recruits for the groups Kanzen, Aura, and Daegu! ͏͏͏  ͏͏͏ ͏͏͏͏͏͏͏͏͏ ͏ ͏", 
                              color=0x2b2d31)
        embed.set_footer(text="Follow the groups below!", 
                         icon_url="https://images-ext-2.discordapp.net/external/eVpj5e3hkU4cFDmIU8KnoGkfnfyDbbJPVs1xJWmUNQg/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1131003330810871979/128ca9e19d2f0aa0e41c99310673dfac.png")

        button = discord.ui.Button(label="Kanzen", url="https://www.instagram.com/kanzengrp/", emoji="<:kanzen:1136701626799886366>")
        button2 = discord.ui.Button(label="Aura", url="https://www.instagram.com/auragrps/", emoji="<:aura:1136701593018978415>")
        button3 = discord.ui.Button(label="Daegu", url="https://www.instagram.com/daegutowngrp/", emoji="<:daegu:1136701608026185879>")

        view = discord.ui.View()
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def lol2(self, ctx):
        view = infobuttons()
        embed = discord.Embed(title="<:rules:1136761913972359178> Server Rules ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏͏͏ ͏ ͏ ͏ ͏ ͏ ͏ ͏͏͏ ͏͏͏ ", 
                                description="<a:arrowpink:1134860720777990224> Follow Discord's [tos](https://discord.com/terms) and [guidelines](https://discord.com/guidelines)\n<a:arrowpink:1134860720777990224> Be nice and respectful to everyone in the server!\n<a:arrowpink:1134860720777990224> No impersonation of other editors (you will be banned)\n<a:arrowpink:1134860720777990224> Use channels for their intended purpose\n<a:arrowpink:1134860720777990224> No spamming pings, you will be warned and then kicked\n<a:arrowpink:1134860720777990224>  No trash talk of other people", 
                                color=0xee518f)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def qnapfft(self, ctx):
        view = qnabutton()
        embed = discord.Embed(title="Editor's Block Q&A",
                              description="information:\n<a:arrowpink:1134860720777990224> You can ask us anything about the server, groups and recruits\n<a:arrowpink:1134860720777990224> We can DM you privately, or send the answer to <#1133771757816393839>\n<a:arrowpink:1134860720777990224> A form will pop up on your screen for you to enter in your question\n<a:arrowpink:1134860720777990224> No question is a dumb question so feel free to ask us anything (appropriate)\n\nother stuff:\n<a:arrowpink:1134860720777990224> Please be patient with us, staff are not online 24/7\n<a:arrowpink:1134860720777990224> If you spam the same question we will not answer it!\n<a:arrowpink:1134860720777990224> Do not abuse this feature or harass staff" ,
                              color=0x2b2d31)
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def verify(self, ctx):
        view = verifycode()
        embed = discord.Embed(title="Verification Required!", 
                              color=0x2b2d31,
                              description=f"To access the server `{ctx.guild.name}` you need to verify first!\nClick the button `Verify` to begin the verify process")
        await ctx.send(embed=embed, view=view)

    @commands.command(aliases=['ap'])
    @commands.has_permissions(manage_guild=True)
    async def answerpriv(self, ctx, answer: str):
        if ctx.message.reference is not None:
            try:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                embed = msg.embeds[0]
                user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)
                question = next((field for field in embed.fields if field.name == 'Question'), None)

                if not question or not user_id_field:
                    await ctx.send("Invalid embed format. Please make sure the embed contains fields 'Group(s) they want to be in:' and 'Discord ID'.")
                    return

                question = question.value.lower()
                question = [question.strip() for question in re.split(r'[,\s]+', question)]

                if user_id_field:
                    user_id = user_id_field.value.strip()

                    user = await ctx.guild.fetch_member(int(user_id))
                    if user:
                        embed = discord.Embed(title="Q&A", color=0x2b2d31, description=f"**You asked a question in editor's block**\n{', '.join(question)}\n**Our answer:**\n{answer}")
                        embed.set_footer(text=f"answered by {ctx.author.display_name}")
                        await user.send(embed=embed)

                        embed = msg.embeds[0]
                        embed.add_field(name="Status", value="Answered ✅")
                        await ctx.message.add_reaction("✅")
                        await msg.edit(embed=embed)
                else:
                    await ctx.send("Failed to find the Discord ID field in the embed.")
            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply to the question you want to answer.")

    @commands.command(aliases=['a'])
    @commands.has_permissions(manage_guild=True)
    async def answer(self, ctx, answer: str):
        if ctx.message.reference is not None:
            try:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                embed = msg.embeds[0]
                user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)
                question = next((field for field in embed.fields if field.name == 'Question'), None)
                answer_channel = self.bot.get_channel(1133771757816393839)

                if not question or not user_id_field:
                    await ctx.send("Invalid embed format. Please make sure the embed contains fields 'Group(s) they want to be in:' and 'Discord ID'.")
                    return
                
                question = question.value.lower()
                question = [question.strip() for question in re.split(r'[,\s]+', question)]

                if user_id_field:
                    user_id = user_id_field.value.strip()

                    user = await ctx.guild.fetch_member(int(user_id))
                    if user:
                        embed = discord.Embed(title="Q&A", color=0x2b2d31, description=f"**Question:**\n{', '.join(question)}\n**Answer:**\n{answer}")
                        embed.set_footer(text=f"asked by {user.display_name} | answered by {ctx.author.display_name}")
                        await answer_channel.send(f"<@{user_id}>", embed=embed)

                        embed = msg.embeds[0]
                        embed.add_field(name="Status", value="Answered ✅")
                        await ctx.message.add_reaction("✅")
                        await msg.edit(embed=embed)
                else:
                    await ctx.send("Failed to find the Discord ID field in the embed.")
            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply to the question you want to answer.")

async def setup(bot):
    await bot.add_cog(ebmessages(bot))