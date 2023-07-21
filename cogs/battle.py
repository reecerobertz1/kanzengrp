
import asyncio
import discord
from discord.ext import commands
import random

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hp = 100
        self.battle_actions = {
            "punch": 5,
            "kick": 10,
            "slap": 3,
            "explode": 40,
            "atomic bomb": 60,
            "fortnite dance": 100
        }
        self.unlocked_actions = ["punch", "kick", "slap"]  # Start with these unlocked actions

    def get_random_action(self):
        return random.choice(list(self.battle_actions.keys()))

    @commands.command()
    async def battle(self, ctx, opponent: discord.Member):
        if opponent == ctx.author:
            await ctx.send("You cannot battle yourself!")
            return

        player_hp = self.hp
        opponent_hp = self.hp

        def check_author(m):
            return m.author == ctx.author and m.content.lower() in self.battle_actions

        def check_opponent(m):
            return m.author == opponent and m.content.lower() in self.battle_actions

        def get_battle_status_embed():
            return discord.Embed(title="Battle!", description=f"{ctx.author.mention} vs {opponent.mention}\n"
                                                              f"{ctx.author.display_name} HP: {player_hp}\n"
                                                              f"{opponent.display_name} HP: {opponent_hp}", color=0xFF5733)

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

        await ctx.send(f"The battle has begun between {ctx.author.mention} and {opponent.mention}!")

        while player_hp > 0 and opponent_hp > 0:
            await ctx.send(f"{ctx.author.mention}, choose your action: {', '.join(self.unlocked_actions)}")
            action = await self.bot.wait_for('message', check=check_author)
            action = action.content.lower()

            if action not in self.unlocked_actions:
                await ctx.send("You can't use this action yet. Keep battling to unlock it!")
                continue

            await ctx.send(f"{opponent.mention}, choose your action: {', '.join(self.unlocked_actions)}")
            response = await self.bot.wait_for('message', check=check_opponent)
            opponent_action = response.content.lower()

            damage_dealt = self.battle_actions[action]
            opponent_damage_dealt = self.battle_actions[opponent_action]

            player_hp -= opponent_damage_dealt
            opponent_hp -= damage_dealt

            embed = get_battle_status_embed()
            embed.add_field(name=f"{ctx.author.display_name} used {action}", value=f"Dealt {opponent_damage_dealt} damage", inline=False)
            embed.add_field(name=f"{opponent.display_name} used {opponent_action}", value=f"Dealt {damage_dealt} damage", inline=False)
            await ctx.send(embed=embed)

        if player_hp <= 0 and opponent_hp <= 0:
            await ctx.send("It's a tie! Both players have run out of HP.")
        elif player_hp <= 0:
            await ctx.send(f"{opponent.mention} won the battle! Better luck next time, {ctx.author.mention}!")
        else:
            await ctx.send(f"{ctx.author.mention} won the battle! Congratulations!")

async def setup(bot):
    await bot.add_cog(Battle(bot))