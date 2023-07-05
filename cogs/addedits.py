import json
import random
import discord
from discord.ext import commands

class addedits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_edits_data(self):
        try:
            with open("edits.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def save_edits_data(self, data):
        with open("edits.json", "w") as file:
            json.dump(data, file, indent=4)

    @commands.command()
    async def addedit(self, ctx, link):
        data = self.get_edits_data()
        data.append(link)
        self.save_edits_data(data)
        await ctx.reply("Your edit added successfully.")

    @commands.group(aliases=['audios'])
    async def audio(self, ctx):
        with open("edits.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add an audio with `+addaudio`\n{choice}")

async def setup(bot):
    await bot.add_cog(addedits(bot))