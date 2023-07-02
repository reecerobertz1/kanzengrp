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
            "Blackpink - Jennie", "Blackpink rosé", "Blackpink - Jisoo"
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
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-20.png"]
        raneffect = random.choice(choices)
        await ctx.reply(raneffect)

async def setup(bot):
    await bot.add_cog(editing(bot))