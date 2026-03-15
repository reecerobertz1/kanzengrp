import discord
from discord.ext import commands
from bot import LalisaBot
import asyncio
import datetime

class MegaLinkView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Mega Link", style=discord.ButtonStyle.link, url="https://mega.nz/folder/PVVwHIgC#1UUQwD-oH4NLBzDWC6g7Vg"))

class LogosView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.add_item(discord.ui.Button(label="Instagram", style=discord.ButtonStyle.link, url="https://www.instagram.com/chromaticagp/"))
        self.add_item(discord.ui.Button(label="TikTok", style=discord.ButtonStyle.link, url="https://www.tiktok.com/@chromaticagp?_r=1&_t=ZN-93JxQO76cHW"))
    
    @discord.ui.button(label="Access Logos", style=discord.ButtonStyle.blurple)
    async def access_logos(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="CHROMATICA LOGOS",
            description="Please make sure you read all out information down below before using the logos.\n\n**INFORMATION**\n・⠀01 : Please make sure you watermark the logos.\n・⠀02 : Do not share this mega link with anyone from outside our group\n・⠀03 : Anyone can make us logos! Feel free to send Reece some of yours."
        )

        if interaction.guild and interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)

        image_url = None
        if interaction.guild and interaction.guild.banner:
            image_url = interaction.guild.banner.url
        elif self.bot.user.banner:
            image_url = self.bot.user.banner.url
        
        if image_url:
            embed.set_image(url=image_url)

        view = MegaLinkView()

        try:
            await interaction.user.send(embed=embed, view=view)
            await interaction.response.send_message("Check your DMs for the logos link!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I couldn't DM you. Please enable DMs from server members.", ephemeral=True)
            return

        log_channel = self.bot.get_channel(1477648325087072276)
        if log_channel:
            log_embed = discord.Embed(
                title="CHROMATICA LOGOS",
                description=f"`{interaction.user.display_name}` has used the logos button.")
            log_embed.set_thumbnail(url=interaction.user.display_avatar.url)
            log_embed.set_footer(text=f"User ID: {interaction.user.id} | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", icon_url=interaction.guild.icon.url)
            await log_channel.send(embed=log_embed)
        

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
        role = message.guild.get_role(1462661321064710164)
        if role:
            try:
                await message.author.add_roles(role)
            except discord.Forbidden:
                pass
        
        log_channel = self.bot.get_channel(1477648405294747690)
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
        banner_embed.set_image(url="https://cdn.discordapp.com/attachments/1477651776139427872/1482750212077522976/Small_Headers_00008.png?ex=69b8163e&is=69b6c4be&hm=421d9f600db7b989bcc67ac9a08f748cb55d25ee863bffc614a1fe7e5f79a27e&")
        info_embed = discord.Embed(title="†⠀SYSTEM STATUS⠀：⠀OFFLINE", description="-# ・⠀Leave your hiatus messages below for Hoshi to process.\n-# ・⠀Messages are logged privately; public logs will be deleted.\n\n**INFORMATION**\n-# ・⠀**VALIDITY:** Hiatuses are only valid for the month you send them. \n-# ・⠀**RESET:** All hiatuses clears on the 1st of every month. \n-# ・⠀**LIMIT:** 3 consecutive months maximum. \n-# ・⠀**EXPIRY:** Inactivity beyond 4 months will result in a demotion.\n\n-# **Note:**⠀Server activity is prioritized over your posting activity.")
        template_embed = discord.Embed(title="†⠀TEMPLATE", description="-# **USERNAME:** your instagram username\n-# **HIATUS REASON:** your hiatus reason\n-# **CURRENT DATE:** 19/01/2026\n\n-# ・⠀Ensure the templates correctly used before submitting a hiatus. \n-# ・⠀Incomplete templates will result in a processing error.")
        template_embed.set_footer(text="CHRT_OS // INPUT_REQUIRED")
        await ctx.send(embeds=[banner_embed, info_embed, template_embed])

    @commands.command()
    async def handbook(self, ctx):
        embed_banner = discord.Embed()
        embed_banner.set_image(url="https://cdn.discordapp.com/attachments/1477651776139427872/1482750194079633523/Small_Headers_00006.png?ex=69b8163a&is=69b6c4ba&hm=24ff2ec7ae3f94452fe86d89acc9ebb638a97ae74f5ffc6cdc58deeb758b3be4&")
        embed_info = discord.Embed(title="†    MEMBER ： HANDBOOK", description="・⠀Welcome to the Chromatica interface. Read all protocols below.\n\n**PROTOCOLS**\n ・⠀01 : Must always be following [@chromaticagp](https://www.instagram.com/chromaticagp/).\n ・⠀02 : Mandatory use of group hashtag #𝗰𝗵𝗿𝗼𝗺𝗮𝘁𝗶𝗰𝗮𝗴𝗽.\n ・⠀03 : Set your nickname to format: [ name | username ]. \n・⠀04 : Let staff or leads know when you move accounts or leave.\n ・⠀05 : Please be respectful toward all members of our server.\n\n**Note** ・⠀Demotions or group bans may happen if rules are broken.")
        embed_info.set_footer(text="CHRT_OS // MEMBER_CORE_v1.01")
        embed_info.set_image(url="https://cdn.discordapp.com/attachments/1477651776139427872/1482129813182615693/Comp_5_00000.png?ex=69b7ceb4&is=69b67d34&hm=03d2f507c5438ee6dc717ca27c72483505571562a94e1ee5c5328a037bbd5a2d&")
        embed_logos = discord.Embed(title="†    GROUP ： LOGOS", description="・⠀Please read the information below before using our logos.\n\n**LOGO INFORMATION**\n ・⠀01 : Reach level 3 with Hoshi to gain access to our logos. \n・⠀02 : Always watermark logos when used on plain backgrounds.\n ・⠀03 : Leaking our logos to non-members is strictly prohibited.\n\n**Note** ・⠀Leaking our logos results in a permanent ban and blacklist")
        embed_logos.set_footer(text="CHRT_OS // ASSET_SECURED_v1.01")
        embed_logos.set_image(url="https://cdn.discordapp.com/attachments/1477651776139427872/1482129813182615693/Comp_5_00000.png?ex=69b7ceb4&is=69b67d34&hm=03d2f507c5438ee6dc717ca27c72483505571562a94e1ee5c5328a037bbd5a2d&")
        view = LogosView(self.bot)
        await ctx.send(embeds=[embed_banner, embed_info, embed_logos], view=view)

async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(chromatica(bot))