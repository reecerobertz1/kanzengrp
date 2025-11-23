import asyncio
import math
import re
import textwrap
import discord
from discord.ext import commands
from random import randint
from typing import Optional, TypedDict, List, Union, Tuple
from PIL import Image, ImageFilter, ImageOps, ImageFont, ImageEnhance, ImageDraw, ImageColor
from io import BytesIO
import functools
from discord import app_commands
from PIL import Image
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

class Customise(discord.ui.View):
    def __init__(self, member: int, bot):
        super().__init__(timeout=60)
        self.member = member
        self.bot = bot
        self.add_item(ConfigSelectMenu(member, bot))

class ConfigSelectMenu(discord.ui.Select):
    def __init__(self, member: int, bot):
        self.member = member
        self.bot = bot

        options = [
            discord.SelectOption(label="Socials", description="Update your socials", emoji="<:CF12:1188186414387568691>"),
            discord.SelectOption(label="About Me", description="Write a short about me (300 characters max)", emoji="<:CF12:1188186414387568691>"),
            discord.SelectOption(label="Styles", description="List your editing styles", emoji="<:CF12:1188186414387568691>"),
            discord.SelectOption(label="Stan List", description="Add your most favourites here! (300 characters max)", emoji="<:CF12:1188186414387568691>"),
            discord.SelectOption(label="Birthday", description="Add your birthday", emoji="<:CF12:1188186414387568691>"),
            discord.SelectOption(label="Favourite Games", description="Add your favourite games", emoji="<:CF12:1188186414387568691>"),
        ]

        super().__init__(placeholder="Choose a profile section to edit", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.member:
            await interaction.response.send_message(
                f"<:whitex:1304222877305798697> **{interaction.user.name}**, You cannot edit someone else's profile.\n"
                f"-# <:thread1:1304222965042249781> Do **/profile** if you'd like to edit your profile.",
                ephemeral=True
            )
            return

        selection = self.values[0]
        if selection == "Socials":
            await interaction.response.send_modal(socials(bot=self.bot))

        elif selection == "About Me":
            await self.get_text_response(interaction, "about me", 300, self.set_card_about)

        elif selection == "Styles":
            await self.get_text_response(interaction, "styles you prefer to do", 50, self.set_card_styles)

        elif selection == "Stan List":
            await self.get_text_response(interaction, "your stan list", 400, self.set_card_stan)

        elif selection == "Birthday":
            await self.get_text_response(interaction, "your birthday (e.g. 21st June)", 50, self.set_card_birthday)

        elif selection == "Favourite Games":
            await self.get_text_response(interaction, "your favourite games", 100, self.set_card_games)

    async def get_text_response(self, interaction, label, max_len, db_func):
        await interaction.response.send_message(
            f'<:settings:1304222799639871530> **{interaction.user.name}**, Please enter {label} (Max: {max_len} characters) within 60 seconds.',
            ephemeral=True
        )

        def check(msg):
            return msg.author.id == self.member and msg.channel == interaction.channel and len(msg.content) <= max_len

        try:
            msg = await self.bot.wait_for("message", timeout=60, check=check)
            await db_func(msg.content, self.member)
            await interaction.followup.send(f"<:check:1291748345194348594> Okay **{interaction.user.name}**, I have updated your profile {label}.", ephemeral=True)
            await msg.delete()
        except asyncio.TimeoutError:
            await interaction.followup.send("You didn't respond in time. Please try again.", ephemeral=True)

    async def set_card_about(self, text: str, member_id: int) -> None:
        query = """UPDATE profiles SET aboutme = $1 WHERE member_id = $2"""
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, text, member_id)

    async def set_card_styles(self, text: str, member_id: int) -> None:
        query = """UPDATE profiles SET styles = $1 WHERE member_id = $2"""
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, text, member_id)

    async def set_card_stan(self, text: str, member_id: int) -> None:
        query = """UPDATE profiles SET stanlist = $1 WHERE member_id = $2"""
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, text, member_id)

    async def set_card_birthday(self, text: str, member_id: int) -> None:
        query = """UPDATE profiles SET birthday = $1 WHERE member_id = $2"""
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, text, member_id)

    async def set_card_games(self, text: str, member_id: int) -> None:
        query = """UPDATE profiles SET games = $1 WHERE member_id = $2"""
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, text, member_id)

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
        circle = Image.open('./assets/circle-mask.png').resize((95, 95)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((95, 95))
        return avatar_image, circle

    def resize_and_crop(self, img: Image.Image, target: tuple[int, int]) -> Image.Image:
        target_w, target_h = target
        aspect = img.width / img.height
        target_aspect = target_w / target_h

        if aspect > target_aspect:
            new_width = int(img.height * target_aspect)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        else:
            new_height = int(img.width / target_aspect)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))

        return img.resize(target)

    async def get_rank_image(self, member_id: int, guild_id: int) -> Optional[Union[str, bytes]]:
        query = '''SELECT image FROM levelling WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id))
                row = await cursor.fetchone()
        if row and row[0]:
            return row[0]
        return None

    async def get_color1(self, member_id: int, guild_id: int):
        query = '''SELECT color FROM levelling WHERE member_id = $1 AND guild_id = $2'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id))
                row = await cursor.fetchone()
            await self.bot.pool.release(conn)

        if row and row['color']:
            color = row['color']
            if color.startswith('#'):
                embed_color = int(color.replace('#', '0x'), 16)
                return embed_color
       
        return 0xc45a72

    async def get_color2(self, member_id: int, guild_id: int):
        query = '''SELECT color2 FROM levelling WHERE member_id = $1 AND guild_id = $2'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id))
                row = await cursor.fetchone()
            await self.bot.pool.release(conn)

        if row and row['color2']:
            color = row['color2']
            if color.startswith('#'):
                embed_color = int(color.replace('#', '0x'), 16)
                return embed_color
       
        return 0xc45a72

    def draw_left_aligned_text(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont,
        *,
        x_left: int,
        y_start: int,
        line_spacing: int = 5,
        fill=(255, 255, 255)
    ):
        """Draws multiline text left-aligned at x_left, starting from y_start."""
        lines = text.split('\n')
        for line in lines:
            bbox = font.getbbox(line)
            text_height = bbox[3] - bbox[1]
            draw.text((x_left, y_start), line, font=font, fill=fill)
            y_start += text_height + line_spacing

    def draw_centered_text(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont,
        *,
        x_center: int,
        y_start: int,
        line_spacing: int = 5,
        fill=(255, 255, 255)
    ):
        """Draw multiline text centered at x_center, starting from y_start."""
        lines = text.split('\n')
        for line in lines:
            bbox = font.getbbox(line)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x_text = x_center - (text_width // 2)
            draw.text((x_text, y_start), line, font=font, fill=fill)
            y_start += text_height + line_spacing

    def get_card(self, avatar: BytesIO, profiles: ProfileRow, user: discord.Member, custom_background, color1, color2) -> BytesIO:
        card = Image.new('RGBA', size=(750, 750), color='grey')

        if custom_background:
            if isinstance(custom_background, (bytes, bytearray)):
                background = Image.open(BytesIO(custom_background))
            elif isinstance(custom_background, str):
                background = Image.open(custom_background)
        else:
            background = Image.open("./assets/rankcard/rankcard.png")

        target_size = (750, 750)
        background = background.convert("RGBA")
        background = self.resize_and_crop(background, target_size)
        box_mask = Image.open('./assets/profiles/box-mask.png').convert("L").resize(target_size)
        bright = ImageEnhance.Brightness(background).enhance(1.3)
        blur = bright.filter(ImageFilter.GaussianBlur(10))
        result = background.copy()
        result.paste(blur, (0, 0), box_mask)
        overlay = Image.open('./assets/profiles/overlay.png').resize(target_size)
        avatar_paste, circle = self.get_avatar(avatar)
        card.paste(result, (0, 0))
        card.paste(overlay, (0, 0), overlay)
        card.paste(avatar_paste, (43, 40), circle)

        draw = ImageDraw.Draw(card, 'RGBA')
        Black = ImageFont.truetype("./fonts/Black.otf", size=25)
        Black2 = ImageFont.truetype("./fonts/Black.otf", size=18)
        Semibold = ImageFont.truetype("./fonts/Semibold.otf", size=20)

        about_me = profiles["aboutme"] or "-"
        stans = profiles["stanlist"] or "-"
        styles = profiles["styles"] or "-"
        instagram = profiles["instagram"] or "-"
        tiktok = profiles["tiktok"] or "-"
        games = profiles["games"] or "-"
        birthday = f'Birthday: {profiles["birthday"]}' or "-"
        joined_at = user.joined_at.strftime("%B %d %Y") if user.joined_at else "-"

        wrapped_styles = "\n".join(textwrap.fill(line, width=30) for line in styles.splitlines())
        wrapped_about_me = "\n".join(textwrap.fill(line, width=35) for line in about_me.splitlines())
        wrapped_stans = "\n".join(textwrap.fill(line, width=35) for line in stans.splitlines())
        wrapped_games = "\n".join(textwrap.fill(line, width=30) for line in games.splitlines())
        wrapped_birthday = "\n".join(textwrap.fill(line, width=50) for line in birthday.splitlines())

        if isinstance(color1, int):
            color1 = ((color1 >> 16) & 255, (color1 >> 8) & 255, color1 & 255)
        if isinstance(color2, int):
            color2 = ((color2 >> 16) & 255, (color2 >> 8) & 255, color2 & 255)

        self.draw_centered_text(draw, wrapped_styles, Semibold, x_center=200, y_start=670, fill=color2)
        self.draw_left_aligned_text(draw, wrapped_about_me, Semibold, x_left=65, y_start=185, fill=color2)
        self.draw_left_aligned_text(draw, wrapped_stans, Semibold, x_left=410, y_start=185, fill=color2)
        self.draw_centered_text(draw, wrapped_games, Semibold, x_center=550, y_start=670, fill=color2)
        self.draw_left_aligned_text(draw, wrapped_birthday, Semibold, x_left=450, y_start=88, fill=color2)

        draw.text((168, 91), instagram, font=Semibold, fill=color2)
        draw.text((273, 91), tiktok, font=Semibold, fill=color2)
        draw.text((145, 60), user.name, font=Black, fill=color1)
        draw.text((152, 163), "About Me", font=Black2, fill=color1)
        draw.text((140, 650), "Editing Styles", font=Black2, fill=color1)
        draw.text((515, 163), "Stan List", font=Black2, fill=color1)
        draw.text((505, 650), "Fave Games", font=Black2, fill=color1)
        draw.text((427, 58), f"Joined Chroma: {joined_at}", font=Semibold, fill=color2)

        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def generate_card(self, avatar: BytesIO, profiles: ProfileRow, member: discord.Member) -> BytesIO:
        custom_background_url = await self.get_rank_image(member.id, member.guild.id)
        custom_background = None
        color1 = await self.get_color1(member.id, member.guild.id)
        color2 = await self.get_color2(member.id, member.guild.id)

        if custom_background_url and isinstance(custom_background_url, str) and custom_background_url.startswith("http"):
            async with self.bot.session.get(custom_background_url) as resp:
                custom_background = await resp.read()
        else:
            custom_background = custom_background_url

        loop = asyncio.get_running_loop()
        card = await loop.run_in_executor(
            None,
            functools.partial(self.get_card, avatar, profiles, member, custom_background, color1, color2)
        )
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

        if card:
            if member == interaction.user:
                view=Customise(member=member.id, bot=self.bot)
                await interaction.response.send_message(
                    file=discord.File(card, 'card.png'),
                    view=view
                )
            else:
                instagram = discord.ui.Button(label="Instagram", url=f"https://www.instagram.com/{profiles['instagram']}")
                tiktok = discord.ui.Button(label="TikTok", url=f"https://www.tiktok.com/@{profiles['tiktok']}")
                view=discord.ui.View()
                view.add_item(instagram)
                view.add_item(tiktok)
                await interaction.response.send_message(file=discord.File(card, 'card.png'), view=view)
        else:
            await self.add_member(member.id)
            await interaction.response.send_message(
                f"{member} hasn't set up their profile yet...\n"
                f"If this is your profile, use the buttons below to set up now!",
                view=Customise(member=member.id, bot=self.bot)
            )

async def setup(bot):
    await bot.add_cog(profiles(bot))