import asyncio
from typing import Optional, TypedDict, Literal
import discord
from discord import app_commands
from discord.ext import commands
import re

class settings(TypedDict):
    guild_id: int
    chatxp: int
    voicexp: int
    dailyxp: int
    top20: int
    reprole: int
    channels: str

class channelselect(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="↶")
    async def back(self, interaction: discord.Interaction, button: discord.Button):
        guild = interaction.guild.id
        if guild == 694010548605550675:
            group = "Chroma"
            group1 = "Chromies"
        else:
            group = "Lyra"
            group1 = "Lyres"
        embed = discord.Embed(title=f"<:settings:1304222799639871530> Home Page", description=f"Welcome to the home page!\nHere you can change all the settings for Hoshi in {group}.\n\nCategories:\n<:bulletpoint:1304247536021667871> Levelling for {group1}\n-# <:thread1:1304222965042249781>Change XP amounts\n<:bulletpoint:1304247536021667871> Automatic Roles\n-# <:thread1:1304222965042249781>Change role ID's for the roles Hoshi can give out\n<:bulletpoint:1304247536021667871> Channels\n-# <:thread1:1304222965042249781>Change what channels members can level up in", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=settingselect(bot=self.bot))

    @discord.ui.button(label="Text Channels")
    async def text(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id
        await interaction.response.send_message(
            f"<:settings:1304222799639871530> **{interaction.user.name}**, please enter the channel IDs separated by spaces.\n"
            f"-# <:thread2:1304222916879323136> Default: **None**\n"
            f"-# <:thread2:1304222916879323136> Please enter the IDs within **60 seconds**\n"
            f"-# <:thread1:1304222965042249781> Enter the IDs in chat!",
            ephemeral=True
        )

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=60, check=check)
            channel_ids = msg.content.split()
            invalid_ids = []
            valid_channels = []

            for channel_id in channel_ids:
                if channel_id.isdigit():
                    channel = interaction.guild.get_channel(int(channel_id))
                    if channel:
                        valid_channels.append(channel)
                    else:
                        invalid_ids.append(channel_id)
                else:
                    invalid_ids.append(channel_id)

            await msg.delete()

            if valid_channels:
                channel_mentions = "\n".join(channel.mention for channel in valid_channels)
                await self.set_textchannels(guild_id, channels=str(channel_mentions))
                await interaction.followup.send(
                    f"<:check:1291748345194348594> **{interaction.user.name}**, the following channels have been set:\n{channel_mentions}",
                    ephemeral=True
                )

            if invalid_ids:
                invalid_list = ", ".join(invalid_ids)
                await interaction.followup.send(
                    f"<:whitex:1304222877305798697> **{interaction.user.name}**, the following IDs were invalid or channels not found:\n{invalid_list}",
                    ephemeral=True
                )

        except asyncio.TimeoutError:
            await interaction.followup.send("You didn’t respond in time. Please try again.", ephemeral=True)

    async def set_textchannels(self, guild_id: int, channels: str) -> None:
        query = f'''UPDATE settings SET channels = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, channels, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

class rolesettings(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="↶")
    async def back(self, interaction: discord.Interaction, button: discord.Button):
        guild = interaction.guild.id
        if guild == 694010548605550675:
            group = "Chroma"
            group1 = "Chromies"
        else:
            group = "Lyra"
            group1 = "Lyres"
        embed = discord.Embed(title=f"<:settings:1304222799639871530> Home Page", description=f"Welcome to the home page!\nHere you can change all the settings for Hoshi in {group}.\n\nCategories:\n<:bulletpoint:1304247536021667871> Levelling for {group1}\n-# <:thread1:1304222965042249781>Change XP amounts\n<:bulletpoint:1304247536021667871> Automatic Roles\n-# <:thread1:1304222965042249781>Change role ID's for the roles Hoshi can give out\n<:bulletpoint:1304247536021667871> Channels\n-# <:thread1:1304222965042249781>Change what channels members can level up in", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=settingselect(bot=self.bot))

    @discord.ui.button(label="Top 20")
    async def toptwenty(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id
        await interaction.response.send_message(
            f"<:settings:1304222799639871530> **{interaction.user.name}**, please enter a role ID.\n"
            f"-# <:thread2:1304222916879323136> Default: **None**\n"
            f"-# <:thread2:1304222916879323136> Please enter the ID within **60 seconds**\n"
            f"-# <:thread1:1304222965042249781> Enter the ID in chat!",
            ephemeral=True
        )

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=60, check=check)
            if msg.content.isdigit():
                xp_amount = int(msg.content)
                await self.set_top20(guild_id, amount=str(xp_amount))
                await msg.delete()
                await interaction.followup.send(
                    f"<:check:1291748345194348594> **{interaction.user.name}**, Top 20 role has been set to <@&{xp_amount}>.",
                    ephemeral=True
                )
            else:
                await msg.delete()
                await interaction.followup.send(
                    "<:whitex:1304222877305798697> Invalid input. Please enter the role ID on it's own.",
                    ephemeral=True
                )

        except asyncio.TimeoutError:
            await interaction.followup.send("You didn’t respond in time. Please try again.", ephemeral=True)

    @discord.ui.button(label="Unlocked Rep")
    async def unlockedrep(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id
        await interaction.response.send_message(
            f"<:settings:1304222799639871530> **{interaction.user.name}**, please enter a role ID.\n"
            f"-# <:thread2:1304222916879323136> Default: **None**\n"
            f"-# <:thread2:1304222916879323136> Please enter the ID within **60 seconds**\n"
            f"-# <:thread1:1304222965042249781> Enter the ID in chat!",
            ephemeral=True
        )

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=60, check=check)
            if msg.content.isdigit():
                xp_amount = int(msg.content)
                await self.set_reprole(guild_id, amount=str(xp_amount))
                await msg.delete()
                await interaction.followup.send(
                    f"<:check:1291748345194348594> **{interaction.user.name}**, the unlocked rep role has been set to <@&{xp_amount}>.",
                    ephemeral=True
                )
            else:
                await msg.delete()
                await interaction.followup.send(
                    "<:whitex:1304222877305798697> Invalid input. Please enter the role ID on it's own.",
                    ephemeral=True
                )

        except asyncio.TimeoutError:
            await interaction.followup.send("You didn’t respond in time. Please try again.", ephemeral=True)

    async def set_top20(self, guild_id: int, amount: str) -> None:
        query = f'''UPDATE settings SET top20 = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, amount, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_reprole(self, guild_id: int, amount: str) -> None:
        query = f'''UPDATE settings SET reprole = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, amount, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

class levelsettings(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="↶")
    async def back(self, interaction: discord.Interaction, button: discord.Button):
        guild = interaction.guild.id
        if guild == 694010548605550675:
            group = "Chroma"
            group1 = "Chromies"
        else:
            group = "Lyra"
            group1 = "Lyres"
        embed = discord.Embed(title=f"<:settings:1304222799639871530> Home Page", description=f"Welcome to the home page!\nHere you can change all the settings for Hoshi in {group}.\n\nCategories:\n<:bulletpoint:1304247536021667871> Levelling for {group1}\n-# <:thread1:1304222965042249781>Change XP amounts\n<:bulletpoint:1304247536021667871> Automatic Roles\n-# <:thread1:1304222965042249781>Change role ID's for the roles Hoshi can give out\n<:bulletpoint:1304247536021667871> Channels\n-# <:thread1:1304222965042249781>Change what channels members can level up in", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=settingselect(bot=self.bot))

    @discord.ui.button(label="Enable", style=discord.ButtonStyle.green, row=2)
    async def enable(self, interaction: discord.Interaction, button: discord.Button):
        await self.change_levels_status(interaction.guild.id, 1)
        await interaction.response.send_message("You have enabled the levelling system!\nDo </help:1202303486512083006> to see the commands", ephemeral=True)

    @discord.ui.button(label="Disable", style=discord.ButtonStyle.red, row=2)
    async def disable(self, interaction: discord.Interaction, button: discord.Button):
        await self.change_levels_status(interaction.guild.id, 0)
        await interaction.response.send_message("You have disabled the levelling system!", ephemeral=True)

    @discord.ui.button(label="Daily XP")
    async def dailyxp(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id
        await interaction.response.send_message(
            f"<:settings:1304222799639871530>**{interaction.user.name}**, Please enter an amount for the daily XP command.\n"
            f"-# <:thread2:1304222916879323136> Default: **150 - 300**\n"
            f"-# <:thread2:1304222916879323136> Please enter the amount within **60 seconds**\n"
            f"-# <:thread1:1304222965042249781> Enter the amount in chat!",
            ephemeral=True
        )

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=60, check=check)

            match = re.match(r"(\d+)\s*-\s*(\d+)", msg.content)
            if match:
                min_xp, max_xp = map(int, match.groups())
                await self.set_dailyxp(guild_id, amount=f"{min_xp} - {max_xp}")
                await msg.delete()
                await interaction.followup.send(
                    f"<:check:1291748345194348594> **{interaction.user.name}**, daily XP has been set to **{min_xp}xp - {max_xp}xp**.",
                    ephemeral=True
                )
            else:
                await msg.delete()
                await interaction.followup.send(
                    "<:whitex:1304222877305798697> Invalid input. Please enter two numbers in the format `min - max`.",
                    ephemeral=True
                )

        except asyncio.TimeoutError:
            await interaction.followup.send("You didn’t respond in time. Please try again.", ephemeral=True)

    @discord.ui.button(label="Chat XP")
    async def chatxp(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id
        await interaction.response.send_message(
            f"<:settings:1304222799639871530> **{interaction.user.name}**, please enter an amount for the chat XP command.\n"
            f"-# <:thread2:1304222916879323136> Default: **150**\n"
            f"-# <:thread2:1304222916879323136> Please enter the amount within **60 seconds**\n"
            f"-# <:thread1:1304222965042249781> Enter the amount in chat!",
            ephemeral=True
        )

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=60, check=check)
            if msg.content.isdigit():
                xp_amount = int(msg.content)
                await self.set_chatxp(guild_id, amount=str(xp_amount))
                await msg.delete()
                await interaction.followup.send(
                    f"<:check:1291748345194348594> **{interaction.user.name}**, chat XP has been set to **{xp_amount} XP**.",
                    ephemeral=True
                )
            else:
                await msg.delete()
                await interaction.followup.send(
                    "<:whitex:1304222877305798697> Invalid input. Please enter a single number (e.g., `15`).",
                    ephemeral=True
                )

        except asyncio.TimeoutError:
            await interaction.followup.send("You didn’t respond in time. Please try again.", ephemeral=True)

    @discord.ui.button(label="Chat XP")
    async def chatxp(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id
        await interaction.response.send_message(
            f"<:settings:1304222799639871530> **{interaction.user.name}**, please enter an amount for the chat XP command.\n"
            f"-# <:thread2:1304222916879323136> Default: **25**\n"
            f"-# <:thread2:1304222916879323136> Please enter the amount within **60 seconds**\n"
            f"-# <:thread1:1304222965042249781> Enter the amount in chat!",
            ephemeral=True
        )

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=60, check=check)
            if msg.content.isdigit():
                xp_amount = int(msg.content)
                await self.set_chatxp(guild_id, amount=str(xp_amount))
                await msg.delete()
                await interaction.followup.send(
                    f"<:check:1291748345194348594> **{interaction.user.name}**, chat XP has been set to **{xp_amount} XP**.",
                    ephemeral=True
                )
            else:
                await msg.delete()
                await interaction.followup.send(
                    "<:whitex:1304222877305798697> Invalid input. Please enter a single number (e.g., `25`).",
                    ephemeral=True
                )

        except asyncio.TimeoutError:
            await interaction.followup.send("You didn’t respond in time. Please try again.", ephemeral=True)

    @discord.ui.button(label="Voice XP")
    async def vcxp(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id
        await interaction.response.send_message(
            f"<:settings:1304222799639871530> **{interaction.user.name}**, please enter an amount for the voice chat XP command.\n"
            f"-# <:thread2:1304222916879323136> Default: **25**\n"
            f"-# <:thread2:1304222916879323136> Please enter the amount within **60 seconds**\n"
            f"-# <:thread1:1304222965042249781> Enter the amount in voice chat!",
            ephemeral=True
        )

        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=60, check=check)
            if msg.content.isdigit():
                xp_amount = int(msg.content)
                await self.set_vcxp(guild_id, amount=str(xp_amount))
                await msg.delete()
                await interaction.followup.send(
                    f"<:check:1291748345194348594> **{interaction.user.name}**, voice chat XP has been set to **{xp_amount} XP**.",
                    ephemeral=True
                )
            else:
                await msg.delete()
                await interaction.followup.send(
                    "<:whitex:1304222877305798697> Invalid input. Please enter a single number (e.g., `25`).",
                    ephemeral=True
                )

        except asyncio.TimeoutError:
            await interaction.followup.send("You didn’t respond in time. Please try again.", ephemeral=True)

    async def set_chatxp(self, guild_id: int, amount: str) -> None:
        query = f'''UPDATE settings SET chatxp = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, amount, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def set_vcxp(self, guild_id: int, amount: str) -> None:
        query = f'''UPDATE settings SET voicexp = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, amount, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    async def change_levels_status(self, guild_id: int, status: Literal[1, 0]) -> None:
        former_status = await self.get_levels_status(guild_id)
        if not former_status == status:
            query = '''UPDATE settings SET levels = ? WHERE guild_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, status, guild_id)
                    await conn.commit()
                    await self.bot.pool.release(conn)

    async def get_levels_status(self, guild_id: int) -> int:
        query = '''SELECT levels FROM settings WHERE guild_id = ?'''
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

    async def set_dailyxp(self, guild_id: int, amount: str) -> None:
        query = f'''UPDATE settings SET dailyxp = ? WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, amount, guild_id)
                await conn.commit()
            await self.bot.pool.release(conn)

class settingselect(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Levelling")
    async def levelling(self, interaction: discord.Interaction, button: discord.Button):
        guild = interaction.guild.id
        if guild == 694010548605550675:
            group = "Chroma"
            group1 = "Chromies"
        else:
            group = "Lyra"
            group1 = "Lyres"
        dailyxp = await self.get_dailyxp(interaction.guild.id)
        voicexp = await self.get_voicexp(interaction.guild.id)
        chatxp = await self.get_chatxp(interaction.guild.id)
        statuses = await self.get_levels_status(interaction.guild.id)
        if statuses == 1:
            status = f"The levelling system for {group} is currently **enabled**\n-# You can disable them with the disable button"
        else:
            status = f"The levelling system for {group} is currently **disabled**\n-# You can enable them with the enable button"
        embed = discord.Embed(title=f"<:settings:1304222799639871530> {group}'s Level Settings", description=f"{status}\n\n<:bulletpoint:1304247536021667871> How much XP do {group1} currently gain\n-# <:thread2:1304222916879323136> Text Channels: **{chatxp}xp** every **30 seconds**\n-# <:thread1:1304222965042249781> Voice Channels: **{voicexp}xp** every **30 seconds**\n\n<:bulletpoint:1304247536021667871> How much XP do {group1} currently gain from **+daily**\n-# <:thread1:1304222965042249781> Random amount between: **{dailyxp}**", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=levelsettings(bot=self.bot))

    @discord.ui.button(label="Automatic Roles")
    async def roles(self, interaction: discord.Interaction, button: discord.Button):
        guild = interaction.guild.id
        if guild == 694010548605550675:
            group = "Chroma"
            group1 = "Chromies"
        else:
            group = "Lyra"
            group1 = "Lyres"
        top20 = await self.get_top20(interaction.guild.id)
        reprole = await self.get_reprole(interaction.guild.id)
        embed = discord.Embed(title=f"<:settings:1304222799639871530> {group}'s Automatic Roles", description=f"<:bulletpoint:1304247536021667871> What role do {group1} receive when unlocking rep?\n-# <:thread1:1304222965042249781> <@&{reprole}>\n\n<:bulletpoint:1304247536021667871> What role do {group1} receive when they're top 20?\n-# <:thread1:1304222965042249781> <@&{top20}>\n\n-# If you'd like more automatic roles added to Hoshi. Please feel free to DM Reece!", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=rolesettings(bot=self.bot))

    @discord.ui.button(label="Channels")
    async def channels(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        group = "Chroma" if guild.id == 694010548605550675 else "Lyra"
        textchannels = await self.get_textchannels(interaction.guild.id)
        embed = discord.Embed(title=f"<:settings:1304222799639871530> {group}'s Channels",description=f"<:bulletpoint:1304247536021667871> Text Channels:\n{textchannels}",color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=channelselect(bot=self.bot))

    async def get_dailyxp(self, guild_id: int) -> int:
        query = '''SELECT dailyxp FROM settings WHERE guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, guild_id)
                status = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if status is not None:
            return status[0]
        else:
            await self.add_server(guild_id)
            return 1

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
            await self.add_server(guild_id)
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
            await self.add_server(guild_id)
            return 1

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
            await self.add_server(guild_id)
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
            await self.add_server(guild_id)
            return 1
        
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
            await self.add_server(guild_id)
            return 1

    async def add_server(self, guild_id: int, chatxp = 25, voicexp = 25, dailyxp = "150 - 300") -> None:
        query = '''INSERT INTO settings (guild_id, chatxp, voicexp, dailyxp) VALUES (?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (guild_id, chatxp, voicexp, dailyxp))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_levels_status(self, guild_id: int) -> int:
        query = '''SELECT levels FROM settings WHERE guild_id = ?'''
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

class hoshisettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = None

    async def add_server(self, guild_id: int, chatxp = 25, voicexp = 25, dailyxp = "150 - 300") -> None:
        query = '''INSERT INTO settings (guild_id, chatxp, voicexp, dailyxp) VALUES (?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (guild_id, chatxp, voicexp, dailyxp))
                await conn.commit()
            await self.bot.pool.release(conn)

    @app_commands.command(name="settings", description="Settings for Hoshi")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def settings(self, interaction: discord.Interaction):
        guild = interaction.guild.id
        if guild == 694010548605550675:
            group = "Chroma"
            group1 = "Chromies"
        else:
            group = "Lyra"
            group1 = "Lyres"
        embed = discord.Embed(title=f"<:settings:1304222799639871530> Home Page", description=f"Welcome to the home page!\nHere you can change all the settings for Hoshi in {group}.\n\nCategories:\n<:bulletpoint:1304247536021667871> Levelling for {group1}\n-# <:thread1:1304222965042249781>Change XP amounts\n<:bulletpoint:1304247536021667871> Automatic Roles\n-# <:thread1:1304222965042249781>Change role ID's for the roles Hoshi can give out\n<:bulletpoint:1304247536021667871> Channels\n-# <:thread1:1304222965042249781>Change what channels members can level up in", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, view=settingselect(bot=self.bot), ephemeral=True)

async def setup(bot):
    await bot.add_cog(hoshisettings(bot))