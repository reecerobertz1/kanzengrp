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
        await ctx.send(f"You are now AFK. Reason: {reason}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        author = message.author
        if author.id != self.bot.user.id and author.id in self.afk_users:
            del self.afk_users[author.id]
            await message.channel.send(f"You are no longer AFK.")

        for mention in message.mentions:
            if mention.id in self.afk_users:
                reason = self.afk_users[mention.id]
                await message.channel.send(f"{mention.mention} is AFK. Reason: {reason}")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if user.id != self.bot.user.id and user.id in self.afk_users:
            del self.afk_users[user.id]
            await channel.send(f"{user.mention} is no longer AFK.")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.status != after.status and after.id in self.afk_users:
            del self.afk_users[after.id]


async def setup(bot):
    await bot.add_cog(other(bot))