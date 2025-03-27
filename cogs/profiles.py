import asyncio
import math
import re
import discord
from discord.ext import commands
from random import randint
from typing import Optional, TypedDict, List, Union, Tuple
from PIL import Image, ImageFilter, ImageOps, ImageFont, ImageEnhance, ImageDraw, ImageColor
from io import BytesIO
import functools
from discord import app_commands
from PIL import Image
from stuff.views import Paginator
from colorthief import ColorThief
from discord.app_commands import CommandOnCooldown
from datetime import datetime
import logging
from textwrap import TextWrapper
logger = logging.getLogger("discord")

class ProfileRow(TypedDict):
    member_id: int
    aboutme: str
    stanlist: str
    styles: str
    background: str
    banner: str
    instagram: str
    tiktok: str

class configprofilecard(discord.ui.View):
    def __init__(self, member, bot):
        super().__init__(timeout=60)
        self.member = member
        self.bot = bot
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$"

    @discord.ui.button(label="Banner", row=2)
    async def banner(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.member:
            await interaction.response.send_message(
                f"<:settings:1304222799639871530>**{interaction.user.name}**, Please upload an image for your profile within the next 60 seconds.\n"
                f"-# <:thread2:1304222916879323136> The image size is **750x250**\n"
                f"-# <:thread2:1304222916879323136> Please make sure your image file is a **PNG / JPEG**\n"
                f"-# <:thread1:1304222965042249781> The file cannot be a **GIF, PDF or Video**",
                ephemeral=True
            )

            def check(msg):
                return (
                    msg.author == interaction.user 
                    and msg.channel == interaction.channel 
                    and (msg.attachments or (msg.content.startswith("http://") or msg.content.startswith("https://")))
                )
            try:
                msg = await self.bot.wait_for("message", timeout=60, check=check)
                image_data = None
                if msg.attachments:
                    attachment = msg.attachments[0]
                    if attachment.content_type.split("/")[0] == "image" and not attachment.content_type.split("/")[1] == "gif":
                        async with self.bot.session.get(attachment.url) as resp:
                            image_data = BytesIO(await resp.read())
                            image_data.seek(0)
                    else:
                        return await interaction.followup.send("Invalid image. Please try again with a valid image format.", ephemeral=True)
                else:
                    url = msg.content
                    async with self.bot.session.get(url) as resp:
                        if resp.headers.get('content-type').split("/")[0] == "image" and not resp.headers.get('content-type').split("/")[1] == "gif":
                            image_data = BytesIO(await resp.read())
                            image_data.seek(0)
                        else:
                            return await interaction.followup.send("Invalid image URL. Please try again with a valid image format.", ephemeral=True)

                await self.set_card_banner(image_data, interaction.user.id)
                await interaction.followup.send(f"<:check:1291748345194348594> Okay **{interaction.user.name}**, I have update your profile image", ephemeral=True)
                await msg.delete()

            except asyncio.TimeoutError:
                await interaction.followup.send("You didn't upload an image in time. Please try again.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"<:whitex:1304222877305798697>**{interaction.user.name}**, You cannot edit someone else's profile.\n"
                f"-# <:thread1:1304222965042249781> Do **/profile** if you'd like to edit your profile.",
                ephemeral=True,
            )

    @discord.ui.button(label="Socials", row=2)
    async def socials(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.member:
            await interaction.response.send_modal(socials(bot=self.bot))
        else:
            await interaction.response.send_message(f"<:whitex:1304222877305798697>**{interaction.user.name}**, You cannot edit someone else's profile.\n-# <:thread1:1304222965042249781> Do **/profile** if you'd like to edit your profile.", ephemeral=True)

    @discord.ui.button(label="Background", row=2)
    async def background(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.member:
            await interaction.response.send_message(
                f"<:settings:1304222799639871530>**{interaction.user.name}**, Please upload an image for your profile within the next 60 seconds.\n"
                f"-# <:thread2:1304222916879323136> The image size is **750x750**\n"
                f"-# <:thread2:1304222916879323136> Please make sure your image file is a **PNG / JPEG**\n"
                f"-# <:thread1:1304222965042249781> The file cannot be a **GIF, PDF or Video**",
                ephemeral=True
            )

            def check(msg):
                return (
                    msg.author == interaction.user 
                    and msg.channel == interaction.channel 
                    and (msg.attachments or (msg.content.startswith("http://") or msg.content.startswith("https://")))
                )
            try:
                msg = await self.bot.wait_for("message", timeout=60, check=check)
                image_data = None
                if msg.attachments:
                    attachment = msg.attachments[0]
                    if attachment.content_type.split("/")[0] == "image" and not attachment.content_type.split("/")[1] == "gif":
                        async with self.bot.session.get(attachment.url) as resp:
                            image_data = BytesIO(await resp.read())
                            image_data.seek(0)
                    else:
                        return await interaction.followup.send("Invalid image. Please try again with a valid image format.", ephemeral=True)
                else:
                    url = msg.content
                    async with self.bot.session.get(url) as resp:
                        if resp.headers.get('content-type').split("/")[0] == "image" and not resp.headers.get('content-type').split("/")[1] == "gif":
                            image_data = BytesIO(await resp.read())
                            image_data.seek(0)
                        else:
                            return await interaction.followup.send("Invalid image URL. Please try again with a valid image format.", ephemeral=True)

                await self.set_card_background(image_data, interaction.user.id)
                await interaction.followup.send(f"<:check:1291748345194348594> Okay **{interaction.user.name}**, I have update your profile image", ephemeral=True)
                await msg.delete()

            except asyncio.TimeoutError:
                await interaction.followup.send("You didn't upload an image in time. Please try again.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"<:whitex:1304222877305798697>**{interaction.user.name}**, You cannot edit someone else's profile.\n"
                f"-# <:thread1:1304222965042249781> Do **/profile** if you'd like to edit your profile.",
                ephemeral=True,
            )

    @discord.ui.button(label="About Me")
    async def about(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.member:
            await interaction.response.send_message(
                f'<:settings:1304222799639871530>**{interaction.user.name}**, Please enter a short text description about yourself for your "About Me" within the next 60 seconds. (Max: 300 characters)',
                ephemeral=True
            )

            def check(msg):
                return msg.author == interaction.user and msg.channel == interaction.channel and len(msg.content) <= 300

            try:
                msg = await self.bot.wait_for("message", timeout=60, check=check)
                about_text = msg.content

                await self.set_card_about(about_text, interaction.user.id)
                await interaction.followup.send(f"<:check:1291748345194348594> Okay **{interaction.user.name}**, I have updated your profile about me.", ephemeral=True)
                await msg.delete()
            
            except asyncio.TimeoutError:
                await interaction.followup.send("You didn't provide text in time. Please try again.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"<:whitex:1304222877305798697>**{interaction.user.name}**, You cannot edit someone else's profile.\n"
                f"-# <:thread1:1304222965042249781> Do **/profile** if you'd like to edit your profile.",
                ephemeral=True,
            )

    @discord.ui.button(label="Styles")
    async def styles(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.member:
            await interaction.response.send_message(
                f'<:settings:1304222799639871530>**{interaction.user.name}**, Please enter a short list of styles you prefer to do within the next 60 seconds. (Max: 50 characters)',
                ephemeral=True
            )

            def check(msg):
                return msg.author == interaction.user and msg.channel == interaction.channel and len(msg.content) <= 50

            try:
                msg = await self.bot.wait_for("message", timeout=60, check=check)
                about_text = msg.content

                await self.set_card_styles(about_text, interaction.user.id)
                await interaction.followup.send(f"<:check:1291748345194348594> Okay **{interaction.user.name}**, I have updated your profile styles.", ephemeral=True)
                await msg.delete()
            
            except asyncio.TimeoutError:
                await interaction.followup.send("You didn't provide text in time. Please try again.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"<:whitex:1304222877305798697>**{interaction.user.name}**, You cannot edit someone else's profile.\n"
                f"-# <:thread1:1304222965042249781> Do **/profile** if you'd like to edit your profile.",
                ephemeral=True,
            )

    @discord.ui.button(label="Stan List")
    async def stan(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.member:
            await interaction.response.send_message(
                f'<:settings:1304222799639871530>**{interaction.user.name}**, Please enter a short list of your stans within the next 60 seconds. (Max: 300 characters)',
                ephemeral=True
            )

            def check(msg):
                return msg.author == interaction.user and msg.channel == interaction.channel and len(msg.content) <= 300

            try:
                msg = await self.bot.wait_for("message", timeout=60, check=check)
                about_text = msg.content

                await self.set_card_stan(about_text, interaction.user.id)
                await interaction.followup.send(f"<:check:1291748345194348594> Okay **{interaction.user.name}**, I have updated your profile stan list.", ephemeral=True)
                await msg.delete()
            
            except asyncio.TimeoutError:
                await interaction.followup.send("You didn't provide text in time. Please try again.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"<:whitex:1304222877305798697>**{interaction.user.name}**, You cannot edit someone else's profile.\n"
                f"-# <:thread1:1304222965042249781> Do **/profile** if you'd like to edit your profile.",
                ephemeral=True,
            )

    async def set_card_stan(self, about_text: str, member_id: int) -> None:
        query = """UPDATE profiles SET stanlist = $1 WHERE member_id = $2"""
        
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, about_text, member_id)

    async def set_card_styles(self, about_text: str, member_id: int) -> None:
        query = """UPDATE profiles SET styles = $1 WHERE member_id = $2"""
        
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, about_text, member_id)

    async def set_card_about(self, about_text: str, member_id: int) -> None:
        query = """UPDATE profiles SET aboutme = $1 WHERE member_id = $2"""
        
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, about_text, member_id)

    async def set_card_banner(self, banner: BytesIO, member_id: int) -> None:
        query = """UPDATE profiles SET banner = $1 WHERE member_id = $2"""

        bytes_data = banner.getvalue()
        banner.seek(0)
        
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, bytes_data, member_id)

    async def set_card_background(self, background: BytesIO, member_id: int) -> None:
        query = """UPDATE profiles SET background = $1 WHERE member_id = $2"""

        bytes_data = background.getvalue()
        background.seek(0)

        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, bytes_data, member_id)

class socials(discord.ui.Modal, title='Update socials'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    instagram = discord.ui.TextInput(label="What is your Instagram?", placeholder="Enter here", style=discord.TextStyle.short)
    tiktok = discord.ui.TextInput(label="What is you TikTok?", placeholder="Enter here...", style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        if self.instagram.value:
            await self.update_card_instagram(member_id=interaction.user.id, about_text=self.instagram.value)
        if self.instagram.value:
            await self.update_card_tiktok(member_id=interaction.user.id, about_text=self.tiktok.value)
        await interaction.response.send_message(f'I have updated your social media on your profile!', ephemeral=True)

    async def update_card_instagram(self, about_text: str, member_id: int) -> None:
        query = """UPDATE profiles SET instagram = $1 WHERE member_id = $2"""
        
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, about_text, member_id)

    async def update_card_tiktok(self, about_text: str, member_id: int) -> None:
        query = """UPDATE profiles SET tiktok = $1 WHERE member_id = $2"""
        
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, about_text, member_id)

class profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = None

    async def add_member(self, member_id: int) -> None:
        query = '''INSERT INTO profiles (member_id) VALUES (?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    def get_avatar(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        circle = Image.open('./assets/circle-mask.png').resize((223, 223)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((223, 223))
        return avatar_image, circle

    def get_card(self, avatar: BytesIO, profiles: ProfileRow, user: discord.User) -> BytesIO:
        card = Image.new('RGBA', size=(750, 750), color='grey')
        if profiles['banner'] is not None:
            bg = Image.open(BytesIO(profiles["banner"]))
        else:
            bg = Image.open("./assets/profilebanner.png")

        if profiles['background'] is not None:
            background = Image.open(BytesIO(profiles["background"]))
        else:
            background = Image.open("./assets/profilebg.png")

        target_width, target_height = 750, 250
        bg_aspect_ratio = bg.width / bg.height
        target_aspect_ratio = target_width / target_height
        
        if bg_aspect_ratio > target_aspect_ratio:
            new_width = int(bg.height * target_aspect_ratio)
            left = (bg.width - new_width) // 2
            right = left + new_width
            top = 0
            bottom = bg.height
        else:
            new_height = int(bg.width / target_aspect_ratio)
            top = (bg.height - new_height) // 2
            bottom = top + new_height
            left = 0
            right = bg.width

        bg = bg.crop((left, top, right, bottom))
        bg = bg.resize((750, 250))
        banner_mask = Image.open('./assets/banner-mask.png').convert('L').resize((750, 250))
        bg.putalpha(banner_mask)
        card.paste(background, (0, 0))
        card.paste(bg, (0, 0), bg)
        avatar_paste, circle = self.get_avatar(avatar)
        card.paste(avatar_paste, (68, 132), circle)
        socials = Image.open('./assets/socials.png').resize((750, 750))
        card.paste(socials, (0, 0), socials)
        aboutstan = Image.open('./assets/about-stan.png').resize((750, 750))
        card.paste(aboutstan, (0, 0), aboutstan)
        styles = Image.open('./assets/styles.png').resize((750, 750))
        card.paste(styles, (0, 0), styles)
        draw = ImageDraw.Draw(card, 'RGBA')
        Coolvetica = ImageFont.truetype("./fonts/Coolvetica Rg.otf", size=45)
        Coolvetica2 = ImageFont.truetype("./fonts/Coolvetica Rg.otf", size=25)
        Coolvetica3 = ImageFont.truetype("./fonts/Coolvetica Rg.otf", size=20)

        if profiles["aboutme"]  is not None:
            about_me = profiles["aboutme"]
        else:
            about_me = "No about me set."

        if profiles["stanlist"]  is not None:
            stans = profiles["stanlist"]
        else:
            stans = "No stan list set."

        if profiles["styles"]  is not None:
            styles = profiles["styles"]
        else:
            styles = "No styles set."

        if profiles["instagram"]  is not None:
            instagram = profiles["instagram"]
        else:
            instagram = "Instagram."

        if profiles["tiktok"]  is not None:
            tiktok = profiles["tiktok"]
        else:
            tiktok = "TikTok."

        wrapper = TextWrapper(width=33)
        wrapped_about_me = wrapper.fill(about_me)
        wrapped_stans = wrapper.fill(stans)

        draw.text((65, 430), wrapped_about_me, font=Coolvetica3)
        draw.text((420, 430), wrapped_stans, font=Coolvetica3)
        draw.text((322, 292), styles, font=Coolvetica3)
        draw.text((350, 215), instagram, font=Coolvetica2)
        draw.text((575, 215), tiktok, font=Coolvetica2)
        draw.text((65, 15), user.display_name, font=Coolvetica2)
        
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def generate_card(self, avatar: BytesIO, profiles: ProfileRow, member: discord.Member) -> BytesIO:
        card_generator = functools.partial(self.get_card, avatar, profiles, member)
        card = await self.bot.loop.run_in_executor(None, self.get_card, avatar, profiles, member)
        return card

    async def get_member_profiles(self, member_id: int) -> Optional[ProfileRow]:
        query = '''SELECT * from profiles WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id))
                row = await cursor.fetchone()
                if row:
                    return row
                else:
                    return None

    @app_commands.command(name="profile", description="View a chromies profile")
    async def profile(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        member = member or interaction.user
        profiles = await self.get_member_profiles(member.id)
        avatar_url = member.display_avatar.replace(static_format='png', size=256).url
        response = await self.bot.session.get(avatar_url)
        avatar = BytesIO(await response.read())
        avatar.seek(0)
        if profiles:
                card = await self.generate_card(avatar, profiles, member)
        else:
            card = None
        if member == interaction.user:
            if card:
                await interaction.response.send_message(file=discord.File(card, 'card.png'), view=configprofilecard(member=member.id, bot=self.bot))
        if member == member:
            await interaction.response.send_message(file=discord.File(card, 'card.png'))
        else:
            await self.add_member(member.id)
            await interaction.response.send_message(f"{member} hasn't setup their profile yet...\nIf this is your profile, use the buttons below to setup now!", view=configprofilecard(member=member.id, bot=self.bot))

async def setup(bot):
    await bot.add_cog(profiles(bot))