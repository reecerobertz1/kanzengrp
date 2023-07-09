import json
import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.unlocked_items = {}

    @commands.command()
    async def daily(self, ctx):
        coins = ['150', '250', '300', '350', '400', '450', '500', '550', '600', '650', '700', '750', '800', '850', '900', '950', '1,000']
        rancoins= random.choice(coins)
        await ctx.reply(f'You have received <:coin:1127703632389865682> {rancoins}! Come back tomorrow to get more')

    @commands.command()
    async def xpshop(self, ctx):
        embed = discord.Embed(title='XP Shop', description='Use the command `+buy (XP amount) to buy XP!', color=0x2b2d31)
        embed.add_field(name='<:coin:1127703632389865682> 350', value='500xp', inline=False)
        embed.add_field(name='<:coin:1127703632389865682> 500', value='750xp', inline=False)
        embed.add_field(name='<:coin:1127703632389865682> 750', value='1,000xp', inline=False)
        embed.add_field(name='<:coin:1127703632389865682> 1,000', value='1,250xp', inline=False)
        embed.add_field(name='<:coin:1127703632389865682> 1,250', value='1,500xp', inline=False)
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Unlock(bot))
