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
from easy_pil import Font
from colorthief import ColorThief

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
        primogems = random.randint(1, 10)
        embed=discord.Embed(title="Mora & primogems found", description=f"{interaction.user.name} found\n<:mora:1261680092535455844> **{mora}** <:primo:1261680094141747321> **{primogems}**", color=0xFEBCBE)
        embed.set_thumbnail(url=interaction.user.display_avatar)
        await self.update_mora(interaction.user.id, mora)
        await self.update_primogems(interaction.user.id, primogems)
        await interaction.response.edit_message(content=f"{interaction.user.mention}",embed=embed, view=None)

    async def update_primogems(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET primogems = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        
        if levels is None or levels['stardust'] is None:
            starting_primogems = 0
        else:
            starting_primogems = levels['stardust']
        
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (starting_primogems + amount, member_id,))
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
        super().__init__(timeout=180)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Click to unlock custom roles", emoji="🌙")
    async def one(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['stardust'] >= 60:
            await self.update_roles(interaction.user.id, "yes")
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **Custom Roles** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    async def update_roles(self, member_id: int, text: str):
        query = '''UPDATE levels SET roles = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (text, member_id))
                await conn.commit()

    async def remove_primogems(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET primogems = ? WHERE member_id = ?'''
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
        super().__init__(timeout=180)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="credit", style=discord.ButtonStyle.blurple)
    async def credit(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description="""decor 1. <@1111564587024789504>
        <:1166196258499727480:1215213896256724992> instagram: [sxtqrn](https://instagram.com/sxtqrn)
                              
        decor 2. <@751895538646909038>
        <:1166196258499727480:1215213896256724992> instagram: [lushsfx](https://instagram.com/lushsfx)
                              
        decor 3. <@982720510003658784>
        <:1166196258499727480:1215213896256724992> instagram: [hrts4h0bi](https://instagram.com/hrts4h0bi)
                              
        decor 4. <@609515684740988959>
        <:1166196258499727480:1215213896256724992> instagram: [remqsi](https://instagram.com/remqsi)
                              
        decor 5. <@695197958940917830>
        <:1166196258499727480:1215213896256724992> instagram: [luno1rs](https://instagram.com/luno1rs)
                              
        decor 6. <@609515684740988959>
        <:1166196258499727480:1215213896256724992> instagram: [remqsi](https://instagram.com/remqsi)
                              
        decor 7. <@541538705106534423>
        <:1166196258499727480:1215213896256724992> instagram: [dtqwn](https://instagram.com/dtqwn)
                              
        decor 8. <@695197958940917830>
        <:1166196258499727480:1215213896256724992> instagram: [luno1rs](https://instagram.com/luno1rs)
                              
        decor 9. <@695197958940917830>
        <:1166196258499727480:1215213896256724992> instagram: [luno1rs](https://instagram.com/luno1rs)
                              
        decor 10. <@834786195526778903>
        <:1166196258499727480:1215213896256724992> instagram: [kxpjm](https://instagram.com/kxpjm)
                              
        decor 11. <@609515684740988959>
        <:1166196258499727480:1215213896256724992> instagram: [remqsi](https://instagram.com/remqsi)
                              
        decor 12. <@609515684740988959>
        <:1166196258499727480:1215213896256724992> instagram: [remqsi](https://instagram.com/remqsi)
                              
        decor 13. <@834786195526778903>
        <:1166196258499727480:1215213896256724992> instagram: [kxpjm](https://instagram.com/kxpjm)""", color=0xFEBCBE)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="clear decor", style=discord.ButtonStyle.red)
    async def clear(self, interaction: discord.Interaction, button: discord.Button):
        price = 0
        id = "None"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have removed your rankc ard decoration!", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="1")
    async def one(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "1"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="2")
    async def two(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "2"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="3")
    async def three(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "3"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="4")
    async def four(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "4"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="5")
    async def five(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "5"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="6")
    async def six(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "6"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="7")
    async def seven(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "7"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="8")
    async def eight(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "8"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="9")
    async def nine(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "9"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="10")
    async def ten(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "10"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="11")
    async def eleven(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "11"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="12")
    async def twelve(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "12"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="13")
    async def thirteen(self, interaction: discord.Interaction, button: discord.Button):
        price = 100
        id = "13"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

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

    async def remove_primogems(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET primogems = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['stardust'] - amount, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

class carddecorshopbooster(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=180)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="credit", style=discord.ButtonStyle.blurple)
    async def credit(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description="""decor 1. <@1111564587024789504>
        <:1166196258499727480:1215213896256724992> instagram: [sxtqrn](https://instagram.com/sxtqrn)
                              
        decor 2. <@751895538646909038>
        <:1166196258499727480:1215213896256724992> instagram: [lushsfx](https://instagram.com/lushsfx)
                              
        decor 3. <@982720510003658784>
        <:1166196258499727480:1215213896256724992> instagram: [hrts4h0bi](https://instagram.com/hrts4h0bi)
                              
        decor 4. <@609515684740988959>
        <:1166196258499727480:1215213896256724992> instagram: [remqsi](https://instagram.com/remqsi)
                              
        decor 5. <@695197958940917830>
        <:1166196258499727480:1215213896256724992> instagram: [luno1rs](https://instagram.com/luno1rs)
                              
        decor 6. <@609515684740988959>
        <:1166196258499727480:1215213896256724992> instagram: [remqsi](https://instagram.com/remqsi)
                              
        decor 7. <@541538705106534423>
        <:1166196258499727480:1215213896256724992> instagram: [dtqwn](https://instagram.com/dtqwn)
                              
        decor 8. <@695197958940917830>
        <:1166196258499727480:1215213896256724992> instagram: [luno1rs](https://instagram.com/luno1rs)
                              
        decor 9. <@695197958940917830>
        <:1166196258499727480:1215213896256724992> instagram: [luno1rs](https://instagram.com/luno1rs)
                              
        decor 10. <@834786195526778903>
        <:1166196258499727480:1215213896256724992> instagram: [kxpjm](https://instagram.com/kxpjm)
                              
        decor 11. <@609515684740988959>
        <:1166196258499727480:1215213896256724992> instagram: [remqsi](https://instagram.com/remqsi)
                              
        decor 12. <@609515684740988959>
        <:1166196258499727480:1215213896256724992> instagram: [remqsi](https://instagram.com/remqsi)
                              
        decor 13. <@834786195526778903>
        <:1166196258499727480:1215213896256724992> instagram: [kxpjm](https://instagram.com/kxpjm)""", color=0xFEBCBE)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="clear decor", style=discord.ButtonStyle.red)
    async def clear(self, interaction: discord.Interaction, button: discord.Button):
        price = 0
        id = "None"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have removed your rank card decoration!", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="1")
    async def one(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "1"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="2")
    async def two(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "2"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="3")
    async def three(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "3"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="4")
    async def four(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "4"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="5")
    async def five(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "5"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="6")
    async def six(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "6"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="7")
    async def seven(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "7"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="8")
    async def eight(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "8"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="9")
    async def nine(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "9"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="10")
    async def ten(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "10"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="11")
    async def eleven(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "11"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="12")
    async def twelve(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "12"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

    @discord.ui.button(label="13")
    async def thirteen(self, interaction: discord.Interaction, button: discord.Button):
        price = 60
        id = "13"
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels['stardust'] >= price:
            await self.update_decor(interaction.user.id, id)
            await self.remove_primogems(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **decor {id}** for **<:primo:1261680094141747321>{price} primogems**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:primo:1261680094141747321>primogems to complete this purchase")

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

    async def remove_primogems(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET primogems = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (levels['stardust'] - amount, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

class primogemsshop(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=180)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="5", emoji="<:primo:1261680094141747321>")
    async def five(self, interaction: discord.Interaction, button: discord.Button):
        amount = 5
        price = 15
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 15:
            await self.update_primogems(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:primo:1261680094141747321>{amount} primogems** for **<:mora:1261680092535455844>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1261680092535455844>Mora to complete this purchase")

    @discord.ui.button(label="10", emoji="<:primo:1261680094141747321>")
    async def ten(self, interaction: discord.Interaction, button: discord.Button):
        amount = 10
        price = 30
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 30:
            await self.update_primogems(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:primo:1261680094141747321>{amount} primogems** for **<:mora:1261680092535455844>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1261680092535455844>Mora to complete this purchase")

    @discord.ui.button(label="20", emoji="<:primo:1261680094141747321>")
    async def twenty(self, interaction: discord.Interaction, button: discord.Button):
        amount = 20
        price = 60
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 60:
            await self.update_primogems(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:primo:1261680094141747321>{amount} primogems** for **<:mora:1261680092535455844>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1261680092535455844>Mora to complete this purchase")

    @discord.ui.button(label="40", emoji="<:primo:1261680094141747321>")
    async def fourty(self, interaction: discord.Interaction, button: discord.Button):
        amount = 40
        price = 120
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 120:
            await self.update_primogems(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:primo:1261680094141747321>{amount} primogems** for **<:mora:1261680092535455844>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1261680092535455844>Mora to complete this purchase")

    @discord.ui.button(label="80", emoji="<:primo:1261680094141747321>")
    async def eighty(self, interaction: discord.Interaction, button: discord.Button):
        amount = 80
        price = 240
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 240:
            await self.update_primogems(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:primo:1261680094141747321>{amount} primogems** for **<:mora:1261680092535455844>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1261680092535455844>Mora to complete this purchase")

    @discord.ui.button(label="160", emoji="<:primo:1261680094141747321>")
    async def hunderedsixty(self, interaction: discord.Interaction, button: discord.Button):
        amount = 160
        price = 480
        levels = await self.get_member_levels(interaction.user.id)
        
        if levels and levels['mora'] >= 480:
            await self.update_primogems(interaction.user.id, amount)
            await self.remove_mora(interaction.user.id, amount=price)
            await interaction.response.send_message(f"You have bought **<:primo:1261680094141747321>{amount} primogems** for **<:mora:1261680092535455844>{price} Mora**", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have enough <:mora:1261680092535455844>Mora to complete this purchase")

    async def update_primogems(self, member_id: int, amount: int) -> None:
        query = '''UPDATE levels SET stardust = ? WHERE member_id = ?'''
        levels = await self.get_member_levels(member_id)
        
        if levels is None or levels['stardust'] is None:
            starting_primogems = 0
        else:
            starting_primogems = levels['stardust']
        
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (starting_primogems + amount, member_id,))
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
        self.channels = [1170067469134733322, 1134736054637838490]
        self.guilds = [1134736053803159592]
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)

    async def add_member(self, member_id: int, xp=5, mora=5) -> None:
        query = '''INSERT INTO levels (member_id, xp, messages, color, mora) VALUES (?, ?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, xp, 1, '#c45a72', mora))
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

        zennie_role_id = 1121842393994494082
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
        mask = Image.open("./assets/boxmasklyra.png").resize((1500, 500)).convert("L")
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
        rankdecor = Image.open(f'./assets/{levels["decor"]}.png')
        rankdecor = rankdecor.resize((750, 750))
        card.paste(rankdecor, (0, 0), rankdecor)
        rankboxes = Image.open('./assets/rankboxes.png')
        rankboxes = rankboxes.resize((750, 750))
        card.paste(rankboxes, (0, 0), rankboxes)
        moraicon = Image.open('./assets/mora.png')
        moraicon = moraicon.resize((100, 100))
        card.paste(moraicon, (925, 380), moraicon)
        primogemsicon = Image.open('./assets/primogems.png')
        primogemsicon = primogemsicon.resize((90, 90))
        card.paste(primogemsicon, (1100, 385), primogemsicon)
        draw = ImageDraw.Draw(card, 'RGBA')
        primogems = levels["stardust"]
        mora = levels["mora"]
        if primogems is None:
            primogems = "0"
        else:
            primogems = primogems

        if mora is None:
            mora = "0"
        else:
            mora = mora
        message = levels["messages"]
        messages = self.human_format(message)
        draw.text((100, 345), f'{xp_have} | {xp_need}', fill=levels['color'], font=zhcn)
        draw.text((1020, 410), f'{mora}', fill=levels['color'], font=zhcn)
        draw.text((1190, 410), f'{primogems}', fill=levels['color'], font=zhcn)
        draw.text((100, 345), f'{xp_have} | {xp_need}', fill=levels['color'], font=zhcn)
        draw.text((225, 25), f"{user.display_name}", fill=levels['color'], font=zhcn)
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
        member = interaction.user
        
        if zennie_role_id not in [role.id for role in member.roles]:
            await interaction.response.send_message("Sorry, this is a staff only command", ephemeral=True)
            return
        levels = await self.get_member_levels(member.id)
        await self.add_xp(member.id, amount, levels)
        embed = discord.Embed(title='xp added!',description=f'gave `{amount}xp` to {str(member)}',color=0xFEBCBE)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove", description="Remove xp from someone", extras="+remove @member amount")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def remove(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        zennie_role_id = 1261435772775563315
        member = interaction.user
        
        if zennie_role_id not in [role.id for role in member.roles]:
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
            description += f"**{i}.** <@!{row['member_id']}>\n<:Empty:1188186122350759996><:1166196258499727480:1188190249768210582>**level {lvl-1} | {row['messages']} {msg}**\n<:Empty:1188186122350759996><:1166196258499727480:1188190249768210582><:primogems:1269649520560439359>**{row['primogems']}** |<:mora:1269649518878654556>**{row['mora']}**\n\n"
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

    async def get_primogems_balance(self, user):
        user_id = user.id
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT stardust FROM levels WHERE member_id = ?", (user_id,))
                row = await cursor.fetchone()
                if row:
                    return row[0]
                else:
                    return 0

    @app_commands.command(name="shop", description="Come spend your mora and primogems here!")
    async def shop(self, interaction: discord.Interaction):
        await interaction.response.send_message("The shop is coming soon! Save up your mora and primogems")

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

    async def add_primogems(self, member_id: int, amount: int) -> None:
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
            new_primogems = levels['stardust'] + amount if levels['stardust'] is not None else amount
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (new_primogems, member_id, ))
                    await conn.commit()
                await self.bot.pool.release(conn)

    @app_commands.command(name="addmora", description="Add mora to a zennie")
    async def addmora(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await self.add_mora(member.id, amount)
        await interaction.response.send_message(f"Added <:mora:1261680092535455844> **{amount}** Mora to {member.mention}")

    @app_commands.command(name="addprimogems", description="Add primogems to a zennie")
    async def addprimogems(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        await self.add_primogems(member.id, amount)
        await interaction.response.send_message(f"Added <:primo:1261680094141747321> **{amount}** primogems to {member.mention}")

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

    @app_commands.command(name="resetbg", description="Reset your ranks background")
    async def resetbg(self, interaction: discord.Interaction):
        member_id = interaction.user.id
        async with self.bot.pool.acquire() as conn:
            query = "UPDATE levels SET image = NULL WHERE member_id = ?"
            await conn.execute(query, (member_id))
            await conn.commit()
        await interaction.response.send_message("Okay! I have reset your rank background")

    async def check_prizes(self, member_id: int, prize: str):
        query = f'''SELECT {prize} FROM inventory WHERE member_id = ?'''
        async with self.bot.pool.aquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, prize))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_prizes(self, member_id: int) -> list:
        query = '''SELECT * FROM inventory WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                row = await cursor.fetchone()
                if row is None:
                    return None
                
                prizes = []
                for prize_name in row.keys()[2:]:
                    if row[prize_name] == 1:
                        prizes.append(prize_name)
        return prizes

    @app_commands.command(name="equip", description="Equip rank decorations from our battle pass!")
    async def equip(self, interaction: discord.Interaction):
        prizes = await self.get_prizes(interaction.user.id)
        if prizes:
            prizes_text = "\n•".join(prizes)
            embed = discord.Embed(title="Your rank decorations", description=prizes_text, color=0xFEBCBE)
            embed.set_thumbnail(url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("You haven't unlocked any prizes yet!")

    @app_commands.command(name="addstella", description="Add stellas to someone")
    @app_commands.guilds(discord.Object(id=1134736053803159592))
    async def addstella(self, interaction: discord.Interaction, member: discord.Member, stellas: int):
        zennie_role_id = 1261435772775563315
        if zennie_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("Sorry, this is a staff only command", ephemeral=True)
            return
        amount = int(stellas) * 100
        levels = await self.get_member_levels(member.id)
        await self.add_xp(member.id, amount, levels)
        
        embed = discord.Embed(title='Stella added!', description=f'I have added **{stellas}** stella(s) to {member.name}', color=0xFEBCBE)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(levels(bot))