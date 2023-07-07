import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from spotdl.search.songObj import SongObj
from spotdl.search.spotifyClient import SpotifyClient
from spotdl.download.downloader import download_song
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        channel = ctx.message.author.voice.channel
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
        else:
            voice_client = await channel.connect()

        if "soundcloud.com" in url:
            source = await self.get_soundcloud_source(url)
        elif "spotify.com" in url:
            source = await self.get_spotify_source(url)
        else:
            await ctx.send("Invalid link provided.")
            return

        voice_client.play(source)

    async def get_soundcloud_source(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, method='fallback')

        return source

    async def get_spotify_source(self, url):
        spotify_client = SpotifyClient()
        song_obj = SongObj(url)

        await spotify_client.build_song(song_obj)

        try:
            download_song(song_obj)
        except Exception as e:
            print(f"An error occurred while downloading the song: {e}")
            return None

        source = await discord.FFmpegOpusAudio.from_probe(song_obj.file_path, method='fallback')

        return source

    @commands.command()
    async def pause(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.send("Playback paused.")
        else:
            await ctx.send("No audio is currently playing.")

    @commands.command()
    async def stop(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Playback stopped.")
        else:
            await ctx.send("No audio is currently playing.")

    @commands.command()
    async def queue(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_playing():
            queue = voice_client.source
            await ctx.send(f"Current queue: {queue}")
        else:
            await ctx.send("No audio is currently playing.")


async def setup(bot):
    await bot.add_cog(Music(bot))