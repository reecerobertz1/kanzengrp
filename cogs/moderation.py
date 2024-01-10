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

    async def view_warnings(self, ctx, member: discord.Member):
        guild_id = ctx.guild.id
        member_id = member.id

        async with self.pool.acquire() as conn:
            warning = await conn.fetchrow('SELECT reasons FROM warning WHERE member_id = $1 AND guild_id = $2', member_id, guild_id)

        if warning:
            embed = discord.Embed(
                title=f"Warnings for {member.display_name}",
                color=0x2b2d31,
                timestamp=datetime.utcnow()
            )

            embed.add_field(name="Warning", value=warning['reasons'], inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.display_name} has no warnings.")

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

    @commands.hybrid_command(name="clearwarnings",aliases=['cw'], description="Clear all warnings from a member", extras="+clearwarnings @member : alias +cw")
    @is_staff()
    async def clearwarnings(self, ctx, member: discord.Member):
        guild_id = ctx.guild.id
        member_id = member.id

        async with self.pool.acquire() as conn:
            await conn.execute('DELETE FROM warning WHERE member_id = $1 AND guild_id = $2', member_id, guild_id)

        await ctx.send(f"Warnings for {member.display_name} have been cleared.")

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
        
    @commands.hybrid_command(name="dm", aliases=["message"], description="Dm a user through hoshi", extras="+dm @member (message) : alias +message")
    async def dm(self, ctx, member: discord.Member, *, message: str):
        await member.send(message)
        await ctx.send(f"i have successfully messaged {member.mention}\n{message}")        

    async def get_rep(self, member_id, guild_id, helped):
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

    async def update_rep(self, member_id, guild_id, helped, change=1):
        async with self.pool.acquire() as conn:
            existing_warnings = await conn.fetchone('SELECT count FROM staffrep WHERE member_id = $1 AND guild_id = $2', member_id, guild_id)
            if existing_warnings:
                current_warnings = existing_warnings['count']
                updated_warnings = current_warnings + change
                await conn.execute('UPDATE staffrep SET helped = $1, count = $2 WHERE member_id = $3 AND guild_id = $4',
                                helped, updated_warnings, member_id, guild_id)
            else:
                updated_warnings = change
                await self.add_rep(member_id, guild_id, helped, updated_warnings)
            await conn.commit()
            return updated_warnings

    @commands.hybrid_command(name="staffrep", description="add rep to a staff member for helping", extra="+staffrep @member")
    @commands.has_permissions(administrator=True)
    @commands.has_permissions(manage_guild=True)
    async def staffrep(self, ctx, member: discord.Member, *, helped):
        await self.update_rep(member.id, ctx.guild.id, helped)
        await ctx.reply(f"Successfully added rep for {member.display_name}\n**{helped}**")

    async def reset_staffrep(self, guild_id: int) -> None:
        """Resets the levels for a guild
        
        Parameters
        ----------
        guild_id: int
            ID of guild to reset levels in
        """
        query = '''UPDATE staffrep SET count = 0, helped = NULL WHERE guild_id = $1'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                await conn.commit()
        await self.bot.pool.release(conn)

    @commands.command(aliases=['rr'], description="Reset the staff rep", extras="alias : +rr")
    @commands.has_permissions(administrator=True)
    @commands.has_permissions(manage_guild=True)
    async def resetrep(self, ctx: commands.Context):
        """Wipes all XP from the database"""
        message = await ctx.reply("are you sure you want to reset the staff rep? it's irreversible!")
        await message.add_reaction('👍')

        def check(reaction, user):
            return user == ctx.author and str(reaction) == '👍'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
            await self.reset_staffrep(ctx.guild.id)
            embed = discord.Embed(
                title='success!',
                description=f'reps have been erased.',
                color=0x2B2D31
            )
            return await message.edit(content=None, embed=embed)
        except asyncio.TimeoutError:
            await message.edit(content="~~are you sure you want to reset the ranks? it's irreversible!~~\nreset has been cancelled!")

    @commands.command()
    async def showrep(self, ctx, member: discord.Member, *, helped=""):
        rep = await self.get_rep(member.id, ctx.guild.id, helped)
        embed = discord.Embed(title=f"Rep for {member.display_name}", color=0x2b2d31)
        embed.add_field(name="Amount of rep:", value=rep[0], inline=False)
        embed.add_field(name="Last helped with:", value=rep[1], inline=False)
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))