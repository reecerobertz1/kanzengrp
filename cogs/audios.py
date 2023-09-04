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

    @commands.command()
    async def addsoft(self, ctx, link):
        button = discord.ui.Button(label="Click to hear audio", url=f"{link}")

        view = discord.ui.View()
        view.add_item(button)
        log = self.bot.get_channel(1122627075682078720)
        embed = discord.Embed(title="Added soft audio", description=f"`{ctx.author.display_name}` has added a soft audio!", color=0x2b2d31)
        embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
        await self._add_audio(ctx, "softaudios.json", link)
        await log.send(embed=embed, view=view)


    @commands.command()
    async def addhot(self, ctx, link):
        button = discord.ui.Button(label="Click to hear audio", url=f"{link}")

        view = discord.ui.View()
        view.add_item(button)
        log = self.bot.get_channel(1122627075682078720)
        embed = discord.Embed(title="Added hot audio", description=f"`{ctx.author.display_name}` has added a hot audio!", color=0x2b2d31)
        embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
        await self._add_audio(ctx, "hotaudios.json", link)
        await log.send(embed=embed, view=view)

    @commands.group(invoke_without_command=True)
    async def audio(self, ctx: commands.Context):
        embed = discord.Embed(title="Audio Commands", color=0x2B2D31)
        embed.add_field(name="audio soft", value="Sends a soft audio", inline=False)
        embed.add_field(name="audio hot", value="Sends a hot audio", inline=False)
        await ctx.reply(embed=embed)

    @audio.command()
    async def soft(self, ctx):
        with open("softaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a soft audio with `+addsoft`\n[here is the audio]({choice})")

    @audio.command()
    async def hot(self, ctx):
        with open("hotaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a hot audio with `+addhot`\n[here is the audio]({choice})")

async def setup(bot):
    await bot.add_cog(audios(bot))