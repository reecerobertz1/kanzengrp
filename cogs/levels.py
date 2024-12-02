import asyncio
import re
import discord
from discord.ext import commands
from random import randint
from typing import Optional, TypedDict, List, Union, Tuple
from PIL import Image, ImageFilter, ImageOps, ImageFont, ImageEnhance, ImageDraw
from io import BytesIO
import functools
from discord import app_commands
from PIL import Image
from utils.views import Paginator
from colorthief import ColorThief
from discord.app_commands import CommandOnCooldown
import datetime
from datetime import datetime, timedelta

class LevelRow(TypedDict):
    member_id: int
    xp: int
    messages: int
    guild_id: int
    color: str
    image: str
    decor: str

class claimxp(discord.ui.View):
    def __init__(self, amount, bot, dropper):
        super().__init__(timeout=None)
        self.bot = bot
        self.amount = amount
        self.dropper = dropper

    @discord.ui.button(label="Claim", emoji="<:key:1306072256094404698>", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="<:removal:1306071903198380082> Claimed XP", description=f"**{interaction.user.name}** has claimed `{self.amount} XP`", color=0x2b2d31)
        embed.set_footer(text=f"dropped by {self.dropper}")
        levels = await self.get_member_levels(interaction.user.id, interaction.guild.id)
        if not levels:
            await interaction.response.send_message("Could not retrieve your level data. Please try again later.", ephemeral=True)
            return

        current_xp = levels["xp"]
        new_xp = current_xp + self.amount
        await self.add_xp(interaction.user.id, interaction.guild.id, xp=self.amount, levels=levels)
        lvl = 0
        while True:
            if current_xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                break
            lvl += 1
        next_level_xp = ((50 * (lvl ** 2)) + (50 * (lvl - 1)))

        if new_xp > next_level_xp:
            guild_id = interaction.guild.id
            if guild_id == 694010548605550675:
                if lvl == 2:
                    reprole = await self.get_reprole(guild_id)
                    if reprole:
                        role = interaction.guild.get_role(reprole)
                        if role:
                            await interaction.user.add_roles(role, reason=f"{interaction.user.name} reached level 2")
                await interaction.followup.send(f"Yay! {interaction.user.mention} just reached **level {lvl}**!")

            else:
                stella = "Stella" if lvl == 1 else "Stellas"
                reprole = await self.get_reprole(guild_id)
                if reprole:
                    role = interaction.guild.get_role(reprole)
                    if role and lvl == 1:
                        await interaction.user.add_roles(role, reason=f"{interaction.user.name} reached level 1")

                embed.add_field(name="Level Up!", value=f"Congrats! You've reached **level {lvl}** {stella}!", inline=False)
        await interaction.response.edit_message(embed=embed, view=None)

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

    async def add_xp(self, member_id: int, guild_id: int, xp: int, levels: Optional[LevelRow]) -> None:
        if levels:
            query = '''UPDATE levelling SET xp = ? WHERE member_id = ? AND guild_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (levels['xp'] + xp, member_id, guild_id))
                    await conn.commit()
                await self.bot.pool.release(conn)
        else:
            await self.add_member(member_id, guild_id, xp)

    async def add_member(self, member_id: int, guild_id: int, xp = 25) -> None:
        query = '''INSERT INTO levelling (member_id, guild_id, xp , messages) VALUES (?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id, xp, 1))
                await conn.commit()
            await self.bot.pool.release(conn)

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

class configrankcard(discord.ui.View):
    def __init__(self, member, bot):
        super().__init__(timeout=60)
        self.member = member
        self.bot = bot
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$"

    @discord.ui.button(label="Image")
    async def image(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.member:
            await interaction.response.send_message(
                f"<:settings:1304222799639871530>**{interaction.user.name}**, Please upload an image for your rank card within the next 60 seconds.\n"
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

                await self.set_card_image(image_data, interaction.user.id)
                await interaction.followup.send(f"<:check:1291748345194348594> Okay **{interaction.user.name}**, I have update your rank card image", ephemeral=True)
                await msg.delete()

            except asyncio.TimeoutError:
                await interaction.followup.send("You didn't upload an image in time. Please try again.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"<:whitex:1304222877305798697>**{interaction.user.name}**, You cannot edit someone else's rank card.\n"
                f"-# <:thread1:1304222965042249781> Do **/rank** if you'd like to edit your rank card.",
                ephemeral=True,
            )

    @discord.ui.button(label="Colour")
    async def colour(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.member:
            await interaction.response.send_message(
                f"<:settings:1304222799639871530>**{interaction.user.name}**, Please type a valid hex code within the next 60 seconds.\n"
                f"-# <:thread:1291033931050778694> Enter a hex code for colors ([color picker](https://htmlcolorcodes.com/)).\n"
                f"-# <:thread1:1304222965042249781> The default hex code is **#c45a72**", 
                ephemeral=True
            )

            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            try:
                user_response = await self.bot.wait_for('message', timeout=60.0, check=check)
                color = user_response.content.strip()
                match = re.search(self.regex_hex, color)
                if match:
                    await self.set_rank_color(interaction.user.id, color)
                    await self.get_color(interaction.user.id)
                    await interaction.followup.send(f"<:check:1291748345194348594> Okay **{interaction.user.name}**, I have update your color to **{color}**", ephemeral=True)
                    await user_response.delete()
                else:
                    await interaction.followup.send(f"`{color}` is not a valid hex color. Make sure to add a **#** at the start!", ephemeral=True)

            except asyncio.TimeoutError:
                await interaction.followup.send(f"You took too long to respond, please try again.", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"<:whitex:1304222877305798697>**{interaction.user.name}**, You cannot edit someone else's rank card.\n"
                f"-# <:thread1:1304222965042249781> Do **/rank** if you'd like to edit your rank card.",
                ephemeral=True
            )

    @discord.ui.button(label="Format")
    async def format(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.member:
            await interaction.response.send_message(
                f"<:settings:1304222799639871530>**{interaction.user.name}**, Please type the format number you'd like (1 or 2) within the next 60 seconds.\n"
                f"-# <:thread:1291033931050778694> Here is a preview of what the rank formats look like[.](https://cdn.discordapp.com/attachments/1248039148888129647/1309164689988518008/format_preview_00000.png?ex=67409621&is=673f44a1&hm=a8692f6ae45016b5cff1810e7639412a1c13870b81275c4723b4a388a9f0fc49&)\n"
                f"-# <:thread1:1304222965042249781> The default format is **1**.", 
                ephemeral=True
            )

            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            try:
                user_response = await self.bot.wait_for('message', timeout=60.0, check=check)
                format_choice = user_response.content.strip()
                if format_choice in {'1', '2'}:
                    await self.set_format(interaction.user.id, int(format_choice))
                    await interaction.followup.send(
                        f"<:check:1291748345194348594> Okay **{interaction.user.name}**, I have updated your rank format to **{format_choice}**.", 
                        ephemeral=True
                    )
                    await user_response.delete()
                else:
                    await interaction.followup.send(
                        f"`{format_choice}` is not a valid option. Please choose **1** or **2**.",
                        ephemeral=True
                    )

            except asyncio.TimeoutError:
                await interaction.followup.send(
                    f"You took too long to respond, please try again.",
                    ephemeral=True
                )
        else:
            await interaction.response.send_message(
                f"<:whitex:1304222877305798697>**{interaction.user.name}**, You cannot edit someone else's rank card.\n"
                f"-# <:thread1:1304222965042249781> Use **/rank** if you'd like to edit your rank card.",
                ephemeral=True
            )

    async def set_format(self, member_id: int, format: str) -> None:
        query = '''UPDATE levelling SET format = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, format, member_id, )
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_color(self, member_id: int):
        query = '''SELECT color FROM levelling WHERE member_id = $1'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                row = await cursor.fetchone()
            await self.bot.pool.release(conn)

        if row and row['color']:
            color = row['color']
            if color.startswith('#'):
                embed_color = int(color.replace('#', '0x'), 16)
                return embed_color
       
        return 0x2b2d31

    async def set_rank_color(self, member_id: int, color: str) -> None:
        query = '''UPDATE levelling SET color = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, color, member_id, )
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_card_image(self, image: BytesIO, member_id: int, colorchange: Optional[bool] = False) -> None:
        query = "UPDATE levelling SET image = $1, color = $2 WHERE member_id = $3"
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
            new_query = "UPDATE levelling SET image = $1, accent_color = $4, color = $5 WHERE member_id = $2"
            async with self.bot.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(new_query, bytes_data, member_id, pb_accent, pb_primary)
            await self.bot.pool.release(connection)

class levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_holder = {0: "disabled", 1: "enabled"}
        self.pool = None
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)
        self.voice_times = {}

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
        query = '''INSERT INTO levelling (member_id, guild_id, xp , messages, format) VALUES (?, ?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id, xp, 1, 1))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_messages(self, member_id: int, guild_id: int, levels: LevelRow) -> None:
        query = '''UPDATE levelling SET messages = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, member_id, guild_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_xp(self, member_id: int, guild_id: int, levels: LevelRow, xp: int) -> None:
        query = '''UPDATE levelling SET messages = ?, xp = ? WHERE member_id = ? AND guild_id = ?'''
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
            if message.guild.id == 694010548605550675:
                if lvl == 2:
                    reprole = await self.get_reprole(message.guild.id)
                    role = message.guild.get_role(reprole)
                    if role:
                        await message.author.add_roles(role, reason=f"{message.author.name} reached level 2")
                        top20 = await self.get_top20(message.guild.id)
                        if top20 is not None:
                            await self.top_20_role_handler(message.author, message.guild, top20)
                await message.channel.send(f"Yay! {message.author.mention} you just reached **level {lvl}**")
            if message.guild.id == 1134736053803159592:
                if lvl == 1:
                    stella = "Stella"
                else:
                    stella = "Stellas"
                top20 = await self.get_top20(message.guild.id)
                if top20 is not None:
                    await self.top_20_role_handler(message.author, message.guild, top20)
                embed = discord.Embed(description=f"{message.author.name} you just reached **{lvl}** {stella}!", colour=0xFEBCBE)
                channel = message.guild.get_channel(1135027269853778020)
                await channel.send(message.author.mention, embed=embed)

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
                await self.update_xp(member_id, guild_id, levels, xp)
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

    async def _check_top_20(self, member_id: int, guild_id: int) -> bool:
        rank = await self.get_rank(member_id, guild_id)
        return rank < 21

    async def get_top20(self, guild_id: int) -> int:
        query = '''SELECT top20 FROM settings WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                status = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if status is not None:
            return status[0]
        else:
            return 1

    async def _get_top_20_movedown(self, member_ids: list, guild_id: int) -> int:
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]

    async def _get_number_20(self, guild_id: int) -> int:
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 20'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def top_20_role_handler(self, member: discord.Member, guild: discord.Guild, role_id: int) -> None:
        check = await self._check_top_20(member.id, guild.id)
        if check is True:
            role = member.get_role(role_id)
            if role is None:
                role = guild.get_role(role_id)
                await member.add_roles(role, reason=f'{str(member)} made it to the top 20!')
                if len(role.members) > 20:
                    mem_ids = []
                    for member in role.members:
                        mem_ids.append(member.id)
                    member_movedown_id = await self._get_top_20_movedown(mem_ids, guild.id)
                    remove_member = guild.get_member(member_movedown_id)
                    if remove_member is None:
                        remove_member = await guild.fetch_member(member_movedown_id)
                    await remove_member.remove_roles(role, reason=f'{str(remove_member)} dropped out of the top 20!')

        if check is False:
            role = member.get_role(role_id)
            if role is not None: 
                await member.remove_roles(role, reason=f'{str(member)} dropped out of the top 20!')
                add_mem_id = await self._get_number_20(guild.id)
                add_member = guild.get_member(add_mem_id)
                if add_member is None:
                    add_member = await guild.fetch_member(add_mem_id)
                await add_member.add_roles(role, reason=f'{str(add_member)} made it to the top 20!')

    async def handle_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        guild_id = message.guild.id if message.guild else None
        if guild_id is None:
            return
        
        channels = await self.get_textchannels(guild_id)
        if str(message.channel.id) not in channels:
            return
        
        xp_to_add = await self.get_chatxp(guild_id)
        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        
        await self.level_handler(message, retry_after, xp_to_add)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.bot:
            return

        required_roles = {694016195090710579, 1134797882420117544}

        def has_required_roles(member: discord.Member) -> bool:
            member_roles = {role.id for role in member.roles}
            return not required_roles.isdisjoint(member_roles)

        guild_id = member.guild.id
        channel_id = 822422177612824580 if guild_id == 694010548605550675 else 1135027269853778020

        if before.channel is None and after.channel is not None:
            if len(after.channel.members) >= 2:
                for m in after.channel.members:
                    if has_required_roles(m):
                        self.voice_times[m.id] = datetime.utcnow()

        elif before.channel is not None and after.channel is None:
            join_time = self.voice_times.pop(member.id, None)
            if join_time and has_required_roles(member):
                time_spent = datetime.utcnow() - join_time
                seconds_spent = time_spent.total_seconds()

                minimum_seconds = 30

                if seconds_spent >= minimum_seconds:
                    xp_to_add = await self.get_voicexp(guild_id)
                    xp_earned = (seconds_spent // minimum_seconds) * xp_to_add
                    levels = await self.get_level_row(member.id, guild_id)
                    if not levels:
                        return

                    current_xp = levels["xp"]
                    new_xp = current_xp + xp_earned
                    await self.add_xp(member.id, guild_id, xp_earned, levels)

                    lvl = 0
                    while True:
                        if current_xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                            break
                        lvl += 1

                    reprole = await self.get_reprole(guild_id)
                    if reprole:
                        role = member.guild.get_role(reprole)
                        if guild_id == 694010548605550675:
                            if role and lvl == 2:
                                await member.add_roles(role, reason=f"{member.name} reached level 2 through voice activity")
                            else:
                                if role and lvl == 1:
                                    await member.add_roles(role, reason=f"{member.name} reached level 1 through voice activity")

                    channel = member.guild.get_channel(channel_id)
                    if channel:
                        await channel.send(f"<@{member.id}> you earned **{xp_earned}** XP from speaking in #{before.channel.name}")

            if before.channel.members:
                xp_to_add = await self.get_voicexp(guild_id)
                for m in before.channel.members:
                    if has_required_roles(m):
                        join_time = self.voice_times.pop(m.id, None)
                        if join_time:
                            time_spent = datetime.utcnow() - join_time
                            seconds_spent = time_spent.total_seconds()

                            minimum_seconds = 3

                            if seconds_spent >= minimum_seconds:
                                xp_earned = (seconds_spent // minimum_seconds) * xp_to_add
                                levels = await self.get_level_row(m.id, guild_id)
                                if levels:
                                    current_xp = levels["xp"]
                                    new_xp = current_xp + xp_earned
                                    await self.add_xp(m.id, guild_id, xp_earned, levels)

                                    lvl = 0
                                    while True:
                                        if current_xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                                            break
                                        lvl += 1

                                    reprole = await self.get_reprole(guild_id)
                                    if reprole:
                                        role = member.guild.get_role(reprole)
                                        if role and lvl == 1:
                                            await m.add_roles(role, reason=f"{m.name} reached level 1 through voice activity")
                                channel = member.guild.get_channel(channel_id)
                                if channel:
                                    await channel.send(f"<@{m.id}> you earned **{xp_earned}** XP from speaking in #{before.channel.name}")

                        self.voice_times[m.id] = datetime.utcnow()

        elif before.channel is not None and after.channel is not None:
            pass

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

    def _make_progress_bar1(self, progress, color):
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

    def _make_progress_bar2(self, progress, color):
        width = 750  # Width of the progress bar
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
        circle = Image.open('./assets/circle-mask.png').resize((150, 150)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((150, 150))
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
                xp_progress_need = f"{xp_progress_need} XP"

            if xp_progress_have > 999:
                xp_progress_have = self.human_format(xp_progress_have)

        else:
            xp_progress_have = xp_have
            xp_progress_need = xp_need
            percentage = float(xp_progress_have / xp_progress_need)

        return percentage, xp_progress_have, xp_progress_need, lvl

    def get_card1(self, avatar: BytesIO, levels: LevelRow, rank: int, user: discord.User, guild: discord.Guild) -> BytesIO:
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
        mask = Image.open("./assets/boxmask1.png").resize((1500, 500)).convert("L")
        inverted_mask = ImageOps.invert(mask)
        bg_frosted = Image.composite(bg_blurred, Image.new("RGBA", bg.size, "white"), inverted_mask)
        bg_frosted.putalpha(inverted_mask)
        bar, mask_bar = self._make_progress_bar1(percentage, levels['color'])
        avatar_paste, circle = self.get_avatar(avatar)
        card.paste(bg, (0, 0))
        card.paste(bg_frosted, (0, 0), bg_frosted)
        card.paste(bar, (0, 485), mask_bar)
        card.paste(avatar_paste, (18, 17), circle)
        zhcn = ImageFont.truetype("./fonts/zhcn.ttf", size=36)
        zhcn2 = ImageFont.truetype("./fonts/zhcn.ttf", size=25)
        # rankdecor = Image.open(f'./assets/{levels["decor"]}.png')
        # rankdecor = rankdecor.resize((750, 750))
        # card.paste(rankdecor, (0, 0), rankdecor)
        rankboxes = Image.open('./assets/rankboxes.png')
        rankboxes = rankboxes.resize((750, 750))
        card.paste(rankboxes, (0, 0), rankboxes)
        draw = ImageDraw.Draw(card, 'RGBA')
        message = levels["messages"]
        messages = self.human_format(message)
        if guild == 694010548605550675:
            server = "chroma"
        else:
            server = "lyra"
        draw.text((100, 345), f'{xp_have} | {xp_need}', fill=levels['color'], font=zhcn)
        draw.text((100, 345), f'{xp_have} | {xp_need}', fill=levels['color'], font=zhcn)
        draw.text((225, 25), f"{user.name}", fill=levels['color'], font=zhcn)
        draw.text((225, 65), f"{server} levels", fill=levels['color'], font=zhcn2)
        draw.text((100, 410), f'level | {level-1}   rank | {str(rank)}   {messages} messages', fill=levels['color'], font=zhcn)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    def get_card2(self, avatar: BytesIO, levels: LevelRow, rank: int, user: discord.User, guild: discord.Guild) -> BytesIO:
        percentage, xp_have, xp_need, level = self.xp_calculations(levels)
        card = Image.new('RGBA', size=(750, 750), color='grey')
        
        if levels['image'] is not None:
            bg = Image.open(BytesIO(levels["image"]))
        else:
            bg = Image.open("./assets/rankcard.png")

        bg_aspect_ratio = bg.width / bg.height
        target_aspect_ratio = 750 / 750
        
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
        bg = bg.resize((750, 750))
        dark = ImageEnhance.Brightness(bg)
        bg_dark = dark.enhance(0.8)
        bg_blurred = bg_dark.filter(ImageFilter.GaussianBlur(radius=20))
        mask = Image.open("./assets/boxmask2.png").resize((750, 750)).convert("L")
        inverted_mask = ImageOps.invert(mask)
        bg_frosted = Image.composite(bg_blurred, Image.new("RGBA", bg.size, "white"), inverted_mask)
        bg_frosted.putalpha(inverted_mask)
        bar, mask_bar = self._make_progress_bar2(percentage, levels['color'])
        avatar_paste, circle = self.get_avatar(avatar)
        card.paste(bg, (0, 0))
        card.paste(bg_frosted, (0, 0), bg_frosted)
        card.paste(bar, (0, 735), mask_bar)
        card.paste(avatar_paste, (18, 17), circle)
        zhcn = ImageFont.truetype("./fonts/zhcn.ttf", size=30)
        zhcn2 = ImageFont.truetype("./fonts/zhcn.ttf", size=20)
        # rankdecor = Image.open(f'./assets/{levels["decor"]}.png')
        # rankdecor = rankdecor.resize((750, 750))
        # card.paste(rankdecor, (0, 0), rankdecor)
        draw = ImageDraw.Draw(card, 'RGBA')
        message = levels["messages"]
        messages = self.human_format(message)
        if guild == 694010548605550675:
            server = "chroma"
        else:
            server = "lyra"
        draw.text((65, 620), f'{xp_have} | {xp_need}', fill=levels['color'], font=zhcn)
        draw.text((170, 25), f"{user.name}", fill=levels['color'], font=zhcn)
        draw.text((170, 55), f"{server} levels", fill=levels['color'], font=zhcn2)
        draw.text((57, 670), f'level | {level-1}   rank | {str(rank)}   {messages} messages', fill=levels['color'], font=zhcn)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def generate_card1(self, avatar: BytesIO, levels: LevelRow, rank: int, member: discord.Member, guild: discord.Guild) -> BytesIO:
        card_generator = functools.partial(self.get_card1, avatar, levels, rank, guild)
        card = await self.bot.loop.run_in_executor(None, self.get_card1, avatar, levels, rank, member, guild)
        return card

    async def generate_card2(self, avatar: BytesIO, levels: LevelRow, rank: int, member: discord.Member, guild: discord.Guild) -> BytesIO:
        card_generator = functools.partial(self.get_card2, avatar, levels, rank, guild)
        card = await self.bot.loop.run_in_executor(None, self.get_card2, avatar, levels, rank, member, guild)
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

    async def add_xp(self, member_id: int, guild_id: int, xp: int, levels: Optional[LevelRow]) -> None:
        if levels:
            query = '''UPDATE levelling SET xp = ? WHERE member_id = ? AND guild_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (levels['xp'] + xp, member_id, guild_id))
                    await conn.commit()
                await self.bot.pool.release(conn)
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
        query = '''SELECT * FROM levelling WHERE guild_id = ? ORDER BY xp DESC'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                rows = await cursor.fetchall()
        return rows

    async def get_format(self, member_id: int, guild_id: int) -> int:
        query = '''SELECT format FROM levelling WHERE guild_id = ? AND member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (guild_id, member_id))
                status = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if status is not None:
            return status[0]
        else:
            return 1

    @app_commands.command(name="rank", description="Check your rank")
    @app_commands.checks.cooldown(1, 5)
    async def rank(self, interaction: discord.Interaction, member: Optional[discord.Member] = None):
        required_roles = {1134797882420117544, 694016195090710579}
        member_roles = {role.id for role in interaction.user.roles}
        if required_roles.isdisjoint(member_roles):
            await interaction.response.send_message("Sorry, this command is currently not available for non members!", ephemeral=True)
            return
        
        member = member or interaction.user
        levels = await self.get_member_levels(member.id, interaction.guild_id)
        rank = await self.get_rank(member.id, interaction.guild_id)
        avatar_url = member.display_avatar.replace(static_format='png', size=256).url
        format = await self.get_format(member.id, interaction.guild.id)
        response = await self.bot.session.get(avatar_url)
        guild = interaction.guild.id
        avatar = BytesIO(await response.read())
        avatar.seek(0)

        if format == 1:
            if levels:
                    card = await self.generate_card1(avatar, levels, rank, member, guild)
            else:
                card = None
        elif format == 2:
            if levels:
                    card = await self.generate_card2(avatar, levels, rank, member, guild)
            else:
                card = None

        if card:
            await interaction.response.send_message(file=discord.File(card, 'card.png'), view=configrankcard(member=member.id, bot=self.bot))
        else:
            await interaction.response.send_message(f"{member} hasn't gotten levels yet!")

    @rank.error
    async def rank_error(self, interaction: discord.Interaction, error: Exception):
        try:
            if isinstance(error, CommandOnCooldown):
                remaining_time = int(error.retry_after)
                await interaction.response.send_message(
                    f"Slow down! You're on cooldown for **{remaining_time} seconds**.",
                    ephemeral=True
                )
            else:
                print(f"Error in 'rank' command: {error}")
                if not interaction.response.is_done():
                    await interaction.response.send_message(f"An unexpected error occurred. Please try again later.\n{error}",ephemeral=True)
        except discord.InteractionResponded:
            pass

    @app_commands.command(description="See the level leaderboard")
    @app_commands.checks.cooldown(1, 5)
    async def leaderboard(self, interaction: discord.Interaction):
        required_roles = {1134797882420117544, 694016195090710579}
        member_roles = {role.id for role in interaction.user.roles}
        if required_roles.isdisjoint(member_roles):
            await interaction.response.send_message("Sorry, this command is currently not available for non members!", ephemeral=True)
            return
        
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
            description += f"**{i}.** <@!{row['member_id']}>\n-# <:reply:1290714885792989238> level {lvl-1} | {row['messages']} {msg}\n\n"
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

    @leaderboard.error
    async def daily_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, CommandOnCooldown):
            remaining_time = datetime.timedelta(seconds=error.retry_after)
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            await interaction.response.send_message(f"Slow down! you're on cooldown for **{seconds} seconds**.")
        else:
            await interaction.response.send_message(f"An unexpected error occurred. Please try again later.\n{error}",ephemeral=True)

    @app_commands.command(name="add", description="Add XP to someone", extras="+add @member amount")
    async def add(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        required_roles = {739513680860938290, 1261435772775563315}
        member_roles = {role.id for role in interaction.user.roles}
        if required_roles.isdisjoint(member_roles):
            await interaction.response.send_message("Sorry, this command is only available for staff members.", ephemeral=True)
            return
        levels = await self.get_member_levels(member.id, interaction.guild.id)
        if not levels:
            await interaction.response.send_message("Could not retrieve the member's level data. Please try again later.", ephemeral=True)
            return

        current_xp = levels["xp"]
        new_xp = current_xp + amount
        await self.add_xp(member.id, interaction.guild.id, amount, levels)
        lvl = 0
        while True:
            if current_xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                break
            lvl += 1
        next_level_xp = ((50 * (lvl ** 2)) + (50 * (lvl - 1)))

        if new_xp > next_level_xp:
            guild_id = interaction.guild.id
            if guild_id == 694010548605550675:
                if lvl == 2:
                    reprole = await self.get_reprole(guild_id)
                    if reprole:
                        role = interaction.guild.get_role(reprole)
                        if role:
                            await member.add_roles(role, reason=f"{member.name} reached level 2")
                await interaction.followup.send(f"Yay! {member.mention} just reached **level {lvl}**!")

            else:
                stella = "Stella" if lvl == 1 else "Stellas"
                reprole = await self.get_reprole(guild_id)
                if reprole:
                    role = interaction.guild.get_role(reprole)
                    if role and lvl == 1:
                        await member.add_roles(role, reason=f"{member.name} reached level 1")

                embed = discord.Embed(
                    description=f"{member.name} just reached **{lvl}** {stella}!", colour=0xFEBCBE
                )
                channel = interaction.guild.get_channel(1135027269853778020)
                if channel:
                    await channel.send(member.mention, embed=embed)
        top20 = await self.get_top20(interaction.guild.id)
        if top20 is not None:
            await self.top_20_role_handler(member, interaction.guild, top20)
        embed = discord.Embed(
            title="XP Added!",
            description=f"Gave `{amount} XP` to {str(member)}.",
            color=0x2B2D31
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove", description="Remove xp from someone", extras="+remove @member amount")
    async def remove(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        required_roles = {739513680860938290, 1261435772775563315}
        member_roles = {role.id for role in interaction.user.roles}
        if required_roles.isdisjoint(member_roles):
            await interaction.response.send_message("Sorry, this command is only available for staff members.", ephemeral=True)
            return

        levels = await self.get_member_levels(member.id, interaction.guild_id)
        if levels:
            if amount > levels['xp']:
                await interaction.response.send_message("you can't take away more xp than the user already has!")
            else:
                await self.remove_xp(member.id, interaction.guild_id, amount, levels)
                embed = discord.Embed(
                    title='xp removed!',
                    description=f'removed `{amount}xp` from {str(member)}',
                    color=0x2B2D31
                )
                await interaction.response.send_message(embed=embed)
                top20 = await self.get_top20(interaction.guild.id)
                if top20 is not None:
                    await self.top_20_role_handler(interaction.user, interaction.guild, top20)
        else:
            await interaction.response.send_message(f"{str(member)} doesn't have any xp yet!")

    async def reset_inactive(self, guild_id: int) -> None:
        query_select = '''SELECT member_id FROM chromies WHERE guild_id = ? AND inactive = 1'''
        query_update = '''UPDATE chromies SET inactive = 0 WHERE guild_id = ? AND member_id = ?'''
        
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query_select, (guild_id,))
                members_to_reset = await cursor.fetchall()
                
                for (member_id,) in members_to_reset:
                    await cursor.execute(query_update, (guild_id, member_id))
                
                await conn.commit()

    async def reset_iamsgs(self, guild_id: int) -> None:
        query_select = '''SELECT member_id FROM chromies WHERE guild_id = ? AND iamsgs = 0'''
        query_update = '''UPDATE chromies SET iamsgs = 3 WHERE guild_id = ? AND member_id = ?'''
        
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query_select, (guild_id,))
                members_to_reset = await cursor.fetchall()
                
                for (member_id,) in members_to_reset:
                    await cursor.execute(query_update, (guild_id, member_id))
                
                await conn.commit()

    @app_commands.command(name="reset", description="Resets everyone's xp")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reset(self, interaction: discord.Interaction):
        if interaction.guild.id == 694010548605550675:
            await self.reset_iamsgs(interaction.guild.id)
            await self.reset_inactive(interaction.guild.id)
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
        query = '''SELECT * FROM levelling WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id))
                return await cursor.fetchone()

    @app_commands.command(name="daily", description="Get daily XP with Hoshi for Chroma")
    @app_commands.checks.cooldown(1, 86400)
    async def daily(self, interaction: discord.Interaction):
        required_roles = {694016195090710579}
        member_roles = {role.id for role in interaction.user.roles}
        if required_roles.isdisjoint(member_roles):
            await interaction.response.send_message("Sorry, you need to be a member of Chroma to use this command!", ephemeral=True)
            return

        xprand = await self.get_dailyxp(interaction.guild.id)
        if not xprand:
            await interaction.response.send_message("Daily XP configuration not found.", ephemeral=True)
            return

        min_xp, max_xp = map(int, xprand.split('-'))
        xp_to_add = randint(min_xp, max_xp)
        levels = await self.get_level_row(interaction.user.id, interaction.guild.id)
        if not levels:
            await interaction.response.send_message("Could not retrieve your level data. Please try again later.", ephemeral=True)
            return

        current_xp = levels["xp"]
        new_xp = current_xp + xp_to_add

        await self.add_xp(interaction.user.id, interaction.guild.id, xp_to_add, levels)

        lvl = 0
        while True:
            if current_xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                break
            lvl += 1

        next_level_xp = ((50 * (lvl ** 2)) + (50 * (lvl - 1)))

        if new_xp > next_level_xp:
            guild_id = interaction.guild.id
            if guild_id == 694010548605550675:
                if lvl == 2:
                    reprole = await self.get_reprole(guild_id)
                    if reprole:
                        role = interaction.guild.get_role(reprole)
                        if role:
                            await interaction.user.add_roles(role, reason=f"{interaction.user.name} reached level 2")
                embed = discord.Embed(
                    description=f"{interaction.user.name} you just reached **Level {lvl}**!", colour=0xFEBCBE
                )
                channel = interaction.guild.get_channel(822422177612824580)
                if channel:
                    await channel.send(interaction.user.mention, embed=embed)
            else:
                stella = "Stella" if lvl == 1 else "Stellas"
                reprole = await self.get_reprole(guild_id)
                if reprole:
                    role = interaction.guild.get_role(reprole)
                    if role and lvl == 1:
                        await interaction.user.add_roles(role, reason=f"{interaction.user.name} reached level 1")
                embed = discord.Embed(
                    description=f"{interaction.user.name} you just reached **{lvl}** {stella}!", colour=0xFEBCBE
                )
                channel = interaction.guild.get_channel(1135027269853778020)
                if channel:
                    await channel.send(interaction.user.mention, embed=embed)

        top20 = await self.get_top20(interaction.guild.id)
        if top20 is not None:
            await self.top_20_role_handler(interaction.user, interaction.guild, top20)

        await interaction.response.send_message(f"Yay! **{interaction.user.name}**, you received **{xp_to_add}** XP from daily XP!")

    @daily.error
    async def daily_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, CommandOnCooldown):
            remaining_time = datetime.timedelta(seconds=error.retry_after)
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            await interaction.response.send_message(f"You cannot claim your daily for another **{hours}h {minutes}m {seconds}s**.")
        else:
            await interaction.response.send_message(f"An unexpected error occurred. Please try again later.\n{error}",ephemeral=True)

    @app_commands.command(name="dailies", description="Get daily XP with Hoshi for Lyra")
    @app_commands.checks.cooldown(1, 86400)
    @app_commands.guilds(discord.Object(id=1134736053803159592))
    async def dailies(self, interaction: discord.Interaction):
        required_roles = {1134797882420117544, 694016195090710579}
        member_roles = {role.id for role in interaction.user.roles}
        if required_roles.isdisjoint(member_roles):
            await interaction.response.send_message("Sorry, this command is currently not available for non-members!", ephemeral=True)
            return

        xprand = await self.get_dailyxp(interaction.guild.id)
        if not xprand:
            await interaction.response.send_message("Daily XP configuration not found.", ephemeral=True)
            return

        min_xp, max_xp = map(int, xprand.split('-'))
        xp_to_add = randint(min_xp, max_xp)
        levels = await self.get_level_row(interaction.user.id, interaction.guild.id)
        if not levels:
            await interaction.response.send_message("Could not retrieve your level data. Please try again later.", ephemeral=True)
            return

        current_xp = levels["xp"]
        new_xp = current_xp + xp_to_add

        await self.add_xp(interaction.user.id, interaction.guild.id, xp_to_add, levels)

        lvl = 0
        while True:
            if current_xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                break
            lvl += 1

        next_level_xp = ((50 * (lvl ** 2)) + (50 * (lvl - 1)))

        if new_xp > next_level_xp:
            guild_id = interaction.guild.id
            stella = "Stella" if lvl == 1 else "Stellas"
            reprole = await self.get_reprole(guild_id)
            if reprole:
                role = interaction.guild.get_role(reprole)
                if role and lvl == 1:
                    await interaction.user.add_roles(role, reason=f"{interaction.user.name} reached level 1")
            embed = discord.Embed(
                description=f"{interaction.user.name} you just reached **{lvl}** {stella}!", colour=0xFEBCBE
            )
            channel = interaction.guild.get_channel(1135027269853778020)
            if channel:
                await channel.send(interaction.user.mention, embed=embed)

        top20 = await self.get_top20(interaction.guild.id)
        if top20 is not None:
            await self.top_20_role_handler(interaction.user, interaction.guild, top20)

        await interaction.response.send_message(f"Yay! **{interaction.user.name}**, you received **{xp_to_add}** XP from daily XP!")

    @dailies.error
    async def dailies_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, CommandOnCooldown):
            remaining_time = datetime.timedelta(seconds=error.retry_after)
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            await interaction.response.send_message(f"You cannot claim your daily for another **{hours}h {minutes}m {seconds}s**.")
        else:
            await interaction.response.send_message(f"An unexpected error occurred. Please try again later.\n{error}",ephemeral=True)

    @app_commands.command(name="dropxp", description="Drop XP for server members")
    @app_commands.checks.cooldown(1, 5)
    async def dropxp(self, interaction: discord.Interaction, amount: int):
        required_roles = {739513680860938290, 1261435772775563315}
        member_roles = {role.id for role in interaction.user.roles}
        if required_roles.isdisjoint(member_roles):
            await interaction.response.send_message("Sorry, this command is only available for staff members.", ephemeral=True)
            return

        embed = discord.Embed(title="<:removal:1306071903198380082> Dropped XP", description=f"**{interaction.user.name}** dropped `{amount}xp`.", color=0x2b2d31)
        view = claimxp(bot=self.bot, amount=amount, dropper=interaction.user.name)
        await interaction.response.send_message(embed=embed, view=view)
        await interaction.followup.send(f"<:whitecheck:1304222829595721770> **{interaction.user.name}** `{amount}xp` has been dropped!", ephemeral=True)

    @dropxp.error
    async def dropxp_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, CommandOnCooldown):
            remaining_time = datetime.timedelta(seconds=error.retry_after)
            remainder = divmod(remaining_time.seconds, 60)
            seconds = divmod(remainder, 60)
            await interaction.response.send_message(f"Slow down! you're on cooldown for **{seconds} seconds**.")
        else:
            await interaction.response.send_message("An unexpected error occurred. Please try again later.",ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.handle_message(message)

    async def set_format(self, member_id: int, format: str) -> None:
        query = '''UPDATE levelling SET format = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, format, member_id, )
                await conn.commit()
            await self.bot.pool.release(conn)

    @commands.command()
    async def format(self, ctx):
        await self.set_format(ctx.author.id, 1)
        await ctx.reply("Okay, the issue is now fixed! please try /rank again!")

async def setup(bot):
    await bot.add_cog(levels(bot))