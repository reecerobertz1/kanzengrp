import aiohttp
import discord
from discord.ext import commands, tasks
from discord import app_commands
import yt_dlp
import asyncio
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import io
from collections import deque
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from imageio_ffmpeg import get_ffmpeg_exe
from discord import File
from discord.ui import View, Button

class MusicUI(View):
    def __init__(self, bot, music_cog):
        super().__init__(timeout=None)
        self.bot = bot
        self.music_cog = music_cog

    @discord.ui.button(label="◁◁")
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Sorry, we can't go back to the last song played. This button is just for aesthetics", ephemeral=True)

    @discord.ui.button(label="▷")
    async def play_pause(self, interaction: discord.Interaction, button: discord.Button):
        guild_id = interaction.guild.id
        vc = self.music_cog.voice_clients.get(guild_id)

        if not vc or not vc.is_connected():
            await interaction.response.send_message("I'm not connected to a voice channel.", ephemeral=True)
            return

        if vc.is_playing():
            vc.pause()
            button.label = "▷"
            await interaction.response.send_message("Paused the current song.")
        elif vc.is_paused():
            vc.resume()
            button.label = "❚❚"
            await interaction.response.send_message("Resumed the song.")
        else:
            await interaction.response.send_message("Nothing is playing right now.", ephemeral=True)
            return

        await interaction.message.edit(view=self)

    @discord.ui.button(label="▷▷")
    async def skip(self, interaction: discord.Interaction, button: discord.Button):
        guild_id = interaction.guild.id
        vc = self.music_cog.voice_clients.get(guild_id)

        if not vc or not vc.is_connected():
            await interaction.response.send_message("I'm not connected to a voice channel.", ephemeral=True)
            return

        if vc.is_playing() or vc.is_paused():
            if guild_id in self.music_cog.queues and self.music_cog.queues[guild_id]:
                vc.stop()
                await interaction.response.send_message("Skipped to the next song.")
            else:
                vc.stop()
                await interaction.response.send_message("Queue has ended.")
        else:
            await interaction.response.send_message("No song is playing.", ephemeral=True)

    @discord.ui.button(label="↺")
    async def loop(self, interaction: discord.Interaction, button: discord.Button):
        guild_id = interaction.guild.id
        vc = self.music_cog.voice_clients.get(guild_id)

        if not vc or not vc.is_connected():
            await interaction.response.send_message("I'm not connected to a voice channel.", ephemeral=True)
            return

        self.music_cog.looping[guild_id] = not self.music_cog.looping.get(guild_id, False)
        if self.music_cog.looping[guild_id]:
            button.label = "↻"
            await interaction.response.send_message("The song will now loop.")
        else:
            button.label = "↺"
            await interaction.response.send_message("Looping has been disabled.")

        await interaction.message.edit(view=self)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify = Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id="35fa18c25bd24041af97e3f8f0b27d84",
            client_secret="3ca1783aac3c4f87ade7faab25ce6373"
        ))

        self.ytdl_format_options = {
            "format": "bestaudio[ext=webm]/bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "default_search": "ytsearch",
            "source_address": "0.0.0.0"
        }

        self.ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn"
        }

        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_format_options)
        self.ffmpeg_executable = get_ffmpeg_exe()

        self.queues = {}
        self.voice_clients = {}
        self.last_played_time = {}
        self.now_playing = {}
        self.text_channels = {}
        self.looping = {}  # Track loop state per guild

        self.check_inactivity.start()

    @tasks.loop(minutes=1)
    async def check_inactivity(self):
        current_time = time.time()
        for guild_id, last_time in list(self.last_played_time.items()):
            if current_time - last_time > 300:
                if guild_id in self.voice_clients and self.voice_clients[guild_id].is_connected():
                    if self.voice_clients[guild_id].is_playing():
                        self.voice_clients[guild_id].stop()
                    await self.voice_clients[guild_id].disconnect()
                    del self.voice_clients[guild_id]
                    del self.queues[guild_id]
                    del self.last_played_time[guild_id]
                    del self.text_channels[guild_id]
                    del self.looping[guild_id]
                    print(f"Disconnected from guild {guild_id} due to inactivity.")

    def generate_music_card(self, song_title: str, cover_image: bytes = None, queue: list = None, bg_color=(30, 30, 30), text_color=(255, 255, 255)) -> io.BytesIO:
        width, height = 1500, 500
        image = Image.new("RGBA", (width, height))

        if cover_image:
            cover = Image.open(io.BytesIO(cover_image)).convert("RGBA")
            cover_image_aspect_ratio = cover.width / cover.height
            target_aspect_ratio = 1.0

            if cover_image_aspect_ratio > target_aspect_ratio:
                new_width = int(cover.height * target_aspect_ratio)
                left = (cover.width - new_width) // 2
                right = left + new_width
                top = 0
                bottom = cover.height
            else:
                new_height = int(cover.width / target_aspect_ratio)
                top = (cover.height - new_height) // 2
                bottom = top + new_height
                left = 0
                right = cover.width

            cover = cover.crop((left, top, right, bottom))
            blurred_bg = cover.resize((1500, 1500)).filter(ImageFilter.GaussianBlur(radius=25))
            enhancer = ImageEnhance.Brightness(blurred_bg)
            blurred_bg = enhancer.enhance(0.6)

            y_offset = (1500 - 500) // 2
            cropped_bg = blurred_bg.crop((0, y_offset, 1500, y_offset + 500))
            image.paste(cropped_bg, (0, 0))
            overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw_overlay = ImageDraw.Draw(overlay)
            for y in range(height):
                alpha = int(180 * (y / height))
                draw_overlay.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
            image = Image.alpha_composite(image, overlay)

            cover = cover.resize((405, 405))
            mask = Image.open("./assets/music/cover_mask.png").convert("L").resize((405, 405))
            masked_cover = Image.new("RGBA", cover.size)
            masked_cover.paste(cover, (0, 0), mask)
            image.paste(masked_cover, (30, 45), masked_cover)
        else:
            draw = ImageDraw.Draw(image)
            draw.rectangle([(0, 0), (width, height)], fill=bg_color)

        draw = ImageDraw.Draw(image)

        try:
            font_now = ImageFont.truetype("./fonts/sfpro_bolditalic.otf", 65)
            font_main = ImageFont.truetype("./fonts/sfpro_regular.otf", 30)
            font_queue = ImageFont.truetype("./fonts/sfpro_regular.otf", 30)
        except:
            font_now = font_main = font_queue = ImageFont.load_default()

        def draw_text_with_shadow(draw_obj, position, text, font, fill, shadow_color=(0, 0, 0), offset=(2, 2)):
            x, y = position
            draw_obj.text((x + offset[0], y + offset[1]), text, font=font, fill=shadow_color)
            draw_obj.text((x, y), text, font=font, fill=fill)

        text_x = 466
        y_now = 175

        draw_text_with_shadow(draw, (text_x, y_now), "Now Playing", font_now, text_color)
        draw_text_with_shadow(draw, (text_x, y_now + 90), f"{song_title}", font_main, text_color)

        if queue:
            queues_x = 950
            queues_y = 25
            y_queue_start = queues_y + 0
            draw_text_with_shadow(draw, (queues_x, y_queue_start), "Queue", font_now, text_color)

            for i, item in enumerate(queue[:10], start=1):
                queue_y = y_queue_start + 80 + (i - 1) * 35
                queue_text = f"{i}. {item['title']}"
                draw_text_with_shadow(draw, (queues_x, queue_y), queue_text, font_queue, text_color)

        final = image.convert("RGB")
        buffer = io.BytesIO()
        final.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    @app_commands.command(name="play", description="Plays audio from a YouTube or Spotify URL")
    async def play(self, interaction: discord.Interaction, *, query: str):
        try:
            await interaction.response.defer()

            if not interaction.user.voice:
                return await interaction.followup.send("You must be in a voice channel.")

            if interaction.guild.id not in self.voice_clients or not self.voice_clients[interaction.guild.id].is_connected():
                vc = await interaction.user.voice.channel.connect()
                self.voice_clients[interaction.guild.id] = vc
                self.text_channels[interaction.guild.id] = interaction.channel

            if "spotify.com" in query and "track" in query:
                track = self.spotify.track(query)
                search = f"{track['name']} {track['artists'][0]['name']}"
                await self.add_to_queue(interaction, search)
                song_title = track["name"]
                await interaction.followup.send(f'Added **"{song_title}"** to the queue.')

            elif "spotify.com" in query and "playlist" in query:
                playlist = self.spotify.playlist(query)
                for item in playlist["tracks"]["items"]:
                    track = item["track"]
                    search = f"{track['name']} {track['artists'][0]['name']}"
                    await self.add_to_queue(interaction, search)
                await interaction.followup.send("All songs in the playlist were added to the queue.")

            else:
                await self.add_to_queue(interaction, query)
                last_song = self.queues[interaction.guild.id][-1]
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(last_song["url"], download=False))
                song_title = data.get("title", "Unknown Title")
                await interaction.followup.send(f'Added **"{song_title}"** to the queue.')

            self.last_played_time[interaction.guild.id] = time.time()

            if not self.voice_clients[interaction.guild.id].is_playing():
                await self.play_next(interaction)

        except Exception as e:
            print(f"Error in play: {e}")
            await interaction.followup.send(f"Error occurred while processing your request: {e}")

    async def add_to_queue(self, interaction: discord.Interaction, search: str):
        loop = asyncio.get_event_loop()
        
        try:
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(search, download=False))
            print(f"Extracted data in add_to_queue: {data}")
        except Exception as e:
            await interaction.followup.send(f"Failed to extract song: {e}")
            return

        url = data['webpage_url']
        title = data.get("title", "Unknown Title")
        artist = data.get("uploader", "Unknown Artist")
        thumbnail = data.get("thumbnail")

        cover_image_bytes = None
        if thumbnail:
            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail) as resp:
                    cover_image_bytes = await resp.read()

        song = {
            "url": url,
            "title": title,
            "artist": artist,
            "cover_image_bytes": cover_image_bytes
        }

        if interaction.guild.id not in self.queues:
            self.queues[interaction.guild.id] = deque()

        self.queues[interaction.guild.id].append(song)

    async def play_next(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        print(f"play_next called for guild {guild_id}. Queue length: {len(self.queues.get(guild_id, []))}")
        
        if guild_id not in self.queues or not self.queues[guild_id]:
            if self.looping.get(guild_id, False) and guild_id in self.now_playing:
                self.queues[guild_id] = deque([self.now_playing[guild_id]])
            else:
                print(f"No songs in queue for guild {guild_id}. Cleaning up.")
                self.now_playing.pop(guild_id, None)
                if guild_id in self.voice_clients and self.voice_clients[guild_id].is_connected():
                    await self.voice_clients[guild_id].disconnect()
                    self.voice_clients.pop(guild_id, None)
                    self.text_channels.pop(guild_id, None)
                    self.looping.pop(guild_id, None)
                return

        if guild_id not in self.voice_clients or not self.voice_clients[guild_id].is_connected():
            print(f"No active voice client for guild {guild_id}. Attempting to reconnect.")
            if interaction.user and interaction.user.voice:
                self.voice_clients[guild_id] = await interaction.user.voice.channel.connect()
            else:
                print(f"No user voice channel available for guild {guild_id}.")
                return

        song = self.queues[guild_id].popleft()
        url = song["url"]
        title = song["title"]
        print(f"Attempting to play: {title} (URL: {url})")

        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))
            print(f"Extracted data in play_next: {data}")
            audio_url = data.get("url")

            if not audio_url:
                print(f"No audio URL for {title} in guild {guild_id}.")
                text_channel = self.text_channels.get(guild_id, interaction.channel)
                await text_channel.send(f"⚠️ Failed to retrieve audio URL for **{title}**.")
                return await self.play_next(interaction)

            source = discord.FFmpegOpusAudio(
                audio_url,
                executable=self.ffmpeg_executable,
                **self.ffmpeg_options
            )

            self.now_playing[guild_id] = song

            def after_playing(err):
                if err:
                    print(f"Error after playing {title} in guild {guild_id}: {err}")
                try:
                    print(f"Scheduling play_next_with_channel for guild {guild_id}. Queue length: {len(self.queues.get(guild_id, []))}")
                    asyncio.run_coroutine_threadsafe(self.play_next_with_channel(guild_id), self.bot.loop)
                except Exception as e:
                    print(f"Error scheduling play_next_with_channel for guild {guild_id}: {e}")

            self.voice_clients[guild_id].play(source, after=after_playing)
            text_channel = self.text_channels.get(guild_id, interaction.channel)
            await text_channel.send(f'Now playing **"{title}"**.')
            self.last_played_time[guild_id] = time.time()
            print(f"Started playing {title} in guild {guild_id}.")

        except Exception as e:
            print(f"Error in play_next for {title} in guild {guild_id}: {e}")
            text_channel = self.text_channels.get(guild_id, interaction.channel)
            await text_channel.send(f"⚠️ Failed to play **{title}**: {e}")
            return await self.play_next(interaction)

    async def play_next_with_channel(self, guild_id: int):
        print(f"play_next_with_channel called for guild {guild_id}")
        text_channel = self.text_channels.get(guild_id)
        if not text_channel:
            guild = self.bot.get_guild(guild_id)
            if guild:
                text_channel = guild.text_channels[0]
            else:
                print(f"No guild found for guild_id {guild_id}")
                return

        class DummyInteraction:
            def __init__(self, guild_id, channel, bot):
                self.guild = bot.get_guild(guild_id)
                self.channel = channel
                self.guild_id = guild_id
                self.user = None

        dummy_interaction = DummyInteraction(guild_id, text_channel, self.bot)
        
        if guild_id in self.voice_clients and self.voice_clients[guild_id].is_connected():
            await self.play_next(dummy_interaction)
        else:
            print(f"Voice client not connected for guild {guild_id}. Attempting to reconnect.")
            guild = self.bot.get_guild(guild_id)
            if guild and guild.voice_channels:
                self.voice_clients[guild_id] = await guild.voice_channels[0].connect()
                await self.play_next(dummy_interaction)
            else:
                print(f"No voice channels available for guild {guild_id}. Stopping playback.")
                self.queues.pop(guild_id, None)
                self.now_playing.pop(guild_id, None)
                self.text_channels.pop(guild_id, None)
                self.looping.pop(guild_id, None)

    @commands.command(name="mc")
    async def mc(self, ctx):
        song_title = "Jungkook - Yes or No"
        cover_url = "https://upload.wikimedia.org/wikipedia/en/d/d9/Jungkook_-_Golden.png"

        queue = [
            {"title": "Lisa - Rockstar"},
            {"title": "Ariana Grande - Twilight Zone"},
            {"title": "Blackpink - Ready for love"},
            {"title": "BTS - ON"},
            {"title": "Sabrina Carpenter - Feather"},
            {"title": "Cyclical - The Greeting Commitee"},
            {"title": "Charli XCX - Guess ft. Billie Eilish"},
            {"title": "Billie Eilish - Ocean Eyes"},
            {"title": "Rosé - Messy"},
            {"title": "JENNIE - Like JENNIE"},
        ]

        async with aiohttp.ClientSession() as session:
            async with session.get(cover_url) as resp:
                if resp.status != 200:
                    return await ctx.send("Failed to fetch cover image.")
                cover_image_data = await resp.read()

        image_buffer = self.generate_music_card(
            song_title=song_title,
            cover_image=cover_image_data,
            queue=queue
        )
        view = MusicUI(bot=self.bot, music_cog=self)
        await ctx.send(file=File(fp=image_buffer, filename="music_card.png"), view=view)

    @commands.command(name="stop")
    async def stop(self, ctx):
        vc = ctx.guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
        self.queues[ctx.guild.id] = deque()
        self.now_playing[ctx.guild.id] = None
        self.text_channels.pop(ctx.guild.id, None)
        self.looping.pop(ctx.guild.id, None)
        await ctx.send("Stopped playback and cleared the queue.")

    @app_commands.command(name="skip", description="Skips the current song")
    async def skip(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        vc = self.voice_clients.get(guild_id)
        if vc and (vc.is_playing() or vc.is_paused()):
            if guild_id in self.queues and self.queues[guild_id]:
                vc.stop()
                await interaction.response.send_message("Skipped to the next song.")
            else:
                vc.stop()
                await interaction.response.send_message("Queue has ended.")
        else:
            await interaction.response.send_message("No song is playing.")

    @app_commands.command(name="queue", description="Displays the current music queue")
    async def queue(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id

        if guild_id not in self.now_playing or self.now_playing[guild_id] is None:
            return await interaction.response.send_message("Nothing is currently playing.")

        current_song = self.now_playing[guild_id]
        upcoming_queue = list(self.queues.get(guild_id, []))

        song_title = current_song['title']
        cover_image = current_song.get('cover_image_bytes')

        image_buffer = self.generate_music_card(
            song_title=song_title,
            cover_image=cover_image,
            queue=upcoming_queue
        )
        view = MusicUI(bot=self.bot, music_cog=self)
        await interaction.response.send_message(file=File(fp=image_buffer, filename="queue.png"), view=view)

    @app_commands.command(name="pause", description="Pauses the currently playing song")
    async def pause(self, interaction: discord.Interaction):
        vc = self.voice_clients.get(interaction.guild.id)
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("Paused the current song.")
        else:
            await interaction.response.send_message("Nothing is playing right now.")

    @app_commands.command(name="resume", description="Resumes the paused song")
    async def resume(self, interaction: discord.Interaction):
        vc = self.voice_clients.get(interaction.guild.id)
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("Resumed the song.")
        else:
            await interaction.response.send_message("There's nothing paused to resume.")

    @app_commands.command(name="leave")
    async def leave(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_connected():
            await vc.disconnect()
            self.queues.pop(interaction.guild.id, None)
            self.now_playing.pop(interaction.guild.id, None)
            self.text_channels.pop(interaction.guild.id, None)
            self.looping.pop(interaction.guild.id, None)
            await interaction.response.send_message("Disconnected from the voice channel.")
        else:
            await interaction.response.send_message("I'm not connected to a voice channel.")

    async def cog_unload(self):
        if hasattr(self.bot, 'session'):
            await self.bot.session.close()

async def setup(bot):
    await bot.add_cog(Music(bot))