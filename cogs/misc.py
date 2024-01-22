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

    @commands.hybrid_command(name="buildembed", aliases=['be', 'embed'], description="Build an embed")
    @commands.has_permissions(manage_guild=True)
    async def buildembed(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None):
        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()
        async def ask_question(question):
            message = await ctx.send(question)
            response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            await message.delete()
            await response.delete()
            return response.content

        title = await ask_question("What title do you want your embed to have?")
        description = await ask_question("Okay! What do you want your description to be?")
        color_input = await ask_question("What color do you want your embed to be? (in hex; e.g., 2B2D31)")
        if color_input.lower() == 'x':
            color = 0x60e5fc
        else:
            try:
                color = int(color_input, 16)
            except ValueError:
                await ctx.send("Invalid color code. Using default color.")
                color = 0x60e5fc

        embed = discord.Embed(title=title, description=description, colour=color)
        thumbnail_url = await ask_question("Enter the thumbnail URL (Type `X` to skip)")
        if thumbnail_url.lower() != 'x':
            embed.set_thumbnail(url=thumbnail_url)

        image_url = await ask_question("Enter the image URL (Type `X` to skip)")
        if image_url.lower() != 'x':
            embed.set_image(url=image_url)

        footer_input = await ask_question("What should the footer be? (Type `X` to skip)")
        if footer_input.lower() != 'x':
            embed.set_footer(text=footer_input)

        fields_completed = False
        while not fields_completed:
            field_name = await ask_question("What do you want the name of the field to be? (Type `X` to finish adding fields)")
            if field_name.lower() == 'x':
                fields_completed = True
            else:
                field_value = await ask_question("What do you want the value of the field to be?")
                inline_input = await ask_question("Do you want this field to be inline? (yes/no)")
                if inline_input.lower() == 'yes':
                    inline = True
                else:
                    inline = False
                embed.add_field(name=field_name, value=field_value, inline=inline)

        message = await channel.send(embed=embed)

    @commands.hybrid_command(name="abouthoshi",aliases=["hoshiinfo", "about"], description="Information about Hoshi")
    async def abouthoshi(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        days, hours = divmod(hours, 24)
        minutes, seconds = divmod(remainder, 60)
        embed = discord.Embed(title="About Hoshi", description=f"Hoshi is a multi-purpose bot made for [kanzengrp](https://instagram.com/kanzengrp)\nFor help with commands, do `+help`\n", color=0x2b2d31)
        embed.add_field(name="** **", value=f"** Hoshi was made on:** {discord.utils.format_dt(self.bot.user.created_at, 'D')}", inline=False)
        embed.add_field(name="** **", value=f"**Last reboot:** {discord.utils.format_dt(self.bot.launch_time, 'D')}", inline=False)
        embed.add_field(name="** **", value=f"**Uptime:** {days} days, {hours} hours, {minutes} minutes, {seconds} seconds", inline=False)
        embed.add_field(name="** **", value=f"**Total users:** {sum(g.member_count for g in self.bot.guilds)}", inline=False)
        embed.add_field(name="** **", value=f"**Total Servers:** {len(ctx.bot.guilds)}")
        embed.add_field(name="** **", value=f"**Python version:** {platform.python_version()}", inline=False)
        embed.add_field(name='** **', value=f"**Discord.py version:** {discord.__version__}", inline=False)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Made by {self.bot.application.owner.name}")
        message = await ctx.send(embed=embed)
        await asyncio.sleep(1)
        latency = round(self.bot.latency * 1000, 2)
        embed.set_field_at(5, name="** **", value=f"**Latency:** {latency}ms", inline=False)
        await message.edit(embed=embed)

    @commands.command(description="Get the member count for a server")
    async def membercount(self, ctx):
        total_members = len(ctx.guild.members)
        bot_count = sum(1 for member in ctx.guild.members if member.bot)
        human_count = total_members - bot_count
        embed = discord.Embed(title=f"Total members in {ctx.guild.name}", color=0x2b2d31)
        embed.add_field(name="Total Members", value=total_members, inline=False)
        embed.add_field(name="Humans", value=human_count, inline=False)
        embed.add_field(name="Bots", value=bot_count, inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="afk", extras="+afk (reason)", description="set an afk status")
    async def afk(self, ctx, *, reason: str):
        await self.set_afk(ctx.author.id, reason)
        await ctx.reply(f"Okay! I have set your AFK status as\n**{reason}**")

async def setup(bot):
    await bot.add_cog(misc(bot))