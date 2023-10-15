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

    @commands.group(invoke_without_command=True, description="See the commands for effecrs for each prgram/app")
    async def effects(self, ctx: commands.Context):
        embed = discord.Embed(title="Effect Commands", color=0x2B2D31)
        embed.add_field(name="effects ae", value="Sends effects for After Effects", inline=False)
        embed.add_field(name="effects vs", value="Sends effects for videostar", inline=False)
        await ctx.reply(embed=embed)

    @effects.command(description="Use the +effects ae command for ae effects")
    async def ae(self, ctx):
        choices = ["4-Color Gradient", "S_HalfTone", "Gradient Ramp", "S_PseudoColor", "S_FlysEyeHex", "S_WipeTiles", "S_EdgeRays", "S_WipeMoire", "S_WipeDots", "S_WipePixelate", "S_WipePlasma", "S_WipeFlux", "S_GlowDist", "S_Glint", "Glow", "Turbulent Displace", "Wave Warp", "BCC lens blur OBS", "Invert", "Exposure", "BCC Cross Glitch", "BCC LED", "Omino Diffuse", "Omino Squares", "Grid"]
        raneffect = random.choice(choices)
        await ctx.reply(raneffect)

    @effects.command(description="Use the +effects vs command for vs effects")
    async def vs(self, ctx):
        choices = ["Select Shift", "Luma Fade", "Contrast", "Swap Hue", "Delete Color", "neXt-Ray", "Solarize", "Rainbow Halo", "E-Sample", "E-Saber", "E-Glitter", "E-Rays", "E-Anime", "E-Aura", "Frozen", "Zoom Blur", "Lens Blur", "Ring Blur", "Light Rays", "Minimax Hex", "Minimax Spin", "LED Image Circle", "LED Image Square", "LED Reveal", "Color Shadow", "Cosmic Wave", "Hole Wipe 1", "Hole Wipe 2", "Rect Wipe 1", "Rect Wipe 2", "*-Bit Wipe", "Glitch A0", "Glitch A1", "Glitch A2", "Glitch A4", "Glitch A5", "Glitch A6", "Glitch A7", "Glitch A8", "Glitch A9", "Blacken", "Hue Shift", "Color SHift", "Video Smear", "Video Melt", "Bevel Edge", "Halftone", "Block Filter", "Outline", "Scanner 1", "Scanner 2", "Edge", "White Edge", "White Lines"]
        raneffect = random.choice(choices)
        await ctx.reply(raneffect)

    @commands.command(aliases=["transitions"],description="Get transitions to use in edits")
    async def transition(self, ctx):
        choices = ["Warp Fisheye", "Zoom in", "Zoom out", "Inside Cube", "Ink Splash", "Split Cube", "Polaroid Pop Up", "CC scale wipe", "3D flip", "3D tunnel", "Tile Scramble", "do something with a cube, dont be lazy", "idfk... look at someone's edits take inspo from them (GIVE THEM IB CREDITS THOUGH)", "rotation", "slide down", "slide right", "slide left", "slide up", "slide somewhere", "3D flip into a cube", "i can't think of anything... do the command again"]
        raneffect = random.choice(choices)
        await ctx.reply(raneffect)

    @commands.command(aliases=["who2edit"], description="Stuck for who to edit? Use this command")
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

    @commands.command(aliases=["cs"], description="Get a random color scheme for edits")
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
                   "https://digitalsynopsis.com/wp-content/uploads/2019/11/color-schemes-palettes-47.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654004233089194/dfgsg.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654004564426762/dfgsgf.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654004782542919/dfgsdgd_1.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654005046779975/dfgsdgf.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654005340385310/dfsgsdfg.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654005566873672/dsfgdfgd.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654005772406915/dfgsdgdf.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654006045024266/fdgsdfgd.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654006284112042/dfsgdfgdf.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654006565122109/sdgsdf.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654067684507803/dsfgdgf.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654067961335870/sdfgsfd.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654068313653418/fsdgdg.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654068724711474/dsfgsdfg.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654069148323920/dfgsdgd.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654069404188682/sdfg.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654069647446166/gsdfgdf.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654069911683102/dfasf.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654070347907262/cs2.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654070624718968/cs1.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654081974513684/cs5.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654082280702113/cs4.png",
                   "https://cdn.discordapp.com/attachments/1055747641620832358/1143654082570113134/cs3.png"]
        rancolor = random.choice(choices)
        await ctx.reply(rancolor)

    @commands.command(description="Add your own edits to Hoshi")
    async def addedit(self, ctx, link):
        data = self.get_edits_data()
        data.append(link)
        self.save_edits_data(data)
        await ctx.reply("Your edit added successfully.")

    @commands.group(aliases=['edits'],description="See edits added by other members")
    async def edit(self, ctx):
        with open("./json files/edits.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add your edits with `+addedit`\n[here is the edit]({choice})")

    @commands.command(description="Add a soft audio")
    async def addsoft(self, ctx, link):
        button = discord.ui.Button(label="Click to hear audio", url=f"{link}")

        view = discord.ui.View()
        view.add_item(button)
        log = self.bot.get_channel(1122627075682078720)
        embed = discord.Embed(title="Added soft audio", description=f"`{ctx.author.display_name}` has added a soft audio!", color=0x2b2d31)
        embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
        await self._add_audio(ctx, "./json files/softaudios.json", link)
        await log.send(embed=embed, view=view)

    @commands.command(description="Add a hot audio")
    async def addhot(self, ctx, link):
        button = discord.ui.Button(label="Click to hear audio", url=f"{link}")

        view = discord.ui.View()
        view.add_item(button)
        log = self.bot.get_channel(1122627075682078720)
        embed = discord.Embed(title="Added hot audio", description=f"`{ctx.author.display_name}` has added a hot audio!", color=0x2b2d31)
        embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
        await self._add_audio(ctx, "./json files/hotaudios.json", link)
        await log.send(embed=embed, view=view)

    @commands.command(description="Add a collab audio")
    async def addcollab(self, ctx, link):
        button = discord.ui.Button(label="Click to hear audio", url=f"{link}")

        view = discord.ui.View()
        view.add_item(button)
        log = self.bot.get_channel(1122627075682078720)
        embed = discord.Embed(title="Added collab audio", description=f"`{ctx.author.display_name}` has added a collab audio!", color=0x2b2d31)
        embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
        await self._add_audio(ctx, "./json files/collabaudios.json", link)
        await log.send(embed=embed, view=view)

    @commands.group(invoke_without_command=True, description="See the command categories for audios")
    async def audio(self, ctx: commands.Context):
        embed = discord.Embed(title="Audio Commands", color=0x2B2D31)
        embed.add_field(name="audio soft", value="Sends a soft audio", inline=False)
        embed.add_field(name="audio hot", value="Sends a hot audio", inline=False)
        await ctx.reply(embed=embed)

    @audio.command(description="Use the command +audio soft for soft audios")
    async def soft(self, ctx):
        with open("./json files/softaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a soft audio with `+addsoft`\n[here is the audio]({choice})")

    @audio.command(description="Use the command +audio hot for hot audios")
    async def hot(self, ctx):
        with open("./json files/hotaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a hot audio with `+addhot`\n[here is the audio]({choice})")

    @audio.command(description="Use the command +audio collab for collab audios")
    async def collab(self, ctx):
        with open("./json files/collabaudios.json", "r") as f:
            audios = json.load(f)
            choice = random.choice(audios)
            await ctx.reply(f"Add a collab audio with `+addcollab`\n[here is the audio]({choice})")

async def setup(bot):
    await bot.add_cog(editing(bot))