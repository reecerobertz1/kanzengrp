import discord
from discord.ext import commands
from bot import LalisaBot
from utils.views import VerificationSelectView
import asyncio

class LogosView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Access Logos")
    async def access_logos(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="†⠀CHROMATICA LOGOS", description="・⠀Click the button below to download the Chromatica logos.\n\n**Note** ・⠀Always watermark logos when used on plain backgrounds.")
        

class chromatica(commands.Cog):
    def __init__(self, bot: LalisaBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id == 1462135026421596323:
            await self.handle_hiatus_submission(message)

    async def handle_hiatus_submission(self, message):
        content = message.content.strip()
        lines = content.split('\n')
        
        if len(lines) < 3:
            await self.invalid_template(message)
            return
        
        if not lines[0].lower().startswith('username:'):
            await self.invalid_template(message)
            return
        
        if not lines[1].lower().startswith('hiatus reason:'):
            await self.invalid_template(message)
            return
        
        if not lines[2].lower().startswith('current date:'):
            await self.invalid_template(message)
            return

        await message.delete()
        
        log_channel = self.bot.get_channel(1462660735170641950)
        if log_channel:
            embed = discord.Embed(description=content)
            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url if message.author.avatar else None)
            embed.set_footer(text="Hiatus Submission")
            await log_channel.send(embed=embed)
        
        temp_msg = await message.channel.send(f"{message.author.mention}, your hiatus has been submitted successfully!")
        await asyncio.sleep(5)
        try:
            await temp_msg.delete()
        except:
            pass

    async def invalid_template(self, message):
        await message.delete()
        temp_msg = await message.channel.send(f"{message.author.mention}, your message does not match the required template. Please try again.\n\n**Template:**\nusername:\nhiatus reason:\ncurrent date:")
        await asyncio.sleep(10)
        try:
            await temp_msg.delete()
        except:
            pass

    @commands.command()
    async def offline(self, ctx):
        banner_embed = discord.Embed()
        banner_embed.set_image(url="https://cdn.discordapp.com/attachments/1462091016990494927/1462650940476887143/Info_Banners_00000.png?ex=696ef756&is=696da5d6&hm=c40513afc61ffb6965075800dd3cbec53bdbbad4aa401c7b2917d9f9782031fc&")
        info_embed = discord.Embed(title="†⠀SYSTEM STATUS⠀：⠀OFFLINE", description="-# ・⠀Leave your hiatus messages below for Hoshi to process.\n-# ・⠀Messages are logged privately; public logs will be deleted.\n\n**INFORMATION**\n-# ・⠀**VALIDITY:** Hiatuses are only valid for the month you send them. \n-# ・⠀**RESET:** All hiatuses clears on the 1st of every month. \n-# ・⠀**LIMIT:** 3 consecutive months maximum. \n-# ・⠀**EXPIRY:** Inactivity beyond 4 months will result in a demotion.\n\n-# **Note:**⠀Server activity is prioritized over your posting activity.")
        template_embed = discord.Embed(title="†⠀TEMPLATE", description="-# **USERNAME:** your instagram username\n-# **HIATUS REASON:** your hiatus reason\n-# **CURRENT DATE:** 19/01/2026\n\n-# ・⠀Ensure the templates correctly used before submitting a hiatus. \n-# ・⠀Incomplete templates will result in a processing error.")
        template_embed.set_footer(text="CHRT_OS // INPUT_REQUIRED")
        await ctx.send(embeds=[banner_embed, info_embed, template_embed])

    @commands.command()
    async def handbook(self, ctx):
        embed_banner = discord.Embed()
        embed_banner.set_image(url="https://cdn.discordapp.com/attachments/1462091016990494927/1462650940476887143/Info_Banners_00000.png?ex=696ef756&is=696da5d6&hm=c40513afc61ffb6965075800dd3cbec53bdbbad4aa401c7b2917d9f9782031fc&")
        embed_info = discord.Embed(title="†    MEMBER ： HANDBOOK", description="・⠀Welcome to the Chromatica interface. Read all protocols below.\n\n**PROTOCOLS**\n ・⠀01 : Must always be following [@chromaticagp](https://www.instagram.com/chromaticagp/).\n ・⠀02 : Mandatory use of group hashtag #𝗰𝗵𝗿𝗼𝗺𝗮𝘁𝗶𝗰𝗮𝗴𝗽.\n ・⠀03 : Set your nickname to format: [ name | username ]. \n・⠀04 : Let staff or leads know when you move accounts or leave.\n ・⠀05 : Please be respectful toward all members of our server.\n\n**Note** ・⠀Demotions or group bans may happen if rules are broken.")
        embed_info.set_footer(text="CHRT_OS // MEMBER_CORE_v1.01")
        embed_logos = discord.Embed(title="†    GROUP ： LOGOS", description="・⠀Please read the information below before using our logos.\n\n**LOGO INFORMATION**\n ・⠀01 : Reach level 3 with Hoshi to gain access to our logos. \n・⠀02 : Always watermark logos when used on plain backgrounds.\n ・⠀03 : Leaking our logos to non-members is strictly prohibited.\n\n**Note** ・⠀Leaking our logos results in a permanent ban and blacklist")
        embed_logos.set_footer(text="CHRT_OS // ASSET_SECURED_v1.01")
        view = LogosView()
        await ctx.send(embeds=[embed_banner, embed_info, embed_logos])

async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(chromatica(bot))