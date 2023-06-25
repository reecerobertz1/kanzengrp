import discord
from discord.ext import commands

class inactive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ia(self, ctx, *, message):
        channel = self.bot.get_channel(1121913672822968330)

        member = ctx.author
        server_nickname = member.nick if member.nick else member.name

        embed = discord.Embed(title='Inactivity Message', description=message, color=0xFF6F6F)
        embed.set_footer(text=f"Member ID: {member.id} | Member: {server_nickname}")

        await channel.send(embed=embed)
        await ctx.send("Your inactivity message has been sent!")
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(inactive(bot))