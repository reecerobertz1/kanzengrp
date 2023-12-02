import asyncio
import datetime
from datetime import datetime, timedelta
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
        channel = interaction.client.get_channel(1173113066477588511)
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
    """Commands for mods"""
    def __init__(self, bot):
        self.bot = bot
        self.guilds = [1121841073673736215]
        self.emoji="<:rj:1121909526300479658>"

    @commands.command(hidden=True)
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

    @commands.command(hidden=True)
    async def servericon(self, ctx):
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url=ctx.guild.icon)
        if ctx.guild.icon:
         await ctx.reply(embed=embed)
        else:
         await ctx.reply("Sorry, i can't find the server icon")

    @commands.command(hidden=True)
    async def serverbanner(self, ctx):
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url=ctx.guild.banner)
        if ctx.guild.banner:
         await ctx.reply(embed=embed)
        else:
         await ctx.reply("Sorry, i can't find the server banner")

    @commands.hybrid_command(name="kick", description="Kick a member from the server.", extras="+kick @member (reason)")
    @commands.has_permissions(manage_guild=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await member.send(f"You have been kicked from {member.guild.name} for {reason}")
        await ctx.reply(f'{member.mention} has been kicked for: {reason}')

    @commands.hybrid_command(name="ban", description="Ban a member from the server.", extras="+ban @member (reason)")
    @commands.has_permissions(manage_guild=True)
    async def ban(self ,ctx, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await member.send(f"You have been banned from {member.guild.name} for {reason}")
        await ctx.reply(f'{member.mention} has been banned for: {reason}')
        
    @commands.hybrid_command(name="addrole", description="Add a role to a member.", extras="+addrole @member @role")
    @commands.has_permissions(manage_guild=True)
    async def _add_role(self, ctx, member: discord.Member, role: discord.Role):
        if role in member.roles:
            await ctx.reply(f"{member.mention} already has the role {role.mention}.")
        else:
            await member.add_roles(role)
            await ctx.reply(f"{member.mention} has been given the role {role.mention}.")

    @commands.hybrid_command(name="removerole", description="Remove a role from a member.", extras="+removerole @member @role")
    @commands.has_permissions(manage_guild=True)
    async def _remove_role(self, ctx, member: discord.Member, role: discord.Role):
        if role not in member.roles:
            await ctx.reply(f"{member.mention} doesn't have the role {role.mention}.")
        else:
            await member.remove_roles(role)
            await ctx.reply(f"{member.mention} no longer has the role {role.mention}.")
        
    @app_commands.command(name='logos', description='Get Kanzen logos')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def logos(self, interaction: discord.Interaction):
        channel = interaction.client.get_channel(1122627075682078720)
        log = discord.Embed(title="Logo command has been used!", description=f"`{interaction.user.display_name}` has used the logos command", color=0x2b2d31)
        log.set_footer(text=f"id: {interaction.user.id}", icon_url=interaction.user.display_avatar)
        await interaction.response.send_message('https://mega.nz/folder/J40zCTYY#L73pTeQKWpCh15wpuQaIFA', ephemeral=True)
        await channel.send(embed=log)

    @commands.command(description="Warn a member in Editors Block", extras="+warn @member (reason)")
    @commands.has_permissions(manage_guild=True)
    async def warn(self, ctx, user: discord.User, *, reason: str):
        try:
            await user.send(f"You have been warned for: {reason}")
        except discord.Forbidden:
            await ctx.send("I couldn't send a DM to that user.")
        log_channel = self.bot.get_channel(1134857444250632343)
        if log_channel:
            embed = discord.Embed(title="User Warned",description=f"user:\n<a:arrowpink:1134860720777990224> {user.mention}\n\nreason:\n<a:arrowpink:1134860720777990224> {reason}\n\nmoderator:\n<a:arrowpink:1134860720777990224>{ctx.author.mention}" ,color=0x2b2d31)
            timestamp = datetime.datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"user id : {user.id}")
            await log_channel.send(embed=embed)
        else:
            await ctx.send("Logging channel not found. Please set the correct channel ID.")

    @commands.command(description="Steal any emoji from any server", extras="+emoji (new emoji name) (emoji)")
    async def steal(self, ctx, emoji_name: str, *, emoji: discord.PartialEmoji):
        if not isinstance(emoji, discord.PartialEmoji):
            return await ctx.send("Please provide a valid emoji.")

        try:
            await ctx.guild.create_custom_emoji(name=emoji_name, image=await emoji.read())
        except discord.HTTPException as e:
            return await ctx.send(f"Failed to create the emoji. Error: {e}")
        
        await ctx.send(f"Emoji {emoji} has been added!")

    @commands.command(description="Report a bug report to the Hoshi dev", extras="+report")
    async def report(self, ctx):
        embed = discord.Embed(title="Bug Report", description="<a:Arrow_1:1145603161701224528> Please click the button and fill out the form that appears on your screen!\n<a:Arrow_1:1145603161701224528> Your bug report will send to the developer of Hoshi\n<a:Arrow_1:1145603161701224528> You can be notified when the issue has been resolved!", color=0x2b2d31)
        embed.set_footer(text="Click the button below to send a bug report", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        view = ReportView(bot=self.bot)
        await ctx.reply(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Moderation(bot))