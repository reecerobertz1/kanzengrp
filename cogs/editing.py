import functools
from io import BytesIO
import json
import random
from typing import Union
import aiohttp
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from colorthief import ColorThief

JSON_FILE_PATH = "./json files/colors.json"

class editing(commands.Cog):
    """Commands to help you with editing"""
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:koya:1121909483698925618>"

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

    @commands.command(aliases=["who2edit"], description="Stuck for who to edit? Use this command", extras="alias +who2edit")
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

    def calculate_brightness(self, color):
        return (0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]) / 255

    @commands.command(description="Generate a color palette image", aliases=['cs', 'palette'], extras="aliases +cs, +palette")
    async def colorpalette(self, ctx):
        with open('./json files/colors.json', 'r') as file:
            color_groups = json.load(file)

        group = random.choice(color_groups)
        padding = 5
        square_size = 100
        max_columns = len(group)
        image_width = max_columns * (square_size + padding) - padding
        image_height = square_size
        image = Image.new('RGB', (image_width, image_height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("./fonts/Montserrat-Regular.ttf")
        font1 = ImageFont.truetype("./fonts/Montserrat-Bold.ttf")

        x = 0

        for color_hex in group:
            color = tuple(int(color_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
            draw.rectangle([x, 0, x + square_size, square_size], fill=color)

            hex_code = color_hex.upper()
            text_width, text_height = draw.textsize(hex_code, font=font1)
            text_x = x + (square_size - text_width) // 2
            text_y = square_size - text_height

            brightness = self.calculate_brightness(color)
            text_color = "#272727" if brightness > 0.5 else "#ffffff"
            
            draw.text((text_x, text_y), hex_code, fill=text_color, font=font1)
            x += square_size + padding

        image.save("color_palette.png")
        await ctx.send(file=discord.File("color_palette.png"))

    @commands.command(description="Add a soft audio", extras="+addsoft (soundcloud link)")
    async def addsoft(self, ctx, link):
        button = discord.ui.Button(label="Click to hear audio", url=f"{link}")

        view = discord.ui.View()
        view.add_item(button)
        log = self.bot.get_channel(1011212849965715528)
        embed = discord.Embed(title="Added soft audio", description=f"`{ctx.author.display_name}` has added a soft audio!", color=0x2b2d31)
        embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
        await self._add_audio(ctx, "./json files/softaudios.json", link)
        await log.send(embed=embed, view=view)

    @commands.command(description="Add a hot audio", extras="+addhot (soundcloud link)")
    async def addhot(self, ctx, link):
        button = discord.ui.Button(label="Click to hear audio", url=f"{link}")

        view = discord.ui.View()
        view.add_item(button)
        log = self.bot.get_channel(1011212849965715528)
        embed = discord.Embed(title="Added hot audio", description=f"`{ctx.author.display_name}` has added a hot audio!", color=0x2b2d31)
        embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
        await self._add_audio(ctx, "./json files/hotaudios.json", link)
        await log.send(embed=embed, view=view)

    @commands.command(description="Add a collab audio", extras="+addcollab (soundcloud link)")
    async def addcollab(self, ctx, link):
        button = discord.ui.Button(label="Click to hear audio", url=f"{link}")

        view = discord.ui.View()
        view.add_item(button)
        log = self.bot.get_channel(1011212849965715528)
        embed = discord.Embed(title="Added collab audio", description=f"`{ctx.author.display_name}` has added a collab audio!", color=0x2b2d31)
        embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
        await self._add_audio(ctx, "./json files/collabaudios.json", link)
        await log.send(embed=embed, view=view)

    @commands.group(invoke_without_command=True, description="See the command categories for audios", hidden=True)
    async def audio(self, ctx: commands.Context):
        embed = discord.Embed(title="Audio Commands", color=0x2B2D31)
        embed.add_field(name="soft audios", value="• **+audiosoft** sends a soft audio\n• **+addsoft** adds a soft audio", inline=False)
        embed.add_field(name="hot audios", value="• **+audio hot** sends a hot audio\n• **+addhot** adds a hot audio", inline=False)
        embed.add_field(name="collab audios", value="• **+audio collab** sends a collab audio\n• **+addcollab** adds a collab audio", inline=False)
        await ctx.reply(embed=embed)

    @audio.command(description="Use the command +audio soft for soft audios", extras="+audio soft")
    async def soft(self, ctx):
        with open("./json files/softaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Please make sure to give credits!\n{choice}")

    @audio.command(description="Use the command +audio hot for hot audios", extras="+audio hot")
    async def hot(self, ctx):
        with open("./json files/hotaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Please make sure to give credits!\n{choice}")

    @audio.command(description="Use the command +audio collab for collab audios", extras="+audio collab")
    async def collab(self, ctx):
        with open("./json files/collabaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Please make sure to give credits!\n{choice}")

    @commands.command()
    async def transition(self, ctx):
        transitions = ["cc flo motion + tile rotation",
                       "s_flyseyehex rotation",
                       "zoom in",
                       "rotation",
                       "warp",
                       "middle tile rotation",
                       "zoom out",
                       "skew",
                       "timeslice slide",
                       "butterfly overlay",
                       "fisheye warp",
                       "2 split cube",
                       "3 split cube",
                       "split slide rotation",
                       "y rotation",
                       "x rotation",
                       "vr rotate sphere",
                       "cube expand w something on the inside",
                       "scale stretch",
                       "do something w a cube, dont be lazy",
                       "do something 3d",
                       "shatter",
                       "inside cube rotation",
                       "card wipe",
                       "cube split",
                       "tile rotation",
                       "wipe rings (+turb)",
                       "hexagon tile spin",
                       "zoom in + rotation",
                       "zoom out + rotation",
                       "mirror stretch",
                       "3D tunnel",
                       "torn paper transition",
                       "wipe overlay",
                       "3D flip",
                       "slide + rotation",
                       "vr reorient",
                       "cube rotatiton",
                       "s_warpcornerpin",
                       "s_wipeblobs",
                       "s_flyseyehex corner spin",
                       "s_flyseyerect anchored point rotation",
                       "stretch slide",
                       "cc scale wipe",
                       "s_warppuddle",
                       "vortex spin",
                       "cube shatter",
                       "warp squeeze",
                       "ink splash",
                       "polariod transition",
                       "text morph",
                       "Instagram feed",
                       "Pinterest feed",
                       "Game themed transition",
                       "TV damage transition",
                       "Comic book style",
                       "Food themed transition"]
        transition = random.choice(transitions)
        embed = discord.Embed(description=transition, color=0x2b2d31)
        await ctx.reply(embed=embed)

    @commands.command()
    async def theme(self, ctx):
        themes = ['Game theme', 'Horror movie theme', 'Arcade theme', 'Comic book theme', 'Symphony theme', 'Food themed']
        theme = random.choice(themes)
        embed = discord.Embed(description=theme, color=0x2b2d31)
        if theme == "Symphony theme":
                    embed.set_image(url="https://cdn.discordapp.com/attachments/849724031723634688/1288433068297949194/ezgif-4-74099fde38.png?ex=66f52a4d&is=66f3d8cd&hm=210cc74380e1fdf772ce2e196e79c85446b336727375f93c2ca88d6d327cf9b2&")
        await ctx.reply(embed=embed)

    def get_palette(self, image: BytesIO) -> BytesIO:
        temp_img = Image.open(image)
        if temp_img.width > 256 or temp_img.height > 256:
            temp_img.thumbnail((256, 256))
            image = BytesIO()
            temp_img.save(image, 'PNG')
            image.seek(0)
        zhcn = ImageFont.truetype("./fonts/zhcn.ttf", size=20)
        s = 200
        ct = ColorThief(image)
        colors = ct.get_palette(4, 1)
        img = Image.new('RGB', (s*len(colors), 225), (255, 255, 255))
        for i, color in enumerate(colors):
            hex_c = self.rgb_to_hex(color).upper()
            col = Image.new('RGB', (s, s+25), color)
            img.paste(col, (i*s, 0))
            drw = ImageDraw.Draw(img, 'RGBA')
            drw.rectangle(((i*s, s), ((i+1)*s, s+25)), (0, 0, 0, 65))
            drw.text(((i+0.5)*s, s), f"{hex_c.upper()}", color, font=zhcn, anchor="ma")
        buf = BytesIO()
        img.save(buf, 'PNG')
        buf.seek(0)

        return buf

    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

    @commands.command(aliases=["makepalette", "generatepalette", "gp", "mp"])
    async def getpalette(self, ctx, image_source: Union[discord.Member, str]=None):
        async with ctx.typing():
            if image_source != None:
                if type(image_source) == str:
                    if image_source.startswith("https://") or image_source.startswith("http://"):
                        async with aiohttp.ClientSession() as session:
                            async with session.get(image_source) as resp:
                                image = BytesIO(await resp.read())
                                image.seek(0)
                    else:
                        return await ctx.send("You need to use a https or http URL")
                else:
                    to_edit = image_source.display_avatar.with_size(256)
                    image = BytesIO(await to_edit.read())
                    image.seek(0)
            else:
                if ctx.message.attachments:
                    to_edit = ctx.message.attachments[0]
                    image = BytesIO(await to_edit.read())
                    image.seek(0)
                else:
                    to_edit = ctx.author.display_avatar.with_size(256)
                    image = BytesIO(await to_edit.read())
                    image.seek(0)
            palette_gen = functools.partial(self.get_palette, image)
            palette = await self.bot.loop.run_in_executor(None, palette_gen)
            await ctx.send(file=discord.File(fp=palette, filename="palette.png"))

async def setup(bot):
    await bot.add_cog(editing(bot))