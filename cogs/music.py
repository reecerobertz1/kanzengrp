import asyncio
import discord
from discord.ext import commands
import youtube_dl


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play_song', help='To play a song')
    async def play(self, ctx, url):
        server = ctx.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await self.ytdl_source(url)
            voice_channel.play(discord.FFmpegPCMAudio(executable="C:\\Users\\abhisar.ahuja\\Documents\\ffmpeg\\ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))

    async def ytdl_source(self, url):
        data = await self.bot.loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title']
        return filename

    @commands.command(name='join', help='Tells the bot to join the voice channel')
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.author.name))
            return
        else:
            channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Music(bot))