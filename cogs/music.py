import discord
from discord.ext import commands

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="join", description="joins voice channel", pass_context=True)
    async def join(self, ctx):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
            em = discord.Embed(
            title="Voice Channel Join",
            description="Successfully joined a voice channel",
            color=discord.Color.green()
            )
            await ctx.send(embed=em)
        else:
            await ctx.send("you ain't in a voice channel")

    @commands.hybrid_command(name="leave", description="leaves a voice channel", pass_context=True)
    async def leave(self, ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I left the voice channel")
        else:
            await ctx.send("I am not in a voice channel")

async def setup(bot):
    await bot.add_cog(music(bot))