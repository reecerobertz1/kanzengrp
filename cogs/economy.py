import asyncio
from io import BytesIO
import random
import aiohttp
import discord
from discord.ext import commands
import asqlite
from utils.views import Paginator
from easy_pil import Font
from PIL import Image, ImageDraw, ImageFont

class Economy(commands.Cog):
    """Commands for the economy system"""
    def __init__(self, bot):
        self.bot = bot
        self.pool = None
        self.bot.loop.create_task(self.init_database())

    async def init_database(self):
        self.pool = await asqlite.create_pool('databases/levels.db')
        async with self.pool.acquire() as conn:
            await conn.execute('''CREATE TABLE IF NOT EXISTS bank (
                user INTEGER PRIMARY KEY,
                wallet INTEGER,
                bank INTEGER,
                maxbank INTEGER
            )''')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.init_database()
        print(f'{self.__class__.__name__} Cog is ready')

    async def get_balance(self, user):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT wallet, bank FROM bank WHERE user = ?", (user,))
                row = await cursor.fetchone()
                if row is None:
                    await self.create_account(user)
                    return 0, 0
                return row[0], row[1]

    async def check_inventory(self, user_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT item, quantity FROM inventory WHERE user = ?", (user_id,))
                rows = await cursor.fetchall()
                inventory = {}
                for row in rows:
                    item_name, quantity = row
                    inventory[item_name] = quantity
                return inventory

    async def create_account(self, user):
        async with self.pool.acquire() as conn:
            await conn.execute("INSERT INTO bank (user, wallet, bank, maxbank) VALUES (?, 0, 100, 10000)", (user,))
            await conn.commit()

    async def update_balance(self, user, wallet_change=0, bank_change=0):
        async with self.pool.acquire() as conn:
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

    async def use_item(self, user_id, item_name):
        user_inventory = await self.check_inventory(user_id)
        if item_name not in user_inventory:
            return False
        user_inventory[item_name] -= 1
        await self.set_inventory(user_id, user_inventory)
        if user_inventory[item_name] <= 0:
            del user_inventory[item_name]
        return True

    def kanzen_only():
        def predicate(ctx: commands.Context):
            if ctx.guild.id == 1121841073673736215:
                return True
            else:
                return False
        return commands.check(predicate)

    @commands.command(aliases=["bal"], description="Check your bank and wallet balance")
    @kanzen_only()
    async def balance(self, ctx, user: discord.Member = None):
        async with ctx.typing():
            user = user or ctx.author
            wallet_balance, bank_balance = await self.get_balance(user.id)
            avatar_url = ctx.author.avatar.url
            async with self.bot.session.get(avatar_url) as response:
                if response.status == 200:
                    avatar_data = await response.read()
                else:
                    avatar_data = None

            img = Image.open('./assets/bank_card.png')
            draw = ImageDraw.Draw(img)
            if avatar_data:
                avatar = BytesIO(avatar_data)
                avatar_paste, circle = self._get_round_avatar(avatar)
                img.paste(avatar_paste, (35, 250), circle)

            poppins = Font.poppins(size=25)
            poppins_small = Font.poppins(size=25)
            display_name_parts = ctx.author.display_name.split('|')
            display_name = display_name_parts[0].strip() if display_name_parts else ctx.author.display_name
            draw.text((75, 245), display_name, font=poppins_small)
            draw.text((75, 115), f'wallet: {str(wallet_balance)}', '#FDCA04', font=poppins)
            draw.text((75, 165), f'bank: {str(bank_balance)}', font=poppins)
            coin_img = Image.open('./assets/coin.png')
            coin_img = coin_img.resize((40, 40))
            bank_img = Image.open('./assets/bank.png')
            bank_img = bank_img.resize((40, 40))
            img.paste(coin_img, (25, 115), coin_img)
            img.paste(bank_img, (25, 165), bank_img)
            img.save("bank.png")
            await ctx.reply(file=discord.File("bank.png"))

    @commands.command(aliases=['dep'], description="Deposite money into your bank")
    @kanzen_only()
    async def deposit(self, ctx, amount: int):
        if amount <= 0:
            return await ctx.send("Amount must be greater than 0.")
        wallet_balance, bank_balance = await self.get_balance(ctx.author.id)
        if wallet_balance < amount:
            return await ctx.send("You don't have enough coins in your wallet.")
        if bank_balance + amount > 10000:
            return await ctx.send("Your bank is full.")
        new_wallet_balance, new_bank_balance = await self.update_balance(ctx.author.id, -amount, amount)
        await ctx.send(f"You deposited <a:coin:1154168127802843216> {amount} coins into your bank. Your new balance is: Wallet: <a:coin:1154168127802843216> {new_wallet_balance} coins, Bank: <a:coin:1154168127802843216> {new_bank_balance} coins.")

    @commands.command(description="Withdraw money from your bank")
    @kanzen_only()
    async def withdraw(self, ctx, amount: int):
        if amount <= 0:
            return await ctx.send("Amount must be greater than 0.")
        wallet_balance, bank_balance = await self.get_balance(ctx.author.id)
        if bank_balance < amount:
            return await ctx.send("You don't have enough coins in your bank.")
        new_wallet_balance, new_bank_balance = await self.update_balance(ctx.author.id, amount, -amount)
        await ctx.send(f"You withdrew <a:coin:1154168127802843216> {amount} coins from your bank. Your new balance is: Wallet: <a:coin:1154168127802843216> {new_wallet_balance} coins, Bank: <a:coin:1154168127802843216> {new_bank_balance} coins.")

    @commands.command(description="Donate to ~~the poor~~ other members")
    @kanzen_only()
    async def donate(self, ctx, user: discord.Member, amount: int):
        if amount <= 0:
            return await ctx.send("Amount must be greater than 0.")
        if user == ctx.author:
            return await ctx.send("You can't give coins to yourself.")
        wallet_balance, _ = await self.get_balance(ctx.author.id)
        if wallet_balance < amount:
            return await ctx.send("You don't have enough coins in your wallet.")
        _, _ = await self.update_balance(ctx.author.id, -amount, 0)
        new_wallet_balance, new_bank_balance = await self.update_balance(user.id, amount, 0)
        await ctx.send(f"You gave {user.display_name} {amount} coins. {user.display_name}'s new balance is: Wallet: <a:coin:1154168127802843216> {new_wallet_balance} coins, Bank: <a:coin:1154168127802843216> {new_bank_balance} coins.")

    @commands.command(description="Beg celebs for coins")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @kanzen_only()
    async def beg(self, ctx):
        celeb_names = [
            "Bill Gates",
            "Elon Musk",
            "Jeff Bezos",
            "Oprah Winfrey",
            "Taylor Swift",
            "Dwayne 'The Rock' Johnson",
        ]

        celeb_lines = {
            "Bill Gates": [
                "Oh, you poor thing. Here's some pocket change for you!",
                "'Another one? Well, alright. Here you go.'",
                "Bill Gates generously donates some coins to you."
            ],
            "Elon Musk": [
                "'I'll give you some coins, but only because I like rockets.'",
                "You receive some coins from the richest rocket enthusiast.",
                "Elon Musk tosses some coins your way with a smile."
            ],
            "Jeff Bezos": [
                "'I could spare a few coins. After all, I'm Jeff Bezos.'",
                "You get some coins from the ex-Amazon CEO.",
                "Jeff Bezos donates some of his Amazon money to you."
            ],
            "Oprah Winfrey": [
            "Oprah reaches into her pocket and gives you some coins!",
            "'You get coins! You get coins! Everybody gets coins!' - Oprah",
            "You receive a gift of coins from Oprah Winfrey."
            ],
            "Taylor Swift": [
                "Taylor Swift hands you some coins with a smile.",
                "'Coins for the fans!' - Taylor Swift",
                "You get coins from the pop sensation, Taylor Swift."
            ],
            "Dwayne 'The Rock' Johnson": [
                "'Can you smell what The Rock is giving?' - Dwayne Johnson",
                "The Rock shares some of his success with you in coins.",
                "You receive a 'Rock'-solid amount of coins from Dwayne Johnson."
            ]
        }

        celeb_name = random.choice(celeb_names)
        celeb_line = random.choice(celeb_lines.get(celeb_name, ["No coins for you."]))
        earnings = random.randint(1, 100)
        wallet_balance, _ = await self.update_balance(ctx.author.id, earnings, 0)
        embed=discord.Embed(title=celeb_name, description=celeb_line, color=0x2b2d31)
        embed.add_field(name="You received", value=f"<a:coin:1154168127802843216> {earnings}")
        embed.add_field(name="Your new wallet balance", value=f"<a:coin:1154168127802843216> {wallet_balance}")
        await ctx.reply(embed=embed)

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)
            await ctx.reply(f"You are on cooldown. Try again in {seconds} seconds.")

    @commands.command(description="Search locations for coins")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @kanzen_only()
    async def search(self, ctx):
        search_responses = {
            'a park': [
                ("You searched a park and found a squirrel that gave you some coins!", random.randint(1, 100)),
                ("You explored a park and stumbled upon a hidden treasure!", random.randint(1, 100)),
                ("You searched a park and found some loose change!", random.randint(1, 100))
            ],
            'an alley': [
                ("You searched an alley and found a wallet with some coins inside!", random.randint(1, 100)),
                ("You explored a dark alley and found some discarded coins!", random.randint(1, 100)),
                ("You searched an alley and found nothing but trash.", 0)
            ],
            'a dumpster': [
                ("You searched a dumpster and found a valuable item worth some coins!", random.randint(1, 100)),
                ("You rummaged through a dumpster and found some hidden coins!", random.randint(1, 100)),
                ("You searched a dumpster and got dirty for no reward.", 0)
            ],
            'the forest': [
                ("You ventured into the forest and found a hidden treasure chest!", random.randint(1, 100)),
                ("You explored the forest and found a friendly forest creature!", random.randint(1, 100)),
                ("You searched the forest, but it seems there was nothing valuable there today.", 0)
            ],
            'a cave': [
                ("You entered a dark cave and found a hidden stash of coins!", random.randint(1, 100)),
                ("You explored a mysterious cave and found a rare gemstone!", random.randint(1, 100)),
                ("You searched a cave but found nothing valuable.", 0)
            ]
        }
        random_choices = random.sample(list(search_responses.keys()), 3)
        where = discord.Embed(title="Where would you like to search?", description=f"**{', '.join(random_choices)}**", color=0x2b2d31)
        await ctx.reply(embed=where)
        def check(msg):
            return msg.author == ctx.author and msg.content.lower() in map(str.lower, random_choices)
        try:
            choice_msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            user_choice = choice_msg.content.lower()
        except asyncio.TimeoutError:
            return await ctx.reply("You took too long to choose a location. Try again later.")

        response, earnings = random.choice(search_responses[user_choice])
        if earnings > 0:
            wallet_balance, _ = await self.update_balance(ctx.author.id, earnings, 0)
            searched = discord.Embed(title=f"You searched {user_choice}", description=response, color=0x2b2d31)
            searched.add_field(name="You found", value=f"<a:coin:1154168127802843216> {earnings}")
            searched.add_field(name="Your new wallet balance", value=f"<a:coin:1154168127802843216> {wallet_balance}")
            await ctx.reply(embed=searched)
        else:
            await ctx.reply(response)

    @search.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)
            await ctx.reply(f"You are on cooldown. Try again in {seconds} seconds.")

    @commands.command(description="See the richest kanzen members")
    @kanzen_only()
    async def wealth(self, ctx, page: int = 1):
        if page <= 0:
            return await ctx.send("There is currently no one on the leaderboard")

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT user, wallet, bank FROM bank ORDER BY (wallet + bank) DESC")
                rows = await cursor.fetchall()

        per_page = 10
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        leaderboard_embed = discord.Embed(
            title="Coin Leaderboard",
            description="The richest Kanzen members!",
            color=0x2b2d31
        )

        for idx, (user_id, wallet_balance, bank_balance) in enumerate(rows[start_idx:end_idx], start=start_idx + 1):
            user = self.bot.get_user(user_id)
            if user:
                leaderboard_embed.add_field(
                    name=f"{idx}. {user.display_name}",
                    value=f"<:wallet:1154163630699458660> Wallet: <a:coin:1154168127802843216> {wallet_balance}\n"
                        f"<:bank:1154163938234208367> Bank: <a:coin:1154168127802843216> {bank_balance}",
                    inline=False
                )
                leaderboard_embed.set_footer(text=f"Page {page}", icon_url=ctx.author.avatar)
                leaderboard_embed.set_thumbnail(url=ctx.guild.icon)
            else:
                leaderboard_embed.add_field(
                    name=f"{idx}. User not found",
                    value=f"<a:coin:1154168127802843216> Wallet: {wallet_balance} coins\n"
                        f"<:bank:YOUR_BANK_ICON_ID> Bank: {bank_balance} coins",
                    inline=False
                )
        await ctx.send(embed=leaderboard_embed)

    async def get_wallet_balance(self, user_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT wallet FROM bank WHERE user = ?", (user_id,))
                row = await cursor.fetchone()
                if row:
                    return row[0]
                else:
                    return 0

    async def get_bank_balance(self, user_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT bank FROM bank WHERE user = ?", (user_id,))
                row = await cursor.fetchone()
                if row:
                    return row[0]
                else:
                    return 0

    @commands.command(description="See what is in the shop")
    @kanzen_only()
    async def shop(self, ctx):
        shop_items = {
            "Cookie": 10,
            "Soda": 15,
            "Pizza": 25,
            "Laptop": 100,
            "Gaming PC": 500,
            "Car": 1000,
        }

        shop_embed = discord.Embed(
            title="Welcome to the Shop!",
            description="Buy items to enhance your life!",
            color=0x2b2d31
        )

        for item, price in shop_items.items():
            shop_embed.add_field(
                name=item,
                value=f"Price: <a:coin:1154168127802843216> {price} coins",
                inline=False
            )

        await ctx.send(embed=shop_embed)

    @commands.command(description="Buy items from the shop")
    @kanzen_only()
    async def buy(self, ctx, item: str, quantity: int = 1):
        shop_items = {
            "Cookie": 10,
            "Soda": 15,
            "Pizza": 25,
            "Laptop": 100,
            "Fishing_rod": 250,
            "Gaming PC": 500,
            "Car": 1000,
        }

        item = item.capitalize()

        if item not in shop_items:
            return await ctx.send("Item not found in the shop.")

        price = shop_items[item] * quantity
        wallet_balance, _ = await self.get_balance(ctx.author.id)
        if wallet_balance < price:
            return await ctx.send("You don't have enough coins to buy this item.")

        new_wallet_balance, _ = await self.update_balance(ctx.author.id, -price, 0)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (ctx.author.id, item))
                row = await cursor.fetchone()

        if row:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] + quantity
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, ctx.author.id, item))
                    await conn.commit()
        else:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO inventory (user, item, quantity) VALUES (?, ?, ?)", (ctx.author.id, item, quantity))
                    await conn.commit()

        await ctx.send(f"You have successfully purchased {quantity} {item}(s) for <a:coin:1154168127802843216> {price} coins. Your new wallet balance is <a:coin:1154168127802843216> {new_wallet_balance} coins.")

    @commands.command(description="See what items you have")
    @kanzen_only()
    async def inventory(self, ctx):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT item, quantity FROM inventory WHERE user = ?", (ctx.author.id,))
                rows = await cursor.fetchall()

        if not rows:
            return await ctx.send("Your inventory is empty.")

        inventory_embed = discord.Embed(
            title="Inventory",
            description="Here are the items you have in your inventory:",
            color=0x2b2d31
        )

        for item, quantity in rows:
            inventory_embed.add_field(
                name=f"{item}",
                value=f"You have **{quantity}**",
                inline=False
            )

        await ctx.send(embed=inventory_embed)

    @commands.command(description="Sell your unwanted items")
    @kanzen_only()
    async def sell(self, ctx, item: str, quantity: int = 1):
        shop_items = {
            "Cookie": 10,
            "Soda": 15,
            "Pizza": 25,
            "Laptop": 100,
            "Gaming PC": 500,
            "Car": 1000,
        }

        item = item.capitalize()

        if item not in shop_items:
            return await ctx.send("Item not found in the shop.")

        price = shop_items[item] * quantity
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (ctx.author.id, item))
                row = await cursor.fetchone()

        if not row or row[0] < quantity:
            return await ctx.send("You don't have enough of this item to sell.")
        sell_price = int(price * 0.7)
        wallet_balance, _ = await self.get_balance(ctx.author.id)
        new_wallet_balance, _ = await self.update_balance(ctx.author.id, sell_price, 0)
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                new_quantity = row[0] - quantity
                if new_quantity <= 0:
                    await cursor.execute("DELETE FROM inventory WHERE user = ? AND item = ?", (ctx.author.id, item))
                else:
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, ctx.author.id, item))
                await conn.commit()

        await ctx.send(f"You have successfully sold {quantity} {item}(s) for <a:coin:1154168127802843216> {sell_price} coins. Your new wallet balance is <a:coin:1154168127802843216> {new_wallet_balance} coins.")

    @commands.command(hidden=True)
    @kanzen_only()
    async def newshop(self, ctx):
        categories = [
            "Badges",
            "Gadgets"
        ]
        emojis = [
            ":bt21:1149411052489027674",
            ":tata:1121909389280944169"
        ]
        descriptions = [
            "Home page for the help command",
            "Includes commands you can use for fun!"
        ]
        dropdown = discord.ui.Select(
        placeholder="Select a category",
        options=[discord.SelectOption(label=category, emoji=emoji, description=description) for category, emoji, description in zip(categories, emojis, descriptions)]
        )
        about_hoshi_embed = discord.Embed(description="owner info:\n<a:Arrow_1:1145603161701224528> Hoshi is owned by [Reece](https://instagram.com/remqsi)\n<a:Arrow_1:1145603161701224528> Reece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)\n\ndevelopment info:\n<a:Arrow_1:1145603161701224528> Hoshi is coded in Python 3.11.4\n<a:Arrow_1:1145603161701224528> [Download Python 3.11.4](https://www.python.org/downloads/)\n<a:Arrow_1:1145603161701224528> Developed by [Reece](https://instagram.com/remqsi) with help from [Alex](https://instagram.com/rqinflow)\n\nextra info:\n<a:Arrow_1:1145603161701224528> Hoshi's prefix is `+`\n<a:Arrow_1:1145603161701224528> Hoshi was made for [**__Kanzengrp__**](https://instagram.com/kanzengrp)\n\nbug reports\n<a:Arrow_1:1145603161701224528> Use __+report__ to report bug reports!" ,color=0x2b2d31)
        about_hoshi_embed.set_thumbnail(url=ctx.guild.icon)
        about_hoshi_embed.set_author(name="About Hoshi", icon_url=self.bot.user.display_avatar.url)
        about_hoshi_embed.set_footer(text="Home Page", icon_url=ctx.author.avatar)
        view = discord.ui.View()
        view.add_item(dropdown)
        message = await ctx.send(embed=about_hoshi_embed, view=view)
        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            if selected_category == categories[0]:
                embed = discord.Embed(description="owner info:\n<a:Arrow_1:1145603161701224528> Hoshi is owned by [Reece](https://instagram.com/remqsi)\n<a:Arrow_1:1145603161701224528> Reece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)\n<a:Arrow_1:1145603161701224528> [Download VSC](https://code.visualstudio.com/download)\n\ndevelopment info:\n<a:Arrow_1:1145603161701224528> Hoshi is coded in Python 3.11.4\n<a:Arrow_1:1145603161701224528> [Download Python 3.11.4](https://www.python.org/downloads/)\n<a:Arrow_1:1145603161701224528> Developed by [Reece](https://instagram.com/remqsi) with help from [Alex](https://instagram.com/rqinflow)\n\nextra info:\n<a:Arrow_1:1145603161701224528> Hoshi's prefix is **+**\n<a:Arrow_1:1145603161701224528> Hoshi was made for [**__Kanzengrp__**](https://instagram.com/kanzengrp)\n\nbug reports:\n<a:Arrow_1:1145603161701224528> Use __+report__ to report bug reports!", color=0x2b2d31)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1121841074512605186/1154413210187866202/e02ce86bcfd6d1d6c2f775afb3ec8c01_w200.gif")
                embed.set_author(name="About Hoshi", icon_url=self.bot.user.display_avatar.url)
                embed.set_footer(text="Home Page", icon_url=ctx.author.avatar)
            elif selected_category == categories[1]:
                embed = discord.Embed(color=0x2b2d31)
                embed.set_author(name="fun commands", icon_url=self.bot.user.display_avatar.url)
                embed.add_field(name="+tweet", value="<a:Arrow_1:1145603161701224528> Tweet as yourself with Hoshi")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1121841074512605186/1154413210187866202/e02ce86bcfd6d1d6c2f775afb3ec8c01_w200.gif")
                embed.set_footer(text="page 1/8", icon_url=ctx.author.avatar)
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")
            await interaction.response.edit_message(embed=embed, view=view)
        dropdown.callback = dropdown_callback

    @commands.command(hidden=True)
    @kanzen_only()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def fish(self, ctx):
        user_id = ctx.author.id
        has_fishing_rod = await self.check_inventory(user_id, "Fishing_rod")
        has_another_item = await self.check_inventory(user_id, "fishing_rod")

        if not has_fishing_rod:
            await ctx.send("You need a fishing rod before you can fish DUH")
            return
        if not await self.use_item(user_id, "fishing_rod"):
            await ctx.send("Your fishing rod has run out of uses!")
            return
        catch = random.choice(["fish", "fish", "coins", "nothing"])
        if catch == "fish":
            await self.add_item(user_id, "fish", 1)
            await ctx.send("You caught a fish!")
        elif catch == "coins":
            coins_found = random.randint(1, 10)
            await self.update_balance(user_id, coins_found, 0)
            await ctx.send(f"You found {coins_found} coins while fishing!")
        else:
            await ctx.send("You didn't catch anything while fishing.")

    @fish.error
    async def fish_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)
            await ctx.send(f"You are on cooldown. Try again in {seconds} seconds.")

async def setup(bot):
    await bot.add_cog(Economy(bot))