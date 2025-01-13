import math
import discord
from discord.ext import commands
from bot import LalisaBot
from random import randint
from typing import Optional, TypedDict, List, Union
from PIL import ImageDraw, Image, ImageFont
from io import BytesIO
import functools
from utils.views import Paginator
import re
import asyncio

class LevelRow(TypedDict):
    member_id: int
    xp: int
    messages: int
    bar_color: str

class Asstral(commands.Cog):
    def __init__(self, bot: LalisaBot):
        self.bot = bot
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$"
        self.channels = [1328202149401727018]
        self.guilds = [1115953206497906728]
                
    async def _register_member_levels(self, member_id: int, xp: Optional[int] = 25) -> None:
        query = '''INSERT INTO levels (member_id, messages, xp, bar_color) VALUES (?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, 1, xp, "#FFEDEF"))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def _update_message_count(self, member_id: int, levels: LevelRow) -> None:
        query = '''UPDATE levels SET messages = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, member_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def _update_xp(self, member_id: int, levels: LevelRow, xp: int) -> None:
        query = '''UPDATE levels SET messages = ?, xp = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, levels['xp'] + xp, member_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def _level_check(self, message: discord.Message, xp: int, xp_to_add: int) -> None:
        new_xp = xp + xp_to_add
        lvl = 0
        while True:
            if xp < ((50*(lvl**2))+(50*(lvl-1))):
                break
            lvl += 1
        next_level_xp = ((50*(lvl**2))+(50*(lvl-1)))
        if new_xp > next_level_xp:
            await message.channel.send(f"{message.author.mention} reached **level {lvl+1}**")

    async def _level_handler(self, message: discord.Message, retry_after: Optional[commands.CooldownMapping], xp: int) -> None:
        member_id = message.author.id
        levels = await self.get_member_levels(member_id)
        if levels == None:
            await self._register_member_levels(member_id)
        else:
            if retry_after:
                await self._update_message_count(member_id, levels)
            else:
                await self._update_xp(member_id, levels, xp)
                await self._level_check(message, levels['xp'], xp)

    async def handle_message(self, message: discord.Message) -> None:
        if message.author.bot is True: 
            return
        
        if message.guild.id not in self.guilds:
            return

        if message.channel.id not in self.channels:
            return

        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        xp_to_add = randint(8, 25)

        await self._level_handler(message, retry_after, xp_to_add)

    def _make_progress_bar(self, progress, color, circle_size=195, bar_thickness=7):
        upscale_factor = 4
        upscale_circle_size = circle_size * upscale_factor
        upscale_bar_thickness = bar_thickness * upscale_factor
        arc = Image.new('RGBA', (upscale_circle_size, upscale_circle_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(arc)
        start_angle = -math.pi / 2
        end_angle = start_angle + math.pi * 2 * progress
        if progress == 1.0:
            end_angle = -math.pi / 2
        draw.arc([upscale_bar_thickness // 2, upscale_bar_thickness // 2,
                upscale_circle_size - upscale_bar_thickness // 2, 
                upscale_circle_size - upscale_bar_thickness // 2],
                start=math.degrees(start_angle), end=math.degrees(end_angle), 
                fill=color, width=upscale_bar_thickness)
        mask = Image.new('L', (upscale_circle_size, upscale_circle_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.arc([upscale_bar_thickness // 2, upscale_bar_thickness // 2,
                    upscale_circle_size - upscale_bar_thickness // 2, 
                    upscale_circle_size - upscale_bar_thickness // 2],
                    start=math.degrees(start_angle), end=math.degrees(end_angle), 
                    fill=255, width=upscale_bar_thickness)
        arc = arc.resize((circle_size, circle_size), Image.ANTIALIAS)
        mask = mask.resize((circle_size, circle_size), Image.ANTIALIAS)
        return arc, mask
    
    def _get_round_avatar(self, avatar: BytesIO):
        circle = Image.open('./assets/circle-mask.png').resize((185, 185)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((185, 185))
        return avatar_image, circle
    
    def _human_format(self, number: int) -> str:
        number = float('{:.3g}'.format(number))
        magnitude = 0
        while abs(number) >= 1000:
            magnitude += 1
            number /= 1000.0
        return '{}{}'.format('{:f}'.format(number).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    def _xp_calculations(self, levels: LevelRow) -> tuple[float, Union[str, int], Union[str, int], int]:
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
                xp_progress_need = self._human_format(xp_progress_need)

            else:
                xp_progress_need = f"{xp_progress_need} XP"

            if xp_progress_have > 999:
                xp_progress_have = self._human_format(xp_progress_have)

        else:
            xp_progress_have = xp_have
            xp_progress_need = xp_need
            percentage = float(xp_progress_have / xp_progress_need)

        return percentage, xp_progress_have, xp_progress_need, lvl

    def _get_card(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int) -> BytesIO:
        percentage, xp_have, xp_need, level = self._xp_calculations(levels)
        card = Image.new('RGBA', size=(1000, 500), color='grey')
        bg = Image.open("./assets/rank_bg.png")
        card.paste(bg)
        message = levels["messages"]
        messages = self._human_format(message)
        bar, mask = self._make_progress_bar(percentage, levels['bar_color'])
        avatar_paste, circle = self._get_round_avatar(avatar)
        font = ImageFont.truetype("./fonts/Kaoly Demo-Regular.ttf", 30)
        font4 = ImageFont.truetype("./fonts/Kaoly Demo-Regular.ttf", 23)
        font3 = ImageFont.truetype("./fonts/Smart Duck.otf", 50)
        card.paste(bar, (45, 35), mask)
        card.paste(avatar_paste, (50, 40), circle)
        draw = ImageDraw.Draw(card, 'RGBA')
        draw.text((250, 80), f"{name}", "#ffffff", font=font)
        draw.text((250, 120), f"astral levels", "#ffffff", font=font4)
        draw.text((195, 367), f'{xp_have} / {xp_need}', "#ffffff", font=font3)
        draw.text((650, 367), f"MESSAGES {messages}", "#ffffff", font=font3)
        draw.text((222, 302), f"LEVEL {level}", "#ffffff", font=font3)
        draw.text((680, 302), f"RANK #{str(rank)}", "#ffffff", font=font3)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def get_member_levels(self, member_id: int) -> Optional[LevelRow]:
        query = '''SELECT * from levels WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id))
                row = await cursor.fetchone()
                if row:
                    return row
                else:
                    return None

    async def add_xp(self, member_id: int, xp: int, levels: Optional[LevelRow]) -> None:
        if levels:
            query = '''UPDATE levels SET xp = ? WHERE member_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (levels['xp'] + xp, member_id))
                    await conn.commit()
                await self.bot.pool.release(conn)
        else:
            await self._register_member_levels(member_id, xp)

    async def remove_xp(self, member_id: int, xp: int, levels: LevelRow) -> None:
        query = '''UPDATE levels SET xp = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['xp'] - xp, member_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def reset_levels(self):
        query = '''UPDATE levels SET xp = 0'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_rank(self, member_id: int) -> int:
        query = '''SELECT COUNT(*) FROM levels WHERE xp > (SELECT xp FROM levels WHERE member_id = ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id))
                rank = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return rank[0] + 1

    async def generate_card(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int) -> BytesIO:
        card_generator = functools.partial(self._get_card, name, status, avatar, levels, rank)
        card = await self.bot.loop.run_in_executor(None, card_generator)
        return card

    async def get_leaderboard_stats(self) -> List[LevelRow]:
        query = '''SELECT * FROM levels ORDER BY xp DESC'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall()
        return rows
                
    async def set_rank_color(self, member: discord.Member, color: str) -> None:
        query = '''UPDATE levels SET bar_color = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, color, member.id)
                await conn.commit()
            await self.bot.pool.release(conn)

    @commands.command(aliases=['lb'])
    async def levels(self, ctx: commands.Context):
        embeds = []
        description = ""
        rows = await self.get_leaderboard_stats()
        per_page = 5 if ctx.author.is_on_mobile() else 10

        for i, row in enumerate(rows, start=1):
            xp = row["xp"]
            lvl = 0
            while True:
                if xp < ((50*(lvl**2))+(50*(lvl-1))):
                    break
                lvl += 1
            msg = "messages" if row['messages'] != 1 else "message"

            description += f"**{i}.** <@!{row['member_id']}>\nLevel {lvl} | {row['xp']} xp | {row['messages']} {msg}\n\n"

            if i % per_page == 0 or i == len(rows):
                embed = discord.Embed(title="leaderboard", description=description, color=0xCA253B)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                embeds.append(embed)
                description = ""

        if len(embeds) > 1:
            view = Paginator(embeds)
            await ctx.send(embed=view.initial, view=view)
        else:
            await ctx.send(embed=embed)

    @commands.command(extras={"examples": ["rank", "rank candysnowy", "rank <@609515684740988959>"]})
    async def level(self, ctx: commands.Context, member: Optional[discord.Member]):
        member = member or ctx.author
        levels = await self.get_member_levels(member.id)
        rank = await self.get_rank(member.id)
        avatar_url = member.display_avatar.replace(static_format='png', size=256).url
        response = await self.bot.session.get(avatar_url)
        avatar = BytesIO(await response.read())
        avatar.seek(0)
        if levels:
            card = await self.generate_card(str(member), str(member.status), avatar, levels, rank)
            await ctx.send(file=discord.File(card, 'card.png'))
        else:
            await ctx.send(f"{member} doesn't have any levels yet!!")

    @commands.command(extras={"examples": ["rankcolor #ffffff"]})
    async def rankcolor(self, ctx: commands.Context, color: str):
        match = re.search(self.regex_hex, color)
        if match:
            await self.set_rank_color(ctx.author, color)
            embed = discord.Embed(
                title='changed your bar color!',
                description=f'your new bar color is `{color}`',
                color=0xCA253B
            )
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"`{color}` is not a valid hex color")

    @commands.command(aliases=['give', 'a'], extras={"examples": ["xp add <@609515684740988959> 1000", "xp give candysnowy 1000"]})
    async def xpadd(self, ctx: commands.Context, member: discord.Member, amount: int):
        levels = await self.get_member_levels(member.id)
        await self.add_xp(member.id, amount, levels)
        embed = discord.Embed(
            title='xp added!',
            description=f'gave `{amount}xp` to {str(member)}',
            color=0xCA253B
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=['take', 'r'], extras={"examples": ["xp remove <@609515684740988959> 1000", "xp take candysnowy 1000"]})
    async def xpremove(self, ctx: commands.Context, member: discord.Member, amount: int):
        levels = await self.get_member_levels(member.id)
        if levels:
            if amount > levels['xp']:
                await ctx.reply("you can't take away more xp than the user already has!")
            else:
                await self.remove_xp(member.id, amount, levels)
                embed = discord.Embed(
                    title='xp removed!',
                    description=f'removed `{amount}xp` from {str(member)}',
                    color=0xCA253B
                )
                await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"{str(member)} doesn't have any xp yet!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context):
        message = await ctx.reply("are you sure you want to reset the ranks? it's irreversible!")
        await message.add_reaction('👍')

        def check(reaction, user):
            return user == ctx.author and str(reaction) == '👍'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
            await self.reset_levels()
            embed = discord.Embed(
                title='success!',
                description=f'ranks have been erased.',
                color=0xCA253B
            )
            return await message.edit(content=None, embed=embed)
        except asyncio.TimeoutError:
            await message.edit(content="~~are you sure you want to reset the ranks? it's irreversible!~~\nreset has been cancelled!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.handle_message(message)

    @commands.command()
    async def help(self, ctx):
        embed=discord.Embed(title="Astral Commands", description="**+xpadd**\nAdd xp to a member\n\n**+xpremove**\nRemove xp from a member\n\n**+level**\nCheck your current level in the server\n\n**+levels**\nCheck where you are on Astral's level leaderboard\n\n**+rankcolor**\nUse a hex code to change the colour of the progress bar\n\n**+clear**\nReset all member levels (locked for server admins)", color=0xCA253B)
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.reply(embed=embed)

async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(Asstral(bot))