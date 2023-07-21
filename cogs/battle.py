import discord
from discord.ext import commands
import random
import asyncio

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.battle_in_progress = False

    def is_battle_action(self, action):
        actions = ["punch", "kick", "slap", "explode", "atomic bomb", "fortnite dance"]
        return action in actions

    def get_damage(self, action):
        if action == "punch":
            return 5
        elif action == "kick":
            return 10
        elif action == "slap":
            return 3
        elif action == "explode":
            return 40
        elif action == "atomic bomb":
            return 60
        elif action == "fortnite dance":
            return 100
        else:
            return 0

    def get_battle_status_embed(self, ctx, opponent):
        # Replace this with your own logic to create the embed with the health status
        # You can use the ctx.author and opponent objects to get their names and health

        # Example:
        embed = discord.Embed(title="Battle Status")
        embed.add_field(name=f"{ctx.author.display_name}'s Health", value="100", inline=False)
        embed.add_field(name=f"{opponent.display_name}'s Health", value="100", inline=False)
        return embed

    @commands.command()
    async def battle(self, ctx, opponent: discord.Member):
        if self.battle_in_progress:
            await ctx.send("A battle is already in progress.")
            return

        if opponent == ctx.author:
            await ctx.send("You cannot battle yourself!")
            return

        def check_author(m):
            return m.author == ctx.author and self.is_battle_action(m.content.lower())

        def check_opponent(m):
            return m.author == opponent and m.content.lower() in ["yes", "no"]

        await ctx.send(f"{ctx.author.mention} has challenged {opponent.mention} to a battle!")
        await ctx.send(f"{opponent.mention}, do you accept the challenge? Type `yes` or `no`.")

        try:
            response = await self.bot.wait_for('message', timeout=30.0, check=check_opponent)
        except asyncio.TimeoutError:
            await ctx.send(f"{opponent.mention} did not respond. The battle has been canceled.")
            return

        if response.content.lower() != "yes":
            await ctx.send(f"{opponent.mention} declined the challenge. The battle has been canceled.")
            return

        self.battle_in_progress = True
        player_embed = self.get_battle_status_embed(ctx, opponent)
        status_message = await ctx.send(embed=player_embed)

        await ctx.send(f"The battle has begun between {ctx.author.mention} and {opponent.mention}!")

        while self.battle_in_progress:
            try:
                response = await self.bot.wait_for('message', timeout=30.0, check=check_author)
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.mention} took too long to respond. The battle has been canceled.")
                self.battle_in_progress = False
                break

            if response.content.lower() == "end":
                await ctx.send("The battle has ended.")
                self.battle_in_progress = False
                break

            action = response.content.lower()
            damage = self.get_damage(action)
            # Update the player's health and create a new embed with updated health
            # ...
            player_embed = self.get_battle_status_embed(ctx, opponent)  # Replace with your logic to update the health
            await status_message.edit(embed=player_embed)

    @commands.command()
    async def endbattle(self, ctx):
        if not self.battle_in_progress:
            await ctx.send("No battle is currently in progress.")
            return

        await ctx.send("The battle has been ended.")
        self.battle_in_progress = False


async def setup(bot):
    await bot.add_cog(Battle(bot))