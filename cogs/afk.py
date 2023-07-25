import discord
from discord.ext import commands
import json
import datetime

class afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_data_file = "afk_data.json"

        with open(self.afk_data_file, "r") as f:
            self.afk_data = json.load(f)

    def save_afk_data(self):
        with open(self.afk_data_file, "w") as f:
            json.dump(self.afk_data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)

        if user_id in self.afk_data:
            afk_info = self.afk_data[user_id]
            reason = afk_info["reason"]
            timestamp = afk_info["timestamp"]

            afk_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            elapsed_time = datetime.datetime.utcnow() - afk_time

            await message.channel.send(
                f"{message.author.mention} is currently AFK.\n"
                f"AFK Reason: {reason}\n"
                f"AFK Duration: {elapsed_time}"
            )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.on_message(after)

    @commands.command()
    async def afk(self, ctx, *, reason: str = "AFK"):
        user_id = str(ctx.author.id)

        if user_id not in self.afk_data:
            self.afk_data[user_id] = {
                "reason": reason,
                "timestamp": str(datetime.datetime.utcnow()),
            }
            self.save_afk_data()

            await ctx.send(
                f"{ctx.author.mention} is now AFK. Reason: {reason}."
            )
        else:
            await ctx.send("You are already AFK!")

async def setup(bot):
    await bot.add_cog(afk(bot))