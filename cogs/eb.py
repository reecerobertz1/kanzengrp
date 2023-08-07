import asyncio
import datetime
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

class staffinfo(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value=None

    @discord.ui.button(label="events")
    async def qotd(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="Editors Block events", description="Some help/rules for events", color=0x2b2d31)
        embed.add_field(name="Main events", value="Main events are just general events that everyone can join, this can be anything from game nights - movie nights or anything you can think of\nPlease make sure you ping @staff before you host an event just to make sure everyone isn't wanting to host an event that day / host a similar one", inline=False)
        embed.add_field(name="Question of the day", value="Please make sure you ping @staff before sending a question of the day into <#1137845041784692807> just incase someone else has a question they want to ask that day/if someone has the same question\nTry and make the questions as fun as possible (nothing inappropriate)", inline=False)
        embed.add_field(name="Giveaways", value="You can give anything away like, discord nitro or editing resources. Please do make sure if you're giving away editing resources that they are yours!\nTo host a give away you need to do the command `+giveaway`\n**example:**\n`+giveaway 12 discord nitro @remqsi`\nThe number is how many hours until someone is chosen\nthe discord nitro part is your prize (doesnt need to be nitro)\n@remqsi is for you to ping yourself as the host!\nMake sure you delete your message with the command after!", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="helping members")
    async def helpingmembers(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="Helping members in the server", color=0x2b2d31)
        embed.add_field(name="Answering forums", value="One thing you can help out with is by answering people in <#1133770895593324664>\nYou don't need to answer these but since people may use them they would like an answer!", inline=False)
        embed.add_field(name="With applications", value="Our way of applications isn't the usual way of doing applications since we do it with Hoshi\nYou may get these questions (pretty obvious answers since you all did them to get into my grps but here are some answers)\n\n**How do i apply?**\nTo apply you need to click the button in <#1133771634793250847> that says **Click here to apply** and fill out the form that shows up on screen and press submit!\n\n**How do i know if im accepted or not?**\nOur bot Hoshi will send you a DM once you have been reviewed! If your accepted there will be links for the members servers of the groups you applied for. If you was declined it'll just be a decline message.\n\n**Can i reapp?**\nNo not yet, we usually wait until the end of the recruit to allow everyone to re-apply!\n\nIf you do get a question that you're unsure of you can just ping Reece, Nani or Tae!", inline=False)
        embed.add_field(name="New Discord users", value="There will be some new discord user's here or just people who never use the app! you can just help them with stuff and help them navigate the server", inline=False)
        embed.add_field(name="Accept link expiring", value="If someone has recently been accepted but they didnt see their accept message straight away, their invite link to one of the groups could expire! Just have them contact one of the leads of the group, or have them ping <@1131016327709069353>, <@1131016346642161734> or <@1131016307807109200> depending on what grp they apped for\nor if your staff in those groups, you can create an invite link to that server or try and find their form and just accept again!", inline=False)
        embed.add_field(name="Answering Q&A", value="The qna feature is here so people can ask a question without channel becoming messy.\nIn question messages that are sent into <#1133771810714951732> it will say if they want their question answered in DMs or not.\nIf they want their question answered in DMs you need to reply to the question with the command `+answerpriv`, you need to also include you answer in this message like `+answerprive (answer)`\nIts the same for people who don't want a question answered privately except the command is just `+answer`", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="applications")
    async def applications(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="Applications", color=0x2b2d31)
        embed.add_field(name="Viewing Forms", value="Forms are sent into <#1131006328207327294>", inline=False)
        embed.add_field(name="Majority rule", value="Majority rule is where all of us vote on a form, if you do like the edit and think they should be accepted, react with ✅, if you dont think they should be accepted react with a ❌", inline=False)
        embed.add_field(name="Duplicated forms/spam", value="If you see a duplicated form just delete one of them.\nIf someone is spamming the forms delete them all and kick the person spamming (the form will have their discord name on, click that and kick)", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

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

    @discord.ui.button(label="Affiliate Info", emoji="<:partners:1137446533994909766>")
    async def affinfo(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="<:partners:1137446533994909766> Affiliate Information", color=0x2b2d31)
        embed.add_field(name="Advert with ping", value="<a:arrowpink:1134860720777990224> Follow Discord's [tos](https://discord.com/terms) and [guidelines](https://discord.com/guidelines)\n<a:arrowpink:1134860720777990224> Must have 100+ members\nIf you meet our requirements, please message one of our owners", inline=False)
        embed.add_field(name="Advert without ping", value="<a:arrowpink:1134860720777990224> Follow Discord's [tos](https://discord.com/terms) and [guidelines](https://discord.com/guidelines)\n<a:arrowpink:1134860720777990224> Must have 75+ members\nIf you meet our requirements, please message one of our owners", inline=False)
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

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green)
    async def verify(self, interaction: discord.Interaction, button: discord.Button):
        view = answer()
        embed = discord.Embed(title="Hello! Are you human? Let's find out!", description="`Please type the code below to be able to access this server!`\nClick **Answer** to type the code\n\n**Code:** FBGKDHS", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, view=view , ephemeral=True)

    @discord.ui.button(label="Help")
    async def verifyhelp(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="🔔 `Verification Steps`", description="<a:arrowpink:1134860720777990224> `1` Click **Verify**\n<a:arrowpink:1134860720777990224> `2`  You'll be given the code, click on **Answer** and enter the code (case sensitive)\n<a:arrowpink:1134860720777990224> `3` After passing verfication, you'll be given this role: <@&1131016147282710679>", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
        member = interaction.user
        if self.code.value == "FBGKDHS":
            await interaction.response.defer()
            role_id = 1131016147282710679
            role = interaction.guild.get_role(role_id)
            if role is None:
                print("Role not found. Make sure the role ID is correct.")
                return
            try:
                channel = interaction.client.get_channel(1134857444250632343)
                embed = discord.Embed(title="Verification Logs", description=f"{member.name} has passed the verification process!", color=0x2b2d31)
                timestamp = datetime.datetime.utcnow()
                embed.timestamp = timestamp
                embed.set_footer(text=f"user id : {interaction.user.id}")
                await channel.send(embed=embed)
                await member.add_roles(role)
                await interaction.followup.send(f"Thank you {member.name}! You're all verified, enjoy your time here in Editors Block.", ephemeral=True)
            except Exception as e:
                print(f"An error occurred while adding role: {e}")
                await interaction.response.send_message("An error occurred while adding the role. Please try again later.", ephemeral=True)
        else:
            await interaction.response.send_message("Invalid verification code. Please try again.", ephemeral=True)

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
          embed.add_field(name="Discord Name", value=interaction.user.mention)
          embed.add_field(name='Instagram Name:', value=f'{self.instagram.value}', inline=False)
          embed.add_field(name='Instagram Account Link:', value=f'https://instagram.com/{self.instagram.value}', inline=False)
          embed.add_field(name='Edit:', value=f'{self.edit.value}', inline=False)
          embed.add_field(name='Editing app:', value=f'{self.app.value}', inline=False)
          embed.add_field(name='Group(s) they want to be in:', value=f'{self.grps.value}', inline=False)
          embed.add_field(name='Anything else:', value=f'{self.extra.value}', inline=False)
          embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
          message = interaction.client.get_channel(1131006328207327294)
          await message.send(embed=embed)
          await message.add_reaction("✅")
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
        await ctx.send("https://cdn.discordapp.com/attachments/849724031723634688/1138177832456044644/WELCOME_00000.png")
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

    def is_judge():
        async def predicate(ctx):
            role_id = 1135216335652143104
            role = ctx.guild.get_role(role_id)
            return role in ctx.author.roles
        return commands.check(predicate)

    async def create_invite(self, guild_id):
        try:
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                raise ValueError("Invalid server ID")

            invite = await guild.text_channels[0].create_invite(max_uses=1, unique=True)
            return invite.url
        except Exception as e:
            print(f"Failed to create invite: {e}")
            return None

    @commands.command()
    @is_judge()
    async def accept(self, ctx):
        if ctx.message.reference is not None:
            try:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                embed = msg.embeds[0]
                group_field = next((field for field in embed.fields if field.name == 'Group(s) they want to be in:'), None)
                user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)
                insta_field = next((field for field in embed.fields if field.name == 'Instagram Account Link:'), None)

                if not group_field or not user_id_field or not insta_field:
                    await ctx.send("Invalid embed format. Please make sure the embed contains fields 'Group(s) they want to be in:' and 'Discord ID'.")
                    return

                grps = group_field.value.lower()
                groups = [group.strip() for group in re.split(r'[,\s]+', grps)]

                insta = insta_field.value.lower()
                insta = [insta.strip() for insta in re.split(r'[,\s]+', insta)]

                user_id = int(re.search(r'\d+', user_id_field.value).group())  # Extract the user ID from the field value
                accepted_server_ids = []

                for group in groups:
                    if "kanzen" in group:
                        accepted_server_ids.append((group, 1121841073673736215))
                    elif "aura" in group:
                        accepted_server_ids.append((group, 957987670787764224))
                    elif "daegu" in group:
                        accepted_server_ids.append((group, 896619762354892821))

                if not accepted_server_ids:
                    await ctx.send("Sorry, I could not find a group name in this embed...")
                    return

                embed = discord.Embed(title="Congratulations! You have been accepted!", color=0x2b2d31)
                for group, server_id in accepted_server_ids:
                    invite_link = await self.create_invite(server_id)  # Implement this function to generate the invite link
                    if invite_link:
                        embed.add_field(name=group.capitalize(), value=f"[Join Here]({invite_link})", inline=True)

                user = discord.utils.get(ctx.guild.members, id=user_id)
                if user:
                    await user.send(embed=embed)

                    channel = ctx.guild.get_channel(1131006361921130526)
                    if channel:
                        await channel.send(f"{user.mention} was accepted")

                    instachannel = ctx.guild.get_channel(1137423800623960116)
                    if instachannel:
                        await instachannel.send(f"You need to follow {', '.join(insta)}\nThey were accepted into {', '.join(groups)}")

                embed = msg.embeds[0]
                embed.add_field(name="Status", value="Accepted ✅")
                await ctx.message.add_reaction("✅")
                await msg.edit(embed=embed)

            except Exception as e:
                await ctx.send(f"An error occurred: {e}")

                guild = ctx.guild
                role_to_add = guild.get_role(1131016215754715166)
                if role_to_add:
                    await user.add_roles(role_to_add)

                role_to_remove = guild.get_role(1131016147282710679)
                if role_to_remove:
                    await user.remove_roles(role_to_remove)

            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply with the embed you want to process.")

    @commands.command()
    @is_judge()
    async def decline(self, ctx):
        if ctx.message.reference is not None:
            try:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                embed = msg.embeds[0]
                group_field = next((field for field in embed.fields if field.name == 'Group(s) they want to be in:'), None)
                user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)

                if not group_field or not user_id_field:
                    await ctx.send("Invalid embed format. Please make sure the embed contains fields 'Group(s) they want to be in:' and 'Discord ID'.")
                    return

                grps = group_field.value.lower()
                groups = [group.strip() for group in re.split(r'[,\s]+', grps)]

                user_id = user_id_field.value.strip()

                # DM the user with the decline message
                user = self.bot.get_user(int(user_id))
                if user:
                    decline_message = f"Hey! You have been declined from {', '.join(groups)}. Please don't be upset or discouraged! We will have more recruitments in the future. <3"
                    await user.send(decline_message)

                    channel = ctx.guild.get_channel(1131006361921130526)
                    if channel:
                        await channel.send(f"{user.mention} was declined")

                # Edit the original embed to show the declined status
                embed = msg.embeds[0]
                embed.add_field(name="Status", value="Declined ❌")
                await ctx.message.add_reaction("✅")
                await msg.edit(embed=embed)
            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply with the embed you want to process.")

    @commands.command()
    async def role1(self, ctx):
        embed = discord.Embed(title="<:leaf:1137454366886993950> What are your pronouns?",
                              description="Which of the following pronouns do you use? These roles can help other members of the server use the correct pronouns.\n\n<:1:1137455321028251708> - <@&1131127428668997737> \n<:2:1137455517577531565> - <@&1131127209952809031> \n<:3:1137455658258673704> - <@&1131127449753751663> \n<:4:1137455776877781107> - <@&1131127472142958622> \n<:5:1137455941609078824> - <@&1131127502396465213> \n<:6:1137456046978383892> - <@&1131127523456069723>",
                              color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1137844016692609074/pronouns_00000.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def role2(self, ctx):
        embed = discord.Embed(title="<:leaf:1137454366886993950> What server pings would you like?",
                              description="The staff will ping these roles whenever there's something related to these roles happening in the server.\n\n<:1:1137455321028251708> - <@&1133770119777099866> \n<:2:1137455517577531565> - <@&1131127168102055996> \n<:3:1137455658258673704> - <@&1131127104226992208> \n<:4:1137455776877781107> - <@&1131005057417105418> \n<:5:1137455941609078824> - <@&1131127124187684894>",
                              color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1137843838153666610/pings_00000.png")
        await ctx.send(embed=embed)


    @commands.command()
    async def role3(self, ctx):
        embed = discord.Embed(title="<:leaf:1137454366886993950> What member pings would you like?",
                              description="These roles can be used by anyone in this server to ping other members! Please do not abuse these roles!\n\n<:1:1137455321028251708> - <@&1131130157160206396>\n<:2:1137455517577531565> - <@&1131127084379549757>\n<:3:1137455658258673704> - <@&1131130102328078336>\n<:4:1137455776877781107> - <@&1131127146186821685>\n<:5:1137455941609078824> - <@&1134876934585712773>",
                              color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1137843866800754858/member_pings_00000.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def space1(self, ctx):
        await ctx.send("<:Empty:1137842301188702239>")

    @commands.command()
    async def staffinfo(self, ctx):
        view = staffinfo()
        embed = discord.Embed(title="<:leaf:1137454366886993950> Staff Handbook", description="<a:arrowpink:1134860720777990224> Please do not abuse your staff power!\n<a:arrowpink:1134860720777990224> Help people when they ping you (if you're free)\n<a:arrowpink:1134860720777990224> Not helping in the server will get you removed as staff, unless you have a reason\n<a:arrowpink:1134860720777990224> Set a good example in the server\n<a:arrowpink:1134860720777990224> If you see anyone with inappropriate name, you can change their nicknames\n<a:arrowpink:1134860720777990224> See any scam messages and accounts delete them and ban the account\n<a:arrowpink:1134860720777990224> If there is any inappropriate content sent into the server, delete and ban\n<a:arrowpink:1134860720777990224> If there is any rude and disrespectful messages sent, delete and tell an owner!", color=0x2b2d31)
        embed.set_footer(text="Click the buttons below to show more!")
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send("<@&1131006067564875806>", embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(ebmessages(bot))