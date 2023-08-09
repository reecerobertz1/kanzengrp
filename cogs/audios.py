import json
import random
import discord
from discord.ext import commands

class audios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _add_audio(self, ctx, filename, link):
        audio_data = link
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(audio_data)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        await ctx.reply("Audio added successfully.")

    @commands.group(invoke_without_command=True)
    async def add(self, ctx: commands.Context):
        """group of commands to manage apps"""
        embed = discord.Embed(title="Audio Commands", color=0x2B2D31)
        embed.add_field(name="add soft", value="Adds a soft audio", inline=False)
        embed.add_field(name="add hot", value="Adds a hot audio", inline=False)
        await ctx.reply(embed=embed)

    @add.command()
    async def soft(self, ctx, link):
        """Adds a streamable link to softaudios.json"""
        await self._add_audio(ctx, "./jsonfiles/softaudios.json", link)

    @add.command()
    async def hot(self, ctx, link):
        """Adds a streamable link to hotaudios.json"""
        await self._add_audio(ctx, "./jsonfiles/hotaudios.json", link)

    @commands.group(invoke_without_command=True)
    async def audio(self, ctx: commands.Context):
        """group of commands to manage apps"""
        embed = discord.Embed(title="Giveaway Commands", color=0x2B2D31)
        embed.add_field(name="audio soft", value="Sends a soft audio", inline=False)
        embed.add_field(name="audio hot", value="Sends a hot audio", inline=False)
        await ctx.reply(embed=embed)

    @audio.command()
    async def soft(self, ctx):
        """Sends a random link from softaudios.json"""
        with open("./jsonfiles/softaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a soft audio with `+addsoft`\n{choice}")

    @audio.command()
    async def hot(self, ctx):
        """Sends a random link from hotaudios.json"""
        with open("./jsonfiles/hotaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a hot audio with `+addhot`\n{choice}")

async def setup(bot):
    await bot.add_cog(audios(bot))