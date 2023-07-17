"""import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Embed
from pytube import YouTube
from pytube import Search
import asyncio
import random

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.nowPlaying = ""
        self.sentM = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content == 'bot help':
            await message.channel.send("Commands:\nbot play - This command can play any song on YouTube. You can also add the URL or search term to the end of the command for easier access.\nbot join - Makes the bot join the VC you are in.\nbot leave - Makes the bot leave the VC you are in.\nbot stop - Stops any music playing from the bot.")
        elif message.content == 'bot join':
            # Your implementation for the bot join command
            if message.author.voice is None:
                await message.channel.send("You are not in a voice channel.")
                return

            voice_channel = message.author.voice.channel
            vc = message.guild.voice_client

            if vc is not None:
                if vc.channel == voice_channel:
                    await message.channel.send("I am already connected to your voice channel.")
                else:
                    try:
                        await message.add_reaction('✅')
                    except:
                        pass
                    await vc.move_to(voice_channel)
            else:
                try:
                    await message.add_reaction('✅')
                except:
                    pass
                vc = await voice_channel.connect()
                self.loop.create_task(self.check_for_idle(vc, 120))
        elif message.content == 'bot leave':
            # Your implementation for the bot leave command
            vc = message.guild.voice_client

            if vc is None:
                await message.channel.send("I am not currently in a voice channel.")
                return

            vc.stop()

            try:
                await message.add_reaction('👋')
            except:
                pass
            await vc.disconnect()
            return
        elif message.content.startswith('bot play') or message.content.startswith('bot p'):
            # Your implementation for the bot play command
            if message.author.voice is None:
                await message.channel.send("You are not in a voice channel.")
                return

            words = message.content.split()
            vc = message.guild.voice_client

            if len(words) > 2:
                try:
                    await message.add_reaction('⏳')
                except:
                    pass
                url = await self.url_or_search(words, 2, message)
            else:
                url = None

            if url is None:
                vc = message.guild.voice_client
                url = await self.ask_url(message)
                if url is None:
                    return

            if not (url.startswith('https://www.youtube.com/') or url.startswith('https://youtu.be/') or url.startswith('youtu.be/') or url.startswith('youtube.com/') or url.startswith('https://youtube.com/')):
                await message.channel.send("Please provide a valid YouTube URL.")
                print("DIS URL NO WORK: " + url)
                return

            if not (vc is None) and vc.is_playing():
                self.queue.append(url)
                url = str(self.queue[len(self.queue) - 1])
                try:
                    await message.add_reaction('➕')
                except:
                    pass
                yt = YouTube(url)
                id = yt.video_id
                video_title = yt.title
                embed = Embed(title=yt.author, color=discord.Color.from_rgb(255, 0, 0))
                embed.description = f"[{video_title}]({url})"
                embed.set_image(url="https://img.youtube.com/vi/" + id + "/mqdefault.jpg")
                embed.set_footer(text=f"📃 Queue Position: {len(self.queue)}")
                await message.channel.send(embed=embed)
                try:
                    await message.remove_reaction('⏳', self.bot.user)
                except:
                    pass
                try:
                    await message.remove_reaction('🔎', self.bot.user)
                except:
                    pass
                try:
                    await message.remove_reaction('⏳', self.bot.user)
                except:
                    pass
                try:
                    await message.remove_reaction('🔎', self.bot.user)
                except:
                    pass
                await message.channel.send(f"Added to the queue. (Couldn't get the title at this moment)")
                return

            voice_channel = message.author.voice.channel
            vc = message.guild.voice_client

            if vc is None:
                vc = await voice_channel.connect()

            self.loop.create_task(self.check_for_idle(vc, 120))

            await self.play_audio(message, vc, url)
        elif message.content == 'bot stop':
            # Your implementation for the bot stop command
            vc = message.guild.voice_client
            if vc is None or not vc.is_playing():
                await message.channel.send("Not Playing anything.")
                return
            else:
                self.queue = []
                vc.stop()
                try:
                    await message.add_reaction('🛑')
                except:
                    pass
                return
        elif message.content == 'bot skip':
            # Your implementation for the bot skip command
            vc = message.guild.voice_client
            if vc is None or not vc.is_playing():
                await message.channel.send("Not Playing anything.")
                return
            else:
                await self.skip(message, vc)
                try:
                    await message.add_reaction('⏭️')
                except:
                    pass
                return
        elif message.content == 'bot queue':
            # Your implementation for the bot queue command
            i = 0
            text = "Now Playing:\n"
            yt = YouTube(self.nowPlaying)
            while i < 10:
                try:
                    text = text + yt.title + "\n\nQueue:\n"
                    break
                except:
                    i += 1
            i = 0
            while i < len(self.queue):
                x = 0
                text = text + f"{i+1}: "
                while x < 10:
                    url = self.queue[i]
                    yt = YouTube(url)
                    try:
                        text = text + yt.title + "\n"
                        break
                    except:
                        x += 1
                i += 1
            await message.channel.send(text)
            return
        else:
            # Other message processing if needed
            pass

    # Rest of the methods like ask_url, play_audio, url_or_search, check_if_under_30_min, after_play, check_for_idle, next_q, and skip
    # ... (Copy and paste them here)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user and after.channel is None:
            await before.channel.guild.change_voice_state(channel=None)
        if member.id == self.bot.user.id and before.deaf and not after.deaf:
            await member.edit(deafen=True)

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Music(bot))"""