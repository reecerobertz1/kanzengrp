import discord
from discord.ext import commands
import requests
import random
from typing import List, TypedDict, Optional
import asyncio
from requests.exceptions import Timeout
from datetime import datetime, timedelta, timezone

class LevelRow(TypedDict):
    member_id: int
    xp: int
    messages: int
    color: str
    image: str

class countryvia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_flag(self):
        response = requests.get("https://restcountries.com/v3.1/all")
        if response.status_code == 200:
            countries = response.json()
            country_info = random.choice(countries)
            flag_data = country_info.get('flags', {})
            flag_url = next(iter(flag_data.values()), None)
            country_name = country_info.get('name', {}).get('common', None)
            if flag_url and country_name:
                return flag_url, country_name
            else:
                return await self.fetch_flag()
        else:
            return None, None

    @commands.command(name="countryvia")
    async def countryvia(self, ctx, count: int = 1, mode: str = "singleplayer"):
        if mode.lower() == "multiplayer":
            players = ctx.guild.members
        else:
            players = [ctx.author]

        correct_guesses = 0
        for i in range(1, count + 1):
            flag_url, country_name = await self.fetch_flag()

            if flag_url:
                if flag_url == "https://flagcdn.com/w320/il.png":
                    flag_url = None
                    description = "This here was meant to be Israel's flag... but just a reminder\nto donate to Palestine and help as much as you can!\nIf you're unable to donate, share this link with others!!"
                    view = discord.ui.View()
                    psdonate = discord.ui.Button(label="Donate here", url="https://oc-palestine.carrd.co/", emoji="🇵🇸")
                    view.add_item(psdonate)
                else:
                    timeout_time = datetime.now(timezone.utc) + timedelta(seconds=30)
                    timeout_str = f"<t:{int(timeout_time.timestamp())}:R>"
                    view = None
                    flag_url = flag_url
                    description = f"Guess the country's flag!\nFlag Timeout: {timeout_str}"

                embed = discord.Embed(description=description, color=0x2b2d31)
                embed.set_image(url=flag_url)
                embed.set_footer(text=f"Flag: {i}/{count}", icon_url=ctx.author.avatar)
                
                await ctx.reply(embed=embed, view=view)
                
                try:
                    guess = await self.bot.wait_for(
                        "message",
                        timeout=30,
                        check=lambda m: m.author in players and m.channel == ctx.channel,
                    )
                except asyncio.TimeoutError:
                    await ctx.reply("Time's up! The correct answer was: " + country_name)
                else:
                    if guess.content.lower() == country_name.lower():
                        correct_guesses += 1
                        await ctx.reply("Correct!")
                    else:
                        await ctx.reply("Incorrect! The correct answer was: " + country_name)
            else:
                await ctx.reply("Failed to fetch flag.")
        embed = discord.Embed(title="Game Over", description=f"You got **{correct_guesses}/{count}** correct", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.author.avatar)
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(countryvia(bot))