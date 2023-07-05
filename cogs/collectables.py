import json
import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_unlock_data(self, guild_id):
        if guild_id not in self.unlock_data:
            self.unlock_data[guild_id] = {}
        return self.unlock_data[guild_id]

    def save_unlock_data(self):
        with open("unlock_data.json", "w") as file:
            json.dump(self.unlock_data, file, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            with open("unlock_data.json", "r") as file:
                self.unlock_data = json.load(file)
        except FileNotFoundError:
            self.unlock_data = {}

    @commands.command()
    async def unlock(self, ctx):
        guild_id = 1121841073673736215
        member = ctx.author

        if ctx.guild.id != guild_id:
            await ctx.send("This command can only be used in the specified server.")
            return

        unlock_levels = {
            "common": {
                "message": "Hey! You found a common item! Here's a cool emoji to add to your collection:",
                "xp": 0,
                "emojis": ["emoji1", "emoji2", "emoji3", ...]  # Add 30 different emojis here
            },
            "uncommon": {
                "message": "Hey! You found an uncommon item! Here's a cool emoji to add to your collection:",
                "xp": 0,
                "emojis": ["emoji1", "emoji2", "emoji3", ...]  # Add 30 different emojis here
            },
            "rare": {
                "message": "Hey! You found a rare item! Here's an emoji to add to your collection and 500 XP:",
                "xp": 500,
                "emojis": ["emoji1", "emoji2", "emoji3", ...]  # Add 30 different emojis here
            },
            "epic": {
                "message": "Hey! You found an epic item! Here's an emoji to add to your collection and 1000 XP:",
                "xp": 1000,
                "emojis": ["emoji1", "emoji2", "emoji3", ...]  # Add 30 different emojis here
            },
            "legendary": {
                "message": "Hey! You found a legendary item! Here's an emoji to add to your collection and 2000 XP:",
                "xp": 2000,
                "emojis": ["emoji1", "emoji2", "emoji3", ...]  # Add 30 different emojis here
            }
        }

        unlock_level = random.choices(
            ["common", "uncommon", "rare", "epic", "legendary"],
            weights=[40, 30, 15, 10, 5],
            k=1
        )[0]
        unlock_data = unlock_levels[unlock_level]

        if unlock_level in ["rare", "epic", "legendary"]:
            xp = unlock_data["xp"]
            xp_message = unlock_data["message"]
            unlock_channel_id = 1125999933149949982  # ID of the unlock channel
            unlock_channel = self.bot.get_channel(unlock_channel_id)
            await unlock_channel.send(f"{member.mention} has found {xp} XP!")

            if unlock_level == "legendary":
                embed = discord.Embed(
                    title="Legendary Unlock",
                    description="Congratulations on unlocking a legendary item!\n\nPlease don't share this with anyone else in the server.",
                    color=discord.Color.gold()
                )
                await member.send(embed=embed)
                await unlock_channel.send(f"{member.mention} has unlocked 2000 XP!")
            else:
                await ctx.send(f"{xp_message} {random.choice(unlock_data['emojis'])}")

        elif unlock_level in ["common", "uncommon"]:
            xp_message = unlock_data["message"]
            await ctx.send(f"{xp_message} {random.choice(unlock_data['emojis'])}")

        guild_unlock_data = self.get_unlock_data(ctx.guild.id)
        if str(member.id) not in guild_unlock_data:
            guild_unlock_data[str(member.id)] = []
        guild_unlock_data[str(member.id)].append(unlock_level)
        self.save_unlock_data()

    @commands.command()
    async def unlocked(self, ctx):
        guild_id = 1121841073673736215
        member = ctx.author

        if ctx.guild.id != guild_id:
            await ctx.send("This command can only be used in the specified server.")
            return

        guild_unlock_data = self.get_unlock_data(ctx.guild.id)

        if str(member.id) in guild_unlock_data and guild_unlock_data[str(member.id)]:
            unlocked_items = ", ".join(guild_unlock_data[str(member.id)])
            await ctx.send(f"{member.mention}, you have unlocked the following items: {unlocked_items}")
        else:
            await ctx.send(f"{member.mention}, you have not unlocked any items yet.")


async def setup(bot):
    await bot.add_cog(Unlock(bot))
