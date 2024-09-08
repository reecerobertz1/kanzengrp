import asyncio
import io
import platform
from typing import Optional
import discord
from discord.ext import commands
from datetime import datetime
import asqlite
from easy_pil import Font
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
import textwrap
from discord import app_commands

class misc(commands.Cog):
    """Miscellaneous Commands"""
    def __init__(self, bot):
        self.bot = bot
        self.emoji="<:mang:1121909428866793582>"

    async def set_afk(self, userid: int, reason: str) -> None:
        query = "INSERT INTO afk (user_id, reason, time) VALUES ($1, $2, $3) ON CONFLICT (user_id) DO UPDATE SET reason = $2, time = $3"
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, userid, reason, discord.utils.utcnow())
        await self.bot.pool.release(connection)

    @app_commands.command(name="about", description="Information about hoshi")
    async def about(self, interaction: discord.Interaction):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        days, hours = divmod(hours, 24)
        minutes, seconds = divmod(remainder, 60)
        embed = discord.Embed(title="ABOUT HOSHI",description=f"Hoshi is a multi-purpose bot made for [kanzengrp](https://instagram.com/kanzengrp)\nFor help with commands, do </help:1206682941372104804>\n\n🎂 | **Created** {discord.utils.format_dt(self.bot.user.created_at, 'D')}\n\n<:ut:1206976312187686964> | **Last reboot** {discord.utils.format_dt(self.bot.launch_time, 'D')}\n\n<:ut:1206977202714058813> | **Uptime** | {days} days, {hours} hours, {minutes} minutes, {seconds} seconds\n\n👥 | **Total users** {sum(g.member_count for g in self.bot.guilds)}\n\n<:dpy:1206976478839963690> | **Discord.py version** {discord.__version__}\n\n<:py:1206976405053640724> | **Python version** {platform.python_version()}\n\n🔃 | **Latency** | {round(self.bot.latency * 1000, 2)}" ,color=0x2b2d31)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Made by reeceroberts", icon_url=self.bot.application.owner.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Information about the server")
    async def serverinfo(self, interaction: discord.Interaction):
        embed = discord.Embed(title="SERVER INFO", description=f"Name: **{interaction.guild.name}**\n<:1166196254141861979:1188190233267818566>ID: **1121841073673736215**\n<:1166196254141861979:1188190233267818566>Owned by: **<@{interaction.guild.owner_id}>**\n<:1166196258499727480:1188190249768210582>Date created: <t:1687518840:D> \n<:CF10:1207282336413130752>**{len(interaction.guild.channels)}** channels\n<:CF10:1207282336413130752>**{len(interaction.guild.roles)}** roles\n<:CF10:1207282336413130752>**{interaction.guild._member_count}** members\n<:CF10:1207282336413130752>**{interaction.guild.premium_subscription_count}** boosts\n<:Empty:1188186122350759996><:1166196254141861979:1188190233267818566>Booster tier: **{interaction.guild.premium_tier}**\n<:Empty:1188186122350759996><:1166196258499727480:1188190249768210582>Booster role: <@&{interaction.guild.premium_subscriber_role.id}>", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_image(url=interaction.guild.banner)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="report", description="Found a bug? report it to the Hoshi devs")
    async def report(self, interaction: discord.Interaction, command_name: str, problem: str):
        embed=discord.Embed(title="Bug Report", description=f"**Command:** {command_name}\n**Bug:** {problem}", color=0x2b2d31)
        embed.set_footer(text=f"Bug found by {interaction.user.name} | {interaction.user.id}", icon_url=interaction.user.avatar)
        channel =  interaction.client.get_channel(1198665603897118720)
        await channel.send("<@609515684740988959>",embed=embed)
        await interaction.response.send_message("Your bug report has been sent!")

    @app_commands.command(name="request", description="Got an idea for Hoshi? Send it to the Hoshi devs")
    async def request(self, interaction: discord.Interaction, idea: str):
        embed=discord.Embed(title="Request", description=idea, color=0x2b2d31)
        embed.set_footer(text=f"Requested by {interaction.user.name} | {interaction.user.id}", icon_url=interaction.user.avatar)
        channel =  interaction.client.get_channel(1198665603897118720)
        await channel.send("<@609515684740988959>",embed=embed)
        await interaction.response.send_message("Your request has been sent!")

    @commands.hybrid_command(name="afk", extras="+afk (reason)", description="set an afk status")
    async def afk(self, ctx, *, reason: str):
        await self.set_afk(ctx.author.id, reason)
        await ctx.reply(f"Okay! I have set your AFK status as\n**{reason}**")

async def setup(bot):
    await bot.add_cog(misc(bot))