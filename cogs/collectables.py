import json
import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.unlocked_items = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.unlocked_items = {}

    @commands.command()
    async def unlock(self, ctx):
        guild_id = 1121841073673736215
        member = ctx.author

        if ctx.guild.id != guild_id:
            await ctx.reply("This command can only be used in the specified server.")
            return

        unlock_levels = {
            "common": {
                "message": "Hey! You found a <:common_00000:1126105163225120780> item! Here's a cool badge to add to your collection :",
                "xp": 0,
                "emojis": ["emoji1", "emoji2", "emoji3", ...]  # Add 30 different emojis here
            },
            "uncommon": {
                "message": "Hey! You found an <:uncommon_00001:1126105110972465193> item! Here's a cool badge to add to your collection :",
                "xp": 0,
                "emojis": ["emoji1", "emoji2", "emoji3", ...]  # Add 30 different emojis here
            },
            "rare": {
                "message": "Hey! You found a <:rare_00002:1126105193960984577> item! You found **500 XP** and an badge to add to your collection :",
                "xp": 500,
                "emojis": ["emoji1", "emoji2", "emoji3", ...]  # Add 30 different emojis here
            },
            "epic": {
                "message": "Hey! You found an <:epic_00003:1126105134552850452> item! You found **1000 XP** and an badge to add to your collection :",
                "xp": 1000,
                "emojis": ["emoji1", "emoji2", "emoji3", ...]  # Add 30 different emojis here
            },
            "legendary": {
                "message": "Hey! You found a <:legendary_00004:1126105079892680786> item! You found **2000 XP** and Here's an badge to add to your collection :",
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
                    description=f"{member.mention}, you have unlocked a legendary item!",
                    color=discord.Color.gold()
                )
                await member.send(embed=embed)
                await unlock_channel.send(f"{member.mention} has unlocked 2000 XP!")

        else:
            xp_message = unlock_data["message"]

        emoji = random.choice(unlock_data["emojis"])
        await ctx.reply(f"{xp_message} {emoji}")

        self.record_unlocked_item(member.id, unlock_level, emoji)

    @commands.command()
    async def unlocked(self, ctx):
        guild_id = 1121841073673736215
        member = ctx.author

        if ctx.guild.id != guild_id:
            await ctx.send("This command can only be used in the specified server.")
            return

        if member.id in self.unlocked_items and self.unlocked_items[member.id]:
            embed = discord.Embed(
                title="Unlocked Badges",
                description="You have unlocked the following items:",
                color=discord.Color.green()
            )

            rarity_categories = {
                "common": [],
                "uncommon": [],
                "rare": [],
                "epic": [],
                "legendary": []
            }

            for unlock in self.unlocked_items[member.id]:
                unlock_level, emoji = unlock
                rarity_categories[unlock_level].append(emoji)

            for rarity, emojis in rarity_categories.items():
                if emojis:
                    embed.add_field(name=rarity.capitalize(), value="\n".join(emojis))

            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"You have not unlocked any badges yet.")


    @commands.command()
    async def resetunlocks(self, ctx, member: discord.Member = None):
        guild_id = 1121841073673736215

        if ctx.guild.id != guild_id:
            await ctx.reply("This command can only be used in the specified server.")
            return

        member = member or ctx.author

        if member.id in self.unlocked_items:
            del self.unlocked_items[member.id]
            await ctx.send(f"Unlocked items for {member.mention} have been reset.")
        else:
            await ctx.reply(f"{member.mention} does not have any unlocked items.")


async def setup(bot):
    await bot.add_cog(Unlock(bot))
