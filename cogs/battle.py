import discord
from discord.ext import commands
import random
import asyncio

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

        def check_author(m):
            return m.author == ctx.author and m.content.lower() in self.battle_actions

        def check_opponent(m):
            return m.author == opponent and m.content.lower() in self.battle_actions

        def get_battle_status_embed():
            return discord.Embed(title="Battle!", description=f"{ctx.author.mention} vs {opponent.mention}\n"
                                                              f"{ctx.author.display_name} HP: {self.hp}\n"
                                                              f"{opponent.display_name} HP: {self.hp}", color=0xFF5733)

        await ctx.send(f"{ctx.author.mention} has challenged {opponent.mention} to a battle!")
        await ctx.send(f"{opponent.mention}, do you accept the challenge? Type `yes` or `no`.")

        try:
            response = await self.bot.wait_for('message', timeout=30.0, check=lambda m: m.author == opponent)
        except asyncio.TimeoutError:
            await ctx.send(f"{opponent.mention} did not respond. The battle has been canceled.")
            return

        if response.content.lower() != "yes":
            await ctx.send(f"{opponent.mention} declined the challenge. The battle has been canceled.")
            return

        player_embed = get_battle_status_embed()
        await ctx.send(embed=player_embed)

        await ctx.send(f"The battle has begun between {ctx.author.mention} and {opponent.mention}!")

        while player_embed.fields[0].value != "0" and player_embed.fields[1].value != "0":
            await ctx.send(f"{ctx.author.mention}, choose your action: {', '.join(self.unlocked_actions)}")
            try:
                action = await self.bot.wait_for('message', timeout=30.0, check=check_author)
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.mention} did not respond in time. The battle has been canceled.")
                return

            action = action.content.lower()

            if action not in self.unlocked_actions:
                await ctx.send("You can't use this action yet. Keep battling to unlock it!")
                continue

            opponent_action = self.get_random_action()
            damage_dealt = self.battle_actions[action]
            opponent_damage_dealt = self.battle_actions[opponent_action]

            player_embed.fields[0].value = str(int(player_embed.fields[0].value) - opponent_damage_dealt)
            player_embed.fields[1].value = str(int(player_embed.fields[1].value) - damage_dealt)

            await ctx.send(f"{ctx.author.mention} used {action} and dealt {opponent_damage_dealt} damage!")
            await ctx.send(f"{opponent.mention} used {opponent_action} and dealt {damage_dealt} damage!")

            await asyncio.sleep(1)
            await ctx.send(embed=player_embed)

        if player_embed.fields[0].value == "0" and player_embed.fields[1].value == "0":
            await ctx.send("It's a tie! Both players have run out of HP.")
        elif player_embed.fields[0].value == "0":
            await ctx.send(f"{opponent.mention} won the battle! Better luck next time, {ctx.author.mention}!")
        else:
            await ctx.send(f"{ctx.author.mention} won the battle! Congratulations!")


async def setup(bot):
    await bot.add_cog(Battle(bot))