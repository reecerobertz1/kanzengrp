import discord
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='play_song', help='To play a song')
    async def play(self, ctx, url):
        server = ctx.guild
        voice_client = server.voice_client
        async with ctx.typing():
            voice_client.play(discord.FFmpegPCMAudio(url))
        await ctx.send('Now playing: {}'.format(url))

    @commands.command()
    async def join(self, ctx):
        channel_id = 1055799905978957854  # Replace with your desired voice channel ID
        channel = self.bot.get_channel(channel_id)

        if channel and channel.type == discord.ChannelType.voice:
            voice_state = ctx.author.voice
            bot_voice_state = ctx.guild.me.voice

            if voice_state and voice_state.channel:
                if voice_state.channel.id != channel.id:
                    await ctx.send("You must be in the same voice channel as me to use this command.")
                    return

                if bot_voice_state and bot_voice_state.channel:
                    if bot_voice_state.channel.id == channel.id:
                        await ctx.send("I am already in the specified voice channel.")
                        return

                    await bot_voice_state.move_to(channel)
                else:
                    await channel.connect()
                await ctx.send(f"Joined the voice channel: {channel.name}")
            else:
                await ctx.send("You must be in a voice channel to use this command.")
        else:
            await ctx.send("The specified voice channel does not exist or is not a voice channel.")



    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Music(bot))