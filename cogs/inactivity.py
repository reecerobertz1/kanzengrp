import discord
from discord.ext import commands

class inactive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server1_channel_id = 1121913672822968330
        self.server2_channel_id = 1122251494700363868

    @commands.command()
    async def ia(self, ctx, *, message):
        channel_id = self.get_channel_id(ctx.guild.id)
        if channel_id is None:
            await ctx.send("This command is not available in this server.")
            return

        channel = self.bot.get_channel(channel_id)
        member = ctx.author
        server_nickname = member.nick if member.nick else member.name

        embed = discord.Embed(title='Inactivity Message', description=message, color=0xFF6F6F)
        embed.set_footer(text=f"Member ID: {member.id} | Member: {server_nickname}")

        await channel.send(embed=embed)
        await ctx.send("Your inactivity message has been sent!")
        await ctx.message.delete()

    def get_channel_id(self, guild_id):
        if guild_id == 1121841073673736215:
            return self.server1_channel_id
        elif guild_id == 957987670787764224:
            return self.server2_channel_id
        else:
            return None


async def setup(bot):
    await bot.add_cog(inactive(bot))