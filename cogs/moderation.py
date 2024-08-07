import asyncio
import datetime
from datetime import datetime, timedelta
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from discord.utils import get
from discord.ui import View, Select
import asqlite
from typing import TypedDict, List

class RepRow(TypedDict):
    count: int
    helped: str

class reportmemberbutton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Report Member", style=discord.ButtonStyle.red)
    async def link(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(reportmember())

class reportmember(ui.Modal, title='Report Member'):
    def __init__(self):
        super().__init__()
        self.value = None

    notified = ui.TextInput(label='Who are you reporting', placeholder="Enter their name + instagram name (if you know it)", style=discord.TextStyle.short)
    command = ui.TextInput(label='Why are you reporting this member?', placeholder="Provide detailed info for effective resolution.", style=discord.TextStyle.long)
    bug = ui.TextInput(label='Do you have screenshots?', placeholder="Yes/No, if yes we will DM you", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title="`❗`Report a member", color=0x2b2d31)
        embed.add_field(name='Who are you reporting', value=f'{self.notified.value}', inline=False)
        embed.add_field(name='Why are you reporting this member?', value=f'{self.command.value}', inline=False)
        embed.add_field(name='Do you have screenshots?', value=f'{self.bug.value}', inline=False)
        embed.set_footer(text=f"{interaction.user.name} | {interaction.user.id}", icon_url=interaction.user.display_avatar)
        timestamp = datetime.utcnow()
        embed.timestamp = timestamp
        channel = interaction.client.get_channel(1178952898273628200)
        await channel.send("<@&1135244903165722695>", embed=embed)
        await interaction.followup.send(f'Your report was sent successfully', ephemeral=True)

class ga(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Click for link")
    async def link(self, interaction: discord.Interaction, button: discord.Button):
        channel = interaction.client.get_channel(1122627075682078720)
        log = discord.Embed(title="Giveaway button has been used!", description=f"`{interaction.user.display_name}` has used the giveaway button", color=0x2b2d31)
        log.set_footer(text=f"id: {interaction.user.id}", icon_url=interaction.user.display_avatar)
        await channel.send(embed=log)
        await interaction.response.send_message("https://mega.nz/folder/048lUZaY#5_OEu5tYJQCxfyo-dW03hw")

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
        self.emoji = "<:rj:1121909526300479658>"
        self.warning_channel_id = 1178952898273628200
        self.pool = None
        bot.loop.create_task(self.init_database())

    async def init_database(self):
        self.pool = await asqlite.create_pool('databases/levels.db')
        async with self.pool.acquire() as conn:
            await conn.execute('''CREATE TABLE IF NOT EXISTS warning (member_id INTEGER, guild_id INTEGER, reasons TEXT, warnings INTEGER)''')

    async def get_warnings(self, member_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT warnings, reasons FROM warning WHERE member_id = ?", (member_id,))
                row = await cursor.fetchone()
                if row is None:
                    await self.add_warning(member_id)
                    return 0, 0
                return row[0], row[1]
            
    async def add_warning(self, member_id, guild_id, reason, change):
        async with self.pool.acquire() as conn:
            await conn.execute("INSERT INTO warning (member_id, guild_id, reasons, warnings) VALUES ($1, $2, $3, $4)", member_id, guild_id, reason, change)
            await conn.commit()

    async def get_warn_leaderboard_stats(self) -> List[RepRow]:
        query = '''SELECT * FROM warning ORDER BY warnings DESC'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall()
        return rows

    @app_commands.command(description="See the warnings leaderboard")
    async def warnings(self, interaction: discord.Interaction):
        rows = await self.get_warn_leaderboard_stats()
        
        if not rows:
            await interaction.response.send_message("The leaderboard is empty.")
            return
        
        description = ""
        
        for i, row in enumerate(rows, start=1):
            if i == 1:
                i = "🥇"
            if i == 2:
                i = "🥈"
            if i == 3:
                i = "🥉"
            else:
                i = i
            description += f"**{i}.** <@!{row['member_id']}>\n> **{row['warnings']} warnings**\n> reason: {row['reasons']}\n\n"
        
        embed = discord.Embed(title="Warnings Leaderboard", description=description, color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        
        await interaction.response.send_message(embed=embed)

    async def update_warnings(self, conn, member_id, guild_id, reason, change=1):
        async with self.pool.acquire() as conn:
            existing_warnings = await conn.fetchone('SELECT warnings FROM warning WHERE member_id = $1 AND guild_id = $2', member_id, guild_id)

            if existing_warnings:
                current_warnings = existing_warnings['warnings']
                updated_warnings = current_warnings + change

                await conn.execute('UPDATE warning SET reasons = $1, warnings = $2 WHERE member_id = $3 AND guild_id = $4',
                                reason, updated_warnings, member_id, guild_id)

            else:
                updated_warnings = change
                await self.add_warning(member_id, guild_id, reason, updated_warnings)

            await conn.commit()

            return updated_warnings

    def is_staff():
        async def predicate(ctx):
            role_id = 1135244903165722695
            role = ctx.guild.get_role(role_id)
            return role in ctx.author.roles
        return commands.check(predicate)

    @commands.hybrid_command(name="warn", description="Give a warning to a member", extras="+warn @member (reason)")
    @is_staff()
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        guild_id = ctx.guild.id
        warner = ctx.author.name
        member_id = member.id
        async with self.pool.acquire() as conn:
            warning_count = await self.update_warnings(conn, member_id, guild_id, reason)
            try:
                await self.send_warning_embed(ctx.guild, member, reason, warning_count, warner)
                await self.send_warning_dm(member, reason, warning_count)
                await ctx.reply(f"Successfully warned <@{member_id}>")
            except discord.Forbidden:
                print(f"Failed to send a warning message to {member}.")

    async def send_warning_embed(self, guild, member, reason, warning_count, warner):
        channel = guild.get_channel(self.warning_channel_id)
        if channel:
            embed = discord.Embed(
                title=f"Member Warned: {member.display_name}",
                color=0x2b2d31,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Warning Count", value=warning_count, inline=False)
            embed.set_thumbnail(url=member.display_avatar)
            embed.set_footer(text=f"warning from @{warner}")

            await channel.send(embed=embed)

    async def send_warning_dm(self, member, reason, warning_count):
        embed = discord.Embed(
            title="<:warn:1182986477634859090> Warning <:warn:1182986477634859090>",
            description=f"reason:\n{reason}\nYou now have {warning_count} warning(s)",
            color=0x2b2d31
        )
        embed.set_thumbnail(url=member.display_avatar)

        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            print(f"Failed to send a warning DM to {member}.")

    @commands.hybrid_command(name="clearwarnings",aliases=['cw'], description="Clear all warnings from a member", extras="+clearwarnings @member : alias +cw", hidden=True)
    @is_staff()
    async def clearwarnings(self, ctx, member: discord.Member):
        guild_id = ctx.guild.id
        member_id = member.id

        async with self.pool.acquire() as conn:
            await conn.execute('DELETE FROM warning WHERE member_id = $1 AND guild_id = $2', member_id, guild_id)

        await ctx.send(f"Warnings for {member.display_name} have been cleared.")

    @app_commands.command(description="Get the server icon")
    async def servericon(self, interaction: discord.Interaction):
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url=interaction.guild.icon)
        if interaction.guild.icon:
         await interaction.response.send_message(embed=embed)
        else:
         await interaction.response.send_message("Sorry, i can't find the server icon")

    @app_commands.command(description="Get the server banner")
    async def serverbanner(self, interaction: discord.Interaction):
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url=interaction.guild.banner)
        if interaction.guild.banner:
         await interaction.response.send_message(embed=embed)
        else:
         await interaction.response.send_message("Sorry, i can't find the server banner")

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
        
    @app_commands.command(name='logos', description='Get Kanzen logos')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def logos(self, interaction: discord.Interaction):
        channel = interaction.client.get_channel(1122627075682078720)
        log = discord.Embed(title="Logo command has been used!", description=f"`{interaction.user.display_name}` has used the logos command", color=0x2b2d31)
        log.set_footer(text=f"id: {interaction.user.id}", icon_url=interaction.user.display_avatar)
        await interaction.response.send_message('https://mega.nz/folder/J40zCTYY#L73pTeQKWpCh15wpuQaIFA', ephemeral=True)
        await channel.send(embed=log)

    @commands.command(description="Steal any emoji from any server", extras="+emoji (new emoji name) (emoji)")
    async def steal(self, ctx, emoji_name: str, *, emoji: discord.PartialEmoji):
        if not isinstance(emoji, discord.PartialEmoji):
            return await ctx.send("Please provide a valid emoji.")

        try:
            await ctx.guild.create_custom_emoji(name=emoji_name, image=await emoji.read())
        except discord.HTTPException as e:
            return await ctx.send(f"Failed to create the emoji. Error: {e}")
        
        await ctx.send(f"Emoji {emoji} has been added!")
        
    @commands.hybrid_command(name="dm", aliases=["message"], description="Dm a user through hoshi", extras="+dm @member (message) : alias +message")
    async def dm(self, ctx, member: discord.Member, *, message: str):
        await member.send(message)
        await ctx.send(f"i have successfully messaged {member.mention}\n{message}")        

    async def get_rep(self, member_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT count, helped FROM staffrep WHERE member_id = ?", (member_id,))
                row = await cursor.fetchone()
                if row is None:
                    await self.add_rep(member_id)
                    return 0, 0
                return row[0], row[1]

    async def add_rep(self, member_id, guild_id, helped, change):
        async with self.pool.acquire() as conn:
            await conn.execute("INSERT INTO staffrep (member_id, guild_id, helped, count) VALUES ($1, $2, $3, $4)", member_id, guild_id, helped, change)
            await conn.commit()

    async def update_rep_reece(self, member_id, guild_id, helped, giver, change=3):
        async with self.pool.acquire() as conn:
            existing_warnings = await conn.fetchone('SELECT count FROM staffrep WHERE member_id = $1 AND guild_id = $2', member_id, guild_id)
            if existing_warnings:
                current_warnings = existing_warnings['count']
                updated_warnings = current_warnings + change
                await conn.execute('UPDATE staffrep SET helped = $1, count = $2 WHERE member_id = $3 AND guild_id = $4',
                                f"{helped}\n> **Added by:** <@{giver}>", updated_warnings, member_id, guild_id)
            else:
                updated_warnings = change
                await self.add_rep(member_id, guild_id, helped, updated_warnings)
            await conn.commit()
            return updated_warnings

    async def update_rep(self, member_id, guild_id, helped, giver, change=1):
        async with self.pool.acquire() as conn:
            existing_warnings = await conn.fetchone('SELECT count FROM staffrep WHERE member_id = $1 AND guild_id = $2', member_id, guild_id)
            if existing_warnings:
                current_warnings = existing_warnings['count']
                updated_warnings = current_warnings + change
                await conn.execute('UPDATE staffrep SET helped = $1, count = $2 WHERE member_id = $3 AND guild_id = $4',
                                f"{helped}\n> **Added by:** <@{giver}>", updated_warnings, member_id, guild_id)
            else:
                updated_warnings = change
                await self.add_rep(member_id, guild_id, helped, updated_warnings)
            await conn.commit()
            return updated_warnings

    @commands.hybrid_command(name="addrep", description="add rep to a staff member for helping", extra="+addrep @member", hidden=True)
    @commands.has_permissions(administrator=True)
    @commands.has_permissions(manage_guild=True)
    async def addrep(self, ctx, member: discord.Member, *, helped):
        await self.update_rep_reece(member.id, ctx.guild.id, helped, giver=ctx.author.id)
        rep = await self.get_rep_count(member.id)
        embed = discord.Embed(title="You got Staff Rep!", description=f"{ctx.author.name} has given you **3 rep** for helping them!\n\nYou got rep for {helped}\n\nYou now have **{rep} rep**! Well done", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.reply(f"Successfully added rep for {member.display_name}\n**{helped}**")
        await member.send(embed=embed)

    @commands.hybrid_command(name="supportstaff", description="add rep to a staff member for helping", extra="+supportstaff @member", hidden=True)
    async def supportstaff(self, ctx, member: discord.Member, *, helped):
        await self.update_rep(member.id, ctx.guild.id, helped, giver=ctx.author.id)
        rep = await self.get_rep_count(member.id)
        embed = discord.Embed(title="You got Staff Rep!", description=f"{ctx.author.name} has given you **1 rep** for helping them!\n\nYou got rep for {helped}\n\nYou now have **{rep} rep**! Well done", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.reply(f"Successfully added rep for {member.display_name}\n**{helped}**")
        await member.send(embed=embed)

    async def reset_staffrep(self, guild_id: int) -> None:
        query = '''UPDATE staffrep SET count = 0, helped = NULL WHERE guild_id = $1'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                await conn.commit()
        await self.bot.pool.release(conn)

    async def get_leaderboard_stats(self) -> List[RepRow]:
        query = '''SELECT * FROM staffrep ORDER BY count DESC'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall()
        return rows

    @app_commands.command(description="Reset the staff rep")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def resetrep(self, interaction: discord.Interaction):
        await self.reset_staffrep(interaction.guild_id)
        embed = discord.Embed(title='success!',description=f'reps have been erased.',color=0x2B2D31)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="See the staff rep leaderboard")
    async def toprep(self, interaction: discord.Interaction):
        rows = await self.get_leaderboard_stats()
        
        if not rows:
            await interaction.response.send_message("The leaderboard is empty.")
            return
        
        description = ""
        
        for i, row in enumerate(rows, start=1):
            if i == 1:
                i = "🥇"
            if i == 2:
                i = "🥈"
            if i == 3:
                i = "🥉"
            else:
                i = i
            description += f"**{i}.** <@!{row['member_id']}>\n> **{row['count']} rep**\n> **task:** {row['helped']}\n\n"
        
        embed = discord.Embed(title="Staff Rep Leaderboard", description=description, color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        
        await interaction.response.send_message(embed=embed)

    async def get_rep_count(self, member_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT count FROM staffrep WHERE member_id = ?", (member_id,))
                row = await cursor.fetchone()
                if row is None:
                    await self.add_rep(member_id)
                    return 0, 0
                return row[0]

    @app_commands.command(name="reportmember", description="See one of our members breaking our rules? you can report them here")
    async def reportmember(self, interaction: discord.Interaction):
        embed = discord.Embed(title="`❗`Report a member", description="- **__How to report a Member:__**\n - Click the Report button below to access our report form.\n - Provide detailed information to assist us in addressing the issue effectively.\n - Note: Incidents originating outside our server are not within our jurisdiction unless they originated within Kanzen and transitioned to private communication.\n - Screenshots can be sent to a staff member or Reece for further review.\n - Thank you for helping us maintain a safe environment.", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text="Please wait for Hoshi to confirm your report has been sent before sending another!", icon_url=interaction.user.avatar)
        view = reportmemberbutton()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def delete_rep(self, member_id):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM staffrep WHERE member_id = ?", member_id)
            await conn.commit()

    @commands.command()
    async def delrep(self, ctx, id: str):
        await self.delete_rep(member_id=id)
        await ctx.reply(f'Okay! I have deleted <@{id}> from the staff rep database')

async def setup(bot):
    await bot.add_cog(Moderation(bot))