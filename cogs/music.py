import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command(pass_context = True)
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.reply("You are currently not in a voice channel!")
            voice_channel = ctx.author.voice_channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)


    @commands.command(pass_context = True)
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.reply("Okay, i have disconnected!")

async def setup(bot):
    await bot.add_cog(music(bot))