import datetime as dt
from datetime import datetime, timedelta
import textwrap
import discord
from discord.ext import commands, tasks
from bot import LalisaBot
from random import randint
from typing import Optional, TypedDict, List, Union, Tuple
from PIL import ImageDraw, Image, ImageFont, ImageColor, ImageFilter, ImageEnhance, ImageOps
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
        self.embed_colour = 0xCA253B
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$"
        self.channels = [1115953207898820660, 1116540790139781251, 1328202149401727018, 1138631181257146379, 1115962090092507207, 1115959285818589226 ,1116901595423199306]
        self.guilds = [1115953206497906728]
        self.role = 1116511748875362346
                
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
            channel = self.bot.get_channel(1115958863993241700)
            await channel.send(f"{message.author.mention} reached **level {lvl+1}** <:pompom_heart:1227493111836708884>")

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
        if message.author.bot:
            return

        if message.guild.id not in self.guilds:
            return

        if message.channel.id not in self.channels:
            return

        if self.role not in [role.id for role in message.author.roles]:
            return

        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        xp_to_add = randint(8, 25)

        await self._level_handler(message, retry_after, xp_to_add)

    def _make_progress_bar(self, progress: float, color, color2="#ffffff"):
        width = 1360
        height = 11
        radius = 100

        if isinstance(color, str):
            color = ImageColor.getcolor(color, "RGBA")
        elif len(color) == 3:
            color = (*color, 255)

        if isinstance(color2, str):
            color2 = ImageColor.getcolor(color2, "RGBA")
        elif len(color2) == 3:
            color2 = (*color2, 255)

        def interpolate_color(c1, c2, factor):
            r = int(c1[0] + (c2[0] - c1[0]) * factor)
            g = int(c1[1] + (c2[1] - c1[1]) * factor)
            b = int(c1[2] + (c2[2] - c1[2]) * factor)
            a = int(c1[3] + (c2[3] - c1[3]) * factor)
            return (r, g, b, a)

        progress_width = int(width * progress)

        if progress_width == 0:
            return Image.new("RGBA", (1, height), (0, 0, 0, 0)), None

        gradient = Image.new('RGBA', (progress_width, height), (0, 0, 0, 0))
        gradient_draw = ImageDraw.Draw(gradient)

        segments = progress_width
        for i in range(segments):
            t = i / segments
            color = interpolate_color(color, color2, t)
            gradient_draw.line([(i, 0), (i, height)], fill=color)

  
        mask = Image.new('L', (progress_width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (progress_width, height)], fill=255, radius=radius)
        rounded_gradient = Image.new("RGBA", (progress_width, height), (0, 0, 0, 0))
        rounded_gradient.paste(gradient, (0, 0), mask)

        return rounded_gradient, mask
    
    def get_avatar(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        circle = Image.open('./assets/circle-mask.png').resize((102, 102)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((102, 102))
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

    def draw_centered_text(self, draw: ImageDraw.ImageDraw,levels: LevelRow, text: str, font: ImageFont.FreeTypeFont, *, x_center: int, y_start: int, line_spacing: int = 5):
        """Draws multiline text centered at x_center, starting from y_start."""
        lines = text.split('\n')
        for line in lines:
            text_width, text_height = draw.textsize(line, font=font)
            x_position = x_center - text_width // 2
            draw.text((x_position, y_start), line, font=font, fill=levels["bar_color"])
            y_start += text_height + line_spacing

    def draw_centered_text2(self, draw: ImageDraw.ImageDraw,levels: LevelRow, text: str, font: ImageFont.FreeTypeFont, *, x_center: int, y_start: int, line_spacing: int = 5):
        """Draws multiline text centered at x_center, starting from y_start."""
        lines = text.split('\n')
        for line in lines:
            text_width, text_height = draw.textsize(line, font=font)
            x_position = x_center - text_width // 2
            draw.text((x_position, y_start), line, font=font, fill="#ffffff")
            y_start += text_height + line_spacing    

    def _get_card(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int) -> BytesIO:
        percentage, xp_have, xp_need, level = self._xp_calculations(levels)
        card = Image.new('RGBA', size=(1500, 500), color='grey')
        bg = Image.open("./assets/astral/rankcard.png")

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
        bg_dark = dark.enhance(0.7)
        bg_blurred = bg_dark.filter(ImageFilter.GaussianBlur(radius=20))
        mask = Image.open("./assets/astral/rank_mask.png").resize((1500, 500)).convert("L")
        inverted_mask = ImageOps.invert(mask)
        bg_frosted = Image.composite(bg_blurred, Image.new("RGBA", bg.size, "white"), inverted_mask)
        bg_frosted.putalpha(inverted_mask)
        bar, mask_bar = self._make_progress_bar(percentage, levels['bar_color'])
        avatar_paste, circle = self.get_avatar(avatar)
        card.paste(bg, (0, 0))
        card.paste(bg_frosted, (0, 0), bg_frosted)
        card.paste(bar, (70, 459), mask_bar)
        card.paste(avatar_paste, (59, 64), circle)
        message = levels["messages"]
        messages = self._human_format(message)
        bar, mask = self._make_progress_bar(percentage, levels['bar_color'])
        avatar_paste, circle = self.get_avatar(avatar)
        regular_size20 = ImageFont.truetype("./fonts/Regular.otf", size=20)
        bold_size23 = ImageFont.truetype("./fonts/Bold.otf", size=23)
        black_size20 = ImageFont.truetype("./fonts/Black.otf", size=20)
        black_size27 = ImageFont.truetype("./fonts/Black.otf", size=27)
        black_size32 = ImageFont.truetype("./fonts/Black.otf", size=32)
        bar, mask_bar = self._make_progress_bar(percentage, levels['bar_color'])
        draw = ImageDraw.Draw(card, 'RGBA')

        ranked = f"#{str(rank)}"
        levelled = f"{level}"
        xp = f"{xp_have}/{xp_need}"
        msgs = f"{levels['messages']}"

        wrapped_rank = "\n".join(textwrap.fill(line, width=75) for line in ranked.splitlines())
        self.draw_centered_text2(draw, text=wrapped_rank, font=bold_size23, x_center=201, y_start=400, levels=levels)

        wrapped_levels = "\n".join(textwrap.fill(line, width=75) for line in levelled.splitlines())
        self.draw_centered_text2(draw, text=wrapped_levels, font=bold_size23, x_center=95, y_start=400, levels=levels)

        wrapped_messages = "\n".join(textwrap.fill(line, width=75) for line in msgs.splitlines())
        self.draw_centered_text2(draw, text=wrapped_messages, font=bold_size23, x_center=331, y_start=400, levels=levels)

        wrapped_xp = "\n".join(textwrap.fill(line, width=75) for line in xp.splitlines())
        self.draw_centered_text2(draw, text=wrapped_xp, font=bold_size23, x_center=482, y_start=400, levels=levels)

        draw.text((172, 84), f"{name}", fill=levels['bar_color'], font=black_size32)
        draw.text((72, 380), f"level", fill=levels['bar_color'], font=black_size20)
        draw.text((180, 380), f"rank", fill=levels['bar_color'], font=black_size20)
        draw.text((283, 380), f"messages", fill=levels['bar_color'], font=black_size20)
        draw.text((471, 380), f"xp", fill=levels['bar_color'], font=black_size20)
        draw.text((172, 116), f"Astral Levels", fill="#ffffff", font=bold_size23)
        draw.text((1250, 10), f"hoshi | made by chromagrp", fill="#ffffff", font=regular_size20)
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

    @commands.command()
    async def levels(self, ctx: commands.Context):
        required_role_id = self.role
        role = ctx.guild.get_role(required_role_id)
        if role not in ctx.author.roles:
            return await ctx.reply("Hello! You aren't a member on Astral. Only members can use Hoshi's levels <3")
        
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
                embed = discord.Embed(title="leaderboard", description=description, color=self.embed_colour)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                embeds.append(embed)
                description = ""

        if len(embeds) > 1:
            view = Paginator(embeds)
            await ctx.send(embed=view.initial, view=view)
        else:
            await ctx.send(embed=embed)

    @commands.command()
    async def level(self, ctx: commands.Context, member: Optional[discord.Member]):
        required_role_id = self.role
        role = ctx.guild.get_role(required_role_id)
        if role not in ctx.author.roles:
            return await ctx.reply("Hello! You aren't a member on Astral. Only members can use Hoshi's levels <3")
        
        async with ctx.typing():
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

    @commands.command()
    async def colour(self, ctx: commands.Context, color: str):
        required_role_id = self.role
        role = ctx.guild.get_role(required_role_id)
        if role not in ctx.author.roles:
            return await ctx.reply("Hello! You aren't a member on Astral. Only members can use Hoshi's levels <3")
        
        match = re.search(self.regex_hex, color)
        if match:
            await self.set_rank_color(ctx.author, color)
            embed = discord.Embed(
                title='changed your bar color!',
                description=f'your new bar color is `{color}`',
                color=self.embed_colour
            )
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"`{color}` is not a valid hex color")

    @commands.command()
    async def xpadd(self, ctx: commands.Context, member: discord.Member, amount: int):
        required_role_id = self.role
        role = ctx.guild.get_role(required_role_id)
        if role not in ctx.author.roles:
            return await ctx.reply("Hello! You aren't a member on Astral. Only members can use Hoshi's levels <3")
        
        levels = await self.get_member_levels(member.id)
        await self.add_xp(member.id, amount, levels)
        embed = discord.Embed(
            title='xp added!',
            description=f'gave `{amount}xp` to {str(member)}',
            color=self.embed_colour
        )
        await ctx.reply(embed=embed)

    @commands.command()
    async def xpremove(self, ctx: commands.Context, member: discord.Member, amount: int):
        required_role_id = self.role
        role = ctx.guild.get_role(required_role_id)
        if role not in ctx.author.roles:
            return await ctx.reply("Hello! You aren't a member on Astral. Only members can use Hoshi's levels <3")
        
        levels = await self.get_member_levels(member.id)
        if levels:
            if amount > levels['xp']:
                await ctx.reply("you can't take away more xp than the user already has!")
            else:
                await self.remove_xp(member.id, amount, levels)
                embed = discord.Embed(
                    title='xp removed!',
                    description=f'removed `{amount}xp` from {str(member)}',
                    color=self.embed_colour
                )
                await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"{str(member)} doesn't have any xp yet!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def erase(self, ctx: commands.Context):
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
                color=self.embed_colour
            )
            return await message.edit(content=None, embed=embed)
        except asyncio.TimeoutError:
            await message.edit(content="~~are you sure you want to reset the ranks? it's irreversible!~~\nreset has been cancelled!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.handle_message(message)
        
    @commands.command()
    async def astralhelp(self, ctx):
        required_role_id = self.role
        role = ctx.guild.get_role(required_role_id)
        if role not in ctx.author.roles:
            return await ctx.reply("Hello! You aren't a member on Astral. Only members can use Hoshi's levels <3")

        embed = discord.Embed(
            description=(
                "### Astral Commands\n"
                "Below are all available commands for Astral's levels, sorted by who can use them.\n"
                "If you need any help, please ping the bot developer!\n"
                "\n"
                "### 🌸 Member Commands\n"
                "### **+level**\n"
                "```+level | +level @member```\n"
                "### **+levels**\n"
                "```+levels shows leaderboard```\n"
                "### **+colour**\n"
                "```+colour #000000 (hex codes only)```\n"
                "\n"
                "### 🛠️ Staff Commands\n"
                "### **+xpadd**\n"
                "```+xpadd @member xp```\n"
                "### **+xpremove**\n"
                "```+xpremove @member xp```\n"
                "### **+erase**\n"
                "```+erase (will ask for confirmation)```"
            ),
            color=self.embed_colour
        )
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel = self.bot.get_channel(1115958863993241700)
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
            guild = self.bot.get_guild(694010548605550675)
            member = guild.get_member(member_id) if guild else None
            if member and member.voice and len(member.voice.channel.members) > 1:
                if not member.voice.self_mute and not member.voice.self_deaf:
                    self.xp_tracker[member_id] += 1

    @gain_xp.before_loop
    async def before_gain_xp(self):
        await self.bot.wait_until_ready()

    async def check_level_for_logos(self, ctx, member: discord.Member, message: discord.Message):
        levels = await self.get_member_levels(member.id, ctx.guild.id)
        required_level = 2

        xp = levels["xp"]
        lvl = 0
        while True:
            if xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                break
            lvl += 1

        role_id = 1312344613926862909
        rep_role = ctx.guild.get_role(role_id)

        if lvl >= required_level and rep_role not in member.roles:
            await member.add_roles(rep_role)
            await message.channel.send(
                f"Congrats {member.mention}! You have unlocked logos!\n"
                "The role should be automatically added. If not, please ping a staff member!"
            )

async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(Asstral(bot))