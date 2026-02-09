import discord
from discord.ext import commands
from discord import app_commands

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2b2d31

    @commands.command(name="dm")
    async def dm(self, ctx, user: discord.User, *, message: str):
        await user.send(message)
        await ctx.send(f"i have successfully messaged {user.mention}\n{message}")   

async def setup(bot):
    await bot.add_cog(mod(bot))