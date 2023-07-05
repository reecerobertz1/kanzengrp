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
            data = {}
        return data

    def save_edits_data(self, data):
        with open("edits.json", "w") as file:
            json.dump(data, file, indent=4)

    @commands.command()
    async def addedit(self, ctx, link):
        guild_id = str(ctx.guild.id)
        data = self.get_edits_data()

        if guild_id not in data:
            data[guild_id] = []

        data[guild_id].append(link)
        self.save_edits_data(data)
        await ctx.send("Edit added successfully.")

    @commands.command()
    async def edits(self, ctx):
        guild_id = str(ctx.guild.id)
        data = self.get_edits_data()

        if guild_id in data:
            edit_links = data[guild_id]
            if edit_links:
                response = "\n".join(edit_links)
                await ctx.send(f"Edit links for this server:\n{response}")
            else:
                await ctx.send("No edit links found for this server.")
        else:
            await ctx.send("No edit links found for this server.")

async def setup(bot):
    await bot.add_cog(addedits(bot))