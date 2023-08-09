import discord
from discord.ext import commands

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 


    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel!")
            voice_channel = ctx.author.voice.channel
            if ctx.voice_channel is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.reply("Okay, i have disconnected!")

async def setup(bot):
    await bot.add_cog(music(bot))