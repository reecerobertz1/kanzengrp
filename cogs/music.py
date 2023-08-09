import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def join(self, ctx):
        if (ctx.author.voice):
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You are currently not in a voice channel!")

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.reply("Okay, i have disconnected!")

async def setup(bot):
    await bot.add_cog(music(bot))