import json
import random
import discord
from discord.ext import commands


class editing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["effect"])
    async def effects(self, ctx):
        choices = ["4-Color Gradient", "S_HalfTone", "Gradient Ramp", "S_PseudoColor", "S_FlysEyeHex", "S_WipeTiles", "S_EdgeRays", "S_WipeMoire", "S_WipeDots", "S_WipePixelate", "S_WipePlasma", "S_WipeFlux", "S_GlowDist", "S_Glint", "Glow", "Turbulent Displace", "Wave Warp", "BCC lens blur OBS", "Invert", "Exposure", "BCC Cross Glitch", "BCC LED", "Omino Diffuse", "Omino Squares", "Grid"]
        raneffect = random.choice(choices)
        await ctx.reply(raneffect)

    @commands.command(aliases=["transitions"])
    async def transition(self, ctx):
        choices = ["Warp Fisheye", "Zoom in", "Zoom out", "Inside Cube", "Ink Splash", "Split Cube", "Polaroid Pop Up", "CC scale wipe", "3D flip", "3D tunnel", "Tile Scramble", "do something with a cube, dont be lazy", "idfk... look at someone's edits take inspo from them (GIVE THEM IB CREDITS THOUGH)", "rotation", "slide down", "slide right", "slide left", "slide up", "slide somewhere", "3D flip into a cube", "i can't think of anything... do the command again"]
        raneffect = random.choice(choices)
        await ctx.reply(raneffect)

    @commands.command(aliases=["who2edit"])
    async def whotoedit(self, ctx):
        """Displays a random transition effect for video editing."""

        choices = [
            "BTS - Taehyung", "BTS - Hoseok", "BTS - Yoongi",  "BTS - Namjoon", "BTS - Jimin", "BTS - Jin", "BTS - Jungkook", "Blackpink - Lisa", 
            "Blackpink - Jennie", "Blackpink rosé", "Blackpink - Jisoo", "Lesserafim - Yunjin", "Lesserafim - Sakura", "Lesserafim - Chaewon", "Lesserafim - Kazuha", 
            "Lesserafim - Eunchae", "Enhypen - Jake", "Enhypen - Jay", "Enhypen - Heeseung", "Enhypen - Sunghoon", "Enhypen - Sunoo", "Enhypen - Jungwon", "Enhypen - Ni-ki",
            "New Jeans - Minji", "New Jeans - Hanni", "New Jeans - Danielle", "New Jeans - Haerin", "New Jeans - Hyein", "P1harmony - Keeho", "P1harmony - Intak",
            "P1harmony - Theo", "P1harmony - Jiung", "P1harmony - Soul", "P1harmony - Jongseob", "Twice - Nayeon", "Twice - Jeonyeon", "Twice - Momo", "Twice - Sana",
            "Twice - Jihyo", "Twice - Mina", "Twice - Dahyun", "Twice - Chaeyoung", "Twice - Tzuyu", "Ateez - Wooyoung", "Ateez - San", "Ateez - Hoongjoon", "Ateez - Seonghwa",
            "Ateez - Jongho", "Ateez - Yunho", "Ateez - Mingi", "Seventeen - DK", "Seventeen - Seungkwan", "Seventeen - Mingyu", "Seventeen - Woozi", "Seventeen - Hoshi (not the bot)", "Seventeen - Dino",
            "Seventeen - Wonwoo", "Seventeen - Junhui", "Seventeen - The8", "Seventeen - Scoups", "Seventeen - Joshua", "Seventeen - Vernon", "Seventeen - Jeonghan", "Aespa - Karina",
            "Aespa - Ninging", "Aespa - Winter", "Aespa - Giselle", "Aespa - Karina", "TXT - Kai", "TXT - Soobin", "TXT - Yeonjun", "TXT - Beomgyu", "TXT - Taehyun", "Stray Kids - Bang Chan",
            "Stray Kids - Lee Know", "Stray Kids - Changbin", "Stray Kids - Han", "Stray Kids - Felix", "Stray Kids - Seungmin", "Stray Kids - I.N", "Stray Kids - Hyunjin", "Itzy - Yeji",
            "Itzy - Ryujin", "Itzy - Lia", "Itzy - Chaeryeong", "Itzy - Yuna"
        ]

        person = random.choice(choices)
        await ctx.reply(person)

    @commands.command(aliases=["cs"])
    async def colorscheme(self, ctx):
        choices = ["https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-1.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-2.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-3.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-4.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-5.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-6.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-7.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-8.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-9.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-10.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-11.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-12.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-13.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-14.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-15.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-16.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-17.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-18.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-19.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-20.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-21.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-22.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-23.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-24.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-25.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-26.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-27.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-28.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-29.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-30.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-31.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-32.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-33.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-34.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-35.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-36.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-37.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-38.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-39.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-40.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-41.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-42.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-43.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-44.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-45.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-46.png",
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-47.png",]
        rancolor = random.choice(choices)
        await ctx.reply(rancolor)

async def setup(bot):
    await bot.add_cog(editing(bot))