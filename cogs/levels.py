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

# class for every database entry
class LevelRow(TypedDict):
    member_id: int
    xp: int
    messages: int
    bar_color: str

class Levels(commands.Cog):
    """Commands for the levelling system"""
    def __init__(self, bot: LalisaBot):
        self.bot = bot
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user) # cooldown for xp (1 minute/60 seconds)
        self.top20_role_id = 1113200212811448352 # role id for top 20 role
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$" # regex to match hex colors for progress bar color
                
    async def _register_member_levels(self, member_id: int, xp: Optional[int] = 25) -> None:
        """Registers a member to the levels database
        
        Parameters
        ----------
        member_id: int
            ID of the member to register
        xp: int, optional
            The amount of xp to be added, defaults to 25
        """
        query = '''INSERT INTO levels (member_id, messages, xp, bar_color) VALUES (?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, 1, xp, "#4089ff"))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def _update_message_count(self, member_id: int, levels: LevelRow) -> None:
        """Updates a member's message count.
        
        Parameters
        ----------
        member_id: int
            ID of the member to register
        levels: LevelRow
            The member's levels before updating message count
        """
        query = '''UPDATE levels SET messages = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, member_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def _update_xp(self, member_id: int, levels: LevelRow, xp: int) -> None:
        """Updates a member's xp and message count.
        
        Parameters
        ----------
        member_id: int
            ID of the member to register
        levels: LevelRow
            The member's levels before update
        xp: int
            The amount of XP to add
        """
        query = '''UPDATE levels SET messages = ?, xp = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, levels['xp'] + xp, member_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def _level_check(self, message: discord.Message, xp: int, xp_to_add: int) -> None:
        """Checks if member has levelled up.
        
        Parameters
        ----------
        message: discord.Message
            The message object of the message sent on Discord
        xp: int
            The amount of XP the member has from before
        xp_to_add: int
            The amount of XP to be added to the member's levels
        """
        new_xp = xp + xp_to_add
        lvl = 0
        while True:
            if xp < ((50*(lvl**2))+(50*(lvl-1))):
                break
            lvl += 1
        next_level_xp = ((50*(lvl**2))+(50*(lvl-1)))
        if new_xp > next_level_xp: # author has leveled up
            await message.channel.send(f"{message.author.mention} reached **level {lvl+1}**")

    async def _level_handler(self, message: discord.Message, retry_after: Optional[commands.CooldownMapping], xp: int) -> None:
        """Handles levels for members when they send messages on Discord.
        
        Parameters
        ----------
        message: discord.Message
            The message object of the message sent on Discord
        retry_after: commands.CooldownMapping, optional
            The cooldown for member if they are on cooldown
        xp: int
            The XP to (potentially) add to member's levels
        """
        member_id = message.author.id
        levels = await self.get_member_levels(member_id)
        if levels == None: # the member hasn't sent a message yet
            # so we have to add them to the database
            await self._register_member_levels(member_id)
        else: # have sent a message before
            if retry_after: # on cooldown
                await self._update_message_count(member_id, levels)
            else: # not on cooldown so we update the xp
                await self._update_xp(member_id, levels, xp)
                await self._level_check(message, levels['xp'], xp)
                await self.top_20_role_handler(message.author, message.guild)

    async def handle_message(self, message: discord.Message) -> None:
        """Handles messages sent on Discord.
        
        Parameters
        ----------
        message: discord.Message
            The message object for the message sent on Discord
        """

        if message.author.bot is True: 
            return # author is a bot, we don't want to add xp to bots
        
        if message.guild.id != 1121841073673736215: 
          return

        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        xp_to_add = randint(8, 25)

        await self._level_handler(message, retry_after, xp_to_add)

    def _make_progress_bar(self, progress: float, color: str):
        """Makes a progress bar for a member's rank card.
        
        Parameters
        ----------
        progress: float
            How far into their current level the member is
        color: int
            The color of their progress bar
        """
        width = 1050  # Width of the progress bar
        height = 65  # Height of the progress bar
        radius = 32.5  # Radius of the rounded corners

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
    
    def _get_round_avatar(self, avatar: BytesIO):
        """Converts square avatar retrieved from Discord into a circle avatar
        
        avatar: BytesIO
            The avatar to convert into a circle
        """
        circle = Image.open('./assets/circle-mask.png').resize((325, 325)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((325, 325))
        return avatar_image, circle
    
    def _human_format(self, number: int) -> str:
        """Converts a large number into a more readable format
        
        Parameters
        ----------
        number: int
            The number to convert

        Returns
        -------
        str
            The converted number
        """
        number = float('{:.3g}'.format(number))
        magnitude = 0
        while abs(number) >= 1000:
            magnitude += 1
            number /= 1000.0
        return '{}{}'.format('{:f}'.format(number).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    def _xp_calculations(self, levels: LevelRow) -> tuple[float, Union[str, int], Union[str, int], int]:
        """Calculates XP, level progress and current level.
        
        Parameters
        ----------
        levels: LevelRow
            A database level row to calculate from

        Returns
        -------
        percentage: float
            Percentage of progress in current level
        xp_progress_have: str or int
            The amount of XP gained since advancing to the current level
        xp_progress_need: str or int
            The amount of XP needed to advance from current level
        lvl: int
            The current level
        """
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
        """Creates a rank card.
        
        Parameters
        ----------
        name: str
            Username to display on card
        status: str
            Discord activity status to display next to avatar
        avatar: BytesIO
            Circle shaped avatar to display on card
        levels: LevelRow
            Database level row to retrieve level information
        rank: int
            Rank to display on card

        Returns
        -------
        BytesIO
            The rank card as a stream of in-memory bytes
        """
        percentage, xp_have, xp_need, level = self._xp_calculations(levels)
        card = Image.new('RGBA', size=(1500, 500), color='grey')
        bg = Image.open("./assets/rank_bg.png")
        card.paste(bg)
        status_circle = Image.open(f'./assets/{status}.png')
        bar, mask = self._make_progress_bar(percentage, levels['bar_color'])
        avatar_paste, circle = self._get_round_avatar(avatar)
        font = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 64)
        font2 = ImageFont.truetype("./fonts/Montserrat-Regular.ttf", 46)
        font3 = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 50)
        card.paste(avatar_paste, (25, 84), circle)
        card.paste(status_circle, (250, 315), status_circle)
        card.paste(bar, (390, 325), mask)
        draw = ImageDraw.Draw(card, 'RGBA')
        draw.text((420, 240), name, "#ffffff", font=font)
        draw.text((1140, 255), f'{xp_have} / {xp_need}', "#ffffff", font=font2)
        draw.text((860, 75), f"RANK {str(rank)}    LEVEL {level}", "#ffffff", font=font3)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def _check_top_20(self, member: discord.Member) -> bool:
        """Checks if a member is in the top 20.
        
        Parameters
        ----------
        member: discord.Member
            Member to check

        Returns
        -------
        bool
            True for top 20, otherwise False
        """
        rank = await self.get_rank(member.id)
        return rank < 21 # true if top 20 false if not
    
    async def _get_top_20_movedown(self, member_ids: list) -> int:
        """
        Gets the member to remove from top 20 role when a new member gets the role 
        
        (if 20 people already have the role)
        
        Parameters
        ----------
        member_ids: list
            List containing all the IDs of members with the top 20 role

        Returns
        -------
        int
            The ID of the member to remove from the top 20 role
        """
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {})".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]

    async def _get_number_20(self) -> int:
        """Gets the member ranked 20th.

        Returns
        -------
        int
            The ID of the member ranked 20th
        """
        query = '''SELECT member_id FROM levels ORDER BY xp LIMIT 20'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def get_member_levels(self, member_id: int) -> Optional[LevelRow]:
        """Gets a member's level row from database.
        
        Parameters
        ----------
        member_id: int
            ID of the member to get the levels for

        Returns
        -------
        row: LevelRow
            Dictionary-like row of the member's levels
        """
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
        """Adds XP to a member's levels, if member isn't already registered it also registers them.
        
        Parameters
        ----------
        member_id: int
            ID of the member to register
        xp: int
            The amount of XP to add
        levels: LevelRow, optional
            The member's levels before update
        """
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
        """Removes XP from a member's levels.
        
        Parameters
        ----------
        member_id: int
            ID of the member to register
        xp: int
            The amount of XP to add
        levels: LevelRow
            The member's levels before update
        """
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
        """Get the current rank of a member.
        
        Parameters
        ----------
        member_id: int
            ID of member whose rank you want to get
        """
        query = '''SELECT COUNT(*) FROM levels WHERE xp > (SELECT xp FROM levels WHERE member_id = ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id))
                rank = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return rank[0] + 1

    async def generate_card(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int) -> BytesIO:
        """Generates a rank card asynchronously.
        
        Parameters
        ----------
        name: str
            Username to display on card
        status: str
            Discord activity status to display next to avatar
        avatar: BytesIO
            Circle shaped avatar to display on card
        levels: LevelRow
            Database level row to retrieve level information
        rank: int
            Rank to display on card

        Returns
        -------
        BytesIO
            The rank card as a stream of in-memory bytes
        """
        card_generator = functools.partial(self._get_card, name, status, avatar, levels, rank)
        card = await self.bot.loop.run_in_executor(None, card_generator)
        return card

    async def top_20_role_handler(self, member: discord.Member, guild: discord.Guild) -> None:
        """
        Handles top 20 role.
        
        Checks if a member's XP-changes requires modifications to the role members
        
        Parameters
        ----------
        member: discord.Member
            Member to check for role modifications
        guild: discord.Guild
            Guild containing the role
        """
        check = await self._check_top_20(member)
        if check is True:
            role = member.get_role(self.top20_role_id)
            if role is None:
                role = guild.get_role(self.top20_role_id)
                await member.add_roles(role, reason=f'{str(member)} made it to the top 20!')
                if len(role.members) > 20:
                    mem_ids = []
                    for member in role.members:
                        mem_ids.append(member.id)
                    member_movedown_id = await self._get_top_20_movedown(mem_ids)
                    remove_member = guild.get_member(member_movedown_id)
                    if remove_member is None:
                        remove_member = await guild.fetch_member(member_movedown_id)
                    await remove_member.remove_roles(role, reason=f'{str(remove_member)} dropped out of the top 20!')
                    
        if check is False:
            role = member.get_role(self.top20_role_id)
            if role is not None: 
                await member.remove_roles(role, reason=f'{str(member)} dropped out of the top 20!')
                mem_ids = []
                for member in role.members:
                    mem_ids.append(member.id)
                add_mem_id = await self._get_number_20(mem_ids)
                add_member = guild.get_member(add_mem_id)
                if add_member is None:
                    add_member = await guild.fetch_member(add_mem_id)
                await add_member.add_roles(role, reason=f'{str(add_member)} made it to the top 20!')

    async def get_leaderboard_stats(self) -> List[LevelRow]:
        """Gets every member's levels ordered by XP
        
        Returns
        -------
        list
            List of LevelRow instances
        """
        query = '''SELECT * FROM levels ORDER BY xp DESC'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall()
        return rows
                
    async def set_rank_color(self, member: discord.Member, color: str) -> None:
        """Changes the progress bar color for a member's rank card
        
        Parameters
        ----------
        member: discord.Member
            Member whose color is being changed
        color: str
            Hex color to change to
        """
        query = '''UPDATE levels SET bar_color = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, color, member.id)
                await conn.commit()
            await self.bot.pool.release(conn)

    @commands.command(aliases=['levels', 'lb'])
    async def leaderboard(self, ctx: commands.Context):
        """sends the current leaderboard"""
        embeds = []
        description = ""
        rows = await self.get_leaderboard_stats()
        per_page = 5 if ctx.author.is_on_mobile() else 10

        for i, row in enumerate(rows, start=1):

            msg = "messages" if row['messages'] != 1 else "message"

            description += f"**{i}.** <@!{row['member_id']}>\n{row['xp']} xp | {row['messages']} {msg}\n\n"

            if i % per_page == 0 or i == len(rows):
                embed = discord.Embed(title="leaderboard", description=description, color=0x2B2D31)
                embed.set_thumbnail(url=ctx.guild.icon.url)
                embeds.append(embed)
                description = ""

        if len(embeds) > 1:
            view = Paginator(embeds)
            await ctx.send(embed=view.initial, view=view)
        else:
            await ctx.send(embed=embed)

    @commands.command(extras={"examples": ["rank", "rank candysnowy", "rank <@609515684740988959>"]})
    async def rank(self, ctx: commands.Context, member: Optional[discord.Member]):
        """makes a rank card"""
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
        """
        change the color of your progressbar
        
        Parameters
        ----------
        color: str
            the color you want for your progress bar
        """
        match = re.search(self.regex_hex, color)
        if match:
            await self.set_rank_color(ctx.author, color)
            embed = discord.Embed(
                title='changed your bar color!',
                description=f'your new bar color is `{color}`',
                color=0x2B2D31
            )
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"`{color}` is not a valid hex color")

    @commands.group(invoke_without_command=True)
    async def xp(self, ctx: commands.Context):
        """group of commands to manage xp"""
        embed = discord.Embed(title="xp manager", color=0x2B2D31)
        embed.add_field(name="xp add <member> <xp amount>", value="adds the specified amount of xp to a member", inline=False)
        embed.add_field(name="xp remove <member> <xp amount>", value="subtracts the specified amount of xp from a member", inline=False)
        await ctx.reply(embed=embed)

    @xp.command(aliases=['give', 'a'], extras={"examples": ["xp add <@609515684740988959> 1000", "xp give candysnowy 1000"]})
    async def add(self, ctx: commands.Context, member: discord.Member, amount: int):
        """
        add xp to a member's level xp

        Parameters
        -----------
        member: discord.Member
            member to give xp to
        amount: int
            the amount of xp to add
        """
        levels = await self.get_member_levels(member.id)
        await self.add_xp(member.id, amount, levels)
        await self.top_20_role_handler(member, ctx.guild)
        embed = discord.Embed(
            title='xp added!',
            description=f'gave `{amount}xp` to {str(member)}',
            color=0x2B2D31
        )
        await ctx.reply(embed=embed)

    @xp.command(aliases=['take', 'r'], extras={"examples": ["xp remove <@609515684740988959> 1000", "xp take candysnowy 1000"]})
    async def remove(self, ctx: commands.Context, member: discord.Member, amount: int):
        """
        remove xp from a member's level xp

        Parameters
        -----------
        member: discord.Member
            member to remove xp from
        amount: int
            the amount of xp to remove
        """
        levels = await self.get_member_levels(member.id)
        if levels:
            if amount > levels['xp']:
                await ctx.reply("you can't take away more xp than the user already has!")
            else:
                await self.remove_xp(member.id, amount, levels)
                await self.top_20_role_handler(member, ctx.guild)
                embed = discord.Embed(
                    title='xp removed!',
                    description=f'removed `{amount}xp` from {str(member)}',
                    color=0x2B2D31
                )
                await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"{str(member)} doesn't have any xp yet!")

    @xp.command()
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx: commands.Context):
        """Wipes all XP from the database"""
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
                color=0x2B2D31
            )
            return await message.edit(content=None, embed=embed)
        except asyncio.TimeoutError:
            await message.edit(content="~~are you sure you want to reset the ranks? it's irreversible!~~\nreset has been cancelled!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.handle_message(message)

async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(Levels(bot))