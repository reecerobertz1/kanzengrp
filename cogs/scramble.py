import discord
import random
from discord.ext import commands
import asyncio

# List of words for the game
WORDS = ["apple", "banana", "orange", "grape", "strawberry", "melon", "kiwi", "cherry", "peach"]

class scramble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def scramble(self, ctx):
        word = random.choice(WORDS)
        scrambled_word = ''.join(random.sample(word, len(word)))

        # Send the scrambled word as a message
        await ctx.reply(f"Unscramble the word: **{scrambled_word}**")

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            # Wait for the user's response
            response = await self.bot.wait_for('message', check=check, timeout=10.0)

            if response.content.lower() == word:
                await ctx.reply(f"Correct! The word is **{word}**.")
            else:
                await ctx.reply(f"Sorry, that's incorrect. The correct word is **{word}**.")
        except asyncio.TimeoutError:
            await ctx.reply("Time's up! The correct word is **{word}**.")

async def setup(bot):
    await bot.add_cog(scramble(bot))