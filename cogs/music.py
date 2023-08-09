import discord
from discord.ext import commands

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    """@commands.command()
    async def join(self, ctx):
        voice_channel = discord.utils.get(ctx.guild.voice_channels, id=1055799905978957854)
        if voice_channel:
            await voice_channel.connect()
        else:
            await ctx.send("Voice channel not found!")


    @commands.command(pass_context = True)
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.reply("Okay, i have disconnected!")"""

async def setup(bot):
    await bot.add_cog(music(bot))