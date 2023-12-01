import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from tof.getQuestions import getQuestions
from tof.manager import buttonHandler

class tof (commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.hidden = True
        self.emoji = "<:shooky:1121909564799987722>"

    @commands.hybrid_command(name="trueorfalse", description="Play guess True or False", timeout=3.0)
    async def trueorfalse(self, ctx):
        initial_message = await ctx.send("True or False?")
        view = buttonHandler(initial_message)
        embed, answer = await getQuestions()
        view.currentAns = answer
        await initial_message.edit(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(tof(bot))