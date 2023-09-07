import asyncio
import datetime
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from discord.utils import get
from discord.ui import View, Select

class ReportView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.value = None

    @discord.ui.button(label="Report", style=discord.ButtonStyle.red)
    async def report(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(reportmodal(bot=self.bot))

class reportmodal(ui.Modal, title='Bug Report'):
    def __init__(self, bot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
        self.value = None

    notified = ui.TextInput(label='Do you want to be notified when its fixed?', placeholder="Yes/No", style=discord.TextStyle.short)
    command = ui.TextInput(label='What command is broken', placeholder="Command name here... example: +about", style=discord.TextStyle.short)
    bug = ui.TextInput(label='What happens when you do the command?', placeholder="Bug here...", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title="Bug reports", color=0xFF0000)
        embed.add_field(name='Should we notify you?', value=f'{self.notified.value}', inline=False)
        embed.add_field(name='What is the command?', value=f'{self.command.value}', inline=False)
        embed.add_field(name='What is the bug?', value=f'{self.bug.value}', inline=False)
        embed.add_field(name='Discord ID:', value=interaction.user.id, inline=False)
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.display_avatar)
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        view = resolved(self.bot, self.bug.value, self.command.value, interaction.message.reference.message_id)
        command = self.command.value
        bug = self.bug.value
        channel = interaction.client.get_channel(1149339743675502612)
        await channel.send("<@609515684740988959>", embed=embed, view=view)
        await interaction.followup.send(f'Your bug report was sent successfully', ephemeral=True)

class resolved(discord.ui.View):
    def __init__(self, bot, bug, command, message_id):
        super().__init__()
        self.bot = bot
        self.value = None
        self.command = command
        self.bug = bug
        self.message_id = message_id

    @discord.ui.button(label="Resolved", style=discord.ButtonStyle.green)
    async def resolved(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message_id = interaction.message.id
        msg = await interaction.channel.fetch_message(message_id)
        if msg.embeds:
            embed = msg.embeds[0]
            user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)
            if user_id_field:
                user_id = user_id_field.value.strip()
                user = await interaction.guild.fetch_member(int(user_id))
                if user:
                    embed.add_field(name="Status", value="Resolved :white_check_mark:")
                    await msg.edit(embed=embed, view=None)
                    resolvedembed = discord.Embed(title="Your report has been resolved!", description=f"Command: {self.command}\nIssue: {self.bug}", color=0x42FF00)
                    resolvedembed.set_thumbnail(url=self.bot.user.display_avatar.url)
                    await user.send(embed=resolvedembed)
                    await interaction.followup.send("The issue has been marked as resolved, and a message has been sent to the user.", ephemeral=True)
                else:
                    await interaction.followup.send("Failed to find the user associated with the report.", ephemeral=True)
            else:
                await interaction.followup.send("Invalid embed format. Please make sure the embed contains a field with the name 'Discord ID:'.", ephemeral=True)
        else:
            await interaction.followup.send("No embeds found in the original message.", ephemeral=True)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
        self.guilds =[1121841073673736215]

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        server_id = ctx.guild.id

        if server_id == 1121841073673736215:
            suggestion_channel_id = 1124038649814724638
        elif server_id == 957987670787764224:
            suggestion_channel_id = 1124043648716247061
        else:
            await ctx.send("This command is not available in this server.")
            return

        suggestion_channel = self.bot.get_channel(suggestion_channel_id)
        if suggestion_channel:
            embed = discord.Embed(title="New Suggestion", description=suggestion, color=0x2b2d31)

            suggestion_message = await suggestion_channel.send(f"Suggestion made by {ctx.author.mention}", embed=embed)
            await suggestion_message.add_reaction("<:YES:1137798542640025640>")
            await suggestion_message.add_reaction("<:NO:1137798539238445127>")

            confirmation_message = await ctx.reply(f"Suggestion has been sent to {suggestion_channel.mention}.")
            await asyncio.sleep(5)
            await ctx.message.delete()
            await confirmation_message.delete()
        else:
            await ctx.send("Failed to find the suggestion channel.")

    @commands.command()
    async def servericon(self, ctx):
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url=ctx.guild.icon)
        if ctx.guild.icon:
         await ctx.reply(embed=embed)
        else:
         await ctx.reply("Sorry, i can't find the server icon")

    @commands.command()
    async def serverbanner(self, ctx):
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url=ctx.guild.banner)
        if ctx.guild.banner:
         await ctx.reply(embed=embed)
        else:
         await ctx.reply("Sorry, i can't find the server banner")

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.checks.has_permissions(administrator=True)
    async def kick(self ,interaction: discord.Interaction ,member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await member.send(f"You have been kicked from {member.guild.name} for {reason}")
        await interaction.response.send_message(f'{member.mention} has been banned for: {reason}', ephemeral=True)
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("You have no admin", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(self ,interaction: discord.Interaction ,member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await member.send(f"You have been banned from {member.guild.name} for {reason}")
        await interaction.response.send_message(f'{member.mention} has been banned for: {reason}', ephemeral=True)
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("You have no admin", ephemeral=True)
        
    @app_commands.command(name="addrole", description="Add a role to a member.")
    @app_commands.checks.has_permissions(administrator=True)
    async def _add_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if role in member.roles:
            await interaction.response.send_message(f"{member.mention} already has the role {role.mention}.", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"{member.mention} has been given the role {role.mention}.", ephemeral=True)
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("You have no admin", ephemeral=True)

    @app_commands.command(name="removerole", description="Remove a role from a member.")
    @app_commands.checks.has_permissions(administrator=True)
    async def _remove_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if role not in member.roles:
            await interaction.response.send_message(f"{member.mention} doesn't have the role {role.mention}.", ephemeral=True)
        else:
            await member.remove_roles(role)
            await interaction.response.send_message(f"{member.mention} no longer has the role {role.mention}.", ephemeral=True)
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("You have no admin", ephemeral=True)
        
    @app_commands.command(name='kanzen', description='Get Kanzen logos')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def kanzenlogos(self, interaction: discord.Interaction):
        channel = interaction.client.get_channel(1122627075682078720)
        log = discord.Embed(title="Logo command has been used!", description=f"`{interaction.user.display_name}` has used the logos command", color=0x2b2d31)
        log.set_footer(text=f"id: {interaction.user.id}", icon_url=interaction.user.display_avatar)
        await interaction.response.send_message('https://mega.nz/folder/J40zCTYY#L73pTeQKWpCh15wpuQaIFA', ephemeral=True)
        await channel.send(embed=log)

    @app_commands.command(name='aura', description='Get Aura logos')
    @app_commands.guilds(discord.Object(id=957987670787764224))
    async def auralogos(self, interaction: discord.Interaction):
        await interaction.response.send_message('https://mega.nz/folder/SNkySBBb#kNViVZOVnHzEFmFsuhtLOQ', ephemeral=True)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, user: discord.User, *, reason: str):
        # Send DM to the user
        try:
            await user.send(f"You have been warned for: {reason}")
        except discord.Forbidden:
            await ctx.send("I couldn't send a DM to that user.")

        # Get the logging channel (replace CHANNEL_ID with the actual channel ID)
        log_channel = self.bot.get_channel(1134857444250632343)

        # Send the log to the logging channel
        if log_channel:
            embed = discord.Embed(title="User Warned",description=f"user:\n<a:arrowpink:1134860720777990224> {user.mention}\n\nreason:\n<a:arrowpink:1134860720777990224> {reason}\n\nmoderator:\n<a:arrowpink:1134860720777990224>{ctx.author.mention}" ,color=0x2b2d31)
            timestamp = datetime.datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"user id : {user.id}")
            await log_channel.send(embed=embed)
        else:
            await ctx.send("Logging channel not found. Please set the correct channel ID.")

    @commands.command()
    async def steal(self, ctx, emoji_name: str, *, emoji: discord.PartialEmoji):
        if not isinstance(emoji, discord.PartialEmoji):
            return await ctx.send("Please provide a valid emoji.")

        try:
            await ctx.guild.create_custom_emoji(name=emoji_name, image=await emoji.read())
        except discord.HTTPException as e:
            return await ctx.send(f"Failed to create the emoji. Error: {e}")
        
        await ctx.send(f"Emoji {emoji} has been added!")

    @commands.command()
    async def membercount(self, ctx):
        total_members = len(ctx.guild.members)
        bot_count = sum(1 for member in ctx.guild.members if member.bot)
        human_count = total_members - bot_count
        
        embed = discord.Embed(title=f"Total members in {ctx.guild.name}", color=0x2b2d31)
        embed.add_field(name="Total Members", value=total_members, inline=False)
        embed.add_field(name="Humans", value=human_count, inline=False)
        embed.add_field(name="Bots", value=bot_count, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def hoshiupdate(self, ctx):
        embed = discord.Embed(title='test', description="", color=0x2b2d31)
        embed.set_footer(text="Go and use these commands in Hoshi's channel!")
        embed.set_author(name="Hoshi#3105", icon_url="https://cdn.discordapp.com/avatars/849682093575372841/f04c5815341216fdafe736a2564a4d09.png?size=1024")
        message = await ctx.reply("Are you sure you want to send this update message?", embed=embed)
        await message.add_reaction('👍')
        
        def check(reaction, user):
            return user == ctx.author and str(reaction) == '👍'
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
            
            kanzen_channel_id = 1122655402899800234
            aura_channel_id = 1122242141037547531
            
            for guild in self.bot.guilds:
                kanzen = guild.get_channel(kanzen_channel_id)
                aura = guild.get_channel(aura_channel_id)
                
                if kanzen:
                    await kanzen.send("<@&1122655473368314017>", embed=embed)
                
                if aura:
                    await aura.send("<@&1122999466438438962>", embed=embed)
            
            await ctx.send("Great! I have sent out the update message!")
            await message.edit(content=None)
        except asyncio.TimeoutError:
            await message.edit(content="~~Are you sure you want to send this update message?~~\nThe update has been cancelled")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def khoshiupdate(self, ctx):
        embed = discord.Embed(title='Confessions command!', description="The new confessions command is where you can tell us your darkest secrets by using the command </confess:1140190517066465341>!\n\nThe messages are sent anonymously so don't worry to much about people knowing who you are when they are sent (they are also not logged either)\n\nThere are reactions that are added onto each confession for you to show how you feel about a confession\nCan't wait to see the weird shit we get!\n\n**This command is kanzengrp only!**", color=0x2b2d31)
        embed.set_footer(text="Go and use these commands in Hoshi's channel!")
        embed.set_author(name="Hoshi#3105", icon_url="https://cdn.discordapp.com/avatars/849682093575372841/f04c5815341216fdafe736a2564a4d09.png?size=1024")
        message = await ctx.reply("Are you sure you want to send this update message?", embed=embed)
        await message.add_reaction('👍')
        
        def check(reaction, user):
            return user == ctx.author and str(reaction) == '👍'
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
            
            kanzen_channel_id = 1122655402899800234
            
            for guild in self.bot.guilds:
                kanzen = guild.get_channel(kanzen_channel_id)
                
                if kanzen:
                    await kanzen.send("<@&1122655473368314017>", embed=embed)
            
            await ctx.send("Great! I have sent out the update message!")
            await message.edit(content=None)
        except asyncio.TimeoutError:
            await message.edit(content="~~Are you sure you want to send this update message?~~\nThe update has been cancelled")

    @commands.command()
    async def report(self, ctx):
        embed = discord.Embed(title="Bug Report", description="<a:Arrow_1:1145603161701224528> Please click the button and fill out the form that appears on your screen!\n<a:Arrow_1:1145603161701224528> Your bug report will send to the developer of Hoshi\n<a:Arrow_1:1145603161701224528> You can be notified when the issue has been resolved!", color=0x2b2d31)
        embed.set_footer(text="Click the button below to send a bug report", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        view = ReportView(bot=self.bot)
        await ctx.reply(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Moderation(bot))