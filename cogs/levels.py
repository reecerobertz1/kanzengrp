import discord
from discord.ext import commands
import requests
from bot import LalisaBot
from random import randint
from typing import Optional, TypedDict, List, Union, Literal, Tuple
from PIL import ImageDraw, Image, ImageFont
from io import BytesIO
import functools
from utils.views import Paginator
import re
import asyncio
from easy_pil import Canvas, Editor, Font
from PIL import Image, ImageEnhance, ImageFilter, UnidentifiedImageError

class LevelRow(TypedDict):
    member_id: int
    xp: int
    messages: int
    bar_color: str
    format: str

class Levels(commands.Cog):
    """Commands for the levelling system"""
    def __init__(self, bot: LalisaBot):
        self.bot = bot
        self.status_holder = {0: "not active", 1: "active"}
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user) # cooldown for xp (1 minute/60 seconds)
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$" # regex to match hex colors for progress bar color
        self.emoji="<:cooky:1121909627156705280>"

    def levels_is_activated():
        async def predicate(ctx: commands.Context):
            query = '''SELECT activated FROM setup WHERE guild_id = ?'''
            async with ctx.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, ctx.guild.id)
                    status = await cursor.fetchone()
            if status is not None:
                status = status[0]
            else:
                query = '''INSERT INTO setup (guild_id, activated) VALUES (?, 1)'''
                async with ctx.bot.pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(query, ctx.guild.id)
                        await conn.commit()
                    await ctx.bot.pool.release(conn)
                status = 1
            return status == 1
        return commands.check(predicate)

    def kanzen_only():
        def predicate(ctx: commands.Context):
            if ctx.guild.id == 1121841073673736215:
                return True
            else:
                return False
        return commands.check(predicate)

    def kanzen_cooldown(message: discord.Message):

        # reece has no cooldown
        if message.author.id == 609515684740988959:
            return None

        role = message.guild.get_role(1128460924886458489)
        if role in message.author.roles:
            # boosters have a 12 hour cooldown
            return commands.Cooldown(1, 43200)
        
        daegu = message.guild.get_role(896925970672549958)
        if daegu in message.author.roles:
            # boosters have a 12 hour cooldown
            return commands.Cooldown(1, 43200)
        
        # other members have a 24 hour cooldown
        return commands.Cooldown(1, 86400)
    
    def kanzen_monthly_cooldown(message: discord.Message):
        role = message.guild.get_role(1128460924886458489)
        if role in message.author.roles:
            # boosters have a 2 week cooldown
            return commands.Cooldown(1, 1209600)
        
        # other members have a 1 month cooldown
        return commands.Cooldown(1, 2592000)

    async def get_rank_format(self, member_id, guild_id):
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                query = "SELECT format FROM levels WHERE member_id = ? AND guild_id = ? LIMIT 1"
                result = await conn.execute(query, member_id, guild_id)
                row = await result.fetchone()
                if row:
                    return row['format']
        return None

    async def register_member_levels(self, member_id: int, guild_id: int, xp: Optional[int] = 25) -> None:
        """Registers a member to the levels database
        
        Parameters
        ----------
        member_id: int
            ID of the member to register
        guild_id: int
            ID of the guild to register in
        xp: int, optional
            The amount of xp to be added, defaults to 25
        """
        query = '''INSERT INTO levels (member_id, guild_id, messages, xp, bar_color) VALUES (?, ?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id, 1, xp, "#ecdfb3"))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def _update_message_count(self, member_id: int, guild_id: int, levels: LevelRow) -> None:
        """Updates a member's message count.
        
        Parameters
        ----------
        member_id: int
            ID of the member to update
        guild_id: int
            ID of the guild to update in
        levels: LevelRow
            The member's levels before updating message count
        """
        query = '''UPDATE levels SET messages = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, member_id, guild_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def _update_xp(self, member_id: int, guild_id: int, levels: LevelRow, xp: int) -> None:
        """Updates a member's xp and message count.
        
        Parameters
        ----------
        member_id: int
            ID of the member to register
        guild_id: int
            ID of the guild to register in
        levels: LevelRow
            The member's levels before update
        xp: int
            The amount of XP to add
        """
        query = '''UPDATE levels SET messages = ?, xp = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['messages'] + 1, levels['xp'] + xp, member_id, guild_id))
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
        guild_id = message.guild.id
        levels = await self.get_member_levels(member_id, guild_id)
        if levels == None: # the member hasn't sent a message yet
            # so we have to add them to the database
            await self.register_member_levels(member_id, guild_id)
        else: # have sent a message before
            if retry_after: # on cooldown
                await self._update_message_count(member_id, guild_id, levels)
            else: # not on cooldown so we update the xp
                await self._update_xp(member_id, guild_id, levels, xp)
                await self._level_check(message, levels['xp'], xp)
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

    async def handle_message(self, message: discord.Message) -> None:
        """Handles messages sent on Discord.
        
        Parameters
        ----------
        message: discord.Message
            The message object for the message sent on Discord
        """

        if message.author.bot is True: 
            return # author is a bot, we don't want to add xp to bots

        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        xp_to_add = randint(8, 25)
        await self._level_handler(message, retry_after, xp_to_add)

    def _make_progress_bar(self, progress, color):
        """Makes a progress bar for a member's rank card.
        
        Parameters
        ----------
        progress: float
            How far into their current level the member is
        color: int
            The color of their progress bar
        """
        width = 1500  # Width of the progress bar
        height = 10  # Height of the progress bar
        radius = 0  # Radius of the rounded corners
        progress_bar = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(progress_bar)
        draw.rectangle([(0, 0), (width, height)], fill=(195, 195, 195, 255))
        bg_width = int(width * 1)
        progress_width = int(width * progress)
        draw.rounded_rectangle([(0, 0), (bg_width, height)], fill=(24, 25, 28, 255),width=1, radius=radius)
        draw.rounded_rectangle([(0, 0), (progress_width, height)], fill=color, width=1, radius=radius)
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (bg_width, height)], fill=255, width=0, radius=radius)
        return progress_bar, mask
    
    def _make_progress_bar2(self, progress, color):
        """Makes a progress bar for a member's rank card.
        
        Parameters
        ----------
        progress: float
            How far into their current level the member is
        color: int
            The color of their progress bar
        """
        width = 1080  # Width of the progress bar
        height = 30  # Height of the progress bar
        radius = 0  # Radius of the rounded corners
        progress_bar = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(progress_bar)
        draw.rectangle([(0, 0), (width, height)], fill=(195, 195, 195, 255))
        bg_width = int(width * 1)
        progress_width = int(width * progress)
        draw.rounded_rectangle([(0, 0), (bg_width, height)], fill=(24, 25, 28, 255),width=1, radius=radius)
        draw.rounded_rectangle([(0, 0), (progress_width, height)], fill=color, width=1, radius=radius)
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (bg_width, height)], fill=255, width=0, radius=radius)
        return progress_bar, mask
    
    def _make_progress_bar3(self, progress, color):
        """Makes a progress bar for a member's rank card.
        
        Parameters
        ----------
        progress: float
            How far into their current level the member is
        color: int
            The color of their progress bar
        """
        width = 1080  # Width of the progress bar
        height = 35  # Height of the progress bar
        radius = 0  # Radius of the rounded corners
        progress_bar = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(progress_bar)
        draw.rectangle([(0, 0), (width, height)], fill=(195, 195, 195, 255))
        bg_width = int(width * 1)
        progress_width = int(width * progress)
        draw.rounded_rectangle([(0, 0), (bg_width, height)], fill=(24, 25, 28, 255),width=1, radius=radius)
        draw.rounded_rectangle([(0, 0), (progress_width, height)], fill=color, width=1, radius=radius)
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), (bg_width, height)], fill=255, width=0, radius=radius)
        return progress_bar, mask
    
    def _get_round_avatar1(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        """Converts square avatar retrieved from Discord into a circle avatar
        
        avatar: BytesIO
            The avatar to convert into a circle
        """
        circle = Image.open('./assets/circle-mask.png').resize((75, 75)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((75, 75))
        return avatar_image, circle

    def _get_round_avatar2(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        """Converts square avatar retrieved from Discord into a circle avatar
        
        avatar: BytesIO
            The avatar to convert into a circle
        """
        circle = Image.open('./assets/circle-mask.png').resize((150, 150)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((150, 150))
        return avatar_image, circle

    def _get_round_avatar3(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        """Converts square avatar retrieved from Discord into a circle avatar
        
        avatar: BytesIO
            The avatar to convert into a circle
        """
        circle = Image.open('./assets/circle-mask.png').resize((150, 150)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((150, 150))
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

    def _xp_calculations(self, levels: LevelRow) -> Tuple[float, Union[str, int], Union[str, int], int]:
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
    
    def _get_bg_image(self, url: str):
            """Gets background image"""
            image = requests.get(url, stream=True)
            b_img = Image.open(BytesIO(image.content))
            return b_img

    def _get_card1(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, user: discord.User) -> BytesIO:
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
        user: discord.User
            User object to check roles

        Returns
        -------
        BytesIO
            The rank card as a stream of in-memory bytes
        """
        percentage, xp_have, xp_need, level = self._xp_calculations(levels)
        card = Image.new('RGBA', size=(1500, 500), color='grey')
        if levels['image'] is not None:
            bg = self._get_bg_image(levels['image'])
        else:
            bg = Image.open("./assets/rank_bg.png")
        aspect_ratio = bg.size[0] / bg.size[1]
        if aspect_ratio > 3:
            new_width = int(bg.height * 3)
            bg = bg.crop(((bg.width - new_width) / 2, 0, (bg.width + new_width) / 2, bg.height))
        elif aspect_ratio < 3:
            new_height = int(bg.width / 3)
            bg = bg.crop((0, (bg.height - new_height) / 2, bg.width, (bg.height + new_height) / 2))
        bg = bg.resize((1500, 500))
        card.paste(bg)
        status_circle = Image.open(f'./assets/{status}.png')
        bar, mask = self._make_progress_bar(percentage, levels['bar_color'])
        avatar_paste, circle = self._get_round_avatar1(avatar)
        poppins = Font.poppins(size=67)
        poppins_small = Font.poppins(size=50)
        poppins_xsmall = Font.poppins(size=35)
        poppins_xxsmall = Font.montserrat(size=25)
        font2 = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 35)
        font2small = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 15)
        font3 = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 50)
        roles_img = Image.open('./assets/roles.png')
        lead_roles_x = (card.width - roles_img.width) // 2
        lead_roles_y = (card.height - roles_img.height) // 2
        card.paste(roles_img, (lead_roles_x, lead_roles_y), roles_img)
        zennies_role_id = 1121842393994494082
        has_zennies_role = any(role.id == zennies_role_id for role in user.roles)
        if has_zennies_role:
            zennies_role_img = Image.open('./assets/rank box.png')
            zennies_role_img = zennies_role_img.resize((1500, 500))
            custom_x = 0
            custom_y = 0
            card.paste(zennies_role_img, (custom_x, custom_y), zennies_role_img)
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
            eliterank_role_img = eliterank_role_img.resize((175, 175))
            custom_x = 1055
            custom_y = 35
            card.paste(eliterank_role_img, (custom_x, custom_y), eliterank_role_img)
        elif has_platrank_role:
            platrank_role_img = Image.open('./assets/platrank.png')
            platrank_role_img = platrank_role_img.resize((175, 175))
            custom_x = 1055
            custom_y = 35
            card.paste(platrank_role_img, (custom_x, custom_y), platrank_role_img)
        elif has_diamondrank_role:
            diamondrank_role_img = Image.open('./assets/diamondrank.png')
            diamondrank_role_img = diamondrank_role_img.resize((175, 175))
            custom_x = 1055
            custom_y = 35
            card.paste(diamondrank_role_img, (custom_x, custom_y), diamondrank_role_img)
        elif has_goldrank_role:
            goldrank_role_img = Image.open('./assets/goldrank.png')
            goldrank_role_img = goldrank_role_img.resize((175, 175))
            custom_x = 1055
            custom_y = 35
            card.paste(goldrank_role_img, (custom_x, custom_y), goldrank_role_img)
        elif has_silverrank_role:
            silverrank_role_img = Image.open('./assets/silverrank.png')
            silverrank_role_img = silverrank_role_img.resize((175, 175))
            custom_x = 1055
            custom_y = 35
            card.paste(silverrank_role_img, (custom_x, custom_y), silverrank_role_img)
        elif has_bronzerank_role:
            bronzerank_role_img = Image.open('./assets/bronzerank.png')
            bronzerank_role_img = bronzerank_role_img.resize((175, 175))
            custom_x = 1055
            custom_y = 35
            card.paste(bronzerank_role_img, (custom_x, custom_y), bronzerank_role_img)
        lead_role_id = 1121842279351590973
        has_lead_role = any(role.id == lead_role_id for role in user.roles)
        if has_lead_role:
            special_role_img = Image.open('./assets/lead.png')
            special_role_img = special_role_img.resize((75, 75))
            custom_x = 1375
            custom_y = 375
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        hstaff_id = 1178924350523588618
        has_lead_role = any(role.id == lead_role_id for role in user.roles)
        if has_lead_role:
            special_role_img = Image.open('./assets/hstaff.png')
            special_role_img = special_role_img.resize((100, 100))
            custom_x = 1265
            custom_y = 365
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        staff_role_id = 1135244903165722695
        has_staff_role = any(role.id == staff_role_id for role in user.roles)
        if has_staff_role:
            staff_role_img = Image.open('./assets/staff.png')
            staff_role_img = staff_role_img.resize((75, 75))
            custom_x = 1275
            custom_y = 275
            card.paste(staff_role_img, (custom_x, custom_y), staff_role_img)
        mods_id = 1135244903165722695
        mods_role = any(role.id == mods_id for role in user.roles)
        if mods_role:
            mods_img = Image.open('./assets/mods.png')
            mods_img = mods_img.resize((75, 75))
            custom_x = 1375
            custom_y = 275
            card.paste(mods_img, (custom_x, custom_y), mods_img)
        devs_id = 1179255802003988573
        devs_role = any(role.id == devs_id for role in user.roles)
        if devs_role:
            devs_img = Image.open('./assets/devs.png')
            devs_img = devs_img.resize((75, 75))
            custom_x = 1375
            custom_y = 175
            card.paste(devs_img, (custom_x, custom_y), devs_img)
        booster_role_id = 1128460924886458489
        has_booster_role = any(role.id == booster_role_id for role in user.roles)
        if has_booster_role:
            booster_role_img = Image.open('./assets/booster.png')
            booster_role_img = booster_role_img.resize((75, 75))
            custom_x = 1275
            custom_y = 175
            card.paste(booster_role_img, (custom_x, custom_y), booster_role_img)
        top20_role_id = 1125233965599555615
        has_top20_role = any(role.id == top20_role_id for role in user.roles)
        if has_top20_role:
            top20_role_img = Image.open('./assets/top20.png')
            top20_role_img = top20_role_img.resize((75, 75))
            custom_x = 1375
            custom_y = 90
            card.paste(top20_role_img, (custom_x, custom_y), top20_role_img)
        zennies_role_id = 1121842393994494082
        has_zennies_role = any(role.id == zennies_role_id for role in user.roles)
        if has_zennies_role:
            zennies_role_img = Image.open('./assets/zennies.png')
            zennies_role_img = zennies_role_img.resize((75, 75))
            custom_x = 1275
            custom_y = 90
            card.paste(zennies_role_img, (custom_x, custom_y), zennies_role_img)
        
        card.paste(avatar_paste, (15, 15), circle)
        card.paste(bar, (0, 490), mask)
        draw = ImageDraw.Draw(card, 'RGBA')
        draw.text((105, 15), name, fill=levels['bar_color'], font=poppins_xsmall)
        draw.text((1283, 25), 'Server Badges', fill=levels['bar_color'], font=poppins_xxsmall)
        draw.text((650, 425), f'{xp_have} / {xp_need}', fill=levels['bar_color'], font=poppins_small)
        draw.text((235, 430), f'{level}', fill=levels['bar_color'], font=font2)
        draw.text((15,425), 'Server Level','#ffffff', font=poppins_xsmall)
        draw.text((15,390), 'Server Rank', '#ffffff', font=poppins_xsmall)
        draw.text((235, 390), f"#{str(rank)}", fill=levels['bar_color'], font=font2)
        draw.text((1065, 15), f"Kanzen Ranked", fill=levels['bar_color'], font=font2small)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer
    
    def _get_card2(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, user: discord.User) -> BytesIO:
        """Creates a rank card.
        
        Parameters
        ----------
        name: str
            Username to display on the card
        status: str
            Discord activity status to display next to the avatar
        avatar: BytesIO
            Circle-shaped avatar to display on the card
        levels: LevelRow
            Database level row to retrieve level information
        rank: int
            Rank to display on the card
        user: discord.User
            User object to check roles

        Returns
        -------
        BytesIO
            The rank card as a stream of in-memory bytes
        """
        percentage, xp_have, xp_need, level = self._xp_calculations(levels)
        card = Image.new('RGBA', size=(1080, 1080), color='grey')
        if levels['image'] is not None:
            bg = self._get_bg_image(levels['image'])
            bg = bg.resize((1080, 1080))
        else:
            bg = Image.open("./assets/rank2_bg.png")
            min_dim = min(bg.size)
            bg = bg.crop((0, 0, min_dim, min_dim))
            bg = bg.resize((1080, 1080))
        card.paste(bg)
        status_circle = Image.open(f'./assets/{status}.png')
        bar, mask = self._make_progress_bar2(percentage, levels['bar_color'])
        avatar_paste, circle = self._get_round_avatar2(avatar)
        poppins = Font.poppins(size=67)
        poppins_small = Font.poppins(size=50)
        poppins_xsmall = Font.poppins(size=35)
        poppins_xxsmall = Font.montserrat(size=25)
        font2 = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 35)
        font3 = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 50)
        font2small = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 23)
        roles_img = Image.open('./assets/rank2_badges.png')
        lead_roles_x = (card.width - roles_img.width) // 2
        lead_roles_y = (card.height - roles_img.height) // 2
        card.paste(roles_img, (lead_roles_x, lead_roles_y), roles_img)
        lead_roles_x = (card.width - roles_img.width) // 2
        lead_roles_y = (card.height - roles_img.height) // 2
        card.paste(roles_img, (lead_roles_x, lead_roles_y), roles_img)
        lead_role_id = 1121842279351590973
        has_lead_role = any(role.id == lead_role_id for role in user.roles)
        zennies_role_id = 1121842393994494082
        has_zennies_role = any(role.id == zennies_role_id for role in user.roles)
        if has_zennies_role:
            zennies_role_img = Image.open('./assets/rank box.png')
            zennies_role_img = zennies_role_img.resize((1500, 500))
            custom_x = -190
            custom_y = 800
            card.paste(zennies_role_img, (custom_x, custom_y), zennies_role_img)
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
            eliterank_role_img = eliterank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 825
            card.paste(eliterank_role_img, (custom_x, custom_y), eliterank_role_img)
        elif has_platrank_role:
            platrank_role_img = Image.open('./assets/platrank.png')
            platrank_role_img = platrank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 825
            card.paste(platrank_role_img, (custom_x, custom_y), platrank_role_img)
        elif has_diamondrank_role:
            diamondrank_role_img = Image.open('./assets/diamondrank.png')
            diamondrank_role_img = diamondrank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 825
            card.paste(diamondrank_role_img, (custom_x, custom_y), diamondrank_role_img)
        elif has_goldrank_role:
            goldrank_role_img = Image.open('./assets/goldrank.png')
            goldrank_role_img = goldrank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 825
            card.paste(goldrank_role_img, (custom_x, custom_y), goldrank_role_img)
        elif has_silverrank_role:
            silverrank_role_img = Image.open('./assets/silverrank.png')
            silverrank_role_img = silverrank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 825
            card.paste(silverrank_role_img, (custom_x, custom_y), silverrank_role_img)
        elif has_bronzerank_role:
            bronzerank_role_img = Image.open('./assets/bronzerank.png')
            bronzerank_role_img = bronzerank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 825
            card.paste(bronzerank_role_img, (custom_x, custom_y), bronzerank_role_img)
        lead_role_id = 1121842279351590973
        has_lead_role = any(role.id == lead_role_id for role in user.roles)
        if has_lead_role:
            special_role_img = Image.open('./assets/lead.png')
            special_role_img = special_role_img.resize((75, 75))
            custom_x = 1375
            custom_y = 375
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        hstaff_id = 1178924350523588618
        has_lead_role = any(role.id == lead_role_id for role in user.roles)
        if has_lead_role:
            special_role_img = Image.open('./assets/hstaff.png')
            special_role_img = special_role_img.resize((100, 100))
            custom_x = 1265
            custom_y = 365
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        staff_role_id = 1135244903165722695
        has_staff_role = any(role.id == staff_role_id for role in user.roles)
        if has_staff_role:
            staff_role_img = Image.open('./assets/staff.png')
            staff_role_img = staff_role_img.resize((75, 75))
            custom_x = 1275
            custom_y = 275
            card.paste(staff_role_img, (custom_x, custom_y), staff_role_img)
        mods_id = 1135244903165722695
        mods_role = any(role.id == mods_id for role in user.roles)
        if mods_role:
            mods_img = Image.open('./assets/mods.png')
            mods_img = mods_img.resize((75, 75))
            custom_x = 1375
            custom_y = 275
            card.paste(mods_img, (custom_x, custom_y), mods_img)
        devs_id = 1179255802003988573
        devs_role = any(role.id == devs_id for role in user.roles)
        if devs_role:
            devs_img = Image.open('./assets/devs.png')
            devs_img = devs_img.resize((75, 75))
            custom_x = 1375
            custom_y = 175
            card.paste(devs_img, (custom_x, custom_y), devs_img)
        booster_role_id = 1128460924886458489
        has_booster_role = any(role.id == booster_role_id for role in user.roles)
        if has_booster_role:
            booster_role_img = Image.open('./assets/booster.png')
            booster_role_img = booster_role_img.resize((75, 75))
            custom_x = 1275
            custom_y = 175
            card.paste(booster_role_img, (custom_x, custom_y), booster_role_img)
        top20_role_id = 1125233965599555615
        has_top20_role = any(role.id == top20_role_id for role in user.roles)
        if has_top20_role:
            top20_role_img = Image.open('./assets/top20.png')
            top20_role_img = top20_role_img.resize((75, 75))
            custom_x = 1375
            custom_y = 90
            card.paste(top20_role_img, (custom_x, custom_y), top20_role_img)
        zennies_role_id = 1121842393994494082
        has_zennies_role = any(role.id == zennies_role_id for role in user.roles)
        if has_zennies_role:
            zennies_role_img = Image.open('./assets/zennies.png')
            zennies_role_img = zennies_role_img.resize((75, 75))
            custom_x = 1275
            custom_y = 90
            card.paste(zennies_role_img, (custom_x, custom_y), zennies_role_img)
        if has_lead_role:
            special_role_img = Image.open('./assets/lead.png')
            special_role_img = special_role_img.resize((100, 100))
            custom_x = 200
            custom_y = 725
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        hstaff_id = 1178924350523588618
        has_hstaff_role = any(role.id == hstaff_id for role in user.roles)
        if has_hstaff_role:
            special_role_img = Image.open('./assets/hstaff.png')
            special_role_img = special_role_img.resize((125, 125))
            custom_x = 55
            custom_y = 715
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        staff_role_id = 1135244903165722695
        has_staff_role = any(role.id == staff_role_id for role in user.roles)
        if has_staff_role:
            staff_role_img = Image.open('./assets/staff.png')
            staff_role_img = staff_role_img.resize((100, 100))
            custom_x = 200
            custom_y = 600
            card.paste(staff_role_img, (custom_x, custom_y), staff_role_img)
        mods_id = 1135244903165722695
        mods_role = any(role.id == mods_id for role in user.roles)
        if mods_role:
            mods_img = Image.open('./assets/mods.png')
            mods_img = mods_img.resize((100, 100))
            custom_x = 65
            custom_y = 600
            card.paste(mods_img, (custom_x, custom_y), mods_img)
        devs_id = 1179255802003988573
        devs_role = any(role.id == devs_id for role in user.roles)
        if devs_role:
            devs_img = Image.open('./assets/devs.png')
            devs_img = devs_img.resize((100, 100))
            custom_x = 200
            custom_y = 450
            card.paste(devs_img, (custom_x, custom_y), devs_img)
        booster_role_id = 1128460924886458489
        has_booster_role = any(role.id == booster_role_id for role in user.roles)
        if has_booster_role:
            booster_role_img = Image.open('./assets/booster.png')
            booster_role_img = booster_role_img.resize((100, 100))
            custom_x = 65
            custom_y = 450
            card.paste(booster_role_img, (custom_x, custom_y), booster_role_img)
        top20_role_id = 1125233965599555615
        has_top20_role = any(role.id == top20_role_id for role in user.roles)
        if has_top20_role:
            top20_role_img = Image.open('./assets/top20.png')
            top20_role_img = top20_role_img.resize((100, 100))
            custom_x = 200
            custom_y = 300
            card.paste(top20_role_img, (custom_x, custom_y), top20_role_img)
        zennies_role_id = 1121842393994494082
        has_zennies_role = any(role.id == zennies_role_id for role in user.roles)
        if has_zennies_role:
            zennies_role_img = Image.open('./assets/zennies.png')
            zennies_role_img = zennies_role_img.resize((100, 100))
            custom_x = 65
            custom_y = 300
            card.paste(zennies_role_img, (custom_x, custom_y), zennies_role_img)
        
        card.paste(avatar_paste, (800, 35), circle)
        card.paste(bar, (0, 1055), mask)
        draw = ImageDraw.Draw(card, 'RGBA')
        draw.text((775, 175), name, fill=levels['bar_color'], font=poppins_xsmall)
        draw.text((60, 225), 'Server Badges', fill=levels['bar_color'], font=font2)
        draw.text((400, 1000), f'{xp_have} / {xp_need}', fill=levels['bar_color'], font=font3)
        draw.text((290, 853), f'{level}', fill=levels['bar_color'], font=font2)
        draw.text((75, 850), 'Server Level','#ffffff', font=poppins_xsmall)
        draw.text((75, 900), 'Server Rank', '#ffffff', font=poppins_xsmall)
        draw.text((290, 903), f"#{str(rank)}", fill=levels['bar_color'], font=font2)
        draw.text((845, 780), f"Kanzen Ranked", fill=levels['bar_color'], font=font2small)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    def _get_card3(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, user: discord.User) -> BytesIO:
        """Creates a rank card.
        
        Parameters
        ----------
        name: str
            Username to display on the card
        status: str
            Discord activity status to display next to the avatar
        avatar: BytesIO
            Circle-shaped avatar to display on the card
        levels: LevelRow
            Database level row to retrieve level information
        rank: int
            Rank to display on the card
        user: discord.User
            User object to check roles

        Returns
        -------
        BytesIO
            The rank card as a stream of in-memory bytes
        """
        percentage, xp_have, xp_need, level = self._xp_calculations(levels)
        card = Image.new('RGBA', size=(1080, 1500), color='grey')
        if levels['image'] is not None:
            bg = self._get_bg_image(levels['image'])
        else:
            bg = Image.open("./assets/rank3_bg.png")
        bg_width, bg_height = bg.size
        card_width, card_height = card.size
        aspect_ratio = bg_width / bg_height
        new_width = card_width
        new_height = int(card_width / aspect_ratio)
        bg = bg.resize((new_width, new_height))
        y_offset = (card_height - new_height) // 2
        card.paste(bg, (0, y_offset))
        card.paste(bg)
        status_circle = Image.open(f'./assets/{status}.png')
        bar, mask = self._make_progress_bar3(percentage, levels['bar_color'])
        avatar_paste, circle = self._get_round_avatar3(avatar)
        poppins = Font.poppins(size=67)
        poppins_small = Font.poppins(size=50)
        poppins_xsmall = Font.poppins(size=35)
        poppins_xxsmall = Font.montserrat(size=25)
        font2 = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 35)
        font3 = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 50)
        font2small = ImageFont.truetype("./fonts/Montserrat-Bold.ttf", 23)
        roles_img = Image.open('./assets/rank3_badges.png')
        lead_roles_x = (card.width - roles_img.width) // 2
        lead_roles_y = (card.height - roles_img.height) // 2
        card.paste(roles_img, (lead_roles_x, lead_roles_y), roles_img)
        lead_role_id = 1121842279351590973
        has_lead_role = any(role.id == lead_role_id for role in user.roles)
        zennies_role_id = 1121842393994494082
        has_zennies_role = any(role.id == zennies_role_id for role in user.roles)
        if has_zennies_role:
            zennies_role_img = Image.open('./assets/rank box.png')
            zennies_role_img = zennies_role_img.resize((1500, 500))
            custom_x = -190
            custom_y = 1225
            card.paste(zennies_role_img, (custom_x, custom_y), zennies_role_img)
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
            eliterank_role_img = eliterank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 1250
            card.paste(eliterank_role_img, (custom_x, custom_y), eliterank_role_img)
        elif has_platrank_role:
            platrank_role_img = Image.open('./assets/platrank.png')
            platrank_role_img = platrank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 1250
            card.paste(platrank_role_img, (custom_x, custom_y), platrank_role_img)
        elif has_diamondrank_role:
            diamondrank_role_img = Image.open('./assets/diamondrank.png')
            diamondrank_role_img = diamondrank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 1250
            card.paste(diamondrank_role_img, (custom_x, custom_y), diamondrank_role_img)
        elif has_goldrank_role:
            goldrank_role_img = Image.open('./assets/goldrank.png')
            goldrank_role_img = goldrank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 1250
            card.paste(goldrank_role_img, (custom_x, custom_y), goldrank_role_img)
        elif has_silverrank_role:
            silverrank_role_img = Image.open('./assets/silverrank.png')
            silverrank_role_img = silverrank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 1250
            card.paste(silverrank_role_img, (custom_x, custom_y), silverrank_role_img)
        elif has_bronzerank_role:
            bronzerank_role_img = Image.open('./assets/bronzerank.png')
            bronzerank_role_img = bronzerank_role_img.resize((175, 175))
            custom_x = 865
            custom_y = 1250
            card.paste(bronzerank_role_img, (custom_x, custom_y), bronzerank_role_img)
        if has_lead_role:
            special_role_img = Image.open('./assets/lead.png')
            special_role_img = special_role_img.resize((125, 125))
            custom_x = 260
            custom_y = 1035
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        hstaff_id = 1178924350523588618
        has_hstaff_role = any(role.id == hstaff_id for role in user.roles)
        if has_hstaff_role:
            special_role_img = Image.open('./assets/hstaff.png')
            special_role_img = special_role_img.resize((125, 125))
            custom_x = 90
            custom_y = 1050
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        staff_role_id = 1135244903165722695
        has_staff_role = any(role.id == staff_role_id for role in user.roles)
        if has_staff_role:
            staff_role_img = Image.open('./assets/staff.png')
            staff_role_img = staff_role_img.resize((125, 125))
            custom_x = 90
            custom_y = 850
            card.paste(staff_role_img, (custom_x, custom_y), staff_role_img)
        mods_id = 1135244903165722695
        mods_role = any(role.id == mods_id for role in user.roles)
        if mods_role:
            mods_img = Image.open('./assets/mods.png')
            mods_img = mods_img.resize((125, 125))
            custom_x = 250
            custom_y = 850
            card.paste(mods_img, (custom_x, custom_y), mods_img)
        devs_id = 1179255802003988573
        devs_role = any(role.id == devs_id for role in user.roles)
        if devs_role:
            devs_img = Image.open('./assets/devs.png')
            devs_img = devs_img.resize((125, 125))
            custom_x = 250
            custom_y = 650
            card.paste(devs_img, (custom_x, custom_y), devs_img)
        booster_role_id = 1128460924886458489
        has_booster_role = any(role.id == booster_role_id for role in user.roles)
        if has_booster_role:
            booster_role_img = Image.open('./assets/booster.png')
            booster_role_img = booster_role_img.resize((125, 125))
            custom_x = 90
            custom_y = 650
            card.paste(booster_role_img, (custom_x, custom_y), booster_role_img)
        top20_role_id = 1125233965599555615
        has_top20_role = any(role.id == top20_role_id for role in user.roles)
        if has_top20_role:
            top20_role_img = Image.open('./assets/top20.png')
            top20_role_img = top20_role_img.resize((125, 125))
            custom_x = 250
            custom_y = 450
            card.paste(top20_role_img, (custom_x, custom_y), top20_role_img)
        zennies_role_id = 1121842393994494082
        has_zennies_role = any(role.id == zennies_role_id for role in user.roles)
        if has_zennies_role:
            zennies_role_img = Image.open('./assets/zennies.png')
            zennies_role_img = zennies_role_img.resize((125, 125))
            custom_x = 90
            custom_y = 450
            card.paste(zennies_role_img, (custom_x, custom_y), zennies_role_img)
        
        card.paste(avatar_paste, (75, 75), circle)
        card.paste(bar, (0, 1475), mask)
        draw = ImageDraw.Draw(card, 'RGBA')
        draw.text((250, 85), name, fill=levels['bar_color'], font=poppins)
        draw.text((120, 325), 'Server Badges', fill=levels['bar_color'], font=poppins_xsmall)
        draw.text((415, 1400), f'{xp_have} / {xp_need}', fill=levels['bar_color'], font=poppins_small)
        draw.text((325, 1203), f'{level}', fill=levels['bar_color'], font=font2)
        draw.text((100,1200), 'Server Level','#ffffff', font=poppins_xsmall)
        draw.text((100,1250), 'Server Rank', '#ffffff', font=poppins_xsmall)
        draw.text((325, 1253), f"#{str(rank)}", fill=levels['bar_color'], font=font2)
        draw.text((845, 1205), f"Kanzen Ranked", fill=levels['bar_color'], font=font2small)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer
    
    async def _check_silver(self, member_id: int, guild_id: int) -> bool:
        """Checks if a member is in silver rank.
        
        Parameters
        ----------
        member_id: int
            ID of member to check
        guild_id: int
            ID of the guild to check in

        Returns
        -------
        bool
            True for silver rank, otherwise False
        """
        rank = await self.get_rank(member_id, guild_id)
        return rank < 36
    
    async def _check_gold(self, member_id: int, guild_id: int) -> bool:
        """Checks if a member is in silver rank.
        
        Parameters
        ----------
        member_id: int
            ID of member to check
        guild_id: int
            ID of the guild to check in

        Returns
        -------
        bool
            True for silver rank, otherwise False
        """
        rank = await self.get_rank(member_id, guild_id)
        return rank < 21
    
    async def _check_diamond(self, member_id: int, guild_id: int) -> bool:
        """Checks if a member is in silver rank.
        
        Parameters
        ----------
        member_id: int
            ID of member to check
        guild_id: int
            ID of the guild to check in

        Returns
        -------
        bool
            True for silver rank, otherwise False
        """
        rank = await self.get_rank(member_id, guild_id)
        return rank < 16

    async def _check_plat(self, member_id: int, guild_id: int) -> bool:
        """Checks if a member is in silver rank.
        
        Parameters
        ----------
        member_id: int
            ID of member to check
        guild_id: int
            ID of the guild to check in

        Returns
        -------
        bool
            True for silver rank, otherwise False
        """
        rank = await self.get_rank(member_id, guild_id)
        return rank < 6
    
    async def _check_elite(self, member_id: int, guild_id: int) -> bool:
        """Checks if a member is in silver rank.
        
        Parameters
        ----------
        member_id: int
            ID of member to check
        guild_id: int
            ID of the guild to check in

        Returns
        -------
        bool
            True for silver rank, otherwise False
        """
        rank = await self.get_rank(member_id, guild_id)
        return rank < 4

    async def _get_silver_movedown(self, member_ids: list, guild_id: int) -> int:
        """
        Gets the member to remove from top 20 role when a new member gets the role 
        
        (if 20 people already have the role)
        
        Parameters
        ----------
        member_ids: list
            List containing all the IDs of members with the top 20 role
        guild_id: int
            ID of the guild to get role info from

        Returns
        -------
        int
            The ID of the member to remove from the top 20 role
        """
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]
    
    async def _get_gold_movedown(self, member_ids: list, guild_id: int) -> int:
        """
        Gets the member to remove from top 20 role when a new member gets the role 
        
        (if 20 people already have the role)
        
        Parameters
        ----------
        member_ids: list
            List containing all the IDs of members with the top 20 role
        guild_id: int
            ID of the guild to get role info from

        Returns
        -------
        int
            The ID of the member to remove from the top 20 role
        """
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]
    
    async def _get_diamond_movedown(self, member_ids: list, guild_id: int) -> int:
        """
        Gets the member to remove from top 20 role when a new member gets the role 
        
        (if 20 people already have the role)
        
        Parameters
        ----------
        member_ids: list
            List containing all the IDs of members with the top 20 role
        guild_id: int
            ID of the guild to get role info from

        Returns
        -------
        int
            The ID of the member to remove from the top 20 role
        """
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]

    async def _get_plat_movedown(self, member_ids: list, guild_id: int) -> int:
        """
        Gets the member to remove from top 20 role when a new member gets the role 
        
        (if 20 people already have the role)
        
        Parameters
        ----------
        member_ids: list
            List containing all the IDs of members with the top 20 role
        guild_id: int
            ID of the guild to get role info from

        Returns
        -------
        int
            The ID of the member to remove from the top 20 role
        """
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]

    async def _get_elite_movedown(self, member_ids: list, guild_id: int) -> int:
        """
        Gets the member to remove from top 20 role when a new member gets the role 
        
        (if 20 people already have the role)
        
        Parameters
        ----------
        member_ids: list
            List containing all the IDs of members with the top 20 role
        guild_id: int
            ID of the guild to get role info from

        Returns
        -------
        int
            The ID of the member to remove from the top 20 role
        """
        t = tuple(member_ids)
        query = "SELECT member_id FROM levels WHERE guild_id = ? AND xp = (SELECT MIN(xp) FROM levels WHERE member_id IN {} AND guild_id = ?)".format(t)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id, guild_id)
                member_id = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return member_id[0]

    async def _get_silver(self, guild_id: int) -> int:
        """Gets the member silver ranked.

        Parameters
        ----------
        guild_id: int
            ID of the guild to get member from

        Returns
        -------
        int
            The ID of the member ranked silver
        """
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 35'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def _get_gold(self, guild_id: int) -> int:
        """Gets the member silver ranked.

        Parameters
        ----------
        guild_id: int
            ID of the guild to get member from

        Returns
        -------
        int
            The ID of the member ranked silver
        """
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 20'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def _get_diamond(self, guild_id: int) -> int:
        """Gets the member silver ranked.

        Parameters
        ----------
        guild_id: int
            ID of the guild to get member from

        Returns
        -------
        int
            The ID of the member ranked silver
        """
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 15'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def _get_plat(self, guild_id: int) -> int:
        """Gets the member silver ranked.

        Parameters
        ----------
        guild_id: int
            ID of the guild to get member from

        Returns
        -------
        int
            The ID of the member ranked silver
        """
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 5'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def _get_elite(self, guild_id: int) -> int:
        """Gets the member silver ranked.

        Parameters
        ----------
        guild_id: int
            ID of the guild to get member from

        Returns
        -------
        int
            The ID of the member ranked silver
        """
        query = '''SELECT member_id FROM levels WHERE guild_id = ? ORDER BY xp LIMIT 3'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                member_ids = await cursor.fetchall()
            await self.bot.pool.release(conn)
        return member_ids[-1][0]

    async def get_member_levels(self, member_id: int, guild_id: int) -> Optional[LevelRow]:
        """Gets a member's level row from database.
        
        Parameters
        ----------
        member_id: int
            ID of the member to get the levels for
        guild_id: int
            ID of the guild to get the levels from

        Returns
        -------
        row: LevelRow
            Dictionary-like row of the member's levels
        """
        query = '''SELECT * from levels WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id))
                row = await cursor.fetchone()
                if row:
                    return row
                else:
                    return None

    async def add_xp(self, member_id: int, guild_id: int, xp: int, levels: Optional[LevelRow]) -> None:
        """Adds XP to a member's levels, if member isn't already registered it also registers them.
        
        Parameters
        ----------
        member_id: int
            ID of the member to register
        guild_id: int
            ID of the guild to register levels for
        xp: int
            The amount of XP to add
        levels: LevelRow, optional
            The member's levels before update
        """
        if levels:
            query = '''UPDATE levels SET xp = ? WHERE member_id = ? AND guild_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (levels['xp'] + xp, member_id, guild_id))
                    await conn.commit()
                await self.bot.pool.release(conn)
        else:
            await self.register_member_levels(member_id, guild_id, xp)

    async def remove_xp(self, member_id: int, guild_id: int, xp: int, levels: LevelRow) -> None:
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
        query = '''UPDATE levels SET xp = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['xp'] - xp, member_id, guild_id))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def reset_levels(self, guild_id: int) -> None:
        """Resets the levels for a guild
        
        Parameters
        ----------
        guild_id: int
            ID of guild to reset levels in
        """
        query = '''UPDATE levels SET xp = 0, messages = 0 WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_rank(self, member_id: int, guild_id: int) -> int:
        """Get the current rank of a member.
        
        Parameters
        ----------
        member_id: int
            ID of member whose rank you want to get
        """
        query = '''SELECT COUNT(*) FROM levels WHERE guild_id = ? AND xp > (SELECT xp FROM levels WHERE member_id = ? AND guild_id = ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (guild_id, member_id, guild_id))
                rank = await cursor.fetchone()
            await self.bot.pool.release(conn)
        return rank[0] + 1

    async def generate_card_rank1(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, member: discord.Member) -> BytesIO:
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
        card_generator = functools.partial(self._get_card1, name, status, avatar, levels, rank)
        card = await self.bot.loop.run_in_executor(None, self._get_card1, str(member), str(member.status), avatar, levels, rank, member)
        return card
    
    async def generate_card_rank2(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, member: discord.Member) -> BytesIO:
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
        card_generator = functools.partial(self._get_card2, name, status, avatar, levels, rank)
        card = await self.bot.loop.run_in_executor(None, self._get_card2, str(member), str(member.status), avatar, levels, rank, member)
        return card

    async def generate_card_rank3(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, member: discord.Member) -> BytesIO:
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
        card_generator = functools.partial(self._get_card3, name, status, avatar, levels, rank)
        card = await self.bot.loop.run_in_executor(None, self._get_card3, str(member), str(member.status), avatar, levels, rank, member)
        return card

    async def silver_role_handler(self, member: discord.Member, guild: discord.Guild, role_id: int) -> None:
        """
        Handles silver rank role.
        
        Checks if a member's XP-changes requires modifications to the role members
        
        Parameters
        ----------
        member: discord.Member
            Member to check for role modifications
        guild: discord.Guild
            Guild containing the role
        role_id: int
            ID of the silver rank role
        """
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
        """
        Handles gold rank role.
        
        Checks if a member's XP-changes requires modifications to the role members
        
        Parameters
        ----------
        member: discord.Member
            Member to check for role modifications
        guild: discord.Guild
            Guild containing the role
        role_id: int
            ID of the gold rank role
        """
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
        """
        Handles diamond rank role.
        
        Checks if a member's XP-changes requires modifications to the role members
        
        Parameters
        ----------
        member: discord.Member
            Member to check for role modifications
        guild: discord.Guild
            Guild containing the role
        role_id: int
            ID of the diamond rank role
        """
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
        """
        Handles plat rank role.
        
        Checks if a member's XP-changes requires modifications to the role members
        
        Parameters
        ----------
        member: discord.Member
            Member to check for role modifications
        guild: discord.Guild
            Guild containing the role
        role_id: int
            ID of the plat rank role
        """
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
        """
        Handles elite rank role.
        
        Checks if a member's XP-changes requires modifications to the role members
        
        Parameters
        ----------
        member: discord.Member
            Member to check for role modifications
        guild: discord.Guild
            Guild containing the role
        role_id: int
            ID of the elite rank role
        """
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

    async def get_leaderboard_stats(self, guild_id: int) -> List[LevelRow]:
        """Gets every member's levels ordered by XP

        Parameters
        ----------
        guild_id: int
            ID of the guild to get leaderboard for
        
        Returns
        -------
        list
            List of LevelRow instances
        """
        query = '''SELECT * FROM levels WHERE guild_id = ? ORDER BY xp DESC'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                rows = await cursor.fetchall()
        return rows
                
    async def set_rank_color(self, member_id: int, guild_id: int, color: str) -> None:
        """Changes the progress bar color for a member's rank card
        
        Parameters
        ----------
        member_id: int
            ID of member whose color is being changed
        guild_id: int
            ID of guild to change color in
        color: str
            Hex color to change to
        """
        query = '''UPDATE levels SET bar_color = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, color, member_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_rank_image(self, member_id: int, guild_id: int, image: str) -> None:
        """Changes the progress bar image for a member's rank card
        
        Parameters
        ----------
        member_id: int
            ID of member whose image is being changed
        guild_id: int
            ID of guild to change image in
        image: str
            image to change to
        """
        query = '''UPDATE levels SET image = ? WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, image, member_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def register_guild(self, guild_id: int) -> None:
        """Adds guild to database
        
        Parameters
        ----------
        guild_id: int
            ID of guild to register
        """
        query = '''INSERT INTO setup (guild_id, activated) VALUES (?, 1)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_levels_status(self, guild_id: int) -> int:
        """Checks whether levels is activated or not in a guild
        
        Parameters
        ----------
        guild_id: int
            ID of guild to get status for
        """
        query = '''SELECT activated FROM setup WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                status = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if status is not None:
            return status[0]
        else:
            await self.register_guild(guild_id)
            return 1

    async def change_status(self, guild_id: int, status: Literal[1, 0]) -> None:
        """Adds guild to database
        
        Parameters
        ----------
        guild_id: int
            ID of guild to register
        status: int
            The status to update to
        """
        former_status = await self.get_levels_status(guild_id)
        if not former_status == status:
            query = '''UPDATE setup SET activated = ? WHERE guild_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, status, guild_id)
                    await conn.commit()
                await self.bot.pool.release(conn)
        
    async def get_bronze_role_id(self, guild_id: int) -> Union[int, None]:
        """Gets the Bronze role id for a guild if there is one
        
        Parameters
        ----------
        guild_id: int
            ID of the guild to get status for
        """
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
        """Gets the gold role id for a guild if there is one
        
        Parameters
        ----------
        guild_id: int
            ID of the guild to get status for
        """
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
        """Gets the diamond role id for a guild if there is one
        
        Parameters
        ----------
        guild_id: int
            ID of the guild to get status for
        """
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
        """Gets the plat role id for a guild if there is one
        
        Parameters
        ----------
        guild_id: int
            ID of the guild to get status for
        """
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
        """Gets the elite role id for a guild if there is one
        
        Parameters
        ----------
        guild_id: int
            ID of the guild to get status for
        """
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
        """Gets the silver role id for a guild if there is one
        
        Parameters
        ----------
        guild_id: int
            ID of the guild to get status for
        """
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
        """Sets a guild's silver role
        
        Parameters
        ----------
        guild_id: int
            ID of guild with the role in it
        role_id: int, optional
            ID of the role to give to silver
        """
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET silver_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_gold_role(self, guild_id: int, role_id: int) -> None:
        """Sets a guild's gold role
        
        Parameters
        ----------
        guild_id: int
            ID of guild with the role in it
        role_id: int, optional
            ID of the role to give to gold
        """
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET gold_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_diamond_role(self, guild_id: int, role_id: int) -> None:
        """Sets a guild's diamond role
        
        Parameters
        ----------
        guild_id: int
            ID of guild with the role in it
        role_id: int, optional
            ID of the role to give to diamond
        """
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET diamond_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_plat_role(self, guild_id: int, role_id: int) -> None:
        """Sets a guild's plat role
        
        Parameters
        ----------
        guild_id: int
            ID of guild with the role in it
        role_id: int, optional
            ID of the role to give to plat
        """
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET plat_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_elite_role(self, guild_id: int, role_id: int) -> None:
        """Sets a guild's elite role
        
        Parameters
        ----------
        guild_id: int
            ID of guild with the role in it
        role_id: int, optional
            ID of the role to give to elite
        """
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET elite_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_bronze_role(self, guild_id: int, role_id: int) -> None:
        """Sets a guild's Bronze role
        
        Parameters
        ----------
        guild_id: int
            ID of the guild with the role
        role_id: int, optional
            ID of the Bronze role
        """
        role_id = "NULL" if role_id == 0 else role_id
        query = '''UPDATE setup SET bronze_role_id = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, role_id, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.register_guild(guild.id)

    @commands.group(invoke_without_command=True, hidden=True)
    @commands.has_permissions(administrator=True)
    async def levelling(self, ctx: commands.Context):
        """Group that manages status of the levelling system"""
        status_num = await self.get_levels_status(ctx.guild.id)
        status = self.status_holder[status_num]
        role_id = await self.get_top_20_role_id(ctx.guild.id)
        embed = discord.Embed(title="level system information", color=0x2B2D31)
        embed.add_field(name="status", value=f"the levelling system is **{status}**", inline=False)
        if role_id is not None and role_id != "NULL":
            embed.add_field(name="top 20 role", value=f"members ranked top 20 get the <@&{role_id}> role", inline=False)
        else:
            embed.add_field(name="top 20 role", value="a top 20 role has not been set.\nuse `+levelling setrole <role>` if you want to give a role to members ranked top 20!", inline=False)
        await ctx.send(embed=embed)

    @levelling.command(aliases=["on"], description="Activate the levelling system in a server", extras="+levelling activate")
    @commands.has_permissions(administrator=True)
    async def activate(self, ctx: commands.Context):
        """Activates levelling system in current guild"""
        await self.change_status(ctx.guild.id, 1)
        embed = discord.Embed(
            title='status changed!',
            description=f'levelling system has now been **activated** for this server!',
            color=0x2B2D31
        )
        await ctx.reply(embed=embed)

    @levelling.command(aliases=["off"], description="Deactivate the levelling system in a server", extras="+levelling deactivate")
    @commands.has_permissions(administrator=True)
    async def deactivate(self, ctx: commands.Context):
        """Activates levelling system in current guild"""
        await self.change_status(ctx.guild.id, 0)
        embed = discord.Embed(
            title='status changed!',
            description=f'levelling system has now been **deactivated** for this server!',
            color=0x2B2D31
        )
        await ctx.reply(embed=embed)

    @levelling.command(description="Set the Bronze role", extras="+levelling setbronze @role")
    @commands.has_permissions(administrator=True)
    async def setbronze(self, ctx: commands.Context, role: discord.Role):
        """Sets a role for members ranked Bronze
        
        Parameters
        ----------
        role: discord.Role
            The role to give to Bronze members
        """
        guild = ctx.guild
        bronze_role_id = role.id
        await self.set_bronze_role(guild.id, bronze_role_id)
        for member in guild.members:
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
        await ctx.reply(embed=embed)

    @levelling.command(description="Set the silver role", extras="+levelling setsilver @role")
    @commands.has_permissions(administrator=True)
    async def setsilver(self, ctx: commands.Context, role: discord.Role):
        """Sets a role for members ranked silver
        
        Parameters
        ----------
        role: discord.Role
            the role to give the members
        """
        await self.set_silver_role(ctx.guild.id, role.id)
        embed = discord.Embed(
            title='silver role has been set!',
            description=f'members ranked silver will receive the {role.mention} role!',
            color=0x2B2D31
        )
        await ctx.reply(embed=embed)

    @levelling.command(description="Set the gold role", extras="+levelling setgold @role")
    @commands.has_permissions(administrator=True)
    async def setgold(self, ctx: commands.Context, role: discord.Role):
        """Sets a role for members ranked gold
        
        Parameters
        ----------
        role: discord.Role
            the role to give the members
        """
        await self.set_gold_role(ctx.guild.id, role.id)
        embed = discord.Embed(
            title='gold role has been set!',
            description=f'members ranked gold will receive the {role.mention} role!',
            color=0x2B2D31
        )
        await ctx.reply(embed=embed)

    @levelling.command(description="Set the diamond role", extras="+levelling setdiamond @role")
    @commands.has_permissions(administrator=True)
    async def setdiamond(self, ctx: commands.Context, role: discord.Role):
        """Sets a role for members ranked diamond
        
        Parameters
        ----------
        role: discord.Role
            the role to give the members
        """
        await self.set_diamond_role(ctx.guild.id, role.id)
        embed = discord.Embed(
            title='diamond role has been set!',
            description=f'members ranked diamond will receive the {role.mention} role!',
            color=0x2B2D31
        )
        await ctx.reply(embed=embed)

    @levelling.command(description="Set the plat role", extras="+levelling setplat @role")
    @commands.has_permissions(administrator=True)
    async def setplat(self, ctx: commands.Context, role: discord.Role):
        """Sets a role for members ranked plat
        
        Parameters
        ----------
        role: discord.Role
            the role to give the members
        """
        await self.set_plat_role(ctx.guild.id, role.id)
        embed = discord.Embed(
            title='plat role has been set!',
            description=f'members ranked plat will receive the {role.mention} role!',
            color=0x2B2D31
        )
        await ctx.reply(embed=embed)

    @levelling.command(description="Set the elite role", extras="+levelling setelite @role")
    @commands.has_permissions(administrator=True)
    async def setelite(self, ctx: commands.Context, role: discord.Role):
        """Sets a role for members ranked elite
        
        Parameters
        ----------
        role: discord.Role
            the role to give the members
        """
        await self.set_elite_role(ctx.guild.id, role.id)
        embed = discord.Embed(
            title='elite role has been set!',
            description=f'members ranked elite will receive the {role.mention} role!',
            color=0x2B2D31
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=['lb', 'levels'], description="See the level leaderboard", extras="aliases +lb, +levels")
    @levels_is_activated()
    async def leaderboard(self, ctx: commands.Context, role: discord.Role):
        """sends the current leaderboard"""
        embeds = []
        description = ""
        rows = await self.get_leaderboard_stats(ctx.guild.id)
        per_page = 5 if ctx.author.is_on_mobile() else 10

        for i, row in enumerate(rows, start=1):
            msg = "messages" if row['messages'] != 1 else "message"
            xp = row["xp"]
            lvl = 0

            while True:
                if xp < ((50*(lvl**2))+(50*(lvl-1))):
                    break
                lvl += 1

            user = ctx.guild.get_member(row['member_id'])

            elite_role = 1187540294221172786
            has_elite = discord.utils.get(user.roles, id=elite_role) is not None
            emoji = "<:elite:1187761795109244988>" if has_elite else ""

            platinum_role = 1187540267696398427
            has_platinum = discord.utils.get(user.roles, id=platinum_role) is not None
            emoji = "<:platinum:1187746184803143700>" if has_platinum and not has_elite else emoji

            diamond_role = 1187540240836087858
            has_diamond = discord.utils.get(user.roles, id=diamond_role) is not None
            emoji = "<:diamond:1187746195276316682>" if has_diamond and not has_elite and not has_platinum else emoji

            gold_role = 1187540222708297748
            has_gold = discord.utils.get(user.roles, id=gold_role) is not None
            emoji = "<:gold:1187746191182676070>" if has_gold and not has_elite and not has_platinum and not has_diamond else emoji

            silver_role = 1187508615364477039
            has_silver = discord.utils.get(user.roles, id=silver_role) is not None
            emoji = "<:silver:1187746188196327524>" if has_silver and not has_elite and not has_platinum and not has_diamond and not has_gold else emoji

            bronze_role = 1187508597761003572
            has_bronze = discord.utils.get(user.roles, id=bronze_role) is not None
            emoji = "<:bronze:1187746198879207475>" if has_bronze and not has_elite and not has_platinum and not has_diamond and not has_gold and not has_silver else emoji
            
            description += f"**{i}.**<@!{row['member_id']}> {emoji}\n{row['xp']} xp | {row['messages']} {msg} | level {lvl}\n\n"

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

    @commands.command(description="Check your rank", extras="+rank (optional @member)")
    @levels_is_activated()
    async def rank(self, ctx: commands.Context, member: Optional[discord.Member]):
        async with ctx.typing():
            member = member or ctx.author
            levels = await self.get_member_levels(member.id, ctx.guild.id)
            rank = await self.get_rank(member.id, ctx.guild.id)
            avatar_url = member.display_avatar.replace(static_format='png', size=256).url
            response = await self.bot.session.get(avatar_url)
            avatar = BytesIO(await response.read())
            avatar.seek(0)

            if ctx.guild.id == 896619762354892821:
                button = discord.ui.Button(label=f"Made for Kanzengrp", url=f"https://instagram.com/kanzengrp")
                view = discord.ui.View()
                view.add_item(button)
            else:
                view = None

            if levels:
                format = await self.get_rank_format(member.id, ctx.guild.id)
                if format == "Rank 1":
                    card = await self.generate_card_rank1(str(member), str(member.status), avatar, levels, rank, member)
                elif format == "Rank 2":
                    card = await self.generate_card_rank2(str(member), str(member.status), avatar, levels, rank, member)
                elif format == "Rank 3":
                    card = await self.generate_card_rank3(str(member), str(member.status), avatar, levels, rank, member)
                else:
                    card = None
                if card:
                    await ctx.reply(file=discord.File(card, 'card.png'), mention_author=False, view=view)
                else:
                    await ctx.reply(f"Hey! new update for ranks has been released, you can now choose between 3 different formats for your rank card.\nPlease select a format! to do so do +rank1, +rank2, or +rank3!", mention_author=False)  # Display the unknown format
            else:
                await ctx.reply(f"{member} doesn't have any levels yet!!", mention_author=False)

    async def update_rank_format(self, member_id, guild_id, format):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE levels SET format = $1 WHERE member_id = $2 AND guild_id = $3", format, member_id, guild_id)

    @commands.command(description="Change your rank card format to version 1", extras="+rank1")
    async def rank1(self, ctx):
        await self.update_rank_format(ctx.author.id, ctx.guild.id, "Rank 1")
        embed = discord.Embed(title="New format selected!", description="You have selected format **version 1**\n\nIf you want to cusomise this rank card you can with the commands **+rankcolor** and include a hexcode (example: #2b2d31)\n\nYou can also change your background with +rankbg and attach you background image, please do remember that the background image needs to be **1500x500** format so it isn't cropped!", color=0x2b2d31)
        await ctx.reply(embed=embed)

    @commands.command(description="Change your rank card format to version 2", extras="+rank2")
    async def rank2(self, ctx):
        await self.update_rank_format(ctx.author.id, ctx.guild.id, "Rank 2")
        embed = discord.Embed(title="New format selected!", description="You have selected format **version 2**\n\nIf you want to cusomise this rank card you can with the commands **+rankcolor** and include a hexcode (example: #2b2d31)\n\nYou can also change your background with +rankbg and attach you background image, please do remember that the background image needs to be **1080x1080** format so it isn't cropped!", color=0x2b2d31)
        await ctx.reply(embed=embed)

    @commands.command(description="Change your rank card format to version 3", extras="rank3")
    async def rank3(self, ctx):
        await self.update_rank_format(ctx.author.id, ctx.guild.id, "Rank 3")
        embed = discord.Embed(title="New format selected!", description="You have selected format **version 3**\n\nIf you want to cusomise this rank card you can with the commands **+rankcolor** and include a hexcode (example: #2b2d31)\n\nYou can also change your background with +rankbg and attach you background image, please do remember that the background image needs to be **1080x1500** format so it isn't cropped!", color=0x2b2d31)
        await ctx.reply(embed=embed)

    @commands.command(description="Change your rank card color with hex codes", extras="+rankcolor #2b2d31")
    @levels_is_activated()
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
            await self.set_rank_color(ctx.author.id, ctx.guild.id, color)
            embed = discord.Embed(
                title='changed your bar color!',
                description=f'your new bar color is `{color}`',
                color=0x2B2D31
            )
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"`{color}` is not a valid hex color")

    @commands.command(description="Attatch an image when doing this command!", extras="+rankbg (attatch image)")
    async def rankbg(self, ctx):
        if len(ctx.message.attachments) == 0:
            await ctx.reply("Please attach an image to set as your rank background.")
            return

        attachment = ctx.message.attachments[0]
        if not attachment.content_type.split("/")[0] == "image":
            await ctx.reply("Please attach a valid image (PNG, JPG, JPEG, GIF).")
            return

        member_id = ctx.author.id
        async with self.bot.pool.acquire() as conn:
            query = "UPDATE levels SET image = ? WHERE member_id = ? AND guild_id = ?"
            await conn.execute(query, (attachment.url, member_id, ctx.guild.id))
            await conn.commit()
        embed=discord.Embed(title="Rank background has been updated!", color=0x2b2d31)
        embed.set_image(url=attachment.url)
        await ctx.reply(embed=embed)

    @commands.command(description="Add xp to someone", extras="+add @member amount")
    @levels_is_activated()
    @commands.has_permissions(manage_guild=True)
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
        levels = await self.get_member_levels(member.id, ctx.guild.id)
        await self.add_xp(member.id, ctx.guild.id, amount, levels)
        silver = await self.get_silver_role_id(ctx.guild.id)
        if silver is not None:
            await self.silver_role_handler(member, ctx.guild, silver)
        gold = await self.get_gold_role_id(ctx.guild.id)
        if gold is not None:
            await self.gold_role_handler(member, ctx.guild, gold)
        diamond = await self.get_diamond_role_id(ctx.guild.id)
        if diamond is not None:
            await self.diamond_role_handler(member, ctx.guild, diamond)
        plat = await self.get_plat_role_id(ctx.guild.id)
        if plat is not None:
            await self.plat_role_handler(member, ctx.guild, plat)
        elite = await self.get_elite_role_id(ctx.guild.id)
        if elite is not None:
            await self.elite_role_handler(member, ctx.guild, elite)
        embed = discord.Embed(
            title='xp added!',
            description=f'gave `{amount}xp` to {str(member)}',
            color=0x2B2D31
        )
        await ctx.reply(embed=embed)

    @commands.command(description="Add xp to multiple people", extras="+multiadd @member @member amount")
    @levels_is_activated()
    @commands.has_permissions(manage_guild=True)
    async def multiadd(self, ctx: commands.Context, members: commands.Greedy[discord.Member], amount: int):
        """
        add xp to multiple members' level xp

        Parameters
        -----------
        amount: int
            the amount of xp to add
        members: List[discord.Member]
            members to give xp to
        """
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
                levels = await self.get_member_levels(member.id, ctx.guild.id)
                await self.add_xp(member.id, ctx.guild.id, amount, levels)
                silver = await self.get_silver_role_id(ctx.guild.id)
                if silver is not None:
                    await self.silver_role_handler(member, ctx.guild, silver)
                gold = await self.get_gold_role_id(ctx.guild.id)
                if gold is not None:
                    await self.gold_role_handler(member, ctx.guild, gold)
                diamond = await self.get_diamond_role_id(ctx.guild.id)
                if diamond is not None:
                    await self.diamond_role_handler(member, ctx.guild, diamond)
                plat = await self.get_plat_role_id(ctx.guild.id)
                if plat is not None:
                    await self.plat_role_handler(member, ctx.guild, plat)
                elite = await self.get_elite_role_id(ctx.guild.id)
                if elite is not None:
                    await self.elite_role_handler(member, ctx.guild, elite)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['take'], description="Remove xp from someone", extras="+remove @member amount")
    @levels_is_activated()
    @commands.has_permissions(manage_guild=True)
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
        levels = await self.get_member_levels(member.id, ctx.guild.id)
        if levels:
            if amount > levels['xp']:
                await ctx.reply("you can't take away more xp than the user already has!")
            else:
                await self.remove_xp(member.id, ctx.guild.id, amount, levels)
                silver = await self.get_silver_role_id(ctx.guild.id)
                if silver is not None:
                    await self.silver_role_handler(member, ctx.guild, silver)
                gold = await self.get_gold_role_id(ctx.guild.id)
                if gold is not None:
                    await self.gold_role_handler(member, ctx.guild, gold)
                diamond = await self.get_diamond_role_id(ctx.guild.id)
                if diamond is not None:
                    await self.diamond_role_handler(member, ctx.guild, diamond)
                plat = await self.get_plat_role_id(ctx.guild.id)
                if plat is not None:
                    await self.plat_role_handler(member, ctx.guild, plat)
                elite = await self.get_elite_role_id(ctx.guild.id)
                if elite is not None:
                    await self.elite_role_handler(member, ctx.guild, elite)
                embed = discord.Embed(
                    title='xp removed!',
                    description=f'removed `{amount}xp` from {str(member)}',
                    color=0x2B2D31
                )
                await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"{str(member)} doesn't have any xp yet!")

    @commands.command(description="Reset the levels", extras="+reset")
    @commands.has_permissions(administrator=True)
    @levels_is_activated()
    @commands.has_permissions(manage_guild=True)
    async def reset(self, ctx: commands.Context):
        """Wipes all XP from the database"""
        message = await ctx.reply("are you sure you want to reset the ranks? it's irreversible!")
        await message.add_reaction('👍')

        def check(reaction, user):
            return user == ctx.author and str(reaction) == '👍'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
            await self.reset_levels(ctx.guild.id)
            embed = discord.Embed(
                title='success!',
                description=f'ranks have been erased.',
                color=0x2B2D31
            )
            return await message.edit(content=None, embed=embed)
        except asyncio.TimeoutError:
            await message.edit(content="~~are you sure you want to reset the ranks? it's irreversible!~~\nreset has been cancelled!")

    @commands.command(description="Get anywhere from 100xp - 300xp everyday!", extras="+daily")
    @commands.dynamic_cooldown(kanzen_cooldown, commands.BucketType.user)
    async def daily(self, ctx: commands.Context):
        """Command to claim daily xp"""
        xp = randint(100, 300)
        levels = await self.get_member_levels(ctx.author.id, ctx.guild.id)
        if levels is not None:
            await self.add_xp(ctx.author.id, ctx.guild.id, xp, levels)
        else:
            await self.register_member_levels(ctx.member.id, ctx.guild.id, xp)
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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        status = await self.get_levels_status(message.guild.id)
        if status == 1:
            await self.handle_message(message)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Handles errors occuring in this cog"""
        if isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, commands.RoleNotFound):
            await ctx.reply("Couldn't find that role.", mention_author=False)

    @commands.command(description="Remove a member from the levels databse for a server", extras="+delete @member")
    async def delete(self, ctx, member_id: int):
        guild_id = ctx.guild.id

        async with self.bot.pool.acquire() as conn:
            await conn.execute('DELETE FROM levels WHERE member_id = $1 AND guild_id = $2', member_id, guild_id)

        await ctx.send(f"Member with ID {member_id} has been removed from the database.")

async def setup(bot):
    await bot.add_cog(Levels(bot))