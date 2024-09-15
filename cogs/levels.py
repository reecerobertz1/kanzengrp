import asyncio
import math
import random
import re
import discord
from discord.ext import commands
from random import randint
from typing import List, Optional, TypedDict, Union, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO
import functools
from discord import app_commands
from PIL import Image, ImageFilter, ImageOps, UnidentifiedImageError
import requests
from utils.views import Paginator
from colorthief import ColorThief

class LevelRow(TypedDict):
    member_id: int
    xp: int
    messages: int
    color: str
    image: str

class levels(commands.Cog):
    def __init__(self, bot):
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$"
        self.bot = bot
        self.status_holder = {0: "disabled", 1: "enabled"}
        self.pool = None
        self.channels = [1134742133421658193, 1140616319801237515, 1197155970988646431, 1140180038902354001]
        self.guilds = [1134736053803159592]
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)

    def kanzen_only():
        def predicate(ctx: commands.Context):
            if ctx.guild.id == 1134736053803159592:
                return True
            else:
                return False
        return commands.check(predicate)
    
    def kanzen_cooldown(message: discord.Message):
        if message.author.id == 609515684740988959:
            return None
        
        role = message.guild.get_role(1134797882420117544)
        if role in message.author.roles:
            return commands.Cooldown(1, 86400)
        
        booster = message.guild.get_role(1134793235408093254)
        if booster in message.author.roles:
            return commands.Cooldown(1, 43200)
        
        return commands.Cooldown(1, 86400)

    async def add_member(self, member_id: int, xp=5) -> None:
        query_check = '''SELECT 1 FROM levels WHERE member_id = ?'''
        query_insert = '''INSERT INTO levels (member_id, xp, messages, color) VALUES (?, ?, ?, ?)'''
        query_update = '''UPDATE levels SET xp = xp + ?, messages = messages + 1 WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query_check, (member_id,))
                exists = await cursor.fetchone()
                if exists:
                    await cursor.execute(query_update, (xp, member_id))
                else:
                    await cursor.execute(query_insert, (member_id, xp, 1, '#c45a72'))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_messages(self, member_id: int, levels: LevelRow) -> None:
        query = '''UPDATE levels SET messages = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_xp(self, member_id: int, levels: LevelRow, xp: int) -> None:
        query = '''UPDATE levels SET messages = ?, xp = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, levels['xp'] + xp, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_member_levels(self, member_id: int) -> Optional[LevelRow]:
        query = '''SELECT * from levels WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, ))
                row = await cursor.fetchone()
                if row:
                    return row
                else:
                    return None

    async def check_levels(self, message: discord.Message, xp: int, xp_to_add: int) -> None:
        levels = await self.get_member_levels(message.author.id)
        new_xp = xp + xp_to_add
        lvl = 0
        while True:
            if xp < ((50*(lvl**2))+(50*(lvl-1))):
                break
            lvl += 1

        next_level_xp = ((50*(lvl**2))+(50*(lvl-1)))
        if new_xp > next_level_xp:
            current_memberlvl = levels['memberlvl'] or 0
            new_memberlvl = current_memberlvl + 1

            query = '''UPDATE levels SET memberlvl = ? WHERE member_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (new_memberlvl, message.author.id,))
                    await conn.commit()
                await self.bot.pool.release(conn)

            if lvl == 1:
                stella = "Stella"
            else:
                stella = "Stellas"

            embed = discord.Embed(description=f"{message.author.name} you just reached **{lvl}** {stella}!", colour=0xFEBCBE)
            
            if lvl == 1:
                role = message.guild.get_role(1147592763924295681)
                if role:
                    await message.author.add_roles(role, reason=f"{message.author.name} reached 1 stella")
            channel = message.guild.get_channel(1135027269853778020)
            await channel.send(message.author.mention, embed=embed)
            await self.update_mora(message.author.id)

    async def level_handler(self, message: discord.Message, retry_after: Optional[commands.CooldownMapping], xp: int) -> None:
        member_id = message.author.id
        levels = await self.get_member_levels(member_id)
        if levels is None:
            await self.add_member(member_id)
        else:
            if retry_after:
                await self.update_messages(member_id, levels)
            else:
                await self.update_xp(member_id, levels, xp)
                await self.check_levels(message, levels['xp'], xp)

    async def handle_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
            
        if message.channel.id not in self.channels:
            return

        zennie_role_id = 1134797882420117544
        forms_zennie_role_id = 1134797882420117544
        zennie_role = message.guild.get_role(zennie_role_id)
        if zennie_role and zennie_role in message.author.roles:
            bucket = self.cd_mapping.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            xp_to_add = randint(5, 15)
            await self.level_handler(message, retry_after, xp_to_add)
        forms_zennie_role = message.guild.get_role(forms_zennie_role_id)
        if forms_zennie_role and forms_zennie_role in message.author.roles:
            bucket = self.cd_mapping.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            xp_to_add = randint(5, 15)
            await self.level_handler(message, retry_after, xp_to_add)

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
                xp_progress_need = f"{xp_progress_need} XP"

            if xp_progress_have > 999:
                xp_progress_have = self.human_format(xp_progress_have)

        else:
            xp_progress_have = xp_have
            xp_progress_need = xp_need
            percentage = float(xp_progress_have / xp_progress_need)

        return percentage, xp_progress_have, xp_progress_need, lvl

    def _make_progress_bar(self, progress, color):
        width = 1500  # Width of the progress bar
        height = 15  # Height of the progress bar
        radius = 0  # Radius of the rounded corners
        progress_bar = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(progress_bar)
        draw.rectangle([(0, 0), (width, height)], fill=(195, 195, 195, 255))
        bg_width = int(width * 1)
        progress_width = int(width * progress)
        draw.rounded_rectangle([(0, 0), (bg_width, height)], fill=(195, 195, 195, 255), width=1, radius=radius)
        draw.rounded_rectangle([(0, 0), (progress_width, height)], fill=color, width=1, radius=radius)
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (bg_width, height)], fill=255, width=0, radius=radius)
        return progress_bar, mask

    def get_avatar(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        circle = Image.open('./assets/circle-mask.png').resize((190, 190)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((190, 190))
        return avatar_image, circle

    async def set_card_image(self, image: BytesIO, member_id: int, guild_id: int, colorchange: Optional[bool] = False) -> None:
        query = "UPDATE levels SET image = $1, color = $2 WHERE member_id = $3"
        bytes_data = image.getvalue()
        image.seek(0)
        ct = ColorThief(image)
        pb_colors = ct.get_palette(2, 2)
        pb_primary = '#%02x%02x%02x' % pb_colors[0]
        pb_accent = '#%02x%02x%02x' % pb_colors[1]
        if colorchange == False:
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(query, bytes_data, pb_primary, member_id)
            await self.bot.pool.release(connection)
        else:
            new_query = "UPDATE levels SET image = $1, accent_color = $4, color = $5 WHERE member_id = $2"
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(new_query, bytes_data, member_id, pb_accent, pb_primary)
            await self.bot.pool.release(connection)

    def _get_bg_image(self, url: str):
            """Gets background image"""
            image = requests.get(url, stream=True)
            b_img = Image.open(BytesIO(image.content))
            return b_img

    def get_card(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, user: discord.User, guild: discord.Guild) -> BytesIO:
        percentage, xp_have, xp_need, level = self.xp_calculations(levels)
        card = Image.new('RGBA', size=(1500, 500), color='grey')
        
        if levels['image'] is not None:
            bg = Image.open(BytesIO(levels["image"]))
        else:
            bg = Image.open("./assets/rankcard.png")

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
        dark = ImageEnhance.Brightness(bg)
        bg_dark = dark.enhance(0.8)
        bg_blurred = bg_dark.filter(ImageFilter.GaussianBlur(radius=20))
        mask = Image.open("./assets/boxmask.png").resize((1500, 500)).convert("L")
        inverted_mask = ImageOps.invert(mask)
        bg_frosted = Image.composite(bg_blurred, Image.new("RGBA", bg.size, "white"), inverted_mask)
        bg_frosted.putalpha(inverted_mask)
        bar, mask_bar = self._make_progress_bar(percentage, levels['color'])
        avatar_paste, circle = self.get_avatar(avatar)
        card.paste(bg, (0, 0))
        card.paste(bg_frosted, (0, 0), bg_frosted)
        card.paste(bar, (0, 485), mask_bar)
        card.paste(avatar_paste, (18, 17), circle)
        zhcn = ImageFont.truetype("./fonts/zhcn.ttf", size=36)
        zhcn2 = ImageFont.truetype("./fonts/zhcn.ttf", size=25)
        rankboxes = Image.open('./assets/rankboxes.png')
        rankboxes = rankboxes.resize((750, 750))
        card.paste(rankboxes, (0, 0), rankboxes)
        draw = ImageDraw.Draw(card, 'RGBA')
        message = levels["messages"]
        messages = self.human_format(message)
        draw.text((100, 345), f'{xp_have} | {xp_need}', fill=levels['color'], font=zhcn)
        draw.text((100, 345), f'{xp_have} | {xp_need}', fill=levels['color'], font=zhcn)
        draw.text((225, 25), f"{user.name}", fill=levels['color'], font=zhcn)
        draw.text((225, 65), f"lyra levels", fill=levels['color'], font=zhcn2)
        draw.text((300, 410), f'rank | {str(rank)}', fill=levels['color'], font=zhcn)
        draw.text((100, 410), f'level | {level-1}', fill=levels['color'], font=zhcn)
        draw.text((500, 410), f'{messages} messages', fill=levels['color'], font=zhcn)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def generate_card_rank1(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, member: discord.Member) -> BytesIO:
        guild = member.guild
        card_generator = functools.partial(self.get_card, name, status, avatar, levels, rank)
        card = await self.bot.loop.run_in_executor(None, self.get_card, str(member), str(member.status), avatar, levels, rank, member, guild)
        return card

    async def get_rank(self, member_id: int) -> int:
        query = '''SELECT COUNT(*) FROM levels WHERE xp > (SELECT xp FROM levels WHERE member_id = ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id))
                rank = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return rank[0] + 1

    async def reset_levels(self) -> None:
        query = '''UPDATE levels SET xp = 0, messages = 0'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, )
                await conn.commit()
            await self.bot.pool.release(conn)

    async def add_xp(self, member_id: int, xp: int, levels: Optional[LevelRow]) -> None:
        if levels:
            current_xp = levels['xp']
            new_xp = current_xp + xp

            query = '''UPDATE levels SET xp = ? WHERE member_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (new_xp, member_id))
                    await conn.commit()
        else:
            await self.add_member(member_id, xp)

    async def remove_xp(self, member_id: int, xp: int, levels: LevelRow) -> None:
        query = '''UPDATE levels SET xp = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['xp'] - xp, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_rank_color(self, member_id: int, color: str) -> None:
        query = '''UPDATE levels SET color = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, color, member_id, )
                await conn.commit()
            await self.bot.pool.release(conn)

    @app_commands.command(name="rank", description="Check your rank")
    async def rank(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        zennie_role_id = 1134797882420117544
        member = member or interaction.user
        
        if zennie_role_id not in [role.id for role in member.roles]:
            await interaction.response.send_message("Sorry, you cannot use this command.", ephemeral=True)
            return

        levels = await self.get_member_levels(member.id)
        rank = await self.get_rank(member.id)
        avatar_url = member.display_avatar.replace(static_format='png', size=256).url
        response = await self.bot.session.get(avatar_url)
        avatar = BytesIO(await response.read())
        avatar.seek(0)

        if levels:
            card = await self.generate_card_rank1(str(member), str(member.status), avatar, levels, rank, member)
        else:
            card = None

        if interaction.response.is_done():
            return

        if card:
            await interaction.response.send_message(file=discord.File(card, 'card.png'))
        else:
            await interaction.response.send_message(f"{member} hasn't gotten levels yet!")

    @app_commands.command(name="add", description="Add xp to someone", extras="+add @member amount")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def add(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        zennie_role_id = 1261435772775563315
        if zennie_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("Sorry, this is a staff-only command", ephemeral=True)
            return

        levels = await self.get_member_levels(member.id)
        if levels is None:
            await self.add_member(member.id, amount)
            current_xp = amount
        else:
            current_xp = levels["xp"]

        new_xp = current_xp + amount
        await self.add_xp(member.id, amount, levels)
        lvl = 0
        while True:
            xp_needed_for_next_level = ((50 * (lvl ** 2)) + (50 * (lvl - 1)))
            if current_xp < xp_needed_for_next_level:
                break
            lvl += 1

        final_lvl = lvl
        while new_xp >= ((50 * (final_lvl ** 2)) + (50 * (final_lvl - 1))):
            final_lvl += 1

        stella = "Stella" if final_lvl == 1 else "Stellas"
        embed = discord.Embed(description=f"{member.name} you just reached **{final_lvl - 1}** {stella}!", colour=0xFEBCBE)
        embed.set_footer(text=f"This XP was added by {interaction.user.name}")
        channel = interaction.guild.get_channel(1135027269853778020)
        await channel.send(member.mention, embed=embed)
        if final_lvl >= 1:
            role = interaction.guild.get_role(1147592763924295681)
            if role and not any(r.id == role.id for r in member.roles):
                await member.add_roles(role, reason=f"{member.name} reached 1 Stella or higher")
        embed = discord.Embed(title='XP Added!', description=f'Gave `{amount} XP` to {str(member)}', color=0xFEBCBE)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove", description="Remove xp from someone", extras="+remove @member amount")
    async def remove(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        zennie_role_id = 1261435772775563315
        
        if zennie_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("Sorry, this is a staff only command", ephemeral=True)
            return
        levels = await self.get_member_levels(member.id)
        if levels:
            if amount > levels['xp']:
                await interaction.response.send_message("you can't take away more xp than the user already has!")
            else:
                await self.remove_xp(member.id, amount, levels)
                embed = discord.Embed(title='xp removed!',description=f'removed `{amount}xp` from {str(member)}',color=0xFEBCBE)
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{str(member)} doesn't have any xp yet!")

    async def get_leaderboard_stats(self) -> List[LevelRow]:
        query = '''SELECT * FROM levels ORDER BY xp DESC'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall()
        return rows

    @app_commands.command(description="See the level leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        zennie_role_id = 1134797882420117544
        member = interaction.user
        
        if zennie_role_id not in [role.id for role in member.roles]:
            await interaction.response.send_message("Sorry, you currently aren't a member of lyra. This command is for lyre's only!", ephemeral=True)
            return
        embeds = []
        description = ""
        rows = await self.get_leaderboard_stats()
        per_page = 5 if interaction.user.is_on_mobile() else 10
        for i, row in enumerate(rows, start=1):
            msg = "messages" if row['messages'] != 1 else "message"
            xp = row["xp"]
            lvl = 0
            while True:
                if xp < ((50*(lvl**2))+(50*(lvl-1))):
                    break
                lvl += 1
            description += f"**{i}.** <@!{row['member_id']}>\n<:Empty:1188186122350759996><:1166196258499727480:1188190249768210582>**level {lvl-1} | {row['messages']} {msg}**\n\n"
            if i % per_page == 0 or i == len(rows):
                embed = discord.Embed(title=f"{interaction.guild.name}'s leaderboard", description=description, color=0xFEBCBE)
                embed.set_thumbnail(url=interaction.guild.icon.url)
                embeds.append(embed)
                description = ""
        if len(embeds) > 1:
            view = Paginator(embeds)
            await interaction.response.send_message(embed=view.initial, view=view)
        else:
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rankcolor", description="Change your rank card color with hex codes")
    async def rankcolor(self, interaction: discord.Interaction, color: str):
        zennie_role_id = 1134797882420117544
        member = interaction.user
        
        if zennie_role_id not in [role.id for role in member.roles]:
            await interaction.response.send_message("Sorry, you cannot use this command.", ephemeral=True)
            return
        match = re.search(self.regex_hex, color)
        if match:
            await self.set_rank_color(interaction.user.id, color)
            embed = discord.Embed(
                title='changed your bar color!',
                description=f'your new bar color is `{color}`',
                color=0xFEBCBE
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"`{color}` is not a valid hex color. You may need to add a #")

    @app_commands.command(name="rankbg", description="Upload an image when using this command!")
    async def rankbg(self, interaction: discord.Interaction, image: Optional[discord.Attachment] = None):
        zennie_role_id = 1134797882420117544
        member = interaction.user
        
        if zennie_role_id not in [role.id for role in member.roles]:
            await interaction.response.send_message("Sorry, you cannot use this command.", ephemeral=True)
            return
        image_data = None

        if image:
            if image.url.startswith("https://") or image.url.startswith("http://"):
                try:
                    async with self.bot.session.get(image.url) as resp:
                        if resp.headers.get('content-type').split("/")[0] == "image" and not resp.headers.get('content-type').split("/")[1] == "gif":
                            image_data = BytesIO(await resp.read())
                            image_data.seek(0)
                        else:
                            return await interaction.response.send_message("Invalid image.", ephemeral=True)
                except:
                    return await interaction.response.send_message("Couldn't get the image from the link you provided.", ephemeral=True)
            else:
                return await interaction.response.send_message("You need to use a https or http URL", ephemeral=True)
        else:
            if interaction.data.get('attachments'):
                to_edit = interaction.data['attachments'][0]
                if to_edit['content_type'].split("/")[0] == "image" and not to_edit['content_type'].split("/")[1] == "gif":
                    async with self.bot.session.get(to_edit['url']) as resp:
                        image_data = BytesIO(await resp.read())
                        image_data.seek(0)
                else:
                    return await interaction.response.send_message("Invalid image.", ephemeral=True)
            else:
                return await interaction.response.send_message("You need to upload an image attachment or add an image URL", ephemeral=True)

        try:
            b_img = Image.open(image_data)
        except UnidentifiedImageError:
            return await interaction.response.send_message("Invalid image.", ephemeral=True)
        
        await self.set_card_image(image_data, interaction.user.id, interaction.guild.id)
        await interaction.response.send_message("Successfully changed your rank card image!", ephemeral=True)

    @app_commands.command(name="reset", description="Resets everyone's xp")
    async def reset(self, interaction: discord.Interaction):
        zennie_role_id = 1261435772775563315
        member = interaction.user
        
        if zennie_role_id not in [role.id for role in member.roles]:
            await interaction.response.send_message("Sorry, this is a staff only command", ephemeral=True)
            return
        await self.reset_levels()
        await interaction.response.send_message("All levels have been reset! All members are back to level 1 with 0 messages")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.handle_message(message)

    @commands.command()
    @commands.dynamic_cooldown(kanzen_cooldown, commands.BucketType.user)
    async def dailies(self, ctx: commands.Context):
        zennie_role_id = 1134797882420117544
        zennie_role2_id = 1219759999656530130
        member = ctx.author
        if not any(role.id in [zennie_role_id, zennie_role2_id] for role in member.roles):
            await ctx.reply("Sorry, this is a members only command", ephemeral=True)
            return
        emojis = ["<:alhaithamuwu:1257829394995609722>", "<:dilucuwu:1215001949905223721>", "<:arleuwu:1236642544176205866>", "<:danhengiluwu:1236710497454264441>", "<:nilouuwu:1236642546269028443>", "<:xiaouwu:1214631450411016222>", "<:mizookuwu:1263923282072305674>", "<:bambyuwu:1258626994657300531>", "<:asmouwu:1281673436917399652>", "<:sigeuwu:1258217110752989184>", "<:scarauwu:1214787080262262826>", "<:neuviuwu:1259239904240468079>", "<:furinauwu:1269018189614809129>", "<:zhongliuwu:1215001895060512798>", "<:kazuhauwu:1215001799321321532>", "<:kaeyauwu:1258217332975730769>", "<:jiyanuwu:1258215228953591828>", "<:beeluwu:1281673450695557140>", "<:belphieuwu:1281673463517548584>", "<:leviuwu:1281673478831079556>", "<:luciuwu:1281673492449726535>", "<:lukeuwu:1281673507079717007>", "<:mammonuwu:1281673523122933770>", "<:moranuwu:1275808002229801010>"," <:satanuwu:1281673538390200461>", "<:rafayeluwu:1268323216904949820>", "<:ittouwu:1215041496584036455>", "<:eulauwu:1263578777422790687>", "<:chuwanninguwu:1258217513842376714>", "<:childeuwu:1236695748301688953>", "<:aventurineuwu:1236710521114202112>", "<:alhaithamuwu:1257830193750347918>", "<:solomonuwu:1281673568467292191>", "<:simeonuwu:1281673552931721246>", "<:sukunauwu:1268322507929157764>", "<:sylusuwu:1268323281010688154>", "<:tighnariuwu:1261061785406935153>", "<:vashuwu:1261060609278083183>", "<:ventiuwu:1215001849183076432>", "<:wriouwu:1258217203627462769>", "<:wukonguwu:1265138917670387794>", "<:yaeuwu:1258217291477422091>", "<:yejunuwu:1258217244966654013>", "<:yoiuwu:1259241806969704560>", "<:yanfeiuwu:1268323149741690890>"]
        emoji = random.choice(emojis)
        xp = randint(150, 300)
        levels = await self.get_member_levels(ctx.author.id)
        new_xp = levels["xp"] + xp
        lvl = 0
        while True:
            if levels["xp"] < ((50*(lvl**2))+(50*(lvl-1))):
                break
            lvl += 1
        next_level_xp = ((50*(lvl**2))+(50*(lvl-1)))
        if new_xp > next_level_xp:
            if lvl == 1:
                stella = "Stella"
            else:
                stella = "Stellas"

            embed = discord.Embed(description=f"{ctx.author.name} you just reached **{lvl}** {stella}!", colour=0xFEBCBE)
            await self.add_xp(member.id, xp, levels)
            if lvl == 1:
                role = ctx.guild.get_role(1147592763924295681)
                if role:
                    await ctx.author.add_roles(role, reason=f"{ctx.author.name} reached 1 stella")
            channel = ctx.guild.get_channel(1135027269853778020)
            await channel.send(ctx.author.mention, embed=embed)
        else:
            await self.add_member(member.id, xp)
        await ctx.reply(f"{emoji} Yay! You have claimed your daily xp! you got `{xp}xp`")
        
    @dailies.error
    async def daily_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            if error.retry_after > 3600:
                hours = error.retry_after / 3600
                await ctx.reply(f"You need to wait {int(hours)} hours before claiming daily XP again!")
            elif error.retry_after > 60:
                minutes = error.retry_after / 60
                await ctx.reply(f"You need to wait {int(minutes)} minutes before claiming daily XP again!")
            else:
                await ctx.reply(f"You need to wait {int(error.retry_after)} seconds before claiming daily XP again!")

    async def add_msg(self, member_id: int, messages: int, levels: Optional[LevelRow]) -> None:
        if levels:
            query = '''UPDATE levels SET messages = ? WHERE member_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (levels['messages'] + messages, member_id, ))
                    await conn.commit()
                await self.bot.pool.release(conn)
        else:
            await self.add_member(member_id, messages)

    async def add_msg(self, member_id: int, messages: int, levels: Optional[LevelRow]) -> None:
        if levels:
            query = '''UPDATE levels SET messages = ? WHERE member_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (levels['messages'] + messages, member_id, ))
                    await conn.commit()
                await self.bot.pool.release(conn)
        else:
            await self.add_member(member_id, messages)

    @commands.command()
    async def lyraaddmsg(self, ctx, member: discord.Member, messages: int):
        levels = await self.get_member_levels(member.id)
        await self.add_msg(member.id, messages, levels)
        await ctx.reply(f"Added **{messages}** messages to {member.mention}")

async def setup(bot):
    await bot.add_cog(levels(bot))