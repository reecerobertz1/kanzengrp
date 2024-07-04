import asyncio
import datetime
import io
import json
import math
import os
import random
import textwrap
from typing import Optional
import typing
import aiohttp
import discord
from discord.ext import commands
from discord import ui, app_commands
import requests
from typing import Optional, Tuple
from PIL import ImageDraw, Image
from io import BytesIO
from easy_pil import Font
from triviastuff.getQuestions import getQuestions
from triviastuff.checkHandler import buttonHandler

class Fun(commands.Cog):
    """Hoshi's fun commands"""
    def __init__(self, bot):
        self.bot = bot
        self.gif_cache = {}
        self.server1_log_channel_id = 1122627075682078720
        self.server2_log_channel_id = 1122994947444973709
        self.server3_log_channel_id = 1134857444250632343
        self.editorsblock_log_channel_id = 1134857444250632343
        self.emoji="<:chimmy2:1148234652448981072>"

    def get_random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r, g, b

    @commands.hybrid_command(name="say", description="Make Hoshi say something", extras="+say hello")
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.send(message)
            embed = discord.Embed(title="Say command log", description=f"{ctx.author.name} has used the say command\nthey said: `{message}`", color=0x2b2d31)
            embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.avatar)
            log_channel_id = self.get_log_channel_id(ctx.guild.id)
            if log_channel_id is not None:
                log_channel = self.bot.get_channel(log_channel_id)
                if log_channel:
                    await log_channel.send(embed=embed)

    def get_log_channel_id(self, guild_id):
        if guild_id == 1131003330810871979:
            return self.server1_log_channel_id

    @app_commands.command(name="jail", description="Lock someone up in jail")
    async def jail(self, interaction: discord.Interaction, member: Optional[discord.Member]):
        member = member or interaction.user
        avatar_url = member.avatar.url
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar_url)) as response:
                avatar_image = await response.read()

        jail_image = Image.open("./assets/jail_door.png").convert("RGBA")
        avatar_pil = Image.open(io.BytesIO(avatar_image)).convert("RGBA")
        avatar_pil = avatar_pil.resize((550, 550))
        jail_image = jail_image.resize(avatar_pil.size)
        final_image = Image.alpha_composite(avatar_pil, jail_image)
        final_image.save("jail_avatar.png")
        await interaction.response.send_message(file=discord.File("jail_avatar.png"))
        os.remove("jail_avatar.png")

    @app_commands.command(name="ship", description="Ship 2 people together")
    async def ship(self, interaction: discord.Interaction, member1: discord.Member, member2: discord.Member):
        await interaction.response.send_message("<a:loading:1207312514149523476> Calculating your results...")
        time = random.randint(0, 2)
        await asyncio.sleep(time)
        compatibility = random.randint(0, 100)

        if compatibility < 20:
            status = "Incompatible Duo"
            color = 0xF32020
        elif compatibility < 40:
            status = "Awkward Pair"
            color = 0xF37A20
        elif compatibility < 60:
            status = "Potential Couple"
            color = 0xFFFB00
        elif compatibility < 80:
            status = "Perfect Match"
            color = 0x55F320
        else:
            status = "Soulmates"
            color = 0xEDABEF
        embed = discord.Embed(title=f"{member1.name} `💌` {member2.name}", description=f"`💖` | Compatibility: **{compatibility}%**\n`💑` | Status: **{status}**", color=color)
        await interaction.edit_original_response(content=f"shipped {member1.mention} and {member2.mention}", embed=embed)

    @app_commands.command(name="ppsize", description="See who has the biggest pp")
    async def ppsize(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        pp_size = '=' * random.randint(1, 100)
        message = f'{member.mention} Your pp size is: 8{pp_size}D'
        await interaction.response.send_message(message)

    @app_commands.command(name='8ball',description="Ask 8ball a question", extras="+8ball will i have a good day?")
    async def eight_ball(self, interaction: discord.Interaction, question:str):
        responses = ["It is certain.","It is decidedly so.","Without a doubt.","Yes - definitely.","You may rely on it.","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes.","Reply hazy, try again.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again.","Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.","Very doubtful."]
        response = random.choice(responses)
        embed = discord.Embed(description=f"question: {question}\nanswer: {response}", color=0x2b2d31)
        embed.set_author(name="8ball", icon_url="https://cdn.discordapp.com/attachments/1121841074512605186/1151109254959333426/png-clipart-magic-8-ball-eight-ball-crazy-eights-ball-game-logo.png")
        embed.set_footer(text=f"8ball for {interaction.user.name}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="slap", description="Slap a member cause they deserve it")
    async def slap(self, interaction: discord.Interaction, member: discord.Member):
        descriptions = [f'{interaction.user.mention} gave {member.mention} a slap', f'wow {interaction.user.mention} hope you are happy... {member.mention} is crying cause you slapped them', f'LOL {member.mention} you got slapped so good by {interaction.user.mention}']
        description = random.choice(descriptions)
        slaps = ['https://media1.tenor.com/m/xdF1G7Hrxa0AAAAC/slap-christmas.gif', 'https://media1.tenor.com/m/MXZGFeabIIwAAAAC/taiga-toradora.gif', 'https://media1.tenor.com/m/DqE9eSc0Xs8AAAAC/systempack-stewie.gif', 'https://media1.tenor.com/m/Ws6Dm1ZW_vMAAAAC/girl-slap.gif', 'https://media1.tenor.com/m/eU5H6GbVjrcAAAAC/slap-jjk.gif', 'https://media1.tenor.com/m/taxXCAMGXn0AAAAd/genshin-slap.gif', 'https://media1.tenor.com/m/3XwLxStQGXEAAAAC/ddwoo-kpop.gif', 'https://media1.tenor.com/m/vkeCOepvLBIAAAAC/jungkook-slap.gif']
        slap = random.choice(slaps)
        embed = discord.Embed(description=description, color=0x2b2d31)
        embed.set_image(url=slap)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kiss", description="kiss a member")
    async def kiss(self, interaction: discord.Interaction, member: discord.Member):
        descriptions = [f'{interaction.user.mention} gave {member.mention} a kiss', f'so cute {interaction.user.mention} and {member.mention} kissed 🥰', f'ew get a room you two... gross {member.mention} {interaction.user.mention}']
        description = random.choice(descriptions)
        kisses = ['https://media1.tenor.com/m/MkwSXI4PX8EAAAAd/loona-haseul.gif', 'https://media1.tenor.com/m/b7DWF8ecBkIAAAAC/kiss-anime-anime.gif', 'https://media1.tenor.com/m/7P7x7JObd98AAAAC/hori-kyouko-miyamura-izumi.gif', 'https://media1.tenor.com/m/06lz817csVgAAAAd/anime-anime-kiss.gif', 'https://media1.tenor.com/m/Fj_CLLeUrB4AAAAC/seungminkiss-blow-kiss.gif', 'https://media1.tenor.com/m/FDrTOGwUXx0AAAAC/jin-kiss.gif', 'https://media1.tenor.com/m/M7ZtP6rTmAkAAAAd/lovelyz-mijoo.gif', 'https://media1.tenor.com/m/X7qKTiHPkWAAAAAC/txt-tomorrow-x-together.gif']
        kiss = random.choice(kisses)
        embed = discord.Embed(description=description, color=0x2b2d31)
        embed.set_image(url=kiss)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hug", description="Hug a member")
    async def hug(self, interaction: discord.Interaction, member: discord.Member):
        descriptions = [f'{interaction.user.mention} hugged {member.mention}', f'omg how sweet {interaction.user.mention} hugged {member.mention}', f'SOOO CUUUTEEE {member.mention} got a hug from {interaction.user.mention}']
        description = random.choice(descriptions)
        slaps = ['https://media1.tenor.com/m/YNmsataG5WoAAAAd/nishimura-riki-yang-jungwon.gif', 'https://media1.tenor.com/m/KRjC3Ab4KTQAAAAC/stray-kids.gif', 'https://media1.tenor.com/m/IrT616B3ChgAAAAC/bangchan-han.gif', 'https://media1.tenor.com/m/i3EHA2MwEXsAAAAC/rocket-punch-rcpc.gif', 'https://media1.tenor.com/m/L3IZbZiEnpUAAAAd/hanni-danielle.gif', 'https://media1.tenor.com/m/mB_y2KUsyuoAAAAd/cuddle-anime-hug.gif', 'https://media1.tenor.com/m/C0WXbXrrhxgAAAAC/hugs.gif', 'https://media1.tenor.com/m/ImuSrg7mXekAAAAC/genshin-impact-genshin.gif']
        slap = random.choice(slaps)
        embed = discord.Embed(description=description, color=0x2b2d31)
        embed.set_image(url=slap)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='howgay',description="How gay really are you?")
    async def howgay(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        percentage = random.randint(0, 101)
        await interaction.response.send_message(f"{member.mention} is **{percentage}%** gay. 🏳️‍🌈")

async def setup(bot):
    await bot.add_cog(Fun(bot))