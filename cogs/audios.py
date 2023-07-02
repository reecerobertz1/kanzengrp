import json
import random
import discord
from discord.ext import commands

class audios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addaudio(self, ctx, link):
        audio_data = link


        try:
            with open("addedaudios.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(audio_data)

        with open("addedaudios.json", "w") as file:
            json.dump(data, file, indent=4)

        await ctx.reply("Audio added successfully.")

    @commands.group(aliases=['audios'])
    async def audio(self, ctx):
        with open("addedaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add an audio with `+addaudio`\n{choice}")

async def setup(bot):
    await bot.add_cog(audios(bot))