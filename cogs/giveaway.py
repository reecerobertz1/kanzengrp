import asyncio
import discord
from discord.ext import commands
import json
import random

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_data = {}
        self.load_giveaway_data()

    @commands.command()
    async def giveaway(self, ctx, duration: int, *, prize: str):
        """Start a giveaway."""
        if duration <= 0:
            return await ctx.send("The duration must be greater than 0.")
        
        giveaway_message = f"React with 🎉 to enter the giveaway for **{prize}**!\nDuration: {duration} seconds"
        giveaway_embed = discord.Embed(title="Giveaway", description=giveaway_message)
        giveaway_msg = await ctx.send(embed=giveaway_embed)

        await giveaway_msg.add_reaction("🎉")
        self.giveaway_data[giveaway_msg.id] = {"prize": prize, "duration": duration, "entries": set()}
        await self.save_giveaway_data()

        await asyncio.sleep(duration)
        await self.pick_winner(giveaway_msg)

    async def pick_winner(self, message):
        data = self.giveaway_data.get(message.id)
        if not data:
            return
        
        if not data["entries"]:
            return await message.channel.send("No one entered the giveaway. The prize will go unclaimed.")

        winner_id = random.choice(list(data["entries"]))
        winner = self.bot.get_user(winner_id)

        if winner:
            prize = data["prize"]
            await message.channel.send(f"Congratulations to {winner.mention} for winning the giveaway for **{prize}**!")
        else:
            await message.channel.send("The giveaway winner could not be determined.")

        del self.giveaway_data[message.id]
        await self.save_giveaway_data()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot and str(reaction.emoji) == "🎉":
            data = self.giveaway_data.get(reaction.message.id)
            if data:
                data["entries"].add(user.id)
                await self.save_giveaway_data()

    @commands.command()
    async def gapick(self, ctx, message_id: int):
        """Pick a winner for a specific giveaway."""
        message = await ctx.fetch_message(message_id)
        await self.pick_winner(message)

    @commands.command()
    async def gaclear(self, ctx):
        """Clear the giveaway data."""
        self.giveaway_data.clear()
        await self.save_giveaway_data()
        await ctx.send("Giveaway data has been cleared.")

    async def save_giveaway_data(self):
        with open("giveaway_data.json", "w") as f:
            json.dump(self.giveaway_data, f)

    async def load_giveaway_data(self):
        try:
            with open("giveaway_data.json", "r") as f:
                self.giveaway_data = json.load(f)
        except FileNotFoundError:
            self.giveaway_data = {}

async def setup(bot):
    await bot.add_cog(Giveaway(bot))