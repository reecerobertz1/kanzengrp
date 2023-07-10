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
        coins = random.randint(1, 1000)
        xp = random.randint(1, 500)
        await ctx.send(f"You found {coins} coins!")

        if random.random() < 0.5:
            channel = self.bot.get_channel(1125999933149949982)
            await channel.send(f"{ctx.author.mention} found {xp} XP!")

        user_id = str(ctx.author.id)
        update_user_coins(user_id, coins)
        update_user_xp(user_id, xp)

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Shop", description="Welcome to the shop!")
        embed.add_field(name="XP", value="Price: 100 coins", inline=False)
        embed.add_field(name="Emoji", value="Price: 200 coins", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item: str):
        coins = get_user_coins(str(ctx.author.id))
        if item.lower() == "xp":
            price = 100
            if coins >= price:
                # Deduct coins from user's balance
                coins -= price
                update_user_coins(str(ctx.author.id), coins)  # Update user's coin balance
                await ctx.send(f"{ctx.author.mention} bought XP!")
            else:
                await ctx.send("Insufficient coins!")

    @commands.command()
    async def balance(self, ctx):
        coins = get_user_coins(str(ctx.author.id))
        await ctx.send(f"{ctx.author.mention} has {coins} coins.")

def get_user_coins(user_id):
    with open("coin_data.json", "r") as file:
        coin_data = json.load(file)
    return coin_data.get(user_id, 0)

def update_user_coins(user_id, coins):
    with open("coin_data.json", "r") as file:
        coin_data = json.load(file)
    coin_data[user_id] = coins
    with open("coin_data.json", "w") as file:
        json.dump(coin_data, file)

def update_user_xp(user_id, xp):
    with open("xp_data.json", "r") as file:
        xp_data = json.load(file)
    xp_data[user_id] = xp
    with open("xp_data.json", "w") as file:
        json.dump(xp_data, file)

async def setup(bot):
    await bot.add_cog(Unlock(bot))
