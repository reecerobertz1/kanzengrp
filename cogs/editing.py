from io import BytesIO
import json
import random
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

JSON_FILE_PATH = "./json files/colors.json"

class editing(commands.Cog):
    """Commands to help you with editing"""
    def __init__(self, bot):
        self.bot = bot

    def get_edits_data(self):
        try:
            with open("./json files/edits.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def save_edits_data(self, data):
        with open("./json files/edits.json", "w") as file:
            json.dump(data, file, indent=4)

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
    async def effects(self, ctx: commands.Context):
        embed = discord.Embed(title="Effect Commands", color=0x2B2D31)
        embed.add_field(name="effects ae", value="Sends effects for After Effects", inline=False)
        embed.add_field(name="effects vs", value="Sends effects for videostar", inline=False)
        await ctx.reply(embed=embed)

    @effects.command()
    async def ae(self, ctx):
        choices = ["4-Color Gradient", "S_HalfTone", "Gradient Ramp", "S_PseudoColor", "S_FlysEyeHex", "S_WipeTiles", "S_EdgeRays", "S_WipeMoire", "S_WipeDots", "S_WipePixelate", "S_WipePlasma", "S_WipeFlux", "S_GlowDist", "S_Glint", "Glow", "Turbulent Displace", "Wave Warp", "BCC lens blur OBS", "Invert", "Exposure", "BCC Cross Glitch", "BCC LED", "Omino Diffuse", "Omino Squares", "Grid"]
        raneffect = random.choice(choices)
        await ctx.reply(raneffect)

    @effects.command()
    async def vs(self, ctx):
        choices = ["Select Shift", "Luma Fade", "Contrast", "Swap Hue", "Delete Color", "neXt-Ray", "Solarize", "Rainbow Halo", "E-Sample", "E-Saber", "E-Glitter", "E-Rays", "E-Anime", "E-Aura", "Frozen", "Zoom Blur", "Lens Blur", "Ring Blur", "Light Rays", "Minimax Hex", "Minimax Spin", "LED Image Circle", "LED Image Square", "LED Reveal", "Color Shadow", "Cosmic Wave", "Hole Wipe 1", "Hole Wipe 2", "Rect Wipe 1", "Rect Wipe 2", "*-Bit Wipe", "Glitch A0", "Glitch A1", "Glitch A2", "Glitch A4", "Glitch A5", "Glitch A6", "Glitch A7", "Glitch A8", "Glitch A9", "Blacken", "Hue Shift", "Color SHift", "Video Smear", "Video Melt", "Bevel Edge", "Halftone", "Block Filter", "Outline", "Scanner 1", "Scanner 2", "Edge", "White Edge", "White Lines"]
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
            "BTS - Taehyung", "BTS - Hoseok", "BTS - Yoongi",  "BTS - Namjoon", "BTS - Jimin", "BTS - Jin", "BTS - Jungkook", 
            "Blackpink - Lisa","Blackpink - Jennie", "Blackpink rosé", "Blackpink - Jisoo", 
            "Lesserafim - Yunjin", "Lesserafim - Sakura", "Lesserafim - Chaewon", "Lesserafim - Kazuha", "Lesserafim - Eunchae", 
            "Enhypen - Jake", "Enhypen - Jay", "Enhypen - Heeseung", "Enhypen - Sunghoon", "Enhypen - Sunoo", "Enhypen - Jungwon", "Enhypen - Ni-ki",
            "New Jeans - Minji", "New Jeans - Hanni", "New Jeans - Danielle", "New Jeans - Haerin", "New Jeans - Hyein", 
            "P1harmony - Keeho", "P1harmony - Intak","P1harmony - Theo", "P1harmony - Jiung", "P1harmony - Soul", "P1harmony - Jongseob", 
            "Twice - Nayeon", "Twice - Jeonyeon", "Twice - Momo", "Twice - Sana","Twice - Jihyo", "Twice - Mina", "Twice - Dahyun", "Twice - Chaeyoung", "Twice - Tzuyu", 
            "Ateez - Wooyoung", "Ateez - San", "Ateez - Hoongjoon", "Ateez - Seonghwa","Ateez - Jongho", "Ateez - Yunho", "Ateez - Mingi", 
            "Seventeen - DK", "Seventeen - Seungkwan", "Seventeen - Mingyu", "Seventeen - Woozi", "Seventeen - Hoshi (not the bot)", "Seventeen - Dino","Seventeen - Wonwoo", "Seventeen - Junhui", "Seventeen - The8", "Seventeen - Scoups", "Seventeen - Joshua", "Seventeen - Vernon", "Seventeen - Jeonghan", 
            "Aespa - Karina","Aespa - Ningning", "Aespa - Winter", "Aespa - Giselle", "Aespa - Karina", 
            "TXT - Kai", "TXT - Soobin", "TXT - Yeonjun", "TXT - Beomgyu", "TXT - Taehyun", 
            "Stray Kids - Bang Chan","Stray Kids - Lee Know", "Stray Kids - Changbin", "Stray Kids - Han", "Stray Kids - Felix", "Stray Kids - Seungmin", "Stray Kids - I.N", "Stray Kids - Hyunjin", 
            "Itzy - Yeji", "Itzy - Ryujin", "Itzy - Lia", "Itzy - Chaeryeong", "Itzy - Yuna", 
            "Stayc - Sumin", "Stayc - Sieun", "Stayc - Isa", "Stayc - Seeun", "Stayc - Yoon", "Stayc - J", 
            "Viviz - Umji", "Viviz - SinB", "Viviz - Eunha"
        ]

        person = random.choice(choices)
        await ctx.reply(person)

    def colorscheme(self) -> BytesIO:
        with open("json files/colors.json", "r") as f:
            schemes = json.load(f)
            colors = random.choice(schemes)
        font = ImageFont.truetype("Montserrat-Bold.ttf", 20)
        s = 200
        img = Image.new('RGB', (s*len(colors), 225), (255, 255, 255))
        for i, color in enumerate(colors):
            col = Image.new('RGBA', (s, s+25), color)
            img.paste(col, (i*s, 0))
            draw = ImageDraw.Draw(img, 'RGBA')
            draw.rectangle(((i*s, s), ((i+1)*s, s+25)), (0, 0, 0, 65))
            draw.text(((i+0.5)*s, s), f"{color.upper()}", color, font=font, anchor="ma")
        buf = BytesIO()
        img.save(buf, 'PNG')
        buf.seek(0)
        return buf

    @commands.command()
    async def cs(self, ctx):
        try:
            image_buffer = self.colorscheme()
            await ctx.send(file=discord.File(image_buffer, filename="color_palette.png"))

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def addedit(self, ctx, link):
        data = self.get_edits_data()
        data.append(link)
        self.save_edits_data(data)
        await ctx.reply("Your edit added successfully.")

    @commands.group(aliases=['edits'])
    async def edit(self, ctx):
        with open("./json files/edits.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add your edits with `+addedit`\n[here is the edit]({choice})")

    @commands.command()
    async def addsoft(self, ctx, link):
        button = discord.ui.Button(label="Click to hear audio", url=f"{link}")

        view = discord.ui.View()
        view.add_item(button)
        log = self.bot.get_channel(1122627075682078720)
        embed = discord.Embed(title="Added soft audio", description=f"`{ctx.author.display_name}` has added a soft audio!", color=0x2b2d31)
        embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
        await self._add_audio(ctx, "./json files/softaudios.json", link)
        await log.send(embed=embed, view=view)


    @commands.command()
    async def addhot(self, ctx, link):
        button = discord.ui.Button(label="Click to hear audio", url=f"{link}")

        view = discord.ui.View()
        view.add_item(button)
        log = self.bot.get_channel(1122627075682078720)
        embed = discord.Embed(title="Added hot audio", description=f"`{ctx.author.display_name}` has added a hot audio!", color=0x2b2d31)
        embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
        await self._add_audio(ctx, "./json files/hotaudios.json", link)
        await log.send(embed=embed, view=view)

    @commands.group(invoke_without_command=True)
    async def audio(self, ctx: commands.Context):
        embed = discord.Embed(title="Audio Commands", color=0x2B2D31)
        embed.add_field(name="audio soft", value="Sends a soft audio", inline=False)
        embed.add_field(name="audio hot", value="Sends a hot audio", inline=False)
        await ctx.reply(embed=embed)

    @audio.command()
    async def soft(self, ctx):
        with open("./json files/softaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a soft audio with `+addsoft`\n[here is the audio]({choice})")

    @audio.command()
    async def hot(self, ctx):
        with open("./json files/hotaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a hot audio with `+addhot`\n[here is the audio]({choice})")

async def setup(bot):
    await bot.add_cog(editing(bot))