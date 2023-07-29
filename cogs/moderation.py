import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

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
            embed.set_footer(text='React with ✅ for yes and ❌ for no')

            suggestion_message = await suggestion_channel.send(f"Suggestion made by {ctx.author.mention}", embed=embed)
            await suggestion_message.add_reaction("✅")
            await suggestion_message.add_reaction("❌")

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
    async def kick(self, interaction: discord.Interaction ,member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f'{member.mention} has been banned for: {reason}', ephemeral=True)
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("You have no admin", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(self, interaction: discord.Interaction ,member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
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
            embed.set_footer(text=f"users id: {user.id}")
            await log_channel.send(embed=embed)
        else:
            await ctx.send("Logging channel not found. Please set the correct channel ID.")

    @commands.command()
    async def roles(self, ctx):

        all_roles_embed = discord.Embed(title="Pronouns",description="<:1:1134874996955689020><@&1131127209952809031>\n<:2:1134874999342252194><@&1131127428668997737>\n<:3:1134875001045135360><@&1131127449753751663>\n<:4:1134875003746275429><@&1131127502396465213>\n<:5:1134875005243641956><@&1131127472142958622>\n<:6:1134875007567274055><@&1131127523456069723>", color=0x2b2d31)
        all_roles_embed.footer = ("- Use the emojis below to select your role")

        # Create the second embed showing roles categorized by color
        color_roles_embed = discord.Embed(title="Pings",description="<:1:1134874996955689020> <@&1133770119777099866>\n<:2:1134874999342252194> <@&1131127168102055996>\n<:3:1134875001045135360> <@&1131127104226992208>\n<:4:1134875003746275429> <@&1131005057417105418>\n<:5_:1134875005243641956> <@&1131127124187684894>" ,color=0x2b2d31)
        color_roles_embed.footer = ("- Use the emojis below to select your role")

        tits_embed = discord.Embed(title="Member Pings",description="<:1:1134874996955689020> <@&1131130157160206396>\n<:2:1134874999342252194> <@&1131127084379549757>\n<:3:1134875001045135360><@&1131130102328078336>\n<:4:1134875003746275429><@&1131127146186821685>\n<:5_:1134875005243641956><@&1134876934585712773>" ,color=0x2b2d31)
        tits_embed.footer = ("- Use the emojis below to select your role")

        # Send both embeds
        await ctx.send(embed=all_roles_embed)
        await ctx.send(embed=color_roles_embed)
        await ctx.send(embed=tits_embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))