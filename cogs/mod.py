import discord
from discord.ext import commands
from discord import app_commands

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2b2d31

    @commands.hybrid_command(name="dm", aliases=["message"], description="Dm a user through hoshi", extras="+dm @member (message) : alias +message")
    async def dm(self, ctx, member: discord.Member, *, message: str):
        await member.send(message)
        await ctx.send(f"i have successfully messaged {member.mention}\n{message}")   

async def setup(bot):
    await bot.add_cog(mod(bot))