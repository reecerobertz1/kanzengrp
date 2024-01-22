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
        if guild_id == 1121841073673736215:
            return self.server1_log_channel_id
        elif guild_id == 957987670787764224:
            return self.server2_log_channel_id
        elif guild_id == 1131003330810871979:
            return self.server3_log_channel_id
        elif guild_id == 1131003330810871979:
            return self.editorsblock_log_channel_id
        else:
            return None

    @commands.hybrid_command(name="jail", aliases=['prison', 'lockup'],description="Lock someone up in jail", extras="+jail (optional @member) : aliases +prison, +lockup")
    async def jail(self, ctx, member: Optional[discord.Member]):
        async with ctx.typing():
            member = member or ctx.author
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
            await ctx.send(file=discord.File("jail_avatar.png"))
            os.remove("jail_avatar.png")

    @commands.hybrid_command(name="pride", aliases=['gay'],description="Edits your avatar with the pride flag", extras="+pride (optional @member) : alias +gay")
    async def pride(self, ctx, member: Optional[discord.Member]):
        member = member or ctx.author
        avatar_url = member.avatar.url
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar_url)) as response:
                avatar_image = await response.read()

        jail_image = Image.open("./assets/pride.png").convert("RGBA")
        avatar_pil = Image.open(io.BytesIO(avatar_image)).convert("RGBA")
        avatar_pil = avatar_pil.resize((180, 180))
        jail_image = jail_image.resize(avatar_pil.size)
        final_image = Image.alpha_composite(avatar_pil, jail_image)
        final_image.save("pride.png")
        await ctx.send(file=discord.File("pride.png"))
        os.remove("pride.png")

    def kanzen_only():
        def predicate(ctx: commands.Context):
            if ctx.guild.id == 1121841073673736215:
                return True
            else:
                return False
        return commands.check(predicate)

    @commands.hybrid_command(name="ppsize", aliases=['pp'],description="See who has the biggest pp", extras="+ppsize (optional @member) : alias +pp")
    async def ppsize(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        pp_size = '=' * random.randint(1, 10)
        message = f'{member.mention} Your pp size is: 8{pp_size}D'
        await ctx.send(message)

    @commands.hybrid_command(name="hug", description="Hug someone", extras="+hug (optional @member)")
    async def hug(self, ctx, member: typing.Optional[discord.Member]):
        if member is None:
            await ctx.send(f"Hoshi gave {ctx.author.mention} a hug <a:mm_hug_tight:1122621840305684632>")
        else:
            embed = discord.Embed(description=f"{ctx.author.mention} gave {member.mention} a hug!", color=0x2b2d31)
            urls = ['https://cdn.discordapp.com/attachments/804482120671821865/814085524548878346/download_1.gif', "https://cdn.discordapp.com/attachments/804482120671821865/814083420194996224/download.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814086607997108254/tenor.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814087205039243274/tenor_1.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814087528906620968/tenor_2.gif"]
            embed.set_image(url=(random.choice(urls)))
            await ctx.reply(embed=embed)

    @commands.hybrid_command(name="kiss", description="Kiss someone", extras="+kiss (optional @member)")
    async def kiss(self, ctx, member: typing.Optional[discord.Member]):
        author = ctx.message.author.mention
        if member is None:
            await ctx.reply(f"Hoshi kissed {author}! <a:pkiss:1122621758978138283>")
        else:
            embed = discord.Embed(description=f"{author} kissed {member.mention}", color=0x2b2d31)
            hugs = ['https://cdn.discordapp.com/attachments/804482120671821865/814095974611681280/37f9f27715e7dec6f2f4b7d63ad1af13.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814096796582019082/39fe167bdab90223bcc890bcb067b761.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814097411525836851/5f5afb51884af7c58e8d46c90261f990.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814097832494759936/tenor_1.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814098373228625970/tenor_2.gif']
            embed.set_image(url=(random.choice(hugs)))
            await ctx.reply(embed=embed)

    @commands.hybrid_command(name="slap", description="Slap a bitch", extras="+slap (optional @member)")
    async def slap(self, ctx, member: typing.Optional[discord.Member]):
        author = ctx.message.author.mention
        if member is None:
            await ctx.reply(f"Hoshi slapped {author}! HAHAHAHAHAHAHA")
        else:
            embed = discord.Embed(description=f"{author} slapped {member.mention}!", color=0x2b2d31)
            hugs = ['https://cdn.discordapp.com/attachments/804482120671821865/814100958463524884/nK.gif','https://media.tenor.com/XiYuU9h44-AAAAAM/anime-slap-mad.gif','https://media.tenor.com/Ws6Dm1ZW_vMAAAAC/girl-slap.gif','https://media.tenor.com/yJmrNruFNtEAAAAC/slap.gif','https://media.tenor.com/eU5H6GbVjrcAAAAM/slap-jjk.gif','https://media.tenor.com/PeJyQRCSHHkAAAAM/saki-saki-mukai-naoya.gif','https://media.tenor.com/ra17G61QRQQAAAAM/tapa-slap.gif','https://media.tenor.com/kggzZQ1ldoUAAAAC/slapped-anime-slap.gif']
            embed.set_image(url=(random.choice(hugs)))
            await ctx.reply(embed=embed)

    @commands.hybrid_command(name="happybirthday", aliases=["birthday"],description="Wish someone a happy birthday", extras="+happybirthday (optional @member) : +birthday")
    async def happybirthday(self, ctx, member: typing.Optional[discord.Member]):
        author = ctx.message.author.mention
        if member is None:
            await ctx.reply(f"Hoshi wishes {author} a happy birthday!")
        else:
            embed = discord.Embed(description=f"{author} wished {member.mention} a happy birthday!", color=0x2b2d31)
            bday = ['https://media.tenor.com/M-34lT1ySIIAAAAd/hb.gif','https://media.tenor.com/CA8wXuq5Ec8AAAAd/happy40th-birthday.gif','https://media.tenor.com/ekHNpcO0QPEAAAAC/happy-birthday.gif','https://media.tenor.com/4DZR7mxre0IAAAAC/birthday-happy-birthday.gif','https://media.tenor.com/21kzclFhTg8AAAAC/happy-birthday-birthday.gif','https://media.tenor.com/9WoGmoTqej4AAAAC/happy-birthday-hbd.gif','https://media.tenor.com/BHTQmBYipVEAAAAC/anyon-birthday.gif','https://media.tenor.com/eCGKnoBDOAQAAAAC/happy-birthday.gif']
            embed.set_image(url=(random.choice(bday)))
            await ctx.reply(embed=embed)

    @commands.hybrid_command(name='8ball',description="Ask 8ball a question", extras="+8ball will i have a good day?")
    async def eight_ball(self, ctx, *, question):
        responses = ["It is certain.","It is decidedly so.","Without a doubt.","Yes - definitely.","You may rely on it.","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes.","Reply hazy, try again.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again.","Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.","Very doubtful."]
        response = random.choice(responses)
        embed = discord.Embed(description=f"question: {question}\nanswer: {response}", color=0x2b2d31)
        embed.set_author(name="8ball", icon_url="https://cdn.discordapp.com/attachments/1121841074512605186/1151109254959333426/png-clipart-magic-8-ball-eight-ball-crazy-eights-ball-game-logo.png")
        embed.set_footer(text=f"8ball for {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name='ship',description="Ship 2 people together", extras="+ship @member @member")
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member):
        compatibility = random.randint(0, 100)

        if compatibility < 20:
            ship_name = "Incompatible Duo"
        elif compatibility < 40:
            ship_name = "Awkward Pair"
        elif compatibility < 60:
            ship_name = "Potential Couple"
        elif compatibility < 80:
            ship_name = "Perfect Match"
        else:
            ship_name = "Soulmates"

        ship_message = f"❤️ Compatibility between {user1.mention} and {user2.mention}: **{compatibility}%**\n"
        ship_message += f"💑 Ship Name: **__{ship_name}__**"

        await ctx.send(ship_message)

    @commands.hybrid_command(name='howgay',description="How gay really are you?", extras="+howgay (optional @member)")
    async def howgay(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        percentage = random.randint(0, 100)
        await ctx.send(f"{member.mention} is **{percentage}%** gay. 🏳️‍🌈")

    @commands.hybrid_command(name='giphy',description="Search for gifs", extras="+giphy bts dance")
    async def giphy(self, ctx, *, search):
        api_key = "PF48beXJTbUkvh35ThoQ4t1qhyjleLwD"
        url = f"https://api.giphy.com/v1/gifs/search"
        params = {
            "api_key": api_key,
            "q": search,
            "limit": 10,
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
            gifs = data["data"]

            if not gifs:
                await ctx.send("No GIFs found for the given search query.")
                return

            gifs = [gif for gif in gifs if gif["id"] not in self.gif_cache.get(ctx.author.id, [])]

            if not gifs:
                self.gif_cache[ctx.author.id] = []
                gifs = data["data"]

            gif = random.choice(gifs)
            gif_url = gif["images"]["original"]["url"]
            await ctx.send(gif_url)

            self.gif_cache.setdefault(ctx.author.id, []).append(gif["id"])
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        content = message.content.strip()
        if len(content) == 1 and content.isalpha():
            await self.guess(message, content.lower())

    def get_hidden_word(self):
        return "".join(letter if letter in self.guesses else "_" for letter in self.current_word)

    def _get_round_avatar(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        circle = Image.open('./assets/circle-mask.png').resize((160, 160)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((160, 160))
        return avatar_image, circle

    @commands.command(name='tweet',description="Tweet as yourself with Hoshi", extras="+tweet hello twitter")
    async def tweet(self, ctx, *tweet: str) -> BytesIO:
        tweet_text = " ".join(tweet)
        avatar_url = ctx.author.avatar.url
        async with self.bot.session.get(avatar_url) as response:
            if response.status == 200:
                avatar_data = await response.read()
            else:
                avatar_data = None

        img = Image.open(f'./assets/twitter.png')
        draw = ImageDraw.Draw(img)
        if avatar_data:
            avatar = BytesIO(avatar_data)
            avatar_paste, circle = self._get_round_avatar(avatar)
            img.paste(avatar_paste, (37, 17), circle)
            
        poppins = Font.poppins(size=55)
        poppins_small = Font.poppins(size=45)
        poppins_xsmall = Font.poppins(size=35)
        wrapped_text = textwrap.fill(tweet_text, width=45)
        display_name_parts = ctx.author.display_name.split('|')
        display_name = display_name_parts[0].strip() if display_name_parts else ctx.author.display_name
        draw.text((25, 190), wrapped_text, font=poppins)
        draw.text((215, 29), display_name, font=poppins_small)
        draw.text((215, 75), f"@{ctx.author.name}", font=poppins_xsmall, fill=0x2D2D2D)
        img.save("tweet.png")
        await ctx.reply(file=discord.File("tweet.png"))

async def setup(bot):
    await bot.add_cog(Fun(bot))