import discord
from discord.ext import commands

class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}

    @commands.command()
    async def afk(self, ctx, *, reason=""):
        member = ctx.author
        self.afk_users[member.id] = reason
        await ctx.send(f"{member.mention} is now AFK. Reason: {reason}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        for mention in message.mentions:
            if mention.id in self.afk_users:
                reason = self.afk_users[mention.id]
                await message.channel.send(f"{mention.mention} is AFK. Reason: {reason}")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.status != after.status and after.id in self.afk_users:
            del self.afk_users[after.id]


async def setup(bot):
    await bot.add_cog(other(bot))