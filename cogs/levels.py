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
from PIL import Image, ImageFilter, ImageOps
import requests
from utils.views import Paginator
from easy_pil import Font

class LevelRow(TypedDict):
    member_id: int
    xp: int
    messages: int
    color: str
    image: str
    mora: int
    stardust: int
    memberlvl: int
    decor: str

class investigate(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Investigate")
    async def one(self, interaction: discord.Interaction, button: discord.Button):
        mora = random.randint(5, 50)
        stardust = random.randint(1, 10)
        embed=discord.Embed(title="Mora & Stardust found", description=f"{interaction.user.name} found\n<:mora:1230914532675813508> **{mora}** <:stardust:1230256970859155486> **{stardust}**", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.user.display_avatar)
        await self.update_mora(interaction.user.id, mora)
        await self.update_stardust(interaction.user.id, stardust)
        await interaction.response.edit_message(content=f"{interaction.user.mention}",embed=embed, view=None)

    async def update_stardust(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET stardust = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        
        if levels is None or levels['stardust'] is None:
            starting_stardust = 0
        else:
            starting_stardust = levels['stardust']
        
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (starting_stardust + amount, member_id,))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_mora(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET mora = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        
        if levels is None or levels['mora'] is None:
            starting_mora = 0
        else:
            starting_mora = levels['mora']
        
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (starting_mora + amount, member_id,))
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

class roleshop(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Click to unlock custom roles", emoji="🌙")
    async def one(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['stardust'] >= 60:
            await self.update_roles(interaction.user.id, "yes")
            await self.remove_stardust(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **Custom Roles** for **<:stardust:1230256970859155486>{price} Stardust**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:stardust:1230256970859155486>Stardust to complete this purchase")

    async def update_roles(self, member_id: int, text: str):
        query = '''UPDATE levels SET roles = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (text, member_id))
                await conn.commit()

    async def remove_stardust(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET stardust = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['stardust'] - amount, member_id, ))
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

class carddecorshop(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(emoji="<:number1:1209947396637728808>")
    async def one(self, interaction: discord.Interaction, button: discord.Button):
        price = 15
        id = "1"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_stardust(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:stardust:1230256970859155486>{price} Stardust**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:stardust:1230256970859155486>Stardust to complete this purchase")

    @discord.ui.button(emoji="<:number2:1209947399053901824>")
    async def two(self, interaction: discord.Interaction, button: discord.Button):
        price = 30
        id = "2"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_stardust(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:stardust:1230256970859155486>{price} Stardust**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:stardust:1230256970859155486>Stardust to complete this purchase")

    @discord.ui.button(emoji="<:number3:1209947401100595310>")
    async def three(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "3"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_stardust(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:stardust:1230256970859155486>{price} Stardust**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:stardust:1230256970859155486>Stardust to complete this purchase")

    @discord.ui.button(emoji="<:number4:1209947403432624138>")
    async def four(self, interaction: discord.Interaction, button: discord.Button):
        price = 80
        id = "4"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_stardust(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:stardust:1230256970859155486>{price} Stardust**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:stardust:1230256970859155486>Stardust to complete this purchase")

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

    async def update_decor(self, member_id: int, id: str) -> None:
        query = '''UPDATE levels SET decor = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (id, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def remove_stardust(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET stardust = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['stardust'] - amount, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

class carddecorshopbooster(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=30)
        self.value = None
        self.bot = bot

    @discord.ui.button(emoji="<:number1:1209947396637728808>")
    async def one(self, interaction: discord.Interaction, button: discord.Button):
        price = 6
        id = "1"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_stardust(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:stardust:1230256970859155486>{price} Stardust**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:stardust:1230256970859155486>Stardust to complete this purchase")

    @discord.ui.button(emoji="<:number2:1209947399053901824>")
    async def two(self, interaction: discord.Interaction, button: discord.Button):
        price = 12
        id = "2"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_stardust(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:stardust:1230256970859155486>{price} Stardust**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:stardust:1230256970859155486>Stardust to complete this purchase")

    @discord.ui.button(emoji="<:number3:1209947401100595310>")
    async def three(self, interaction: discord.Interaction, button: discord.Button):
        price = 24
        id = "3"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_stardust(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:stardust:1230256970859155486>{price} Stardust**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:stardust:1230256970859155486>Stardust to complete this purchase")

    @discord.ui.button(emoji="<:number4:1209947403432624138>")
    async def four(self, interaction: discord.Interaction, button: discord.Button):
        price = 32
        id = "4"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_stardust(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:stardust:1230256970859155486>{price} Stardust**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:stardust:1230256970859155486>Stardust to complete this purchase")

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

    async def update_decor(self, member_id: int, id: str) -> None:
        query = '''UPDATE levels SET decor = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (id, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def remove_stardust(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET stardust = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['stardust'] - amount, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

class stardustshop(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="5", emoji="<:stardust:1230256970859155486>")
    async def five(self, interaction: discord.Interaction, button: discord.Button):
        amount = 5
        price = 15
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 15:
            await self.update_stardust(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:stardust:1230256970859155486>{amount} Stardust** for **<:mora:1230914532675813508>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1230914532675813508>Mora to complete this purchase")

    @discord.ui.button(label="10", emoji="<:stardust:1230256970859155486>")
    async def ten(self, interaction: discord.Interaction, button: discord.Button):
        amount = 10
        price = 30
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 30:
            await self.update_stardust(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:stardust:1230256970859155486>{amount} Stardust** for **<:mora:1230914532675813508>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1230914532675813508>Mora to complete this purchase")

    @discord.ui.button(label="20", emoji="<:stardust:1230256970859155486>")
    async def twenty(self, interaction: discord.Interaction, button: discord.Button):
        amount = 20
        price = 60
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 60:
            await self.update_stardust(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:stardust:1230256970859155486>{amount} Stardust** for **<:mora:1230914532675813508>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1230914532675813508>Mora to complete this purchase")

    @discord.ui.button(label="40", emoji="<:stardust:1230256970859155486>")
    async def fourty(self, interaction: discord.Interaction, button: discord.Button):
        amount = 40
        price = 120
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 120:
            await self.update_stardust(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:stardust:1230256970859155486>{amount} Stardust** for **<:mora:1230914532675813508>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1230914532675813508>Mora to complete this purchase")

    @discord.ui.button(label="80", emoji="<:stardust:1230256970859155486>")
    async def eighty(self, interaction: discord.Interaction, button: discord.Button):
        amount = 80
        price = 240
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 240:
            await self.update_stardust(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:stardust:1230256970859155486>{amount} Stardust** for **<:mora:1230914532675813508>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1230914532675813508>Mora to complete this purchase")

    @discord.ui.button(label="160", emoji="<:stardust:1230256970859155486>")
    async def hunderedsixty(self, interaction: discord.Interaction, button: discord.Button):
        amount = 160
        price = 480
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 480:
            await self.update_stardust(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:stardust:1230256970859155486>{amount} Stardust** for **<:mora:1230914532675813508>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1230914532675813508>Mora to complete this purchase")

    async def update_stardust(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET stardust = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        
        if levels is None or levels['stardust'] is None:
            starting_stardust = 0
        else:
            starting_stardust = levels['stardust']
        
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (starting_stardust + amount, member_id,))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def remove_mora(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET mora = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['mora'] - amount, member_id, ))
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

class levels(commands.Cog):
    def __init__(self, bot):
        self.regex_hex = "^#(?:[0-9a-fA-F]{3}){1,2}$"
        self.bot = bot
        self.status_holder = {0: "disabled", 1: "enabled"}
        self.pool = None
        self.channels = [1184208577120960632, 1214944837451780116, 1181419043153002546, 1220487352733138954, 1220488547203547267, 1133767338588639323, 1214940039335641089, 1229142761827995831]
        self.guilds = [1121841073673736215]
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)

    def kanzen_cooldown(interaction: discord.Interaction) -> Optional[app_commands.Cooldown]:

        role = interaction.guild.get_role(1128460924886458489)
        if role in interaction.user.roles:
            return commands.Cooldown(1, 43200)
        
        return commands.Cooldown(1, 86400)

    async def add_member(self, member_id: int, xp=5, mora=5) -> None:
        query = '''INSERT INTO levels (member_id, xp, messages, color, mora) VALUES (?, ?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, xp, 1, '#793e79', mora))
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

    async def update_mora(self, member_id: int) -> None:
        query = '''UPDATE levels SET mora = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['mora'] + 5, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def remove_mora(self, member_id: int) -> None:
        query = '''UPDATE levels SET mora = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['mora'] - 5, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    @commands.command()
    async def removedust(self, ctx):
        await self.remove_mora(ctx.author.id)
        await ctx.reply("mk")

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

            await message.channel.send(f"Yay! {message.author.mention} you just reached **level {lvl+1}**\nYou also found **<:mora:1230914532675813508>5 Mora**! You now have <:mora:1230914532675813508>**{levels['mora'] + 5} Mora**")
            await self.update_mora(message.author.id)

    async def level_handler(self, message: discord.Message, retry_after: Optional[commands.CooldownMapping], xp: int) -> None:
        member_id = message.author.id
        levels = await self.get_member_levels(member_id)
        if levels == None:
            await self.add_member(member_id)
        else:
            if retry_after:
                await self.update_messages(member_id, levels)
            else:
                await self.update_xp(member_id, levels, xp)
                await self.check_levels(message, levels['xp'], xp)

    async def get_staffrep(self, member_id: int) -> Optional[LevelRow]:
        query = '''SELECT count FROM staffrep WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, ))
                row = await cursor.fetchone()
                if row:
                    return row
                else:
                    return None

    async def handle_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
            
        if message.channel.id not in self.channels:
            return

        zennie_role_id = 1121842393994494082
        forms_zennie_role_id = 1215364922700206141
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

    def _make_progress_bar(self, progress, color, circle_size=210, bar_thickness=13):
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

    def get_avatar(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        circle = Image.open('./assets/circle-mask.png').resize((190, 190)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((190, 190))
        return avatar_image, circle

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
        dark = ImageEnhance.Brightness(bg)
        bg_dark = dark.enhance(0.8)
        bg_blurred = bg_dark.filter(ImageFilter.GaussianBlur(radius=20))
        mask = Image.open("./assets/boxmask.png").resize((750, 750)).convert("L")
        inverted_mask = ImageOps.invert(mask)
        bg_frosted = Image.composite(bg_blurred, Image.new("RGBA", bg.size, "white"), inverted_mask)
        bg_frosted.putalpha(inverted_mask)
        bg_rgb = bg.convert("RGB")
        bar, mask = self._make_progress_bar(percentage, levels['color'])
        avatar_paste, circle = self.get_avatar(avatar)
        card.paste(bg_rgb, (0, 0))
        card.paste(bg_frosted, (0, 0), bg_frosted)
        card.paste(bar, (7, 7), mask)
        card.paste(avatar_paste, (18, 17), circle)
        zhcn = ImageFont.truetype("./fonts/zhcn.ttf", size=33)
        zhcn2 = ImageFont.truetype("./fonts/zhcn.ttf", size=27)
        rankboxes = Image.open('./assets/rankboxes.png')
        rankboxes = rankboxes.resize((750, 750))
        card.paste(rankboxes, (0, 0), rankboxes)
        if levels["decor"]:
            rankdecor = Image.open(f'./assets/{levels["decor"]}.png')
            rankdecor = rankdecor.resize((750, 750))
            card.paste(rankdecor, (0, 0), rankdecor)
        lead_role_id = 1121842279351590973
        has_lead_role = any(role.id == lead_role_id for role in user.roles)
        hstaff_id = 1178924350523588618
        has_hstaff_role = any(role.id == hstaff_id for role in user.roles)
        staff_role_id = 1135244903165722695
        has_staff_role = any(role.id == staff_role_id for role in user.roles)
        mods_id = 1179249792925306931
        mods_role = any(role.id == mods_id for role in user.roles)
        devs_id = 1179255802003988573
        devs_role = any(role.id == devs_id for role in user.roles)
        zennies_role_id = 1121842393994494082
        has_zennies_role = any(role.id == zennies_role_id for role in user.roles)
        moraicon = Image.open('./assets/mora.png')
        moraicon = moraicon.resize((60, 60))
        card.paste(moraicon, (32, 512), moraicon)
        stardusticon = Image.open('./assets/stardust.png')
        stardusticon = stardusticon.resize((50, 50))
        card.paste(stardusticon, (170, 517), stardusticon)
        mbmerlvl = Image.open('./assets/memberlvl.png')
        mbmerlvl = mbmerlvl.resize((50, 50))
        card.paste(mbmerlvl, (306, 519), mbmerlvl)
        # server thing badges
        if has_lead_role:
            special_role_img = Image.open('./assets/lead.png')
            special_role_img = special_role_img.resize((85, 85))
            custom_x = 135
            custom_y = 135
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        elif has_hstaff_role:
            special_role_img = Image.open('./assets/hstaff.png')
            special_role_img = special_role_img.resize((85, 85))
            custom_x = 135
            custom_y = 135
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        elif mods_role:
            mods_img = Image.open('./assets/mods.png')
            mods_img = mods_img.resize((85, 85))
            custom_x = 135
            custom_y = 135
            card.paste(mods_img, (custom_x, custom_y), mods_img)
        elif has_staff_role:
            staff_role_img = Image.open('./assets/staff.png')
            staff_role_img = staff_role_img.resize((85, 85))
            custom_x = 135
            custom_y = 135
            card.paste(staff_role_img, (custom_x, custom_y), staff_role_img)
        elif devs_role:
            devs_img = Image.open('./assets/devs.png')
            devs_img = devs_img.resize((85, 85))
            custom_x = 135
            custom_y = 135
            card.paste(devs_img, (custom_x, custom_y), devs_img)
        elif has_zennies_role:
            zennies_role_img = Image.open('./assets/zennies.png')
            zennies_role_img = zennies_role_img.resize((85, 85))
            custom_x = 135
            custom_y = 135
            card.paste(zennies_role_img, (custom_x, custom_y), zennies_role_img)

        # other badges
        booster_role_id = 1128460924886458489
        has_booster_role = any(role.id == booster_role_id for role in user.roles)
        if has_booster_role:
            booster_role_img = Image.open('./assets/booster.png')
            booster_role_img = booster_role_img.resize((65, 65))
            custom_x = 115
            custom_y = 656
            card.paste(booster_role_img, (custom_x, custom_y), booster_role_img)
        else:
            special_role_img = Image.open('./assets/emptry badge.png')
            special_role_img = special_role_img.resize((65, 65))
            custom_x = 115
            custom_y = 657
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        top20_role_id = 1189632052727906376
        has_top20_role = any(role.id == top20_role_id for role in user.roles)
        if has_top20_role:
            top20_role_img = Image.open('./assets/top20.png')
            top20_role_img = top20_role_img.resize((65, 65))
            custom_x = 185
            custom_y = 657
            card.paste(top20_role_img, (custom_x, custom_y), top20_role_img)
        else:
            special_role_img = Image.open('./assets/emptry badge.png')
            special_role_img = special_role_img.resize((65, 65))
            custom_x = 185
            custom_y = 657
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        ew_winner_role_id = 1216869981464035439
        has_ew_winner_role = any(role.id == ew_winner_role_id for role in user.roles)
        if has_ew_winner_role:
            ew_winner_role_img = Image.open('./assets/editwars badge.png')
            ew_winner_role_img = ew_winner_role_img.resize((85, 85))
            custom_x = 245
            custom_y = 647
            card.paste(ew_winner_role_img, (custom_x, custom_y), ew_winner_role_img)
        else:
            special_role_img = Image.open('./assets/emptry badge.png')
            special_role_img = special_role_img.resize((65, 65))
            custom_x = 255
            custom_y = 657
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        reeces_family_role_id = 1193494182401163334
        has_reeces_family_role = any(role.id == reeces_family_role_id for role in user.roles)
        if has_reeces_family_role:
            reeces_family_role_img = Image.open('./assets/reeces family.png')
            reeces_family_role_img = reeces_family_role_img.resize((85, 85))
            custom_x = 45
            custom_y = 647
            card.paste(reeces_family_role_img, (custom_x, custom_y), reeces_family_role_img)
        else:
            special_role_img = Image.open('./assets/emptry badge.png')
            special_role_img = special_role_img.resize((65, 65))
            custom_x = 45
            custom_y = 657
            card.paste(special_role_img, (custom_x, custom_y), special_role_img)
        draw = ImageDraw.Draw(card, 'RGBA')
        stardust = levels["stardust"]
        mora = levels["mora"]
        memberlvl = levels["memberlvl"]
        if stardust == None:
            stardust = "0"
        else:
            stardust = stardust

        if mora == None:
            mora = "0"
        else:
            mora = mora

        if memberlvl == None:
            memberlvl = "0"
        else:
            memberlvl = memberlvl
        draw.text((225, 65), f'{xp_have} | {xp_need}', fill=levels['color'], font=zhcn2)
        draw.text((360, 522), f'{memberlvl}', fill=levels['color'], font=zhcn)
        draw.text((85, 522), f'{mora}', fill=levels['color'], font=zhcn)
        draw.text((220, 522), f'{stardust}', fill=levels['color'], font=zhcn)
        draw.text((225, 25), f"{user.display_name}", fill=levels['color'], font=zhcn)
        draw.text((80, 590), f'#{str(rank)}', fill=levels['color'], font=zhcn)
        draw.text((213, 590), f'{level}', fill=levels['color'], font=zhcn)
        draw.text((335, 590), f'{levels["messages"]}', fill=levels['color'], font=zhcn)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def generate_card_rank1(self, name: str, status: str, avatar: BytesIO, levels: LevelRow, rank: int, member: discord.Member) -> BytesIO:
        card_generator = functools.partial(self.get_card, name, status, avatar, levels, rank)
        card = await self.bot.loop.run_in_executor(None, self.get_card, str(member), str(member.status), avatar, levels, rank, member)
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
            query = '''UPDATE levels SET xp = ? WHERE member_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (levels['xp'] + xp, member_id, ))
                    await conn.commit()
                await self.bot.pool.release(conn)
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
        member = member or interaction.user
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
        levels = await self.get_member_levels(member.id)
        await self.add_xp(member.id, amount, levels)
        embed = discord.Embed(title='xp added!',description=f'gave `{amount}xp` to {str(member)}',color=0x2b2d31)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove", description="Remove xp from someone", extras="+remove @member amount")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        levels = await self.get_member_levels(member.id)
        if levels:
            if amount > levels['xp']:
                await interaction.response.send_message("you can't take away more xp than the user already has!")
            else:
                await self.remove_xp(member.id, amount, levels)
                embed = discord.Embed(title='xp removed!',description=f'removed `{amount}xp` from {str(member)}',color=0x2b2d31)
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
        embeds = []
        description = ""
        rows = await self.get_leaderboard_stats()
        per_page = 5 if interaction.user.is_on_mobile() else 10
        for i, row in enumerate(rows, start=1):
            msg = "messages" if row['messages'] != 1 else "message"
            xp = row["xp"]
            if xp is None:
                xp = 0
            lvl = 0
            while True:
                if xp < ((50*(lvl**2))+(50*(lvl-1))):
                    break
                lvl += 1
            description += f"**{i}.** <@!{row['member_id']}>\n<:Empty:1188186122350759996><:1166196258499727480:1188190249768210582>**level {lvl} | {row['messages']} {msg}**\n<:Empty:1188186122350759996><:1166196258499727480:1188190249768210582><:stardust:1230256970859155486>**{row['stardust']}** |<:mora:1230914532675813508>**{row['mora']}**\n\n"
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
            await self.set_rank_color(interaction.user.id, color)
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
            query = "UPDATE levels SET image = ? WHERE member_id = ?"
            await conn.execute(query, (image.url, member_id))
            await conn.commit()
        embed = discord.Embed(title="Rank background has been updated!", color=0x2b2d31)
        embed.set_image(url=image.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reset", description="Resets everyone's xp")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def reset(self, interaction: discord.Interaction):
        await self.reset_levels()
        await interaction.response.send_message("All levels have been reset! All members are back to level 1 with 0 messages")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        await self.handle_message(message)

    async def get_wallet_balance(self, user):
        user_id = user.id
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT mora FROM levels WHERE member_id = ?", (user_id,))
                row = await cursor.fetchone()
                if row:
                    return row[0]
                else:
                    return 0

    async def get_stardust_balance(self, user):
        user_id = user.id
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT stardust FROM levels WHERE member_id = ?", (user_id,))
                row = await cursor.fetchone()
                if row:
                    return row[0]
                else:
                    return 0

    @app_commands.command()
    async def shop(self, interaction: discord.Interaction):
        user = interaction.user
        wallet_balance = await self.get_wallet_balance(user)
        stardust = await self.get_stardust_balance(user)
        
        categories = [
            "stardust",
            "rank card decorations",
            "custom roles"
        ]
        emojis = [
            "<:stardust:1230256970859155486>",
            "🎉",
            "🌙"
        ]
        descriptions = [
            "Exchange Mora for stardust",
            "Decorate your rank cards more with our card decorations",
            "Unlock the ability to make your own custom roles!"
        ]
        booster_role_id = 1128460924886458489
        has_booster_role = any(role.id == booster_role_id for role in user.roles)
        tool_buy_view = stardustshop(bot=self.bot)
        if has_booster_role:
            lotto_buy_view = carddecorshopbooster(bot=self.bot)
        else:
            lotto_buy_view = carddecorshop(bot=self.bot)
        roles_buy_view = roleshop(bot=self.bot)
        dropdown = discord.ui.Select(
            placeholder="Select a category",
            options=[discord.SelectOption(label=category, emoji=emoji, description=description) for category, emoji, description in zip(categories, emojis, descriptions)]
        )
        if stardust == None:
            stardust = "0"
        else:
            stardust = stardust
        tools = discord.Embed(title="Hoshi's Shop", description=f"> Welcome to the shop, Here you can find all sorts of items to buy"
                              "\n> Use the dropdown menu below to select a category"
                              "\n\n**__Categories:__**"
                              "\n<:1166196258499727480:1208228386842087554><:stardust:1230256970859155486> [**Stardust**](https://instagram.com/kanzengrp/)"
                              "\n<:Empty:1207651048710479892> Exchange Mora for stardust"
                              "\n<:1166196258499727480:1208228386842087554>🎉 [**Rank card decor**](https://instagram.com/kanzengrp/)"
                              "\n<:Empty:1207651048710479892> Decorate your rank cards more with our card decorations"
                              "\n<:1166196258499727480:1208228386842087554>🌙 [**Custom Roles**](https://instagram.com/kanzengrp/)"
                              "\n<:Empty:1207651048710479892> Unlock the ability to make your own custom roles!"
                              f"\n\n<:mora:1230914532675813508>**{wallet_balance} Mora**"
                              f"\n<:stardust:1230256970859155486>**{stardust} Stardust**", color=0x2b2d31)
        tools.set_thumbnail(url=interaction.guild.icon)
        
        view = discord.ui.View()
        view.add_item(dropdown)
        
        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            
            for item in view.children:
                if not isinstance(item, discord.ui.Select):
                    view.remove_item(item)
            
            if selected_category == categories[0]:
                for item in tool_buy_view.children:
                    view.add_item(item)
                embed = discord.Embed(title="Stardust", description=f"> Use the buttons below to buy the items you want\n\n<:mora:1230914532675813508>**{wallet_balance} Mora**\n<:stardust:1230256970859155486>**{stardust} Stardust**", color=0x2b2d31)
                embed.set_thumbnail(url=interaction.guild.icon)
                embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1230994171079299143/Comp_1_00000.png?ex=663557a9&is=6622e2a9&hm=804e7422f3aa99537f28f0fe99fcb5a7fe158762cae9cf638c663f9ac0d82eab&")
                embed.set_footer(text="• Use the buttons below to buy an item (clicking it twice will give you another)", icon_url=interaction.user.avatar)
            
            elif selected_category == categories[1]:
                for item in lotto_buy_view.children:
                    view.add_item(item)
                embed = discord.Embed(title="Rank Decorations", description=f"> Use the buttons below to buy the items you want\n\n<:mora:1230914532675813508>**{wallet_balance} Mora**\n<:stardust:1230256970859155486>**{stardust} Stardust**", color=0x2b2d31)
                embed.set_thumbnail(url=interaction.guild.icon)
                booster_role_id = 1128460924886458489
                has_booster_role = any(role.id == booster_role_id for role in user.roles)
                if has_booster_role:
                    image = "https://cdn.discordapp.com/attachments/1184208577120960632/1233830446467649587/rank_decor_shop_00000.png?ex=662e85a5&is=662d3425&hm=2d967585935043f8c7eb3a70cc55901b3962755cf99d0fb43b2f3f65c38cae8c&"
                else:
                    image = "https://cdn.discordapp.com/attachments/1184208577120960632/1232391470695059557/rank_decor_shop_00000.png?ex=662de6bf&is=662c953f&hm=ee4ef00b8772a4cc5b23280ceb83e5ece5b0084545fce0023b60192e932a1d7b&"
                embed.set_image(url=image)
                embed.set_footer(text="• Use the buttons below to buy an item (clicking it twice will give you another)", icon_url=interaction.user.avatar)

            elif selected_category == categories[2]:
                # for item in roles_buy_view.children:
                    # view.add_item(item)
                embed = discord.Embed(title="Custom Roles", description=f"> ~~Unlock the ability to create custom roles!~~\n~~Costs <:stardust:1230256970859155486>**60 Stardust**~~\n\n > **Custom roles are currently disabled, we will provide an update when they are released!**\n\n<:mora:1230914532675813508>**{wallet_balance} Mora**\n<:stardust:1230256970859155486>**{stardust} Stardust**", color=0x2b2d31)
                embed.set_thumbnail(url=interaction.guild.icon)
                embed.set_footer(text="• Use the buttons below to buy an item (clicking it twice will give you another)", icon_url=interaction.user.avatar)
            
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")

            await interaction.response.edit_message(embed=embed, view=view)
        
        dropdown.callback = dropdown_callback
        message = await interaction.response.send_message(embed=tools, view=view)

    async def add_mora(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET mora = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        
        if levels is None:
            query = '''INSERT INTO levels (member_id, mora) VALUES (?, ?)'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (member_id, amount))
                    await conn.commit()
                await self.bot.pool.release(conn)
        else:
            new_mora = levels['mora'] + amount if levels['mora'] is not None else amount
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (new_mora, member_id, ))
                    await conn.commit()
                await self.bot.pool.release(conn)

    async def add_stardust(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET stardust = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        
        if levels is None:
            query = '''INSERT INTO levels (member_id, stardust) VALUES (?, ?)'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (member_id, amount))
                    await conn.commit()
                await self.bot.pool.release(conn)
        else:
            new_stardust = levels['stardust'] + amount if levels['stardust'] is not None else amount
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (new_stardust, member_id, ))
                    await conn.commit()
                await self.bot.pool.release(conn)

    @app_commands.command(name="addmora", description="Add mora to a zennie")
    async def addmora(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await self.add_mora(member.id, amount)
        await interaction.response.send_message(f"Added <:mora:1230914532675813508> **{amount}** Mora to {member.mention}")

    @app_commands.command(name="addstardust", description="Add stardust to a zennie")
    async def addstardust(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await self.add_stardust(member.id, amount)
        await interaction.response.send_message(f"Added <:stardust:1230256970859155486> **{amount}** Stardust to {member.mention}")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        import random

        async with ctx.typing():
            levels = await self.get_member_levels(ctx.author.id)
            mora = random.randint(20, 50)
            stardust = random.randint(2, 5)
            xp = random.randint(50, 200)
            await self.add_mora(ctx.author.id, mora)
            await self.add_stardust(ctx.author.id, stardust)
            await self.add_xp(ctx.author.id, xp, levels)
            card = await self.get_daily_image(mora, xp, stardust, levels, member=ctx.author)
            await ctx.reply(file=discord.File(card, 'card.png'))

    @daily.error
    async def daily_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            if error.retry_after > 3600:
                hours = error.retry_after / 3600
                await ctx.reply(f"You already opened your daily chest! Try again in {int(hours)} hours")
            elif error.retry_after > 60:
                minutes = error.retry_after / 60
                await ctx.reply(f"You already opened your daily chest! Try again in {int(minutes)} minutes")
            else:
                await ctx.reply(f"You already opened your daily chest! Try again in {int(error.retry_after)} seconds")

    async def get_daily_image(self, mora, xp, stardust, levels: LevelRow, member: discord.Member) -> BytesIO:
        card_generator = functools.partial(self.daily_image, mora=mora, xp=xp, stardust=stardust, levels=levels, member=member)
        card = await self.bot.loop.run_in_executor(None, card_generator)
        return card

    def daily_image(self, member, mora, xp, stardust, levels: LevelRow) -> BytesIO:
        card = Image.new('RGBA', size=(750, 750), color='grey')
        if levels['image'] is not None:
            bg = self._get_bg_image(member.guild.icon)
            left = (bg.width - min(bg.width, bg.height)) // 2
            top = (bg.height - min(bg.width, bg.height)) // 2
            right = left + min(bg.width, bg.height)
            bottom = top + min(bg.width, bg.height)
            bg = bg.crop((left, top, right, bottom))
        bg = bg.resize((750, 750))
        dark = ImageEnhance.Brightness(bg)
        bg_dark = dark.enhance(0.8)
        card.paste(bg_dark)
        zhcn = ImageFont.truetype("./fonts/zhcn.ttf", size=28)
        ugh = Image.open('./assets/ugh.png')
        ugh = ugh.resize((750, 750))
        card.paste(ugh, (0, 0), ugh)

        draw = ImageDraw.Draw(card, 'RGBA')
        draw.text((135, 607), f"{mora}", fill=levels['color'], font=zhcn)
        draw.text((582, 607), f"{xp}", fill=levels['color'], font=zhcn)
        draw.text((367, 630), f"{stardust}", fill=levels['color'], font=zhcn)

        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    @commands.command(hidden=True)
    async def delete(self, ctx, member_id: int):
        async with self.bot.pool.acquire() as conn:
            await conn.execute('DELETE FROM levels WHERE member_id = $1', member_id)
        await ctx.send(f"<@{member_id}'s levels have been removed!")

async def setup(bot):
    await bot.add_cog(levels(bot))