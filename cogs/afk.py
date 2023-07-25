import os
import json
import discord
from discord.ext import commands
import datetime

class afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_data = {}  # Dictionary to store AFK data
        self.afk_file = "afk_data.json"  # JSON file to store AFK data

        # Load existing AFK data from the JSON file, if it exists
        if os.path.exists(self.afk_file):
            with open(self.afk_file, "r") as file:
                self.afk_data = json.load(file)

    def save_afk_data(self):
        # Save AFK data to the JSON file
        with open(self.afk_file, "w") as file:
            json.dump(self.afk_data, file)

    @commands.command()
    async def afk(self, ctx, *, reason: str):
        # Store the AFK status and reason for the user in the afk_data dictionary
        self.afk_data[str(ctx.author.id)] = {"reason": reason, "timestamp": datetime.datetime.now().isoformat()}
        self.save_afk_data()

        await ctx.send(f"{ctx.author.mention} is now AFK for {reason}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author.bot:
            return

        author_id = str(message.author.id)
        if author_id in self.afk_data:
            # If the author is AFK, send the AFK message and remove them from the AFK list
            afk_info = self.afk_data.pop(author_id)
            self.save_afk_data()

            timestamp = datetime.datetime.fromisoformat(afk_info["timestamp"])
            afk_duration = datetime.datetime.now() - timestamp
            afk_duration_str = str(afk_duration).split(".")[0]

            await message.channel.send(f"{message.author.mention} is AFK for {afk_info['reason']} and has been AFK for {afk_duration_str}.")

async def setup(bot):
    await bot.add_cog(afk(bot))