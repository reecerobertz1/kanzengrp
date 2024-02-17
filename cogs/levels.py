import math
import re
import discord
from discord.ext import commands
from random import randint
from typing import Optional, TypedDict, List, Union, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO
import functools
from discord import app_commands
from PIL import Image, ImageFilter, ImageOps
import requests
from utils.views import Paginator

class LevelRow(TypedDict):
    member_id: int
    xp: int
    messages: int
    bar_color: str
    image: str

class levels(commands.Cog):
    def __init__(self, bot):
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$"
        self.bot = bot
        self.status_holder = {0: "disabled", 1: "enabled"}
        self.pool = None
        self.channels = [1125053619893440653, 1165791833222291576, 1181419043153002546, 1135247559431032833, 1184208577120960632, 1198665603897118720]
        self.guilds = [1121841073673736215]
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)

    def kanzen_cooldown(interaction: discord.Interaction) -> Optional[app_commands.Cooldown]:

        role = interaction.guild.get_role(1128460924886458489)
        if role in interaction.user.roles:
            return commands.Cooldown(1, 43200)
        
        return commands.Cooldown(1, 86400)

    async def register_guild(self, guild_id: int) -> None:
        query = '''INSERT INTO setup (guild_id) VALUES (?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def add_member(self, member_id: int, guild_id: int, xp = 5) -> None:
        query = '''INSERT INTO levels (member_id, guild_id, xp , messages, bar_color) VALUES (?, ?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id, xp, 1, '#793e79'))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_messages(self, member_id: int, guild_id: int, levels: LevelRow) -> None:
        query = '''UPDATE levels SET messages = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, member_id, guild_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_xp(self, member_id: int, guild_id: int, levels: LevelRow, xp: int) -> None:
        query = '''UPDATE levels SET messages = ?, xp = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, levels['xp'] + xp, member_id, guild_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def check_levels(self, message: discord.Message, xp: int, xp_to_add: int) -> None:
        new_xp = xp + xp_to_add
        lvl = 0
        while True:
            if xp < ((50*(lvl**2))+(50*(lvl-1))):
                break
            lvl += 1
        next_level_xp = ((50*(lvl**2))+(50*(lvl-1)))
        if new_xp > next_level_xp:
            await message.channel.send(f"Yay! {message.author.mention} you just reached **level {lvl+1}**")

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
                await self.update_xp(member_id, guild_id, levels, xp)
                await self.check_levels(message, levels['xp'], xp)
                silver = await self.get_silver_role_id(message.guild.id)
                if silver is not None:
                    await self.silver_role_handler(message.author, message.guild, silver)
                gold = await self.get_gold_role_id(message.guild.id)
                if gold is not None:
                    await self.gold_role_handler(message.author, message.guild, gold)
                diamond = await self.get_diamond_role_id(message.guild.id)
                if diamond is not None:
                    await self.diamond_role_handler(message.author, message.guild, diamond)
                plat = await self.get_plat_role_id(message.guild.id)
                if plat is not None:
                    await self.plat_role_handler(message.author, message.guild, plat)
                elite = await self.get_elite_role_id(message.guild.id)
                if elite is not None:
                    await self.elite_role_handler(message.author, message.guild, elite)

    async def _check_silver(self, member_id: int, guild_id: int) -> bool:
        rank = await self.get_rank(member_id, guild_id)
        return rank < 36
    
    async def _check_gold(self, member_id: int, guild_id: int) -> bool:
        rank = await self.get_rank(member_id, guild_id)
        return rank < 21
    
    async def _check_diamond(self, member_id: int, guild_id: int) -> bool:
        rank = await self.get_rank(member_id, guild_id)
        return rank < 16

    async def _check_plat(self, member_id: int, guild_id: int) -> bool:
        rank = await self.get_rank(member_id, guild_id)
        return rank < 6
    
    async def _check_elite(self, member_id: int, guild_id: int) -> bool:
        rank = await self.get_rank(member_id, guild_id)
        return rank < 4

    async def _get_silver_movedown(self, member_ids: list, guild_id: int) -> int:
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]
    
    async def _get_gold_movedown(self, member_ids: list, guild_id: int) -> int:
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]
    
    async def _get_diamond_movedown(self, member_ids: list, guild_id: int) -> int:
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]

    async def _get_plat_movedown(self, member_ids: list, guild_id: int) -> int:
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]

    async def _get_elite_movedown(self, member_ids: list, guild_id: int) -> int:
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]

    async def _get_silver(self, guild_id: int) -> int:
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 35'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def _get_gold(self, guild_id: int) -> int:
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 20'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def _get_diamond(self, guild_id: int) -> int:
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 15'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def _get_plat(self, guild_id: int) -> int:
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 5'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def _get_elite(self, guild_id: int) -> int:
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 3'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def get_member_levels(self, member_id: int, guild_id: int) -> Optional[LevelRow]:
        query = '''SELECT * from levels WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id))
                row = await cursor.fetchone()
                if row:
                    return row
                else:
                    return None

    async def get_staffrep(self, member_id: int, guild_id: int) -> Optional[LevelRow]:
        query = '''SELECT count FROM staffrep WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id))
                row = await cursor.fetchone()
                if row:
                    return row
                else:
                    return None

    async def silver_role_handler(self, member: discord.Member, guild: discord.Guild, role_id: int) -> None:
        check = await self._check_silver(member.id, guild.id)
        if check is True:
            role = member.get_role(role_id)
            if role is None:
                role = guild.get_role(role_id)
                await member.add_roles(role, reason=f'{str(member)} made it to silver rank!')
                if len(role.members) > 36:
                    mem_ids = []
                    for member in role.members:
                        mem_ids.append(member.id)
                    member_movedown_id = await self._get_silver_movedown(mem_ids, guild.id)
                    remove_member = guild.get_member(member_movedown_id)
                    if remove_member is None:
                        remove_member = await guild.fetch_member(member_movedown_id)
                    await remove_member.remove_roles(role, reason=f'{str(remove_member)} dropped out of silver rank!')
                    
        if check is False:
            role = member.get_role(role_id)
            if role is not None: 
                await member.remove_roles(role, reason=f'{str(member)} dropped out of silver rank!')
                add_mem_id = await self._get_silver(guild.id)
                add_member = guild.get_member(add_mem_id)
                if add_member is None:
                    add_member = await guild.fetch_member(add_mem_id)
                await add_member.add_roles(role, reason=f'{str(add_member)} made it to silver rank!')

    async def gold_role_handler(self, member: discord.Member, guild: discord.Guild, role_id: int) -> None:
        check = await self._check_gold(member.id, guild.id)
        if check is True:
            role = member.get_role(role_id)
            if role is None:
                role = guild.get_role(role_id)
                await member.add_roles(role, reason=f'{str(member)} made it to gold rank!')
                if len(role.members) > 21:
                    mem_ids = []
                    for member in role.members:
                        mem_ids.append(member.id)
                    member_movedown_id = await self._get_gold_movedown(mem_ids, guild.id)
                    remove_member = guild.get_member(member_movedown_id)
                    if remove_member is None:
                        remove_member = await guild.fetch_member(member_movedown_id)
                    await remove_member.remove_roles(role, reason=f'{str(remove_member)} dropped out of gold rank!')
                    
        if check is False:
            role = member.get_role(role_id)
            if role is not None: 
                await member.remove_roles(role, reason=f'{str(member)} dropped out of gold rank!')
                add_mem_id = await self._get_gold(guild.id)
                add_member = guild.get_member(add_mem_id)
                if add_member is None:
                    add_member = await guild.fetch_member(add_mem_id)
                await add_member.add_roles(role, reason=f'{str(add_member)} made it to gold rank!')

    async def diamond_role_handler(self, member: discord.Member, guild: discord.Guild, role_id: int) -> None:
        check = await self._check_diamond(member.id, guild.id)
        if check is True:
            role = member.get_role(role_id)
            if role is None:
                role = guild.get_role(role_id)
                await member.add_roles(role, reason=f'{str(member)} made it to diamond rank!')
                if len(role.members) > 16:
                    mem_ids = []
                    for member in role.members:
                        mem_ids.append(member.id)
                    member_movedown_id = await self._get_diamond_movedown(mem_ids, guild.id)
                    remove_member = guild.get_member(member_movedown_id)
                    if remove_member is None:
                        remove_member = await guild.fetch_member(member_movedown_id)
                    await remove_member.remove_roles(role, reason=f'{str(remove_member)} dropped out of diamond rank!')
                    
        if check is False:
            role = member.get_role(role_id)
            if role is not None: 
                await member.remove_roles(role, reason=f'{str(member)} dropped out of diamond rank!')
                add_mem_id = await self._get_diamond(guild.id)
                add_member = guild.get_member(add_mem_id)
                if add_member is None:
                    add_member = await guild.fetch_member(add_mem_id)
                await add_member.add_roles(role, reason=f'{str(add_member)} made it to diamond rank!')

    async def plat_role_handler(self, member: discord.Member, guild: discord.Guild, role_id: int) -> None:
        check = await self._check_plat(member.id, guild.id)
        if check is True:
            role = member.get_role(role_id)
            if role is None:
                role = guild.get_role(role_id)
                await member.add_roles(role, reason=f'{str(member)} made it to plat rank!')
                if len(role.members) > 6:
                    mem_ids = []
                    for member in role.members:
                        mem_ids.append(member.id)
                    member_movedown_id = await self._get_plat_movedown(mem_ids, guild.id)
                    remove_member = guild.get_member(member_movedown_id)
                    if remove_member is None:
                        remove_member = await guild.fetch_member(member_movedown_id)
                    await remove_member.remove_roles(role, reason=f'{str(remove_member)} dropped out of plat rank!')
                    
        if check is False:
            role = member.get_role(role_id)
            if role is not None: 
                await member.remove_roles(role, reason=f'{str(member)} dropped out of plat rank!')
                add_mem_id = await self._get_plat(guild.id)
                add_member = guild.get_member(add_mem_id)
                if add_member is None:
                    add_member = await guild.fetch_member(add_mem_id)
                await add_member.add_roles(role, reason=f'{str(add_member)} made it to plat rank!')

    async def elite_role_handler(self, member: discord.Member, guild: discord.Guild, role_id: int) -> None:
        check = await self._check_elite(member.id, guild.id)
        if check is True:
            role = member.get_role(role_id)
            if role is None:
                role = guild.get_role(role_id)
                await member.add_roles(role, reason=f'{str(member)} made it to elite rank!')
                if len(role.members) > 4:
                    mem_ids = []
                    for member in role.members:
                        mem_ids.append(member.id)
                    member_movedown_id = await self._get_elite_movedown(mem_ids, guild.id)
                    remove_member = guild.get_member(member_movedown_id)
                    if remove_member is None:
                        remove_member = await guild.fetch_member(member_movedown_id)
                    await remove_member.remove_roles(role, reason=f'{str(remove_member)} dropped out of elite rank!')
                    
        if check is False:
            role = member.get_role(role_id)
            if role is not None: 
                await member.remove_roles(role, reason=f'{str(member)} dropped out of elite rank!')
                add_mem_id = await self._get_elite(guild.id)
                add_member = guild.get_member(add_mem_id)
                if add_member is None:
                    add_member = await guild.fetch_member(add_mem_id)
                await add_member.add_roles(role, reason=f'{str(add_member)} made it to elite rank!')

    async def handle_message(self, message: discord.Message) -> None:
        if message.author.bot is True: 
            return

        if message.channel.id not in self.channels:
            return
        
        if message.guild.id not in self.guilds:
            return

        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        xp_to_add = randint(5, 15)
        await self.level_handler(message, retry_after, xp_to_add)

    def get_avatar(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        circle = Image.open('./assets/circle-mask.png').resize((200, 200)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((200, 200))
        return avatar_image, circle

    async def get_bronze_role_id(self, guild_id: int) -> Union[int, None]:
        query = '''SELECT bronze_role_id FROM setup WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                role_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if role_id is not None:
            return role_id[0]
        else:
            return None
        
    async def get_gold_role_id(self, guild_id: int) -> Union[int, None]:
        query = '''SELECT gold_role_id FROM setup WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                role_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if role_id is not None:
            return role_id[0]
        else:
            return None
        
    async def get_diamond_role_id(self, guild_id: int) -> Union[int, None]:
        query = '''SELECT diamond_role_id FROM setup WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                role_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if role_id is not None:
            return role_id[0]
        else:
            return None

    async def get_plat_role_id(self, guild_id: int) -> Union[int, None]:
        query = '''SELECT plat_role_id FROM setup WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                role_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if role_id is not None:
            return role_id[0]
        else:
            return None

    async def get_elite_role_id(self, guild_id: int) -> Union[int, None]:
        query = '''SELECT elite_role_id FROM setup WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                role_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if role_id is not None:
            return role_id[0]
        else:
            return None

    async def get_silver_role_id(self, guild_id: int) -> Union[int, None]:
        query = '''SELECT silver_role_id FROM setup WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                role_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if role_id is not None:
            return role_id[0]
        else:
            return None

    async def set_silver_role(self, guild_id: int, role_id: int) -> None:
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET silver_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_gold_role(self, guild_id: int, role_id: int) -> None:
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET gold_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_diamond_role(self, guild_id: int, role_id: int) -> None:
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET diamond_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_plat_role(self, guild_id: int, role_id: int) -> None:
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET plat_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_elite_role(self, guild_id: int, role_id: int) -> None:
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET elite_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_bronze_role(self, guild_id: int, role_id: int) -> None:
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET bronze_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

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

    def _make_progress_bar(self, progress, color, circle_size=220, bar_thickness=15):
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

    def _get_bg_image(self, url: str):
            """Gets background image"""
            image = requests.get(url, stream=True)
            b_img = Image.open(BytesIO(image.content))
            return b_img

    def get_card(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, user: discord.User) -> BytesIO:
        percentage, xp_have, xp_need, level = self.xp_calculations(levels)
        card = Image.new('RGBA', size=(750, 750), color='grey')
        if levels['image'] is not None:
            bg = self._get_bg_image(levels['image'])
            left = (bg.width - min(bg.width, bg.height)) // 2
            top = (bg.height - min(bg.width, bg.height)) // 2
            right = left + min(bg.width, bg.height)
            bottom = top + min(bg.width, bg.height)
            bg = bg.crop((left, top, right, bottom))
        else:
            bg = Image.open("./assets/rankcard.png")
        bg = bg.resize((750, 750))
        bg_blurred = bg.filter(ImageFilter.GaussianBlur(radius=20))
        mask = Image.open("./assets/boxmask.png").resize((750, 750)).convert("L")
        inverted_mask = ImageOps.invert(mask)
        bg_frosted = Image.composite(bg_blurred, Image.new("RGBA", bg.size, "white"), inverted_mask)
        bg_frosted.putalpha(inverted_mask)
        bg_rgb = bg.convert("RGB")
        bar, mask = self._make_progress_bar(percentage, levels['bar_color'])
        avatar_paste, circle = self.get_avatar(avatar)
        card.paste(bg_rgb, (0, 0))
        card.paste(bg_frosted, (0, 0), bg_frosted)
        card.paste(bar, (9, 43), mask)
        card.paste(avatar_paste, (20, 53), circle)
        Kotohogi2 = ImageFont.truetype("./fonts/IntegralCF-Regular.otf", size=32)
        Kotohogi4 = ImageFont.truetype("./fonts/IntegralCF-Regular.otf", size=45)
        Kotohogi3 = ImageFont.truetype("./fonts/IntegralCF-Regular.otf", size=27)
        rankboxes = Image.open('./assets/rankboxes.png')
        rankboxes = rankboxes.resize((750, 750))
        card.paste(rankboxes, (0, 0), rankboxes)
        diamondrank_role_id = 1187540240836087858
        has_diamondrank_role = any(role.id == diamondrank_role_id for role in user.roles)
        goldrank_role_id = 1187540222708297748
        has_goldrank_role = any(role.id == goldrank_role_id for role in user.roles)
        silverrank_role_id = 1187508615364477039
        has_silverrank_role = any(role.id == silverrank_role_id for role in user.roles)
        bronzerank_role_id = 1187508597761003572
        has_bronzerank_role = any(role.id == bronzerank_role_id for role in user.roles)
        platrank_role_id = 1187540267696398427
        has_platrank_role = any(role.id == platrank_role_id for role in user.roles)
        eliterank_role_id = 1187540294221172786
        has_eliterank_role = any(role.id == eliterank_role_id for role in user.roles)
        if has_eliterank_role:
            eliterank_role_img = Image.open('./assets/eliterank.png')
            eliterank_role_img = eliterank_role_img.resize((85, 85))
            custom_x = 75
            custom_y = 585
            card.paste(eliterank_role_img, (custom_x, custom_y), eliterank_role_img)
        elif has_platrank_role:
            platrank_role_img = Image.open('./assets/platrank.png')
            platrank_role_img = platrank_role_img.resize((85, 85))
            custom_x = 75
            custom_y = 585
            card.paste(platrank_role_img, (custom_x, custom_y), platrank_role_img)
        elif has_diamondrank_role:
            diamondrank_role_img = Image.open('./assets/diamondrank.png')
            diamondrank_role_img = diamondrank_role_img.resize((85, 85))
            custom_x = 75
            custom_y = 585
            card.paste(diamondrank_role_img, (custom_x, custom_y), diamondrank_role_img)
        elif has_goldrank_role:
            goldrank_role_img = Image.open('./assets/goldrank.png')
            goldrank_role_img = goldrank_role_img.resize((85, 85))
            custom_x = 75
            custom_y = 585
            card.paste(goldrank_role_img, (custom_x, custom_y), goldrank_role_img)
        elif has_silverrank_role:
            silverrank_role_img = Image.open('./assets/silverrank.png')
            silverrank_role_img = silverrank_role_img.resize((85, 85))
            custom_x = 75
            custom_y = 585
            card.paste(silverrank_role_img, (custom_x, custom_y), silverrank_role_img)
        elif has_bronzerank_role:
            bronzerank_role_img = Image.open('./assets/bronzerank.png')
            bronzerank_role_img = bronzerank_role_img.resize((85, 85))
            custom_x = 75
            custom_y = 585
            card.paste(bronzerank_role_img, (custom_x, custom_y), bronzerank_role_img)
        lead_role_id = 1121842279351590973
        has_lead_role = any(role.id == lead_role_id for role in user.roles)
        if has_lead_role:
            special_role_img = Image.open('./assets/lead.png')
            special_role_img = special_role_img.resize((65, 65))
            custom_x = 135
            custom_y = 540
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        hstaff_id = 1178924350523588618
        has_hstaff_role = any(role.id == hstaff_id for role in user.roles)
        if has_hstaff_role:
            special_role_img = Image.open('./assets/hstaff.png')
            special_role_img = special_role_img.resize((80, 80))
            custom_x = 17
            custom_y = 535
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        staff_role_id = 1135244903165722695
        has_staff_role = any(role.id == staff_role_id for role in user.roles)
        if has_staff_role:
            staff_role_img = Image.open('./assets/staff.png')
            staff_role_img = staff_role_img.resize((65, 65))
            custom_x = 135
            custom_y = 485
            card.paste(staff_role_img, (custom_x, custom_y), staff_role_img)
        mods_id = 1135244903165722695
        mods_role = any(role.id == mods_id for role in user.roles)
        if mods_role:
            mods_img = Image.open('./assets/mods.png')
            mods_img = mods_img.resize((65, 65))
            custom_x = 25
            custom_y = 485
            card.paste(mods_img, (custom_x, custom_y), mods_img)
        devs_id = 1179255802003988573
        devs_role = any(role.id == devs_id for role in user.roles)
        if devs_role:
            devs_img = Image.open('./assets/devs.png')
            devs_img = devs_img.resize((55, 55))
            custom_x = 140
            custom_y = 437
            card.paste(devs_img, (custom_x, custom_y), devs_img)
        booster_role_id = 1128460924886458489
        has_booster_role = any(role.id == booster_role_id for role in user.roles)
        if has_booster_role:
            booster_role_img = Image.open('./assets/booster.png')
            booster_role_img = booster_role_img.resize((65, 65))
            custom_x = 25
            custom_y = 435
            card.paste(booster_role_img, (custom_x, custom_y), booster_role_img)
        top20_role_id = 1189632052727906376
        has_top20_role = any(role.id == top20_role_id for role in user.roles)
        if has_top20_role:
            top20_role_img = Image.open('./assets/top20.png')
            top20_role_img = top20_role_img.resize((65, 65))
            custom_x = 135
            custom_y = 375
            card.paste(top20_role_img, (custom_x, custom_y), top20_role_img)
        zennies_role_id = 1121842393994494082
        has_zennies_role = any(role.id == zennies_role_id for role in user.roles)
        if has_zennies_role:
            zennies_role_img = Image.open('./assets/zennies.png')
            zennies_role_img = zennies_role_img.resize((65, 65))
            custom_x = 25
            custom_y = 375
            card.paste(zennies_role_img, (custom_x, custom_y), zennies_role_img)
        draw = ImageDraw.Draw(card, 'RGBA')
        shadow_text = Image.new("RGBA", card.size, (36, 36, 36, 0))
        shadow_draw = ImageDraw.Draw(shadow_text)
        shadow_draw.text((12, 327), name, "#242424", font=Kotohogi3)
        shadow_blurred = shadow_text.filter(ImageFilter.GaussianBlur(radius=0.5))
        card.paste(shadow_blurred, (0, 0), shadow_blurred)
        draw.text((10, 325), name, fill=levels['bar_color'], font=Kotohogi3)
        draw.text((275, 620), f'{xp_have}/{xp_need}', '#ffffff', font=Kotohogi2)
        draw.text((76, 115), f'LVL','#ffffff', font=Kotohogi4)
        draw.text((185, 680), f'Messages', '#ffffff', font=Kotohogi3)
        draw.text((70, 680), f'#{str(rank)}', fill=levels['bar_color'], font=Kotohogi3)
        draw.text((89, 165), f'{level}', fill=levels['bar_color'], font=Kotohogi4)
        draw.text((365, 680), f'{levels["messages"]}', fill=levels['bar_color'], font=Kotohogi3)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def generate_card_rank1(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, member: discord.Member) -> BytesIO:
        card_generator = functools.partial(self.get_card, name, status, avatar, levels, rank)
        card = await self.bot.loop.run_in_executor(None, self.get_card, str(member), str(member.status), avatar, levels, rank, member)
        return card

    async def get_rank(self, member_id: int, guild_id: int) -> int:
        query = '''SELECT COUNT(*) FROM levels WHERE guild_id = ? AND xp > (SELECT xp FROM levels WHERE member_id = ? AND guild_id = ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (guild_id, member_id, guild_id))
                rank = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return rank[0] + 1

    async def reset_levels(self, guild_id: int) -> None:
        query = '''UPDATE levels SET xp = 0, messages = 0 WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def add_xp(self, member_id: int, guild_id: int, xp: int, levels: Optional[LevelRow]) -> None:
        if levels:
            query = '''UPDATE levels SET xp = ? WHERE member_id = ? AND guild_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (levels['xp'] + xp, member_id, guild_id))
                    await conn.commit()
                await self.bot.pool.release(conn)
        else:
            await self.add_member(member_id, guild_id, xp)

    async def remove_xp(self, member_id: int, guild_id: int, xp: int, levels: LevelRow) -> None:
        query = '''UPDATE levels SET xp = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['xp'] - xp, member_id, guild_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_leaderboard_stats(self, guild_id: int) -> List[LevelRow]:
        query = '''SELECT * FROM levels WHERE guild_id = ? ORDER BY xp DESC'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                rows = await cursor.fetchall()
        return rows
    
    async def set_rank_color(self, member_id: int, guild_id: int, color: str) -> None:
        query = '''UPDATE levels SET bar_color = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, color, member_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    @app_commands.command(name="rank", description="Check your rank")
    async def rank(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        member = member or interaction.user
        levels = await self.get_member_levels(member.id, interaction.guild_id)
        rank = await self.get_rank(member.id, interaction.guild_id)
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
        levels = await self.get_member_levels(member.id, interaction.guild_id)
        await self.add_xp(member.id, interaction.guild_id, amount, levels)
        embed = discord.Embed(title='xp added!',description=f'gave `{amount}xp` to {str(member)}',color=0x2b2d31)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove", description="Remove xp from someone", extras="+remove @member amount")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        levels = await self.get_member_levels(member.id, interaction.guild_id)
        if levels:
            if amount > levels['xp']:
                await interaction.response.send_message("you can't take away more xp than the user already has!")
            else:
                await self.remove_xp(member.id, interaction.guild_id, amount, levels)
                embed = discord.Embed(title='xp removed!',description=f'removed `{amount}xp` from {str(member)}',color=0x2b2d31)
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{str(member)} doesn't have any xp yet!")

    @app_commands.command(description="See the level leaderboard")
    async def leaderboard(self, interaction: discord.Interaction):
        embeds = []
        description = ""
        rows = await self.get_leaderboard_stats(interaction.guild_id)
        per_page = 5 if interaction.user.is_on_mobile() else 10
        for i, row in enumerate(rows, start=1):
            msg = "messages" if row['messages'] != 1 else "message"
            xp = row["xp"]
            lvl = 0
            while True:
                if xp < ((50*(lvl**2))+(50*(lvl-1))):
                    break
                lvl += 1
            description += f"**{i}.** <@!{row['member_id']}>\n<:Empty:1188186122350759996><:1166196258499727480:1188190249768210582>**level {lvl} | {row['messages']} {msg}**\n\n"
            if i % per_page == 0 or i == len(rows):
                embed = discord.Embed(title=f"{interaction.guild.name}'s leaderboard", description=description, color=0x2b2d31)
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
        match = re.search(self.regex_hex, color)
        if match:
            await self.set_rank_color(interaction.user.id, interaction.guild_id, color)
            embed = discord.Embed(
                title='changed your bar color!',
                description=f'your new bar color is `{color}`',
                color=0x2B2D31
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"`{color}` is not a valid hex color")

    @app_commands.command(name="rankbg", description="Attach an image when using this command!")
    async def rankbg(self, interaction: discord.Interaction, image: discord.Attachment):
        if not image.content_type.split("/")[0] == "image":
            await interaction.response.send_message("Please attach a valid image (PNG, JPG, JPEG, GIF).")
            return
        member_id = interaction.user.id
        async with self.bot.pool.acquire() as conn:
            query = "UPDATE levels SET image = ? WHERE member_id = ? AND guild_id = ?"
            await conn.execute(query, (image.url, member_id, interaction.guild_id))
            await conn.commit()
        embed = discord.Embed(title="Rank background has been updated!", color=0x2b2d31)
        embed.set_image(url=image.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reset", description="Resets everyone's xp")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reset(self, interaction: discord.Interaction):
        await self.reset_levels(interaction.guild_id)
        await interaction("All levels have been reset! All members are back to level 1 with 0 messages")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.handle_message(message)

    @app_commands.command(description="Get anywhere from 100xp - 300xp everyday!")
    @app_commands.checks.dynamic_cooldown(kanzen_cooldown)
    async def daily(self, interaction: discord.Interaction):
        xp = randint(100, 300)
        levels = await self.get_member_levels(interaction.user.id, interaction.guild_id)
        if levels is not None:
            await self.add_xp(interaction.user.id, interaction.guild_id, xp, levels)
        else:
            await self.add_member(interaction.user.id, interaction.guild_id, xp)
        await interaction.response.send_message(f"You claimed your daily xp! you got **{xp}xp**")

    @app_commands.command(name="setbronze", description="Set bronze role")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setbronze(self, interaction: discord.Interaction, role: discord.Role):
        bronze_role_id = role.id
        await self.register_guild(interaction.guild_id)
        await self.set_bronze_role(interaction.guild_id, bronze_role_id)
        for member in interaction.guild.members:
            if member.bot:
                continue
            try:
                await member.add_roles(role, reason=f'Setting Bronze role for all human members.')
            except Exception as e:
                print(f"Error adding Bronze role to {member}: {e}")

        embed = discord.Embed(
            title='Bronze role has been set!',
            description=f'Bronze role has been set for all human members to {role.mention}!',
            color=0x2B2D31
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setsilver", description="Set silver role")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setsilver(self, interaction: discord.Interaction, role: discord.Role):
        await self.register_guild(interaction.guild_id)
        await self.set_silver_role(interaction.guild_id, role.id)
        embed = discord.Embed(
            title='silver role has been set!',
            description=f'members ranked silver will receive the {role.mention} role!',
            color=0x2B2D31
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setgold", description="Set gold role")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setgold(self, interaction: discord.Interaction, role: discord.Role):
        await self.set_gold_role(interaction.guild_id, role.id)
        embed = discord.Embed(
            title='gold role has been set!',
            description=f'members ranked gold will receive the {role.mention} role!',
            color=0x2B2D31
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setdiamond", description="Set diamond role")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setdiamond(self, interaction: discord.Interaction, role: discord.Role):
        await self.set_diamond_role(interaction.guild_id, role.id)
        embed = discord.Embed(
            title='diamond role has been set!',
            description=f'members ranked diamond will receive the {role.mention} role!',
            color=0x2B2D31
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setplatinum", description="Set platinum role")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setplat(self, interaction: discord.Interaction, role: discord.Role):
        await self.set_plat_role(interaction.guild_id, role.id)
        embed = discord.Embed(
            title='plat role has been set!',
            description=f'members ranked plat will receive the {role.mention} role!',
            color=0x2B2D31
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="setelite", description="Set elite role")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setelite(self, interaction: discord.Interaction, role: discord.Role):
        await self.set_elite_role(interaction.guild_id, role.id)
        embed = discord.Embed(
            title='elite role has been set!',
            description=f'members ranked elite will receive the {role.mention} role!',
            color=0x2B2D31
        )
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.register_guild(guild.id)

async def setup(bot):
    await bot.add_cog(levels(bot))