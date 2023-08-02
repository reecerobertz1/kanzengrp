import json
import random
import discord
from discord.ext import commands

class audios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _add_audio(self, ctx, filename, link):
        audio_data = link
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(audio_data)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        await ctx.reply("Audio added successfully.")

    @commands.command()
    async def addsoft(self, ctx, link):
        """Adds a streamable link to softaudios.json"""
        await self._add_audio(ctx, "softaudios.json", link)

    @commands.command()
    async def addhot(self, ctx, link):
        """Adds a streamable link to hotaudios.json"""
        await self._add_audio(ctx, "hotaudios.json", link)

    @commands.command(aliases=['softaudio'])
    async def soft(self, ctx):
        """Sends a random link from softaudios.json"""
        with open("softaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a soft audio with `+addsoft`\n{choice}")

    @commands.command(aliases=['hotaudio'])
    async def hot(self, ctx):
        """Sends a random link from hotaudios.json"""
        with open("hotaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a hot audio with `+addhot`\n{choice}")

async def setup(bot):
    await bot.add_cog(audios(bot))