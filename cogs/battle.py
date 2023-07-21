
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
    async def battle(self, ctx):
        player_hp = self.hp
        bot_hp = self.hp

        def check_author(m):
            return m.author == ctx.author and m.content.lower() in self.battle_actions

        while player_hp > 0 and bot_hp > 0:
            action = await ctx.bot.wait_for('message', check=check_author)
            action = action.content.lower()

            if action not in self.unlocked_actions:
                await ctx.send("You can't use this action yet. Keep battling to unlock it!")
                continue

            bot_action = self.get_random_action()
            damage_dealt = self.battle_actions[action]
            bot_damage_dealt = self.battle_actions[bot_action]

            player_hp -= bot_damage_dealt
            bot_hp -= damage_dealt

            embed = discord.Embed(title="Battle!", description=f"{ctx.author.mention} used {action} and dealt {bot_damage_dealt} damage to the bot.\n"
                                                              f"The bot used {bot_action} and dealt {damage_dealt} damage to you.\n"
                                                              f"Your HP: {player_hp}\nBot's HP: {bot_hp}", color=0xFF5733)
            await ctx.send(embed=embed)

        if player_hp <= 0:
            await ctx.send("You lost the battle. Better luck next time!")
        else:
            await ctx.send("Congratulations! You won the battle!")

async def setup(bot):
    await bot.add_cog(Battle(bot))