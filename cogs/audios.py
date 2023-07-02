import json
import random
import discord
from discord.ext import commands

class audios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot = bot
        self.audio_links = ['https://on.soundcloud.com/WwHQzqBHCafrdgLe6']

    @commands.command()
    async def addaudio(self, ctx, link):
        self.audio_links.append(link)
        await ctx.send("Audio added successfully.")

    @commands.command()
    async def audios(self, ctx):
        if self.audio_links:
            audio_link = random.choice(self.audio_links)
            await ctx.reply('You can upload an audio by doing `+addaudio`', audio_link)
        else:
            await ctx.send("No one has added their edit yet! Be the first to add an edit by using the command `addedit (streamable link)`.")

async def setup(bot):
    await bot.add_cog(audios(bot))