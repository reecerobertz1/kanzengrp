from datetime import datetime
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.command()
    async def uptime(self, ctx):
        current_time = datetime.now()
        uptime = current_time - self.start_time

        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

        await ctx.reply(f"Bot Uptime: {uptime_str}")



    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def addrole(self, ctx, role: discord.Role, user: discord.Member):
        await user.add_roles(role)
        await ctx.reply(f'Successfully added {role.mention} to {user.mention}')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def removerole(self, ctx, role: discord.Role, user: discord.Member):
        await user.remove_roles(role)
        await ctx.reply(f'Successfully removed {role.mention} from {user.mention}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for reason: {reason}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for reason: {reason}')

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds

        await ctx.reply(f"Pong! :ping_pong: Latency: {latency}ms")


    @commands.command()
    async def createrole(self, ctx, role_name, role_color):
        guild = ctx.guild

        # Check if the role already exists
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if existing_role:
            await ctx.send(f"A role with the name '{role_name}' already exists.")
            return

        # Create the role
        try:
            role = await guild.create_role(name=role_name, color=discord.Color(role_color))
            await ctx.send(f"Role '{role_name}' has been created with color #{role.color.value:06x}.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to create roles.")
        except discord.HTTPException:
            await ctx.send("Failed to create the role.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))