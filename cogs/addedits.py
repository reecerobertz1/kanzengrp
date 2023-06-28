import json
import random
import discord
from discord.ext import commands

class addedits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def addedit(self, ctx, link: str):
        try:
            with open('streamable_links.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(link)

        with open('streamable_links.json', 'w') as file:
            json.dump(data, file, indent=4)

        await ctx.reply("Your edit was added successfully!")

    @commands.command()
    async def edits(self, ctx):
        try:
            with open('streamable_links.json', 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        if len(data) > 0:
            selected_link = random.choice(data)
            await ctx.reply('You can upload your own edits by doing `+addedit`', selected_link)
        else:
            await ctx.reply("No one has added their edit yet! Be the first to add an edit by using the command `addedit (streamable link)`.")




async def setup(bot):
    await bot.add_cog(addedits(bot))