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
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, duration: int, *, args):
        """Start a giveaway."""
        if duration <= 0:
            return await ctx.send("The duration must be greater than 0.")
        
        duration_hours = duration
        duration_seconds = duration_hours * 3600  # Convert hours to seconds

        args = args.split()
        prize = " ".join(args)
        host_mention = None

        if len(args) > 1:
            # Check if the last argument starts with "@" to determine if it's a host mention
            last_arg = args[-1]
            if last_arg.startswith("<@") and last_arg.endswith(">"):
                host_mention = last_arg
                prize = " ".join(args[:-1])
        
        giveaway_message = f"React with 🎉 to enter the giveaway for **{prize}**!\nDuration: {duration_hours} hours"
        giveaway_embed = discord.Embed(title="Giveaway", description=giveaway_message, color=0x2b2d31)

        if host_mention:
            giveaway_embed.add_field(name="Host", value=host_mention, inline=False)

        giveaway_msg = await ctx.send('<@&1131127104226992208>', embed=giveaway_embed)

        await giveaway_msg.add_reaction("🎉")
        self.giveaway_data[giveaway_msg.id] = {"prize": prize, "duration": duration_seconds, "entries": []}
        await self.save_giveaway_data()

        await asyncio.sleep(duration_seconds)
        await self.pick_winner(giveaway_msg)

    async def pick_winner(self, message):
        data = self.giveaway_data.get(message.id)
        if not data:
            return
        
        if not data["entries"]:
            return await message.channel.send("No one entered the giveaway. The prize will go unclaimed.")

        winner_id = random.choice(data["entries"])
        winner = self.bot.get_user(winner_id)

        if winner:
            prize = data["prize"]
            await message.channel.send(f"Congratulations to {winner.mention} for winning the giveaway for **{prize}**!\nPlease message a lead, staff/host for your prize")
        else:
            await message.channel.send("The giveaway winner could not be determined.")

        del self.giveaway_data[message.id]
        await self.save_giveaway_data()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot and str(reaction.emoji) == "🎉":
            data = self.giveaway_data.get(reaction.message.id)
            if data:
                data["entries"].append(user.id)
                await self.save_giveaway_data()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gapick(self, ctx, message_id: int):
        """Pick a winner for a specific giveaway."""
        message = await ctx.fetch_message(message_id)
        await self.pick_winner(message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gaclear(self, ctx):
        """Clear the giveaway data."""
        self.giveaway_data.clear()
        await self.save_giveaway_data()
        await ctx.send("Giveaway data has been cleared.")

    async def save_giveaway_data(self):
        with open("giveaway_data.json", "w") as f:
            json.dump(self.giveaway_data, f, indent=4)

    async def load_giveaway_data(self):
        try:
            with open("giveaway_data.json", "r") as f:
                self.giveaway_data = json.load(f)
        except FileNotFoundError:
            self.giveaway_data = {}

async def setup(bot):
    await bot.add_cog(Giveaway(bot))