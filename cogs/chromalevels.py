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

class EventRow(TypedDict):
    member_id: int
    rank_decors: int
    selected: int
    candy: int

class chromalevels(commands.Cog):
    def __init__(self, bot):
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$"
        self.bot = bot
        self.status_holder = {0: "disabled", 1: "enabled"}
        self.pool = None
        self.channels = [1294028622490767360, 694010549532360726, 725664181428420638, 1157492645086646384, 837290581369683998, 837290581369683998, 1288496930757808201, 1078444175848116285, 1271565278282780684, 1279623211008397324, 1279623242688106608, 1279623277555351593, 1279623313810915423, 1279623356848803862, 1279623396354818058, 1279623456798801990, 1279623499081711667, 1279623538474750014, 1279623582132998144, 1279623615213600829, 1279623652274343938, 1279623689440333865, 1279623728191246408, 1279623770981531729, 1279623800018960425, 1279623838434459648, 1279623869015003137, 1279623908550508616, 1279623936338038904, 1279622704084811776]
        self.guilds = [694010548605550675, 1157492644402970744]
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)

    def kanzen_only():
        def predicate(ctx: commands.Context):
            if ctx.guild.id == 694010548605550675:
                return True
            else:
                return False
        return commands.check(predicate)
    
    def kanzen_cooldown(message: discord.Message):
        if message.author.id == 609515684740988959:
            return None
        
        role = message.guild.get_role(694016195090710579)
        if role in message.author.roles:
            return commands.Cooldown(1, 86400)
        
        booster = message.guild.get_role(728684846846574703)
        if booster in message.author.roles:
            return commands.Cooldown(1, 43200)
        
        return commands.Cooldown(1, 86400)

    async def add_member(self, member_id: int, xp=5) -> None:
        query = '''INSERT INTO chromalevels (member_id, xp, messages, color) VALUES (?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, xp, 1, '#c45a72'))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_messages(self, member_id: int, levels: LevelRow) -> None:
        query = '''UPDATE chromalevels SET messages = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_xp(self, member_id: int, levels: LevelRow, xp: int) -> None:
        query = '''UPDATE chromalevels SET messages = ?, xp = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, levels['xp'] + xp, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_member_levels(self, member_id: int) -> Optional[LevelRow]:
        query = '''SELECT * from chromalevels WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, ))
                row = await cursor.fetchone()
                if row:
                    return row
                else:
                    return None

    async def get_event_details(self, member_id: int) -> Optional[LevelRow]:
        query = '''SELECT * from inventory WHERE member_id = ?'''
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
            await self.add_member_event(message.author.id)
            await self.update_candy(message.author.id)
            await message.channel.send(f"Yay! {message.author.mention} you just reached **level {lvl}**\nYou also found🍬 **2**")

    async def add_member_event(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT 1 FROM inventory WHERE member_id = ?", (member_id,))
                existing_member = await cursor.fetchone()
                if existing_member is not None:
                    return
                
                query = '''INSERT INTO inventory(member_id, rank_decors, selected, candy) VALUES (?, ?, ?, ?)'''
                await cursor.execute(query, (member_id, 0, 0, 2))
                await conn.commit()

    async def candy(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT candy FROM inventory WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

    async def update_candy(self, member_id: int) -> None:
        query = '''UPDATE inventory SET candy = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                candy = await self.candy(member_id)
                await cursor.execute(query, (candy + 2, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

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

        zennie_role_id = 694016195090710579
        forms_zennie_role_id = 836244165637046283
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

    async def set_card_image(self, image: BytesIO, member_id: int, colorchange: Optional[bool] = False) -> None:
        query = "UPDATE chromalevels SET image = $1, color = $2 WHERE member_id = $3"
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
            new_query = "UPDATE chromalevels SET image = $1, accent_color = $4, color = $5 WHERE member_id = $2"
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(new_query, bytes_data, member_id, pb_accent, pb_primary)
            await self.bot.pool.release(connection)

    def _get_bg_image(self, url: str):
            """Gets background image"""
            image = requests.get(url, stream=True)
            b_img = Image.open(BytesIO(image.content))
            return b_img

    def get_card(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, user: discord.User, guild: discord.Guild, event: EventRow) -> BytesIO:
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
        draw = ImageDraw.Draw(card, 'RGBA')
        message = levels["messages"]
        messages = self.human_format(message)

        if event is None or event["selected"] == 0 or event["selected"] is None:
            rankdecor = Image.open(f'./assets/0.png')
        else:
            rankdecor = Image.open(f'./assets/{event["selected"]}.png')

        rankdecor = rankdecor.resize((1500, 500))
        card.paste(rankdecor, (0, 0), rankdecor)
        
        draw.text((100, 345), f'{xp_have} | {xp_need}', fill=levels['color'], font=zhcn)
        draw.text((225, 25), f"{user.name}", fill=levels['color'], font=zhcn)
        draw.text((225, 65), f"chroma levels", fill=levels['color'], font=zhcn2)
        draw.text((300, 407), f'rank | {str(rank)}', fill=levels['color'], font=zhcn)
        draw.text((100, 407), f'level | {level-1}', fill=levels['color'], font=zhcn)
        draw.text((500, 407), f'{messages} messages', fill=levels['color'], font=zhcn)
        
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def generate_card_rank1(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, member: discord.Member, event: EventRow) -> BytesIO:
        guild = member.guild
        card_generator = functools.partial(self.get_card, name, status, avatar, levels, rank, event)
        card = await self.bot.loop.run_in_executor(None, self.get_card, str(member), str(member.status), avatar, levels, rank, member, guild, event)
        return card

    async def get_rank(self, member_id: int) -> int:
        query = '''SELECT COUNT(*) FROM chromalevels WHERE xp > (SELECT xp FROM chromalevels WHERE member_id = ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id))
                rank = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return rank[0] + 1

    async def reset_levels(self) -> None:
        query = '''UPDATE chromalevels SET xp = 0, messages = 0'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, )
                await conn.commit()
            await self.bot.pool.release(conn)

    async def add_xp(self, member_id: int, xp: int, levels: Optional[LevelRow]) -> None:
        if levels:
            current_xp = levels['xp']
            new_xp = current_xp + xp

            query = '''UPDATE chromalevels SET xp = ? WHERE member_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (new_xp, member_id))
                    await conn.commit()
        else:
            await self.add_member(member_id, xp)

    async def remove_xp(self, member_id: int, xp: int, levels: LevelRow) -> None:
        query = '''UPDATE chromalevels SET xp = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['xp'] - xp, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_rank_color(self, member_id: int, color: str) -> None:
        query = '''UPDATE chromalevels SET color = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, color, member_id, )
                await conn.commit()
            await self.bot.pool.release(conn)

    @commands.command(description="Check your rank")
    @kanzen_only()
    async def rank(self, ctx: commands.Context, member: Optional[discord.Member]):
        async with ctx.typing():
            """makes a rank card"""
            member = member or ctx.author
            event = await self.get_event_details(member.id)
            levels = await self.get_member_levels(member.id)
            rank = await self.get_rank(member.id)
            avatar_url = member.display_avatar.replace(static_format='png', size=256).url
            response = await self.bot.session.get(avatar_url)
            avatar = BytesIO(await response.read())
            avatar.seek(0)
            if levels:
                card = await self.generate_card_rank1(str(member), str(member.status), avatar, levels, rank, member, event)
                await ctx.reply(file=discord.File(card, 'card.png'), mention_author=False)
            else:
                await ctx.reply(f"{member} doesn't have any levels yet!!", mention_author=False)

    @commands.command()
    @kanzen_only()
    async def multiadd(self, ctx: commands.Context, members: commands.Greedy[discord.Member], amount: int):
        zennie_role_id = 739513680860938290
        author = ctx.author
        
        if zennie_role_id not in [role.id for role in author.roles]:
            await ctx.reply("Sorry, this is a staff only command", ephemeral=True)
            return
        
        if not members:
            await ctx.send("You must mention at least one member to add XP to.")
            return
        description = f'Gave `{amount}xp` to {", ".join(str(member) for member in members if isinstance(member, discord.Member))}'
        embed = discord.Embed(
            title='xp added!',
            description=description,
            color=0x2B2D31
        )
        for member in members:
            if isinstance(member, discord.Member):
                levels = await self.get_member_levels(member.id)
                await self.add_xp(member.id, amount, levels)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['give', 'a'], extras={"examples": ["xp add <@609515684740988959> 1000", "xp give candysnowy 1000"]})
    @kanzen_only()
    async def add(self, ctx: commands.Context, member: discord.Member, amount: int):
        zennie_role_id = 739513680860938290
        author = ctx.author
        
        if zennie_role_id not in [role.id for role in author.roles]:
            await ctx.reply("Sorry, this is a staff only command", ephemeral=True)
            return
        
        levels = await self.get_member_levels(member.id)
        await self.add_xp(member.id, amount, levels)
        embed = discord.Embed(
            title='xp added!',
            description=f'gave `{amount}xp` to {str(member)}',
            color=0x2B2D31
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=['take', 'r'], extras={"examples": ["xp remove <@609515684740988959> 1000", "xp take candysnowy 1000"]})
    @kanzen_only()
    async def remove(self, ctx: commands.Context, member: discord.Member, amount: int):
        zennie_role_id = 739513680860938290
        author = ctx.author
        
        if zennie_role_id not in [role.id for role in author.roles]:
            await ctx.reply("Sorry, this is a staff only command", ephemeral=True)
            return
        
        levels = await self.get_member_levels(member.id)
        if levels:
            if amount > levels['xp']:
                await ctx.reply("you can't take away more xp than the user already has!")
            else:
                await self.remove_xp(member.id, amount, levels)
                embed = discord.Embed(
                    title='xp removed!',
                    description=f'removed `{amount}xp` from {str(member)}',
                    color=0x2B2D31
                )
                await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"{str(member)} doesn't have any xp yet!")

    async def get_leaderboard_stats(self) -> List[LevelRow]:
        query = '''SELECT * FROM chromalevels ORDER BY xp DESC'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall()
        return rows

    @commands.command(aliases=['lb', 'levels'], description="See the level leaderboard")
    @kanzen_only()
    async def leaderboard(self, ctx: commands.Context):
        """sends the current leaderboard"""
        embeds = []
        description = ""
        rows = await self.get_leaderboard_stats()
        per_page = 5 if ctx.author.is_on_mobile() else 10
        for i, row in enumerate(rows, start=1):
            msg = "messages" if row['messages'] != 1 else "message"
            xp = row["xp"]
            lvl = 0
            while True:
                if xp < ((50*(lvl**2))+(50*(lvl-1))):
                    break
                lvl += 1
            description += f"**{i}.** <@!{row['member_id']}>\n{row['xp']} xp | {row['messages']} {msg} | level {lvl-1}\n\n"
            if i % per_page == 0 or i == len(rows):
                embed = discord.Embed(title="leaderboard", description=description, color=0x2b2d31)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                embeds.append(embed)
                description = ""
        if len(embeds) > 1:
            view = Paginator(embeds)
            await ctx.send(embed=view.initial, view=view)
        else:
            await ctx.send(embed=embed)

    @commands.command(description="Change your rank card color with hex codes")
    @kanzen_only()
    async def rankcolor(self, ctx: commands.Context, color: str):
        match = re.search(self.regex_hex, color)
        if match:
            await self.set_rank_color(ctx.author.id, color)
            embed = discord.Embed(
                title='changed your bar color!',
                description=f'your new bar color is `{color}`',
                color=0x2B2D31
            )
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"`{color}` is not a valid hex color. make sure to add a **#** at the start!")

    @commands.command(name="rankbg", description="Upload an image when using this command!")
    async def rankbg(self, ctx: commands.Context, image: Optional[discord.Attachment] = None):
        zennie_role_id = 694016195090710579
        member = ctx.author
        
        if zennie_role_id not in [role.id for role in member.roles]:
            await ctx.send("Sorry, you cannot use this command.", ephemeral=True)
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
                            return await ctx.send("Invalid image.", ephemeral=True)
                except:
                    return await ctx.send("Couldn't get the image from the link you provided.", ephemeral=True)
            else:
                return await ctx.send("You need to use a https or http URL", ephemeral=True)
        else:
            if ctx.message.attachments:
                to_edit = ctx.message.attachments[0]
                if to_edit.content_type.split("/")[0] == "image" and not to_edit.content_type.split("/")[1] == "gif":
                    async with self.bot.session.get(to_edit.url) as resp:
                        image_data = BytesIO(await resp.read())
                        image_data.seek(0)
                else:
                    return await ctx.send("Invalid image.", ephemeral=True)
            else:
                return await ctx.send("You need to upload an image attachment or add an image URL", ephemeral=True)

        try:
            b_img = Image.open(image_data)
        except UnidentifiedImageError:
            return await ctx.send("Invalid image.", ephemeral=True)
        
        await self.set_card_image(image_data, ctx.author.id)
        await ctx.send("Successfully changed your rank card image!", ephemeral=True)

    @commands.command(name="reset", description="Resets everyone's xp")
    async def reset(self, ctx):
        zennie_role_id = 739513680860938290
        author = ctx.author
        
        if zennie_role_id not in [role.id for role in author.roles]:
            await ctx.reply("Sorry, this is a staff only command", ephemeral=True)
            return
        await self.reset_levels()
        await ctx.reply("All levels have been reset! All members are back to level 1 with 0 messages")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.handle_message(message)

    @commands.command()
    @kanzen_only()
    @commands.dynamic_cooldown(kanzen_cooldown, commands.BucketType.user)
    async def daily(self, ctx: commands.Context):
        """Command to claim daily xp"""
        xp = randint(150, 300)
        levels = await self.get_member_levels(ctx.author.id)
        if levels is not None:
            await self.add_xp(ctx.author.id, xp, levels)
        else:
            await self.add_member(ctx.member.id, xp)
        await ctx.reply(f"You claimed your daily xp! you got **{xp}xp**")
        
    @daily.error
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

    @commands.command()
    async def addmsg(self, ctx, member: discord.Member, messages: int):
        levels = await self.get_member_levels(member.id)
        await self.add_msg(member.id, messages, levels)
        await ctx.reply(f"Added **{messages}** messages to {member.mention}")

    @commands.command(hidden=True)
    async def removedata(self, ctx, member_id: int):
        guild_id = ctx.guild.id

        async with self.bot.pool.acquire() as conn:
            await conn.execute('DELETE FROM chromalevels WHERE member_id = $1', member_id)

        await ctx.send(f"<@{member_id}>'s levels have been removed!")

async def setup(bot):
    await bot.add_cog(chromalevels(bot))