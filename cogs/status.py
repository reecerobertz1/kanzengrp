import discord
from discord.ext import commands
from discord import Game

class status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.set_status()

    async def set_status(self):
        activity = Game(name="Hoshi ♡")
        await self.bot.change_presence(activity=activity)

async def setup(bot):
    await bot.add_cog(status(bot))