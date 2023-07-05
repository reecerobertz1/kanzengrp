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
        await ctx.send("Edit added successfully.")

    @commands.command()
    async def edits(self, ctx):
        data = self.get_edits_data()
        if data:
            response = "\n".join(data)
            await ctx.send(f"Edit links:\n{response}")
        else:
            await ctx.send("No edit links found.")

async def setup(bot):
    await bot.add_cog(addedits(bot))