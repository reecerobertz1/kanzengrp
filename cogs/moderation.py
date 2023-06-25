import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




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



async def setup(bot):
    await bot.add_cog(Moderation(bot))