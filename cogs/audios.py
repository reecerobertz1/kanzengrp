import json
import random
import discord
from discord.ext import commands

class audios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_links = ['https://on.soundcloud.com/WwHQzqBHCafrdgLe6']

    @commands.command()
    async def addaudio(self, ctx, link):
        self.audio_links.append(link)
        await ctx.send("Audio added successfully.")

    @commands.group(aliases=['audios'])
    async def audio(self, ctx):
        with open("audios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.send(f"Add an audio with `+addaudio` {choice}")

async def setup(bot):
    await bot.add_cog(audios(bot))