import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await ctx.join_voice_channel(channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.reply("Okay, i have disconnected!")

async def setup(bot):
    await bot.add_cog(music(bot))