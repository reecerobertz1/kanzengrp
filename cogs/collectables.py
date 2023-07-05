import json
import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 24*60*60, commands.BucketType.user)

    def get_unlock_data(self):
        try:
            with open("unlock_data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def save_unlock_data(self, data):
        with open("unlock_data.json", "w") as file:
            json.dump(data, file, indent=4)

    @commands.command()
    async def unlock(self, ctx):
        server_id = 1121841073673736215
        channel_id = 1125999933149949982
        member = ctx.author
        now = datetime.datetime.utcnow()
        cooldown_bucket = self.cooldown.get_bucket(ctx.message)
        retry_after = cooldown_bucket.update_rate_limit()

        if retry_after:
            seconds = round(retry_after)
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            await ctx.send(f"Please wait {hours} hours, {minutes} minutes, and {seconds} seconds before using this command again.")
            return

        if ctx.guild.id != server_id:
            await ctx.send("This command can only be used in the specified server.")
            return

        unlock_levels = {
            "common": 0,
            "uncommon": 0,
            "rare": 500,
            "epic": 1000,
            "legendary": 2000
        }

        unlock_level = random.choice(["common", "uncommon", "rare", "epic", "legendary"])
        xp = unlock_levels[unlock_level]

        if unlock_level in ["rare", "epic"]:
            xp_message = f"You have unlocked {xp}xp!"
            unlock_channel = self.bot.get_channel(channel_id)
            await unlock_channel.send(f"{member.mention} has unlocked - {xp} xp")

        elif unlock_level == "legendary":
            xp_message = f"You have unlocked a legendary logo! Check your dms!"
            unlock_channel = self.bot.get_channel(channel_id)
            await unlock_channel.send(f"{member.mention} has unlocked {xp}xp")

        else:
            xp_message = None

        if unlock_level == "legendary":
            embed = discord.Embed(title="Legendary Unlock", description="Congratulations on unlocking a legendary logo [click here](https://streamable.com/6l2840)!\nPlease don't share this logo with anyone else in the server!", color=discord.Color.gold())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await member.send(embed=embed)

        if xp_message:
            await ctx.send(xp_message)

        data = self.get_unlock_data()
        if str(member.id) not in data:
            data[str(member.id)] = []

        data[str(member.id)].append(unlock_level)
        self.save_unlock_data(data)

    @commands.command()
    async def unlocked(self, ctx):
        member = ctx.author
        data = self.get_unlock_data()

        if str(member.id) in data:
            unlocked_items = ", ".join(data[str(member.id)])
            await ctx.send(f"{member.mention}, you have unlocked the following items: {unlocked_items}")
        else:
            await ctx.send(f"{member.mention}, you have not unlocked any items yet.")

async def setup(bot):
    await bot.add_cog(Unlock(bot))
