import asyncio
from io import BytesIO
import os
import random
import aiohttp
import discord
from discord.ext import commands
import asqlite
import requests
from utils.views import Paginator
from easy_pil import Font
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from typing import Optional, TypedDict, List, Union, Literal, Tuple

class pccategory(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="BTS", emoji="<:bts:1198273351395856424>")
    async def bts(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="BTS Photocards", description="To buy a photo card do\n**+pcbuy bts(number) | +pcbuy bts1**", color=0x2b2d31)
        embed.add_field(name="Photocard Prices", value="common - <a:coin:1192540229727440896> **150,000**\n rare - <a:coin:1192540229727440896> **550,000**\n epic - <a:coin:1192540229727440896> **1,500,000**")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1198576155054309587/bts_00000.png?ex=65bf6807&is=65acf307&hm=ee7fc3acecf4b114623c209acf7cbfcb6d0e27a96106ee196e5b7d273131dc4b&")
        await interaction.response.edit_message(content=None, embed=embed)

    @discord.ui.button(label="blackpink", emoji="<:bpemoji:1198273746272788510>")
    async def blackpink(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="Blackpink Photocards", description="To buy a photo card do\n**+pcbuy bp(number) | +pcbuy bp1**", color=0x2b2d31)
        embed.add_field(name="Photocard Prices", value="common - <a:coin:1192540229727440896> **150,000**\n rare - <a:coin:1192540229727440896> **550,000**\n epic - <a:coin:1192540229727440896> **1,500,000**")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1198626600024018975/blackpink_00000.png?ex=65bf9702&is=65ad2202&hm=0805658b564e834c534823f8e1f92fd56126417474953d195dd364c2167cadb4&")
        await interaction.response.edit_message(content=None, embed=embed)

class PcRow(TypedDict):
    user_id: int
    photocards: str

class photocards(commands.Cog):
    """Commands for the photocards system"""
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:tata:1121909389280944169>"

    def kanzen_only():
        def predicate(ctx: commands.Context):
            if ctx.guild.id == 1121841073673736215:
                return True
            else:
                return False
        return commands.check(predicate)

    async def get_balance(self, user):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT wallet, bank FROM bank WHERE user = ?", (user,))
                row = await cursor.fetchone()
                if row is None:
                    await self.create_account(user)
                    return 0, 0
                return row[0], row[1]

    async def create_account(self, user):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("INSERT INTO bank (user, wallet, bank, maxbank) VALUES (?, 0, 100, 9999999999999999)", (user,))
            await conn.commit()

    async def check_photocards(self, user_id):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT photocards FROM photocards WHERE user_id = ?", (user_id,))
                row = await cursor.fetchone()
                photocards = set(row[0].split(',')) if row else set()
                return photocards

    async def bts_pcs(self, user_id: discord.User) -> BytesIO:
        card = Image.new('RGBA', size=(1920, 1339), color='grey')
        bg = Image.open("./photocards/btsbg.png")
        card.paste(bg)
        pcs = await self.check_photocards(user_id)
        font = ImageFont.truetype("./fonts/Bohemian Soul.otf", size=100)
        normalpcs = {'bts1', 'bts2', 'bts3', 'bts4', 'bts5', 'bts6', 'bts7', 'bts8', 'bts9', 'bts10', 'bts11', 'bts12', 'bts13', 'bts14', 'bts15', 'bts16', 'bts17', 'bts18', 'bts19', 'bts20', 'bts21'}
        rarepcs = {'bts22', 'bts23', 'bts24', 'bts25', 'bts26', 'bts27', 'bts28', 'bts29', 'bts30', 'bts31', 'bts32', 'bts33', 'bts34', 'bts35'}
        epicpcs = {'bts36', 'bts37', 'bts38', 'bts39', 'bts40', 'bts41', 'bts42', 'bts43', 'bts44', 'bts45', 'bts46', 'bts47', 'bts48', 'bts49'}
        padding = 60
        max_cards_in_row = 14

        normal_y = 145
        normal_x = [25]
        normal_count = 0

        rare_y = 680
        rare_x = [25]
        rare_count = 0

        epic_y = 1050
        epic_x = [25]
        epic_count = 0

        def normal_paste(photocard_path: str, normal_y: int):
            photocard_name = photocard_path.split('/')[-1].split('.')[0]
            if photocard_name in pcs:
                normal_x[0] += padding
                photocard = Image.open(photocard_path)
                photocard = photocard.resize((100, 157))
                card.paste(photocard, (normal_x[0], normal_y), photocard)

        def rare_paste(photocard_path: str, rare_y: int):
            photocard_name = photocard_path.split('/')[-1].split('.')[0]
            if photocard_name in pcs:
                rare_x[0] += padding
                photocard = Image.open(photocard_path)
                photocard = photocard.resize((100, 157))
                card.paste(photocard, (rare_x[0], rare_y), photocard)

        def epic_paste(photocard_path: str, epic_y: int):
            photocard_name = photocard_path.split('/')[-1].split('.')[0]
            if photocard_name in pcs:
                epic_x[0] += padding
                photocard = Image.open(photocard_path)
                photocard = photocard.resize((115, 180))
                card.paste(photocard, (epic_x[0], epic_y), photocard)

        for i, photocard_name in enumerate(pcs):
            if photocard_name in normalpcs:
                normal_paste(f'./photocards/{photocard_name}.png', normal_y)
                normal_x[0] += padding
                normal_count += 1

                if normal_count % max_cards_in_row == 0:
                    normal_y += 200
                    normal_x[0] = 25

            elif photocard_name in rarepcs:
                rare_paste(f'./photocards/{photocard_name}.png', rare_y)
                rare_x[0] += padding
                rare_count += 1

                if rare_count % max_cards_in_row == 0:
                    rare_y += 200
                    rare_x[0] = 25

            elif photocard_name in epicpcs:
                epic_paste(f'./photocards/{photocard_name}.png', epic_y)
                epic_x[0] += padding
                epic_count += 1

                if epic_count % max_cards_in_row == 0:
                    epic_y += 200
                    epic_x[0] = 25

        draw = ImageDraw.Draw(card, 'RGBA')
        draw.text((725, 25), 'Common', '#ffffff', font=font)
        draw.text((815, 555), 'Rare', '#ffffff', font=font)
        draw.text((825, 900), 'Epic', '#ffffff', font=font)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def bp_pcs(self, user_id: discord.User) -> BytesIO:
        card = Image.new('RGBA', size=(1000, 1692), color='grey')
        bg = Image.open("./photocards/bpbg.png")
        card.paste(bg)
        pcs = await self.check_photocards(user_id)
        font = ImageFont.truetype("./fonts/Bohemian Soul.otf", size=100)
        normalpcs = {'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8', 'bp9', 'bp10', 'bp11', 'bp12', 'bp13', 'bp14', 'bp15', 'bp16'}
        rarepcs = {'bp17', 'bp18', 'bp19', 'bp20', 'bp21', 'bp22', 'bp23', 'bp24', 'bp25', 'bp26', 'bp27', 'bp28'}
        epicpcs = {'bp29', 'bp30', 'bp31', 'bp32'}
        padding = 60
        max_cards_in_row = 7

        normal_y = 145
        normal_x = [25]
        normal_count = 0

        rare_y = 825
        rare_x = [25]
        rare_count = 0

        epic_y = 1350
        epic_x = [25]
        epic_count = 0

        def normal_paste(photocard_path: str, normal_y: int):
            photocard_name = photocard_path.split('/')[-1].split('.')[0]
            if photocard_name in pcs:
                normal_x[0] += padding
                photocard = Image.open(photocard_path)
                photocard = photocard.resize((100, 157))
                card.paste(photocard, (normal_x[0], normal_y), photocard)

        def rare_paste(photocard_path: str, rare_y: int):
            photocard_name = photocard_path.split('/')[-1].split('.')[0]
            if photocard_name in pcs:
                rare_x[0] += padding
                photocard = Image.open(photocard_path)
                photocard = photocard.resize((100, 157))
                card.paste(photocard, (rare_x[0], rare_y), photocard)

        def epic_paste(photocard_path: str, epic_y: int):
            photocard_name = photocard_path.split('/')[-1].split('.')[0]
            if photocard_name in pcs:
                epic_x[0] += padding
                photocard = Image.open(photocard_path)
                photocard = photocard.resize((115, 180))
                card.paste(photocard, (epic_x[0], epic_y), photocard)

        for i, photocard_name in enumerate(pcs):
            if photocard_name in normalpcs:
                normal_paste(f'./photocards/{photocard_name}.png', normal_y)
                normal_x[0] += padding
                normal_count += 1

                if normal_count % max_cards_in_row == 0:
                    normal_y += 200
                    normal_x[0] = 25

            elif photocard_name in rarepcs:
                rare_paste(f'./photocards/{photocard_name}.png', rare_y)
                rare_x[0] += padding
                rare_count += 1

                if rare_count % max_cards_in_row == 0:
                    rare_y += 200
                    rare_x[0] = 25

            elif photocard_name in epicpcs:
                epic_paste(f'./photocards/{photocard_name}.png', epic_y)
                epic_x[0] += padding
                epic_count += 1

                if epic_count % max_cards_in_row == 0:
                    epic_y += 200
                    epic_x[0] = 25

        draw = ImageDraw.Draw(card, 'RGBA')
        draw.text((265, 25), 'Common', '#ffffff', font=font)
        draw.text((350, 695), 'Rare', '#ffffff', font=font)
        draw.text((365, 1200), 'Epic', '#ffffff', font=font)
        buffer = BytesIO()
        card.save(buffer, 'png')
        buffer.seek(0)
        return buffer

    async def update_balance(self, user, wallet_change=0, bank_change=0):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT wallet, bank FROM bank WHERE user = ?", (user,))
                row = await cursor.fetchone()
                if row is None:
                    await self.create_account(user)
                    await cursor.execute("SELECT wallet, bank FROM bank WHERE user = ?", (user,))
                    row = await cursor.fetchone()
                wallet_balance = row[0] + wallet_change
                bank_balance = row[1] + bank_change
                await cursor.execute("UPDATE bank SET wallet = ?, bank = ? WHERE user = ?", (wallet_balance, bank_balance, user))
                await conn.commit()
                return wallet_balance, bank_balance

    @commands.command(description="View the photocards that are for sale", extras="+photocards")
    async def photocards(self, ctx):
        embed = discord.Embed(title="BTS Photocards", description="To buy a photo card do\n**+pcbuy bts(number) | +pcbuy bts1**", color=0x2b2d31)
        embed.add_field(name="Photocard Prices", value="common - <a:coin:1192540229727440896> **150,000**\n rare - <a:coin:1192540229727440896> **550,000**\n epic - <a:coin:1192540229727440896> **1,500,000**")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1198576155054309587/bts_00000.png?ex=65bf6807&is=65acf307&hm=ee7fc3acecf4b114623c209acf7cbfcb6d0e27a96106ee196e5b7d273131dc4b&")
        view = pccategory(bot=self.bot)
        await ctx.reply(embed=embed, view=view)

    @commands.command(description="Buy photocards from the PC shop", extras="+buy bts1")
    @kanzen_only()
    async def pcbuy(self, ctx, item: str):
        shop_items = {
            "bts1": 150000,
            "bts2" : 150000,
            "bts3" : 150000,
            "bts4" : 150000,
            "bts5" : 150000,
            "bts6" : 150000,
            "bts7" : 150000,
            "bts8" : 150000,
            "bts9" : 150000,
            "bts10" : 150000,
            "bts11" : 150000,
            "bts12" : 150000,
            "bts13" : 150000,
            "bts14" : 150000,
            "bts15" : 150000,
            "bts16" : 150000,
            "bts17" : 150000,
            "bts18" : 150000,
            "bts19" : 150000,
            "bts20" : 150000,
            "bts21" : 150000,
            "bts22" : 550000,
            "bts23" : 550000,
            "bts24" : 550000,
            "bts25" : 550000,
            "bts26" : 550000,
            "bts27" : 550000,
            "bts28" : 550000,
            "bts29" : 550000,
            "bts30" : 550000,
            "bts31" : 550000,
            "bts32" : 550000,
            "bts33" : 550000,
            "bts34" : 550000,
            "bts35" : 550000,
            "bts36" : 1500000,
            "bts37" : 1500000,
            "bts38" : 1500000,
            "bts39" : 1500000,
            "bts40" : 1500000,
            "bts41" : 1500000,
            "bts42" : 1500000,
            "bts43" : 1500000,
            "bts44" : 1500000,
            "bts45" : 1500000,
            "bts46" : 1500000,
            "bts47" : 1500000,
            "bts48" : 1500000,
            "bts49" : 1500000,
            "bp1": 150000,
            "bp2" : 150000,
            "bp3" : 150000,
            "bp4" : 150000,
            "bp5" : 150000,
            "bp6" : 150000,
            "bp7" : 150000,
            "bp8" : 150000,
            "bp9" : 150000,
            "bp10" : 150000,
            "bp11" : 150000,
            "bp12" : 150000,
            "bp13" : 150000,
            "bp14" : 150000,
            "bp15" : 150000,
            "bp16" : 150000,
            "bp17" : 550000,
            "bp18" : 550000,
            "bp19" : 550000,
            "bp20" : 550000,
            "bp21" : 550000,
            "bp22" : 550000,
            "bp23" : 550000,
            "bp24" : 550000,
            "bp25" : 550000,
            "bp26" : 550000,
            "bp27" : 550000,
            "bp28" : 550000,
            "bp29" : 1500000,
            "bp30" : 1500000,
            "bp31" : 1500000,
            "bp32" : 1500000,
        }
        item_lower = item.lower()
        if item_lower not in shop_items:
            return await ctx.reply("Item not found in the shop.")

        price = shop_items[item_lower]
        wallet_balance, _ = await self.get_balance(ctx.author.id)
        if wallet_balance < price:
            return await ctx.reply("You don't have enough coins to buy this item.")

        new_wallet_balance, _ = await self.update_balance(ctx.author.id, -price, 0)

        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT photocards FROM photocards WHERE user_id = ?", (ctx.author.id,))
                photocards_row = await cursor.fetchone()

        if photocards_row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    current_photocards = set(photocards_row[0].split(','))
                    new_photocards = current_photocards.union({item_lower})
                    await cursor.execute("UPDATE photocards SET photocards = ? WHERE user_id = ?", (','.join(new_photocards), ctx.author.id))
                    await conn.commit()
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO photocards (user_id, photocards) VALUES (?, ?)", (ctx.author.id, item_lower))
                    await conn.commit()

        await ctx.reply(f"You have successfully purchased {item} for <a:coin:1192540229727440896> {price} coins.\nYour new wallet balance is <a:coin:1192540229727440896> {new_wallet_balance} coins.")

    @commands.command(description="Sell photocards to the PC shop", extras="+sell bts1")
    @kanzen_only()
    async def pcsell(self, ctx, item: str):
        shop_items = {
            "bts1": 150000,
            "bts2" : 150000,
            "bts3" : 150000,
            "bts4" : 150000,
            "bts5" : 150000,
            "bts6" : 150000,
            "bts7" : 150000,
            "bts8" : 150000,
            "bts9" : 150000,
            "bts10" : 150000,
            "bts11" : 150000,
            "bts12" : 150000,
            "bts13" : 150000,
            "bts14" : 150000,
            "bts15" : 150000,
            "bts16" : 150000,
            "bts17" : 150000,
            "bts18" : 150000,
            "bts19" : 150000,
            "bts20" : 150000,
            "bts21" : 150000,
            "bts22" : 550000,
            "bts23" : 550000,
            "bts24" : 550000,
            "bts25" : 550000,
            "bts26" : 550000,
            "bts27" : 550000,
            "bts28" : 550000,
            "bts29" : 550000,
            "bts30" : 550000,
            "bts31" : 550000,
            "bts32" : 550000,
            "bts33" : 550000,
            "bts34" : 550000,
            "bts35" : 550000,
            "bts36" : 1500000,
            "bts37" : 1500000,
            "bts38" : 1500000,
            "bts39" : 1500000,
            "bts40" : 1500000,
            "bts41" : 1500000,
            "bts42" : 1500000,
            "bts43" : 1500000,
            "bts44" : 1500000,
            "bts45" : 1500000,
            "bts46" : 1500000,
            "bts47" : 1500000,
            "bts48" : 1500000,
            "bts49" : 1500000,
            "bp1": 150000,
            "bp2" : 150000,
            "bp3" : 150000,
            "bp4" : 150000,
            "bp5" : 150000,
            "bp6" : 150000,
            "bp7" : 150000,
            "bp8" : 150000,
            "bp9" : 150000,
            "bp10" : 150000,
            "bp11" : 150000,
            "bp12" : 150000,
            "bp13" : 150000,
            "bp14" : 150000,
            "bp15" : 150000,
            "bp16" : 150000,
            "bp17" : 550000,
            "bp18" : 550000,
            "bp19" : 550000,
            "bp20" : 550000,
            "bp21" : 550000,
            "bp22" : 550000,
            "bp23" : 550000,
            "bp24" : 550000,
            "bp25" : 550000,
            "bp26" : 550000,
            "bp27" : 550000,
            "bp28" : 550000,
            "bp29" : 1500000,
            "bp30" : 1500000,
            "bp31" : 1500000,
            "bp32" : 1500000,
        }
        item_lower = item.lower()
        if item_lower not in shop_items:
            return await ctx.reply("Item not found in the shop.")

        price = shop_items[item_lower]

        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT photocards FROM photocards WHERE user_id = ?", (ctx.author.id,))
                photocards_row = await cursor.fetchone()

        if photocards_row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    current_photocards = set(photocards_row[0].split(','))
                    if item_lower not in current_photocards:
                        return await ctx.reply("You don't own this photocard.")

                    new_wallet_balance, _ = await self.update_balance(ctx.author.id, price, 0)
                    current_photocards.remove(item_lower)
                    await cursor.execute("UPDATE photocards SET photocards = ? WHERE user_id = ?", (','.join(current_photocards), ctx.author.id))
                    await conn.commit()

            await ctx.reply(f"You have successfully sold {item} for <a:coin:1192540229727440896> {price} coins.\nYour new wallet balance is <a:coin:1192540229727440896> {new_wallet_balance} coins.")
        else:
            await ctx.reply("You don't own any photocards to sell.")

    @commands.command(description="View your BTS photocards", extras="+btspcs")
    async def btspcs(self, ctx, member: Optional[discord.Member]):
        member = member or ctx.author
        user_id = member.id
        photocards = await self.check_photocards(user_id)

        if not photocards:
            return await ctx.reply("You don't have any photocards yet.")

        async with ctx.typing():
            buffer = await self.bts_pcs(user_id)
            file = discord.File(buffer, filename="photocard.png")
            await ctx.reply(file=file)

    @commands.command(description="View your blackpink photocards", extras="+bppcs")
    async def bppcs(self, ctx, member: Optional[discord.Member]):
        member = member or ctx.author
        user_id = member.id
        photocards = await self.check_photocards(user_id)

        if not photocards:
            return await ctx.reply("You don't have any photocards yet.")

        async with ctx.typing():
            buffer = await self.bp_pcs(user_id)
            file = discord.File(buffer, filename="photocard.png")
            await ctx.reply(file=file)

async def setup(bot):
    await bot.add_cog(photocards(bot))