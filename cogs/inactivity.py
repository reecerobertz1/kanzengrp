import discord
from discord.ext import commands

class inactive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ia(self, ctx, *, message):
        channel = self.bot.get_channel(1121913672822968330)

        embed = discord.Embed(title=f'{ctx.author.name} has sent an inactivity message', description=message, color=0x2b2d31)
        embed.set_footer(text=f"Member ID: {ctx.author.id} | Member Name: {ctx.author.name}")

        await channel.send(embed=embed)
        await ctx.send("Your inactivity message has been sent.")

        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(inactive(bot))