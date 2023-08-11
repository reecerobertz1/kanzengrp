import asyncio
import datetime
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from discord.utils import get
from discord.ui import View, Select

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()

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
    async def memberlist(self, ctx):
        members = [member for member in ctx.guild.members if not member.bot]
        member_count = len(members)

        # If there are many members, the list might exceed the Discord message limit
        # In such cases, you can split the list into smaller chunks
        chunk_size = 1000
        chunks = [members[i:i+chunk_size] for i in range(0, len(members), chunk_size)]

        for i, chunk in enumerate(chunks, start=1):
            member_list_text = "\n".join([member.mention for member in chunk])
            await ctx.send(f"**Member List - Part {i}**\n{member_list_text}")

        await ctx.send(f"Total Members in the Server: {member_count}")

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
            
            kanzen_channel_id = 1133772155499327538
            kanzen = ctx.guild.get_channel(kanzen_channel_id)
            if kanzen:
                await kanzen.send(embed=embed)
            
            aura_channel_id = 1122242141037547531
            aura = ctx.guild.get_channel(aura_channel_id)
            if aura:
                await aura.send(embed=embed)
            
            await ctx.send("Great! I have sent out the update message!")
            await message.edit(content=None)
        except asyncio.TimeoutError:
            await message.edit(content="~~Are you sure you want to send this update message?~~\nThe update has been cancelled")

async def setup(bot):
    await bot.add_cog(Moderation(bot))