import asyncio
from random import randint, random
import re
import textwrap
import discord
import discord.backoff
from discord.ext import commands, tasks
from typing import Optional, TypedDict, List, Union, Tuple
from PIL import Image, ImageFilter, ImageOps, ImageFont, ImageEnhance, ImageDraw, ImageColor, ImageChops
from io import BytesIO
import functools
from discord import app_commands
from PIL import Image
from utils.views import Paginator
from colorthief import ColorThief
import datetime as dt
from datetime import datetime, timedelta

class LevelRow(TypedDict):
    guild_id: int
    member_id: int
    xp: int
    messages: int
    color: str
    color2: str
    image: str

class RankCardConfig(discord.ui.View):
    def __init__(self, member, bot):
        super().__init__(timeout=60)
        self.member = member
        self.bot = bot
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$"

    async def _check_user(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.member:
            await interaction.response.send_message(
                f"<:whitex:1304222877305798697> You cannot edit someone else's rank card.\n"
                f"-# <:thread1:1304222965042249781> Do **/rank** to edit your own card.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="Background Image", style=discord.ButtonStyle.secondary)
    async def image_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self._check_user(interaction):
            return
        booster_role_id = 728684846846574703
        extra_role_id = 1462092462292992094
        has_booster = any(role.id == booster_role_id for role in interaction.user.roles)
        has_extra = any(role.id == extra_role_id for role in interaction.user.roles)
        can_upload_gif = has_booster or has_extra
        allowed_types = "PNG, JPEG, or GIF" if can_upload_gif else "PNG or JPEG only — no GIFs, PDFs, or videos."
        await interaction.response.send_message(
            f"<:settings:1304222799639871530>**{interaction.user.name}**, Please upload an image for your rank card within 60 seconds.\n"
            f"- {allowed_types}\n"
            f"- You can upload an image or paste a direct image/GIF URL (e.g. from Tenor, Giphy, Imgur, etc.)",
            ephemeral=True
        )

        def check(msg):
            return (
                msg.author == interaction.user
                and msg.channel == interaction.channel
                and (msg.attachments or msg.content.startswith(("http://", "https://")))
            )

        try:
            msg = await self.bot.wait_for("message", timeout=60, check=check)
            image_data = None

            if msg.attachments:
                attachment = msg.attachments[0]
                filename = attachment.filename.lower()
                is_gif = filename.endswith(".gif")
                print(f"DEBUG: CanUploadGIF={can_upload_gif}, Filename={filename}, is_gif={is_gif}")
                if not can_upload_gif and is_gif:
                    return await interaction.followup.send("GIFs are only allowed for boosters.", ephemeral=True)
                valid_exts = (".png", ".jpg", ".jpeg", ".gif") if can_upload_gif else (".png", ".jpg", ".jpeg")
                if not filename.endswith(valid_exts):
                    return await interaction.followup.send(
                        f"Invalid image format. {'You can use GIFs.' if can_upload_gif else 'Try PNG or JPEG.'}",
                        ephemeral=True
                    )
                async with self.bot.session.get(attachment.url) as resp:
                    image_data = BytesIO(await resp.read())
                    image_data.seek(0)
            elif msg.content.startswith(("http://", "https://")):
                url = msg.content.strip()
                if "tenor.com/view/" in url:
                    async with self.bot.session.get(url) as page_resp:
                        html = await page_resp.text()
                    match = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+\.gif)["\']', html)
                    if not match:
                        match = re.search(r'(https://media\.tenor\.com/[^"\s]+\.gif)', html)
                    if not match:
                        return await interaction.followup.send("Could not find a GIF on that Tenor page.", ephemeral=True)
                    direct_gif_url = match.group(1)
                    url = direct_gif_url
                async with self.bot.session.get(url) as resp:
                    content_type = resp.headers.get("Content-Type", "").lower()
                    allowed_types_gif = ["image/png", "image/jpeg", "image/gif"]
                    allowed_types_no_gif = ["image/png", "image/jpeg"]
                    is_gif = "image/gif" in content_type
                    if not can_upload_gif and is_gif:
                        return await interaction.followup.send("GIFs are only allowed for boosters.", ephemeral=True)
                    if (can_upload_gif and content_type not in allowed_types_gif) or (not can_upload_gif and content_type not in allowed_types_no_gif):
                        return await interaction.followup.send(
                            f"Invalid image URL. {'You can use GIFs.' if can_upload_gif else 'Try PNG or JPEG.'}",
                            ephemeral=True
                        )
                    image_data = BytesIO(await resp.read())
                    image_data.seek(0)

            await self.set_card_image(image_data, interaction.user.id, interaction.guild.id)
            await interaction.followup.send(f"<:check:1291748345194348594> Updated your rank card image.", ephemeral=True)
            await msg.delete()

        except asyncio.TimeoutError:
            await interaction.followup.send("You didn't upload an image in time.", ephemeral=True)

    @discord.ui.button(label="Title Colour", style=discord.ButtonStyle.secondary)
    async def color1_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self._check_user(interaction):
            return
        await interaction.response.send_message(
            f"<:settings:1304222799639871530>**{interaction.user.name}**, Please type a valid hex code within 60 seconds.\n"
            f"- Example: `#c45a72` ([color picker](https://htmlcolorcodes.com/))",
            ephemeral=True
        )

        def check(m): return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=60.0, check=check)
            color = msg.content.strip()
            if re.fullmatch(self.regex_hex, color):
                await self.set_rank_color1(interaction.user.id, color, interaction.guild.id)
                await interaction.followup.send(f"<:check:1291748345194348594> Updated Title Colour to **{color}**", ephemeral=True)
                await msg.delete()
            else:
                await interaction.followup.send("Invalid hex code. Must start with `#` and be 6 characters.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to respond.", ephemeral=True)

    @discord.ui.button(label="Text Colour", style=discord.ButtonStyle.secondary)
    async def color2_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self._check_user(interaction):
            return
        await interaction.response.send_message(
            f"<:settings:1304222799639871530>**{interaction.user.name}**, Please type a valid hex code within 60 seconds.\n"
            f"- Example: `#c45a72` ([color picker](https://htmlcolorcodes.com/))",
            ephemeral=True
        )

        def check(m): return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=60.0, check=check)
            color = msg.content.strip()
            if re.fullmatch(self.regex_hex, color):
                await self.set_rank_color2(interaction.user.id, color, interaction.guild.id)
                await interaction.followup.send(f"<:check:1291748345194348594> Updated Text Colour to **{color}**", ephemeral=True)
                await msg.delete()
            else:
                await interaction.followup.send("Invalid hex code. Must start with `#` and be 6 characters.", ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to respond.", ephemeral=True)

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

    async def set_rank_color1(self, member_id: int, color: str, guild_id: int) -> None:
        query = '''UPDATE levelling SET color = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, color, member_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_rank_color2(self, member_id: int, color: str, guild_id: int) -> None:
        query = '''UPDATE levelling SET color2 = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, color, member_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_card_image(self, image: BytesIO, member_id: int, guild_id: int, colorchange: Optional[bool] = False) -> None:
        if not colorchange:
            query = """UPDATE levelling SET image = $1, color = $2 WHERE member_id = $3 AND guild_id = $4"""
        else:
            query = """UPDATE levelling SET image = $1, accent_color = $2, color = $3 WHERE member_id = $4 AND guild_id = $5"""

        bytes_data = image.getvalue()
        image.seek(0)
        ct = ColorThief(image)
        pb_colors = ct.get_palette(2, 2)
        pb_primary = '#%02x%02x%02x' % pb_colors[0]
        pb_accent = '#%02x%02x%02x' % pb_colors[1]
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                if not colorchange:
                    await connection.execute(query, bytes_data, pb_primary, member_id, guild_id)
                else:
                    await connection.execute(query, bytes_data, pb_accent, pb_primary, member_id, guild_id)

class levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_holder = {0: "disabled", 1: "enabled"}
        self.pool = None
        self.last_xp: dict[int, float] = {}
        self.voice_times = {}
        self.xp_tracker = {}
        self.gain_xp.start()
        self.color = 0x2b2d31
        self.chromie_role = 1462092411122749732

    async def get_voicechannels(self, guild_id: int) -> int:
        query = '''SELECT voicechannels FROM settings WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                status = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if status is not None:
            return status[0]
        else:
            return 1

    async def get_textchannels(self, guild_id: int) -> int:
        query = '''SELECT channels FROM settings WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                status = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if status is not None:
            return status[0]
        else:
            return 1

    async def add_member(self, member_id: int, guild_id: int, xp = 25) -> None:
        query = '''INSERT INTO levelling (member_id, guild_id, xp , messages, format, color, color2) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id, xp, 1, 1, "#92ADB0", "#222E3C"))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_messages(self, member_id: int, guild_id: int, levels: LevelRow) -> None:
        query = '''UPDATE levelling SET messages = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, member_id, guild_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_xp(self, member_id: int, guild_id: int, levels: LevelRow, xp: int, message :discord.Message) -> None:
        query = '''UPDATE levelling SET messages = ?, xp = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, levels['xp'] + xp, member_id, guild_id))
                await conn.commit()
            await self.bot.pool.release(conn)

        member = message.guild.get_member(member_id)
        await self.check_rep(message, member, message)

    async def get_messages(self, member_id: int, guild_id: int) -> int:
        query = '''SELECT messages FROM levelling WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, member_id, guild_id)
                status = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if status is not None:
            return status[0]
        else:
            return 1

    async def check_levels(self, message: discord.Message, xp: int, xp_to_add: int) -> None:
        new_xp = xp + xp_to_add
        lvl = 0
        msgs = await self.get_messages(member_id=message.author.id, guild_id=message.author.guild.id)

        while True:
            required_xp = (50 * (lvl ** 2)) + (50 * (lvl - 1))
            if new_xp < required_xp:
                break
            lvl += 1

        old_lvl = 0
        temp_xp = xp
        while True:
            required_xp = (50 * (old_lvl ** 2)) + (50 * (old_lvl - 1))
            if temp_xp < required_xp:
                break
            old_lvl += 1

        if lvl > old_lvl:
            display_lvl = f"{lvl-1:02d}"
            msg = f" ・⠀LEVEL UP : FREQUENCY INCREASED TO **{display_lvl}**."

            if message.guild.id == 1462079847433244799:
                if lvl == 5:
                    reprole = await self.get_reprole(message.guild.id)
                    role = message.guild.get_role(reprole)
                    if role and role not in message.author.roles:
                        await message.author.add_roles(role, reason=f"{message.author.name} reached level 4")
                    msg += (
                        "\n-# **You can now rep our logos in https://discord.com/channels/1462079847433244799/1462975666206277632!**"
                    )

                elif lvl == 4:
                    role = message.guild.get_role(1463167269814272010)
                    if role and role not in message.author.roles:
                        await message.author.add_roles(role, reason=f"{message.author.name} reached level 3")
                        msg = f" ・⠀LEVEL UP : FREQUENCY INCREASED TO **{display_lvl}**.\n-# **You now have unlocked our logos!**"

            channel = self.bot.get_channel(1462941561221550173)
            if channel:
                embed = discord.Embed(
                    title="FREQUENCY LEVEL UPDATED",
                    description=msg,
                )
                embed.set_footer(text="HOSHI_V3 // NEURAL_LINK_STABLE", icon_url=self.bot.user.display_avatar.url)
                await channel.send(f"{message.author.mention}", embed=embed)

    async def get_reprole(self, guild_id: int) -> int:
        query = '''SELECT reprole FROM settings WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                status = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if status is not None:
            return status[0]
        else:
            return 1

    async def level_handler(self, message: discord.Message, retry_after: Optional[commands.CooldownMapping], xp: int) -> None:
        member_id = message.author.id
        guild_id = message.guild.id
        levels = await self.get_member_levels(member_id, guild_id)
        if levels == None:
            await self.add_member(member_id, guild_id)
        else:
            if retry_after:
                await self.update_messages(member_id, guild_id, levels)
            else:
                await self.update_xp(member_id, guild_id, levels, xp, message)
                await self.check_levels(message, levels['xp'], xp)

    async def get_member_levels(self, member_id: int, guild_id: int) -> Optional[LevelRow]:
        query = '''SELECT * from levelling WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id))
                row = await cursor.fetchone()
                if row:
                    return row
                else:
                    return None

    async def handle_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        if not any(role.id == 1462092411122749732 for role in message.author.roles):
            return

        guild_id = message.guild.id if message.guild else None
        if guild_id is None:
            return
        
        channels = await self.get_textchannels(guild_id)
        if str(message.channel.id) not in channels:
            return
        
        xp_to_add = await self.get_chatxp(guild_id)
        now = asyncio.get_event_loop().time()
        last = self.last_xp.get(message.author.id, 0)
        retry_after = now - last < 30
        if not retry_after:
            self.last_xp[message.author.id] = now

        await self.level_handler(message, retry_after, xp_to_add)

    async def get_voicexp(self, guild_id: int) -> int:
        query = '''SELECT voicexp FROM settings WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                status = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if status is not None:
            return status[0]
        else:
            return 1

    async def get_chatxp(self, guild_id: int) -> int:
        query = '''SELECT chatxp FROM settings WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                status = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if status is not None:
            return status[0]
        else:
            return 1

    async def get_color2(self, member_id: int, guild_id: int):
        query = '''SELECT color2 FROM levelling WHERE member_id = $1 AND guild_id = $2'''
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

    def _make_progress_bar(self, progress: float, color1, color2):
        width = 1384
        height = 16
        radius = 100

        if isinstance(color2, str):
            color2 = ImageColor.getcolor(color2, "RGBA")
        elif len(color2) == 3:
            color2 = (*color2, 255)

        if isinstance(color1, str):
            color1 = ImageColor.getcolor(color1, "RGBA")
        elif len(color1) == 3:
            color1 = (*color1, 255)

        def interpolate_color(c1, c2, factor):
            r = int(c1[0] + (c2[0] - c1[0]) * factor)
            g = int(c1[1] + (c2[1] - c1[1]) * factor)
            b = int(c1[2] + (c2[2] - c1[2]) * factor)
            a = int(c1[3] + (c2[3] - c1[3]) * factor)
            return (r, g, b, a)

        progress_width = int(width * progress)

        if progress_width <= 0:
            empty = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            empty_mask = Image.new("L", (width, height), 0)
            return empty, empty_mask

        gradient = Image.new('RGBA', (progress_width, height), (0, 0, 0, 0))
        gradient_draw = ImageDraw.Draw(gradient)

        for i in range(progress_width):
            t = i / progress_width
            color = interpolate_color(color2, color1, t)
            gradient_draw.line([(i, 0), (i, height)], fill=color)

        full_mask = Image.new("L", (width, height), 0)
        mask_draw = ImageDraw.Draw(full_mask)

        mask_draw.rounded_rectangle(
            [(0, 0), (progress_width, height)],
            radius=radius,
            fill=255
        )

        full_bar = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        full_bar.paste(gradient, (0, 0))

        return full_bar, full_mask

    def get_avatar(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        circle = Image.open('./assets/square-mask.png').resize((165, 165)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((165, 165))
        return avatar_image, circle

    def human_format(self, number: int) -> str:
        number = float('{:.3g}'.format(number))
        magnitude = 0
        while abs(number) >= 1000:
            magnitude += 1
            number /= 1000.0
        return '{}{}'.format('{:f}'.format(number).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    def xp_calculations(self, levels: LevelRow) -> Tuple[float, Union[str, int], Union[str, int], int]:
        xp = levels["xp"]
        lvl = 0

        while True:
            if xp < ((50*(lvl**2))+(50*(lvl-1))):
                break
            lvl += 1

        next_level_xp = ((50*(lvl**2))+(50*(lvl-1)))
        xp_need = next_level_xp
        xp_have = xp

        if not lvl == 1:
            prev_lvl = lvl-1
            previous_level_xp = ((50*(prev_lvl**2))+(50*(prev_lvl-1)))

            xp_progress_have = xp_have - previous_level_xp
            xp_progress_need = xp_need - previous_level_xp

            percentage = float(xp_progress_have / xp_progress_need)

            if xp_progress_need > 999:
                xp_progress_need = self.human_format(xp_progress_need)

            else:
                xp_progress_need = f"{xp_progress_need}"

            if xp_progress_have > 999:
                xp_progress_have = self.human_format(xp_progress_have)

        else:
            xp_progress_have = xp_have
            xp_progress_need = xp_need
            percentage = float(xp_progress_have / xp_progress_need)

        return percentage, xp_progress_have, xp_progress_need, lvl

    def draw_centered_text(self, draw: ImageDraw.ImageDraw, levels: LevelRow, text: str, font: ImageFont.FreeTypeFont, *, x_center: int, y_start: int, line_spacing: int = 5):
        """Draws multiline text centered at x_center, starting from y_start."""
        lines = text.split('\n')
        for line in lines:
            bbox = font.getbbox(line)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x_position = x_center - text_width // 2
            draw.text((x_position, y_start), line, font=font, fill=levels["color"])
            y_start += text_height + line_spacing

    def draw_centered_text2(self, draw: ImageDraw.ImageDraw, levels: LevelRow, text: str, font: ImageFont.FreeTypeFont, *, x_center: int, y_start: int, line_spacing: int = 5):
        """Draws multiline text centered at x_center, starting from y_start."""
        lines = text.split('\n')
        for line in lines:
            bbox = font.getbbox(line)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x_position = x_center - text_width // 2
            draw.text((x_position, y_start), line, font=font, fill=levels["color2"])
            y_start += text_height + line_spacing      

    def get_card(self, avatar: BytesIO, levels: LevelRow, rank: int, user: discord.User, guild: discord.Guild) -> BytesIO:
        percentage, xp_have, xp_need, level = self.xp_calculations(levels)
        card = Image.new('RGBA', size=(1500, 500), color='grey')
        if levels['image'] is not None and levels['image'] != b'':
            bg = Image.open(BytesIO(levels["image"]))
        else:
            bg = Image.open("./assets/rankcard/rankcard.png")

        bg_aspect_ratio = bg.width / bg.height
        target_aspect_ratio = 1500 / 500

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
        bg = bg.resize((1500, 500))
        bright = ImageEnhance.Brightness(bg)
        bg_bright = bright.enhance(1.5)
        bg_blurred = bg_bright.filter(ImageFilter.GaussianBlur(radius=20))
        frame_number = 4
        frame = Image.open(f"./assets/frames/{frame_number}.png").resize((1500, 500)).convert("RGBA")
        mask = Image.open("./assets/rankcard/rank_mask.png").resize((1500, 500)).convert("L")
        inverted_mask = ImageOps.invert(mask)
        bg_frosted = Image.composite(bg_blurred, Image.new("RGBA", bg.size, "white"), inverted_mask)
        bg_frosted.putalpha(inverted_mask)
        bright = ImageEnhance.Brightness(bg)
        texture_bright = bright.enhance(5)
        texture_mask = Image.open("./assets/rankcard/texture.png").resize((1500, 500)).convert("L")
        inverted_texture_mask = ImageOps.invert(texture_mask)
        texture_frosted = Image.composite(texture_bright, Image.new("RGBA", bg.size, "white"), inverted_texture_mask)
        texture_frosted.putalpha(inverted_texture_mask)
        bar, mask_bar = self._make_progress_bar(percentage, levels['color'], levels["color2"])
        avatar_paste, circle = self.get_avatar(avatar)
        card.paste(bg, (0, 0))
        card.paste(bg_frosted, (0, 0), bg_frosted)
        card.paste(bar, (58, 447), mask_bar) 
        texture_crop = texture_frosted.crop((58, 447, 58 + 1384, 447 + 16))
        texture_alpha = texture_crop.getchannel('A')
        final_texture_mask = Image.new("L", texture_crop.size, 0)
        final_texture_mask = ImageChops.multiply(texture_alpha, mask_bar)
        card.paste(texture_crop, (58, 447), final_texture_mask)
        card.paste(avatar_paste, (59, 34), circle)
        card.paste(frame, (0, 0), frame)

        draw = ImageDraw.Draw(card, 'RGBA')

        Extra_Bold_17 = ImageFont.truetype("./fonts/extrabold.ttf", size=17)
        Light_20 = ImageFont.truetype("./fonts/light.ttf", size=20)
        Extra_Bold_32 = ImageFont.truetype("./fonts/extrabold.ttf", size=32)
        Extra_Bold_17 = ImageFont.truetype("./fonts/extrabold.ttf", size=17)
        Bold_22 = ImageFont.truetype("./fonts/bold.ttf", size=22)

        ranked = f"{str(rank)}"
        levelled = f"{level-1}"
        xp = f"{xp_have} / {xp_need} AMPLITUDE"
        msgs = f"{levels['messages']}"

        wrapped_rank = "\n".join(textwrap.fill(line, width=75) for line in ranked.splitlines())
        self.draw_centered_text2(draw, text=wrapped_rank, font=Bold_22, x_center=88, y_start=393, levels=levels)

        wrapped_levels = "\n".join(textwrap.fill(line, width=75) for line in levelled.splitlines())
        self.draw_centered_text2(draw, text=wrapped_levels, font=Bold_22, x_center=184, y_start=393, levels=levels)

        wrapped_messages = "\n".join(textwrap.fill(line, width=75) for line in msgs.splitlines())
        self.draw_centered_text2(draw, text=wrapped_messages, font=Bold_22, x_center=291, y_start=393, levels=levels)

        wrapped_xp = "\n".join(textwrap.fill(line, width=75) for line in xp.splitlines())
        self.draw_centered_text2(draw, text=wrapped_xp, font=Extra_Bold_17, x_center=890, y_start=409, levels=levels)

        draw.text((255, 85), f"{user.name.upper()}", fill=levels['color'], font=Extra_Bold_32)
        draw.text((255, 120), f"CHROMATICA LEVELS", fill=levels['color2'], font=Light_20)
        draw.text((68, 370), f"RANK", fill=levels['color'], font=Extra_Bold_17)
        draw.text((160, 370), f"LEVEL", fill=levels['color'], font=Extra_Bold_17)
        draw.text((250, 370), f"MESSAGES", fill=levels['color'], font=Extra_Bold_17)
        draw.text((360, 409), f"FREQUENCY PROGRESS : {int(percentage * 100)}%", fill=levels['color2'], font=Extra_Bold_17)
        draw.text((1290, 409), f"NEXT LEVEL : {level}", fill=levels['color2'], font=Extra_Bold_17)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def generate_card(self, avatar: BytesIO, levels: LevelRow, rank: int, member: discord.Member, guild: discord.Guild) -> BytesIO:
        card = await self.bot.loop.run_in_executor(None, self.get_card, avatar, levels, rank, member, guild)
        return card

    async def get_rank(self, member_id: int, guild_id: int) -> int:
        query = '''SELECT COUNT(*) FROM levelling WHERE guild_id = ? AND xp > (SELECT xp FROM levelling WHERE member_id = ? AND guild_id = ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (guild_id, member_id, guild_id))
                rank = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return rank[0] + 1

    async def reset_levels(self, guild_id: int) -> None:
        query = '''UPDATE levelling SET xp = 0, messages = 0 WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def add_xp(self, member_id: int, guild_id: int, xp: int) -> None:
        levels = await self.get_member_levels(member_id, guild_id)

        if levels:
            query = '''UPDATE levelling SET xp = ? WHERE member_id = ? AND guild_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (levels['xp'] + xp, member_id, guild_id))
                    await conn.commit()
        else:
            await self.add_member(member_id, guild_id, xp)

    async def remove_xp(self, member_id: int, guild_id: int, xp: int, levels: LevelRow) -> None:
        query = '''UPDATE levelling SET xp = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['xp'] - xp, member_id, guild_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_leaderboard_stats(self, guild_id: int) -> List[LevelRow]:
        query = '''SELECT * FROM levelling WHERE guild_id = ? ORDER BY xp DESC, messages DESC'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (guild_id,))
                rows = await cursor.fetchall()
        return rows

    @app_commands.command(name="rank", description="Check your rank")
    async def rank(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        await interaction.response.defer()
        if not any(role.id == 1462092411122749732 for role in interaction.user.roles):
            return await interaction.followup.send("Sorry, this command is only available for members of Chromatica", ephemeral=True)
        
        member = member or interaction.user
        levels = await self.get_member_levels(member.id, interaction.guild_id)
        rank = await self.get_rank(member.id, interaction.guild_id)
        guild = interaction.guild.id

        is_gif_bg = False
        bg_bytes = levels['image'] if levels else None
        if bg_bytes is not None and bg_bytes[:3] == b'GIF':
            try:
                bg_test = Image.open(BytesIO(bg_bytes))
                is_gif_bg = getattr(bg_test, "is_animated", False)
            except Exception:
                is_gif_bg = False

        avatar_url = None
        if is_gif_bg and hasattr(member, 'avatar') and member.avatar and member.avatar.is_animated:
            avatar_url = member.avatar.url
        else:
            avatar_url = member.display_avatar.replace(static_format='png', size=256).url
            
        response = await self.bot.session.get(avatar_url)
        avatar = BytesIO(await response.read())
        avatar.seek(0)
        if levels:
            card = await self.generate_card(avatar, levels, rank, member, guild)
        else:
            card = None
        if card:
            card.seek(0)
            header = card.read(6)
            card.seek(0)
            ext = 'gif' if header[:3] == b'GIF' else 'png'
            view = RankCardConfig(member.id, bot=self.bot)
            await interaction.followup.send(
                file=discord.File(card, f'card.{ext}'))
        else:
            await interaction.followup.send(f"{member} hasn't gotten levels yet!")

    @app_commands.command(description="See Chromatica's leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        if not any(role.id == 1462092411122749732 for role in interaction.user.roles):
            return await interaction.response.send_message("Sorry, this command is only available for members of Chromatica", ephemeral=True)
        
        embeds = []
        description = ""
        rows = await self.get_leaderboard_stats(interaction.guild_id)
        per_page = 5 if interaction.user.is_on_mobile() else 5
        for i, row in enumerate(rows, start=1):
            msg = "Messages" if row['messages'] != 1 else "Message"
            xp = row["xp"]
            lvl = 0
            while True:
                if xp < ((50*(lvl**2))+(50*(lvl-1))):
                    break
                lvl += 1
            description += f"\n**{i} :** <@!{row['member_id']}>\n**・⠀Frequency Level {lvl-1}**\n**・⠀{row['messages']} {msg}**\n"
            if i % per_page == 0 or i == len(rows):
                embed = discord.Embed(title=f"Chromatica's leaderboard", description=description)
                embed.set_thumbnail(url=interaction.guild.icon.url)
                embeds.append(embed)
                description = ""
        if len(embeds) > 1:
            view = Paginator(embeds)
            await interaction.response.send_message(embed=view.initial, view=view)
        else:
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="iakick", description="Kick members below a frequency level")
    async def iakick(self, interaction: discord.Interaction, requirement: int, level: int):
        staff_roles = {1462092462292992094, 1462092388930687151}
        if staff_roles.isdisjoint({r.id for r in interaction.user.roles}):
            return await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

        await interaction.response.defer()
        guild = interaction.guild
        if guild is None:
            return

        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT member_id, xp FROM levelling WHERE guild_id = $1', guild.id)
                rows = await cursor.fetchall()
            await self.bot.pool.release(conn)

        total = len(rows)
        if total == 0:
            return await interaction.followup.send("No members in database.", ephemeral=True)

        to_kick: list[tuple[int, int]] = []
        protected_role = 1478807893288681693

        def xp_to_level(xp: int) -> int:
            lvl = 0
            while True:
                req = (50 * (lvl ** 2)) + (50 * (lvl - 1))
                if xp < req:
                    break
                lvl += 1
            return lvl - 1

        progress_msg = await interaction.followup.send("0% complete with level checking", ephemeral=True)
        last_percent = -1
        for idx, row in enumerate(rows):
            mid = row['member_id']
            xp = row['xp']
            lvl = xp_to_level(xp)
            if lvl < level:
                member = guild.get_member(mid)
                if member and any(r.id == protected_role for r in member.roles):
                    pass
                else:
                    to_kick.append((mid, lvl))
            percent = int((idx + 1) / total * 100)
            if percent != last_percent:
                last_percent = percent
                await progress_msg.edit(content=f"{percent}% complete with level checking")

        if not to_kick:
            return await interaction.followup.send(f"No members below level {level} (excluding protected role).", ephemeral=True)

        lines = [f"<@{mid}> (lvl {lvl})" for mid, lvl in to_kick]
        summary = f"Members under level {level} ({len(to_kick)}):\n" + "\n".join(lines)
        confirm_msg = await interaction.followup.send(summary)
        await confirm_msg.add_reaction("✅")
        await confirm_msg.add_reaction("❌")

        def check(reaction: discord.Reaction, user: discord.User):
            return (
                user.id == interaction.user.id
                and reaction.message.id == confirm_msg.id
                and str(reaction.emoji) in ("✅", "❌")
            )

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            return await interaction.followup.send("Timed out; aborting.", ephemeral=True)

        if str(reaction.emoji) != "✅":
            return await interaction.followup.send("Operation cancelled.", ephemeral=True)

        role_remove = guild.get_role(1462092411122749732)
        role_add = guild.get_role(1462092433637773322)

        for mid, lvl in to_kick:
            member = guild.get_member(mid)
            if member:
                if role_remove:
                    await member.remove_roles(role_remove, reason="IA kick")
                if role_add:
                    await member.add_roles(role_add, reason="IA kick")
                try:
                    await member.send(
                        f"You have been removed from the {role_remove.name if role_remove else 'role'} role due to being level {lvl} or below."
                    )
                except Exception:
                    pass
            await self.remove_member(mid)

        await interaction.followup.send(f"Completed kicking {len(to_kick)} members.", ephemeral=True)

    @commands.command()
    async def add(self, ctx, member: discord.Member, amount: int):
        staff_roles = {1462092462292992094, 1462092388930687151}
        author_roles = {role.id for role in ctx.author.roles}
        channel = self.bot.get_channel(1462941561221550173)
        
        if staff_roles.isdisjoint(author_roles):
            return await ctx.reply("Sorry, this command is only available for staff members.", ephemeral=True)

        levels = await self.get_member_levels(member.id, ctx.guild.id)
        if not levels:
            await self.add_member(member.id, guild_id=ctx.guild.id)
            await self.add_xp(member.id, ctx.guild.id, 25)
            return await ctx.reply(f"{member.name} was not in the database.\nI've added them and gave them +25 AMP to get started!")

        await self.add_xp(member.id, ctx.guild.id, amount, levels)
        await ctx.reply(f"Gave **{amount}xp** to {member.mention}.")
        await channel.send(f"{member.mention} +{amount} AMP was added to your Frequency Level")
        
    @commands.command()
    async def remove(self, ctx, member: discord.Member, amount: int):
        staff_roles = {1462092462292992094, 1462092388930687151}
        author_roles = {role.id for role in ctx.author.roles}

        if staff_roles.isdisjoint(author_roles):
            return await ctx.reply("Sorry, this command is only available for staff members.", ephemeral=True)

        levels = await self.get_member_levels(member.id, ctx.guild.id)
        if not levels:
            return await ctx.reply(f"{member.mention} doesn't have any AMP yet!")

        if amount > levels["xp"]:
            return await ctx.reply("You can't take away more AMP than the user currently has!")

        await self.remove_xp(member.id, ctx.guild.id, amount, levels)
        await ctx.reply(f"Removed {amount} AMP from {member.mention}.")

    @app_commands.command(name="reset", description="Resets everyone's xp")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reset(self, interaction: discord.Interaction):
        if interaction.guild.id == 1462079847433244799:
            await self.reset_levels(interaction.guild_id)
            await interaction.response.send_message("All levels have been reset! All members are back to level 1 with 0 messages\nIf members had **0** chances to send another inactive message, they will now be able to send more!")
        else:
            await self.reset_levels(interaction.guild_id)
            await interaction.response.send_message("All levels have been reset! All members are back to level 1")

    async def get_dailyxp(self, guild_id: int) -> str:
        query = '''SELECT dailyxp FROM settings WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (guild_id,))
                status = await cursor.fetchone()
        if status is not None:
            return status[0]
        else:
            return "150 - 300"

    async def get_level_row(self, member_id: int, guild_id: int) -> Optional[LevelRow]:
        query = '''SELECT xp, messages FROM levelling WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id))
                return await cursor.fetchone()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.handle_message(message)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel = self.bot.get_channel(822422177612824580)
        levels = await self.get_member_levels(member.id, guild_id=member.guild.id)
        if before.channel is None and after.channel is not None:
            self.voice_times[member.id] = datetime.utcnow()
            self.xp_tracker[member.id] = 0

        elif before.channel is not None and after.channel is None:
            if member.id in self.voice_times:
                join_time = self.voice_times.pop(member.id)
                time_spent = (datetime.utcnow() - join_time).total_seconds()
                xp_earned = self.xp_tracker.pop(member.id, 0)
                required_role = member.guild.get_role(self.chromie_role)

                if required_role in member.roles:
                    if channel:
                        await self.add_xp(member.id, xp=xp_earned, levels=levels, guild_id=member.guild.id)
                        await channel.send(f"{member.mention}, you earned **{xp_earned} XP** from talking in {before.channel.mention}.")
    
    @tasks.loop(seconds=15)
    async def gain_xp(self):
        for member_id in list(self.xp_tracker.keys()):
            guild = self.bot.get_guild(1462079847433244799)
            member = guild.get_member(member_id) if guild else None
            if member and member.voice and len(member.voice.channel.members) > 1:
                if not member.voice.self_mute and not member.voice.self_deaf:
                    self.xp_tracker[member_id] += 1

    @gain_xp.before_loop
    async def before_gain_xp(self):
        await self.bot.wait_until_ready()

    async def add_messages(self, amount, member_id: int, guild_id: int, levels: LevelRow) -> None:
        query = '''UPDATE levelling SET messages = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + amount, member_id, guild_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    @commands.command()
    async def addmsg(self, ctx, member: discord.Member, amount):
        required_roles = {1462092462292992094, 1462092462292992094}
        member_roles = {role.id for role in ctx.author.roles}
        if required_roles.isdisjoint(member_roles):
            await ctx.reply("Sorry, this command is only available for staff members.", ephemeral=True)
            return

        try:
            amount = int(amount)
        except ValueError:
            await ctx.reply("Amount must be a number.", ephemeral=True)
            return

        levels = await self.get_member_levels(member.id, ctx.guild.id)
        if not levels:
            await ctx.reply("Could not retrieve the member's level data. Please try again later.", ephemeral=True)
            return

        await self.add_messages(amount, member.id, ctx.guild.id, levels)
        await ctx.reply(f"Gave `{amount} messages` to {str(member)}.")

    async def check_rep(self, ctx, member: discord.Member, message: discord.Message):
        levels = await self.get_member_levels(member.id, ctx.guild.id)
        required_level = 2
        required_messages = 50

        xp = levels["xp"]
        lvl = 0
        while True:
            if xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                break
            lvl += 1

        messages = levels["messages"]
        role_id = await self.get_reprole(ctx.guild.id)
        rep_role = ctx.guild.get_role(role_id)

        if lvl >= required_level and messages >= required_messages and rep_role not in member.roles:
            await member.add_roles(rep_role)
            await message.channel.send(f"Congrats {member.mention}! You have unlocked rep!\nThe role should be automatically added. If not, please ping a staff member!")

    @commands.command(name="resetcard")
    async def resetcard(self, ctx, member: discord.Member = None):
        staff_roles = {1462092462292992094, 1462092462292992094}
        author_roles = {role.id for role in ctx.author.roles}
        if staff_roles.isdisjoint(author_roles):
            await ctx.reply("Sorry, this command is only available for staff members.", ephemeral=True)
            return

        member = member or ctx.author
        query = '''UPDATE levelling SET color = NULL, color2 = NULL, image = NULL WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member.id, ctx.guild.id))
                await conn.commit()
            await self.bot.pool.release(conn)

        await ctx.reply(f"Reset rank card colors and image for {member.mention}.")

    @commands.command(name="debugcard")
    @commands.has_permissions(administrator=True)
    async def debugcard(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        query = '''SELECT * FROM levelling WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member.id, ctx.guild.id))
                row = await cursor.fetchone()
            await self.bot.pool.release(conn)

        if not row:
            await ctx.reply(f"No data found for {member.mention}.")
            return

        data = "\n".join(f"{key}: {row[key]}" for key in row.keys())
        await ctx.reply(f"```{data}```")

    async def remove_member(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('DELETE FROM levelling WHERE member_id = $1', member_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    @commands.command(name="deleteuser")
    @commands.has_permissions(administrator=True)
    async def deleteuser(self, ctx, member: discord.Member):
        await self.remove_member(member.id)
        await ctx.reply(f"Deleted leveling data for {member.mention}.")

async def setup(bot):
    await bot.add_cog(levels(bot))