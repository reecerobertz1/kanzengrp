import asyncio
import random
import discord
from discord.ext import commands
from typing import TypedDict
import datetime
import humanize
from discord import ui

class AFK(TypedDict):
    user_id: int
    reason: str
    time: datetime.datetime

class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.emoji = "<:tata:1121909389280944169>"

    async def check_afk(self, userid: int) -> AFK:
        query = "SELECT reason, time, user_id FROM afk WHERE user_id = $1"
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                async with connection.cursor() as cursor:
                    await cursor.execute(query, userid)
                    result = await cursor.fetchall()
        return result[0] if result else None

    async def remove_afk(self, userid: int) -> None:
        query = "DELETE FROM afk WHERE user_id = $1"
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                async with connection.cursor() as cursor:
                    await cursor.execute(query, userid)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.lower() == "chroma":
            await message.channel.send(f"<:ilovechroma:1280229204826263704> **{message.author.name}** loves chroma\n-# <:reply:1290714885792989238> we love you too! **<3**")
        if message.content.lower() == "reece":
            await message.channel.send("<@609515684740988959> is the sexiest")
        if message.content.lower() == "rinaya":
            await message.channel.send("#1 ranwan lover")
        if message.content.lower() == "cc":
            await message.channel.send("cece is the most sane diluc stan... *not*")
        if message.content.lower() == "aspenola":
            await message.channel.send("aspen is streaming lower one's eyes")
        if message.content.lower() == "kim":
            await message.channel.send("mizukis lover")
        if message.content.lower() == "denise":
            await message.channel.send("https://tenor.com/qIoidKLXAGv.gif")
        if message.content.lower() == "lyra":
            await message.channel.send("<:ilyrayou:1270405427989057576>")
        if message.content.lower() == "hoshi! come here, your dad wants you":
            await message.channel.send("Hi!! i'm here")
        if message.content.lower() == "good boy":
            await message.channel.send("Thank you dad!!")
        if message.type == discord.MessageType.premium_guild_subscription:
            embed = discord.Embed(
                title="Thank you for boosting",
                description=(
                    "\nthank you for boosting ✧.*lyra!"
                    "\nyou can claim your perks over at <#1139466056361062410>!"
                    "please be sure to give credits when due!"
                ),
                color=0xFEBCBE
            )
            embed.set_footer(
                text=f"We now have {message.guild.premium_subscription_count} boosts!",
                icon_url=message.guild.icon.url if message.guild.icon else None
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)
            
            chromaembed = discord.Embed(
                title="Thank you for boosting",
                description=(
                    f"Thank you {message.author.name} for boosting!\n"
                    "・Your support is greatly appreciated\n"
                    "・Head to <#865516313065947136> to claim our perks"
                ),
                color=0x2b2d31
            )
            chromaembed.set_footer(
                text=f"We now have {message.guild.premium_subscription_count} boosts!",
                icon_url=message.guild.icon.url if message.guild.icon else None
            )
            chromaembed.set_thumbnail(url=message.author.display_avatar.url)

            chroma2embed = discord.Embed(
                title="Thank you for boosting",
                description=(
                    f"Thank you {message.author.name} for boosting!\n"
                    "・Your support is greatly appreciated\n"
                    "・Head to <#853241710658584586> to claim our perks"
                ),
                color=0x2b2d31
            )
            chroma2embed.set_footer(
                text=f"We now have {message.guild.premium_subscription_count} boosts!",
                icon_url=message.guild.icon.url if message.guild.icon else None
            )
            chroma2embed.set_thumbnail(url=message.author.display_avatar.url)

            if message.guild.id == 1134736053803159592:
                await message.channel.send(f"{message.author.mention}", embed=embed)
            elif message.guild.id == 835495688832811039:
                await message.channel.send(f"{message.author.mention}", embed=chromaembed)
            elif message.guild.id == 694010548605550675:
                await message.channel.send(f"{message.author.mention}", embed=chroma2embed)
            else:
                pass
        afk = await self.check_afk(message.author.id)
        if afk is not None:
            await self.remove_afk(message.author.id)
            await message.reply(f"Hey, <@!{afk['user_id']}> welcome back! You were AFK for **{afk['reason']}**")
        if len(message.mentions) > 0:
            for mention in message.mentions:
                afk_mention = await self.check_afk(mention.id)
                if afk_mention is not None:
                    await message.reply(f"**{mention.name}** went AFK **{afk_mention['reason']}**")

async def setup(bot):
    await bot.add_cog(other(bot))