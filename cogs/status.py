import discord
from discord.ext import commands

class status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx, *, status_text):
        """Set the bot's status message."""
        activity = discord.Game(name=status_text)
        await self.bot.change_presence(activity=activity)
        await ctx.send(f"Status set to: {status_text}")

async def setup(bot):
    await bot.add_cog(status(bot))