import discord
from discord.ext import commands

class inactive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server2_channel_id = 1122251494700363868
        self.server3_channel_id = 1058814073380274326

    @commands.command()
    async def ia(self, ctx, *, message):
        if ctx.guild.id == 1121841073673736215:
            await ctx.send("Hey, this command doesn't work anymore in kanzengrp, please use `/ia` instead!")
            return

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
        if guild_id == 957987670787764224:
            return self.server2_channel_id
        elif guild_id == 896619762354892821:
            return self.server3_channel_id
        else:
            return None


async def setup(bot):
    await bot.add_cog(inactive(bot))