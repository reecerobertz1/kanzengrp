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

class misc(commands.Cog):
    """Miscellaneous Commands"""
    def __init__(self, bot):
        self.bot = bot
        self.db = None
        self.bot.loop.create_task(self.initialize_database())

    async def initialize_database(self):
        self.db = await asqlite.connect("levels.db")
        async with self.db.cursor() as cursor:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS profiles (
                    user_id INTEGER PRIMARY KEY,
                    about_me TEXT,
                    instagram_username TEXT,
                    pronouns TEXT,
                    banner_url TEXT,
                    background_url TEXT
                )
            ''')

    @commands.command(aliases=['be', 'embed'], description="Build an embed")
    async def buildembed(self, ctx: commands.Context):
        """Embed Generator With Default Embed And Author Check So Only The Invoker Can Use The Editor"""
        view = EmbedCreator(bot=self.bot)
        async def check(interaction: discord.Interaction):
                if interaction.user.id == ctx.author.id:
                    return True
                else:
                    await interaction.response.send_message(f"Only {ctx.author} can use this interaction!", ephemeral=True)
                    return False
        view.interaction_check = check
        await ctx.send(embed=view.get_default_embed, view=view)

    @commands.command(aliases=["hoshiinfo", "about"], description="Information about Hoshi")
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

    @commands.command(description="Get the server information")
    async def serverinfo(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(title=f"Server Information for the server {ctx.guild.name}", color=0x2b2d31)
            embed.set_thumbnail(url=ctx.guild.icon)
            embed.set_image(url=ctx.guild.banner)
            embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
            embed.add_field(name="Server Owner", value=ctx.guild.owner, inline=True)
            embed.add_field(name="Member Count", value=ctx.guild.member_count, inline=True)
            embed.add_field(name="Channel Count", value=len(ctx.guild.channels), inline=True)
            embed.add_field(name="Role Count", value=len(ctx.guild.roles), inline=True)
            embed.add_field(name="Boost Count", value=ctx.guild.premium_subscription_count, inline=True)
            embed.add_field(name="Boost Tier", value=ctx.guild.premium_tier, inline=True)
            embed.add_field(name="Creation Date", value=ctx.guild.created_at.__format__("%D"), inline=True)
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
            embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
            await ctx.reply(embed=embed)

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

    @commands.command(description="Get the image link for an emoji")
    async def emoji(self, ctx, emoji: discord.Emoji):
        emoji_url = emoji.url
        await ctx.send(f"Here's the image for the emoji {emoji.name}: {emoji_url}")

    @commands.command(aliases=['pfp', 'icon'], description="Get someone's discord avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        avatar_url = member.display_avatar.url
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url=avatar_url)
        button = discord.ui.Button(label="Download", url=avatar_url, emoji="⬇")
        view = discord.ui.View()
        view.add_item(button)
        await ctx.reply(embed=embed, view=view)

    @commands.command(description="See someone's member profile!")
    async def profile(self, ctx, user: Optional[discord.Member] = None):
        async with ctx.typing():
            if user is None:
                user = ctx.author

            display = user.display_name
            sheher = discord.utils.find(lambda r: r.name == 'she/her', ctx.message.guild.roles)
            theythem = discord.utils.find(lambda r: r.name == 'they/them', ctx.message.guild.roles)
            shethey = discord.utils.find(lambda r: r.name == 'she/they', ctx.message.guild.roles)
            hethey = discord.utils.find(lambda r: r.name == 'he/they', ctx.message.guild.roles)
            hehim = discord.utils.find(lambda r: r.name == 'he/him', ctx.message.guild.roles)
            any = discord.utils.find(lambda r: r.name == 'any / ask', ctx.message.guild.roles)
            ae = discord.utils.find(lambda r: r.name == 'after effects', ctx.message.guild.roles)
            vs = discord.utils.find(lambda r: r.name == 'videostar', ctx.message.guild.roles)
            am = discord.utils.find(lambda r: r.name == 'alight motion', ctx.message.guild.roles)
            cutecut = discord.utils.find(lambda r: r.name == 'cute cut', ctx.message.guild.roles)
            fm = discord.utils.find(lambda r: r.name == 'funimate', ctx.message.guild.roles)
            cc = discord.utils.find(lambda r: r.name == 'capcut', ctx.message.guild.roles)
            sony = discord.utils.find(lambda r: r.name == 'sony vegas', ctx.message.guild.roles)
            lead = discord.utils.find(lambda r: r.name == 'lead', ctx.message.guild.roles)
            leads = discord.utils.find(lambda r: r.name == 'leads', ctx.message.guild.roles)
            Hoshi = discord.utils.find(lambda r: r.name == 'Hoshi', ctx.message.guild.roles)
            zennies = discord.utils.find(lambda r: r.name == 'zennies', ctx.message.guild.roles)
            staff = discord.utils.find(lambda r: r.name == 'staff', ctx.message.guild.roles)
            members = discord.utils.find(lambda r: r.name == 'members', ctx.message.guild.roles)

            if ae in user.roles:
                program = "after effects"
            elif cutecut in user.roles:
                program = "cute cut pro"
            elif sony in user.roles:
                program = "sony vegas"
            elif vs in user.roles:
                program = "videostar"
            elif cc in user.roles:
                program = "cap cut"
            elif fm in user.roles:
                program = "funimate"
            elif am in user.roles:
                program = "alight motion"
            else:
                program = "an unspecified editing software"

            if lead in user.roles:
                title = "a Kanzen lead"
            elif leads in user.roles:
                title = "an Aura lead"
            elif staff in user.roles:
                title = "a Kanzen staff member"
            elif zennies in user.roles:
                title = "a Kanzen member"
            elif members in user.roles:
                title = "an Aura member"
            elif Hoshi in user.roles:
                title = "Reece's son"

            if sheher in user.roles:
                prns = "she/her"
                prn1 = "she uses"
                prn2 = "her"
                prn3 = "she is"
            elif hehim in user.roles:
                prns = "he/him"
                prn1 = "he uses"
                prn2 = "his"
                prn3 = "he is"
            elif shethey in user.roles:
                prns = "she/they"
                prn1 = "they use"
                prn2 = "her"
                prn3 = "they are"
            elif hethey in user.roles:
                prns = "he/they"
                prn1 = "they use"
                prn2 = "his"
                prn3 = "they are"
            elif theythem in user.roles:
                prns = "they/them"
                prn1 = "they use"
                prn2 = "their"
                prn3 = "they are"
            elif any in user.roles:
                prns = "any pronouns"
                prn1 = "they use"
                prn2 = "their"
                prn3 = "they are"
            else:
                prns = "not specified"
                prn1 = "they use"
                prn2 = "their"
                prn3 = "they are"

            user_id = ctx.author.id
            async with self.db.cursor() as cursor:
                await cursor.execute('SELECT about_me, instagram_username, pronouns, banner_url, background_url FROM profiles WHERE user_id = ?', (user_id,))
                profile_data = await cursor.fetchone()

            if profile_data:
                about_me, instagram_username, pronouns, banner_url, background_url = profile_data
                image = Image.new("RGBA", (1080, 1080), (255, 255, 255, 255))

                if background_url:
                    background_response = requests.get(background_url)
                    background_image = Image.open(io.BytesIO(background_response.content))
                    background_image = background_image.crop((0, 0, 1080, 1080))
                    background_mask = Image.open('./assets/background_mask.png').convert("L")
                    background_mask = background_mask.crop((0, 0, 1080, 1080))
                    masked_background = Image.new("RGBA", (1080, 1080), (255, 255, 255, 255))
                    masked_background.paste(background_image, (0, 0), background_mask)
                    image.paste(masked_background, (0, 0))

                if banner_url:
                    banner_response = requests.get(banner_url)
                    banner_image = Image.open(io.BytesIO(banner_response.content))
                    banner_image = banner_image.crop((0, 0, 1080, 390))
                    banner_mask = Image.open('./assets/banner_mask.png').convert("L")
                    banner_mask = banner_mask.crop((0, 0, 1080, 390))
                    masked_banner = Image.new("RGBA", (1080, 390), (255, 255, 255, 255))
                    masked_banner.paste(banner_image, (0, 0), banner_mask)
                    image.paste(masked_banner, (0, 0))

                user_avatar_url = ctx.author.display_avatar.url
                user_avatar_response = requests.get(user_avatar_url)
                user_avatar_image = Image.open(io.BytesIO(user_avatar_response.content))
                user_avatar_image = user_avatar_image.resize((265, 265))
                user_avatar_image = user_avatar_image.convert("RGBA")
                circle_mask = Image.new("L", (265, 265))
                draw = ImageDraw.Draw(circle_mask)
                draw.ellipse((0, 0, 265, 265), fill=255)
                user_avatar_image.putalpha(circle_mask)
                image.paste(user_avatar_image, (121, 233), user_avatar_image)

                textbox_path = './assets/textbox.png'
                textbox_image = Image.open(textbox_path)
                image.paste(textbox_image, (0, 0), textbox_image)

                draw = ImageDraw.Draw(image)
                poppins = Font.poppins(size=43)
                font2 = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 65)
                font4 = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 35)

                about_me_lines = textwrap.wrap(about_me, 47)
                about_me_text = "\n".join(about_me_lines)

                draw.text((417, 292), display, '#000000', font=font2)
                draw.text((415, 290), display, '#ffffff', font=font2)
                draw.text((60, 720), about_me_text, '#ffffff', font=font)
                draw.text((450, 460), f"{prn1} the pronouns {prns}\n{prn3} {title}\n{prn2} edit on {program}", '#ffffff', font=font)
                draw.text((470, 680), "About Me", fill=(255, 255, 255), font=font4)
                draw.text((640, 410), "Extra Info", fill=(255, 255, 255), font=font4)

                image.save("profile_image.png")
                if "|" in display:
                    list = display.split("|")
                    name1 = list[0]
                    name = name1.replace(" ", "")
                    username = list[1]
                    acc = username.replace(" ", "")
                    button = discord.ui.Button(label=f"Click here to go to {prn2} Instagram", url=f"https://instagram.com/{acc}")
                    view = discord.ui.View()
                    view.add_item(button)
                    await ctx.send(file=discord.File("profile_image.png"), view=view)
                else:
                    await ctx.send("You haven't set up your profile yet!")

    @commands.command(description="Set your profile about me")
    async def aboutme(self, ctx, about_me: str):
        user_id = ctx.author.id
        async with self.db.cursor() as cursor:
            await cursor.execute('SELECT about_me, banner_url, background_url FROM profiles WHERE user_id = ?', (user_id,))
            existing_profile_data = await cursor.fetchone()

        if existing_profile_data:
            existing_about_me, banner_url, background_url = existing_profile_data
            if about_me:
                existing_about_me = about_me
            async with self.db.cursor() as cursor:
                await cursor.execute('''
                    UPDATE profiles
                    SET about_me = ?
                    WHERE user_id = ?
                ''', (existing_about_me, user_id))
                await self.db.commit()

            await ctx.send("Your profile information has been updated!")
        else:
            async with self.db.cursor() as cursor:
                await cursor.execute('''
                    INSERT INTO profiles (user_id, about_me)
                    VALUES (?, ?)
                ''', (user_id, about_me))
                await self.db.commit()

            await ctx.send("Your profile information has been set!")

    @commands.command(description="Set your profile banner")
    async def profilebanner(self, ctx):
        user_id = ctx.author.id
        if len(ctx.message.attachments) > 0:
            banner_url = ctx.message.attachments[0].url
            async with self.db.cursor() as cursor:
                await cursor.execute('SELECT about_me, instagram_username, pronouns, background_url FROM profiles WHERE user_id = ?', (user_id,))
                existing_data = await cursor.fetchone()

            if existing_data:
                about_me, instagram_username, pronouns, background_url = existing_data
            else:
                about_me, instagram_username, pronouns, background_url = None, None, None, None

            async with self.db.cursor() as cursor:
                await cursor.execute('''
                    INSERT OR REPLACE INTO profiles (user_id, about_me, instagram_username, pronouns, banner_url, background_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, about_me, instagram_username, pronouns, banner_url, background_url))
                await self.db.commit()
            await ctx.send("Your profile banner has been updated!")


    @commands.command(description="Set your profile background")
    async def profilebg(self, ctx):
        user_id = ctx.author.id
        if len(ctx.message.attachments) > 0:
            background_url = ctx.message.attachments[0].url
            async with self.db.cursor() as cursor:
                await cursor.execute('SELECT about_me, instagram_username, pronouns, banner_url FROM profiles WHERE user_id = ?', (user_id,))
                existing_data = await cursor.fetchone()

            if existing_data:
                about_me, instagram_username, pronouns, banner_url = existing_data
            else:
                about_me, instagram_username, pronouns, banner_url = None, None, None, None

            async with self.db.cursor() as cursor:
                await cursor.execute('''
                    INSERT OR REPLACE INTO profiles (user_id, about_me, instagram_username, pronouns, banner_url, background_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, about_me, instagram_username, pronouns, banner_url, background_url))
                await self.db.commit()
            await ctx.send("Your profile background has been updated!")

async def setup(bot):
    await bot.add_cog(misc(bot))