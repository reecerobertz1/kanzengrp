import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import PyNaCl

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()


    @commands.command(pass_context = True)
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.reply("Okay, i have disconnected!")

async def setup(bot):
    await bot.add_cog(music(bot))