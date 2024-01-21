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
from typing import Optional, Tuple

gifs = {
    "0": [
        "https://cdn.discordapp.com/attachments/1184208577120960632/1193993133457940510/dogwalker-man_00000.png?ex=65aebbc2&is=659c46c2&hm=e7f05ac5edd74becf1be518216103005e94f7d496b11241a0564c094abb2daa3&",
        "https://cdn.discordapp.com/attachments/1184208577120960632/1193993484206624768/dogwalker-man.gif?ex=65aebc15&is=659c4715&hm=d2cc0d043e77f718c89e9eea3f7927b2eefe6fa1ff5f5a25215664098353645c&"
    ],
    "1": [
        "https://cdn.discordapp.com/attachments/1184208577120960632/1193993708656394360/dogwalker-girl_00000.png?ex=65aebc4b&is=659c474b&hm=e7ff476ec8608cea0538e50ca864091bdc0a6869308df273619b351530fb92eb&",
        "https://cdn.discordapp.com/attachments/1184208577120960632/1193993876365643856/dogwalker-girl_1.gif?ex=65aebc73&is=659c4773&hm=c0d0ddbf5aa5ab73e192b1ad2f72f9490f5152177a54077851135624695c6999&"
    ]
}

class tryagain(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot
        self.amount = None

    def set_amount(self, amount):
        self.amount = amount

    async def create_account(self, user):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("INSERT INTO bank (user, wallet, bank, maxbank) VALUES (?, 0, 100, 9999999999999999)", (user,))
            await conn.commit()

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

    @discord.ui.button(label="Spin Again")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button,):
        user = interaction.user.id
        doubled = "https://cdn.discordapp.com/attachments/1184208577120960632/1197220330675126322/double.gif?ex=65ba7952&is=65a80452&hm=c8ff676af6ef8368a3a8e540195f9efc6c0e264ec4f2ecfdfa8eeb95681fe7d4&"
        tripled = "https://cdn.discordapp.com/attachments/1184208577120960632/1197220403156885504/triple.gif?ex=65ba7963&is=65a80463&hm=40389da7e1bfa5239b80a441f483be2f4f44e718fd095be0b55d1d0654eeb6ba&"
        gave = "https://cdn.discordapp.com/attachments/1184208577120960632/1197488790252552212/donate.gif?ex=65bb7357&is=65a8fe57&hm=a50ffb7c923c8263582e87f61982979a1d12ef7dde745b61510f6a432871dbf6&"
        lost = "https://cdn.discordapp.com/attachments/1184208577120960632/1197488816412434482/loose.gif?ex=65bb735e&is=65a8fe5e&hm=098beb449ad5f5fe13fbfa396b2d1a1245f456607f69f02559c7934ef42a886c&"
        ranwheel = ['triple', 'double', 'loose']
        wheelran = random.choice(ranwheel)
        newamount = self.amount

        if wheelran == 'double':
            newamount *= 2
            title = 'YOUR MONEY HAS BEEN DOUBLED!'
            description = f"Your money has been **DOUBLED**! <a:coin:1192540229727440896> {newamount} has been added to your wallet"
            await self.update_balance(user, newamount)
            wheel = doubled
            color = 0x5BD437
            editedwheel = "https://cdn.discordapp.com/attachments/1184208577120960632/1197220425114075206/double_image_00000.png?ex=65ba7968&is=65a80468&hm=801eb50b3387d076245c7b513375e34e316d4fe4ba89239f4600a8ef21b7db3d&"
        elif wheelran == 'triple':
            newamount *= 3
            title = 'YOUR MONEY HAS BEEN TRIPLED!!!'
            await self.update_balance(user, newamount)
            color = 0xd4af37
            description = f"Your money has been **TRIPLED**! <a:coin:1192540229727440896> {newamount} has been added to your wallet"
            wheel = tripled
            editedwheel = "https://cdn.discordapp.com/attachments/1184208577120960632/1197220443891978250/triple_image_00000.png?ex=65ba796d&is=65a8046d&hm=eec1def1122ae9fcabd817fb5368d165ea928953c078d71c7d20496651e0c3e1&"
        elif wheelran == 'give':
            wheel = gave
            title = 'Someone else got rich'
            color = 0xD11717
            description = 'You had to give your money to someone else'
            editedwheel = "https://cdn.discordapp.com/attachments/1184208577120960632/1197489245330350131/donate_image_00000.png?ex=65bb73c4&is=65a8fec4&hm=fd7b1080beecc7a47f9f04b2897fd11da2ac164fdedaff6a6f839ac082c8271d&"
        elif wheelran == 'loose':
            wheel = lost
            title = 'YOU LOST'
            lostamount = self.amount
            await self.update_balance(user, -lostamount)
            description = 'You lost all your money... rip'
            color = 0xD11717
            editedwheel = "https://cdn.discordapp.com/attachments/1184208577120960632/1197489178875809872/loose_image_00000.png?ex=65bb73b4&is=65a8feb4&hm=cd100a25d999ea78a0d650188ec67762e52fba10e26b4084992c970dae2addcb&"

        embed = discord.Embed(title=f"You gambled <a:coin:1192540229727440896> {self.amount}", color=0x2b2d31)
        embed.set_image(url=wheel)
        embed.set_footer(text="Goodluck!")
        message = await interaction.response.edit_message(content=None, embed=embed, view=None)
        await asyncio.sleep(2.4)
        edited_embed = discord.Embed(title=title, description=description, color=color)
        edited_embed.set_image(url=editedwheel)
        edited_embed.set_footer(text="Thank you for playing!")
        if message:
            await message.edit(content=None, embed=edited_embed)
        else:
            await interaction.followup.send(embed=edited_embed)

class amazon(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="package 1")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1196001945652047902/amazon2_00000.png?ex=65b60a9c&is=65a3959c&hm=55fd203885c87fe22b434d531defd8318b6dfa253d122e00638111cf891cedbb&")
        await interaction.response.edit_message(content=None, view=amazon1(bot=self.bot), embed=embed)

class amazon1(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="package 2")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1196001962957738005/amazon3_00000.png?ex=65b60aa0&is=65a395a0&hm=e62cf11483e759de433d8c050bc380982c9e626263e14b00f94faa6d4558d3f4&")
        await interaction.response.edit_message(content=None, view=amazon2(bot=self.bot), embed=embed)

class amazon2(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="package 3")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1196001978623459358/amazon4_00000.png?ex=65b60aa4&is=65a395a4&hm=dd5fc6ce25fcf6a03164722f7778e959952c71e3fa9b2603da94093a13affaf3&")
        await interaction.response.edit_message(content=None, view=amazon3(bot=self.bot), embed=embed)

class amazon3(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="finish job")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        earnings = random.randint(2435, 2435)
        query = "UPDATE bank SET wallet = wallet + $1 WHERE user = $2"
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, earnings, interaction.user.id)
        embed = discord.Embed(description=f"You earned <a:coin:1192540229727440896> **{earnings}**", color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1196005062363840562/amazon5_00000.png?ex=65b60d83&is=65a39883&hm=42a5d3a2a32fc576c7045d47f457de5d0e58b9c69474fa425bf6516541545883&")
        await interaction.response.edit_message(content=None, view=None, embed=embed)
        rantip = ["1","2","3","4"]
        tipran = random.choice(rantip)
        tips = random.randint(100, 1000)
        if tipran == "3":
            query = "UPDATE bank SET wallet = wallet + $1 WHERE user = $2"
            async with self.bot.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(query, tips, interaction.user.id)
                    await interaction.followup.send(f"you have been tipped <a:coin:1192540229727440896> {tips}")

class makeburger(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="start burger")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1191096093002440835/burger_2_00000.png?ex=65a431ae&is=6591bcae&hm=97e934864962b7cfdc0c4c7c8df5906788131d99232c2d9e5e59ec1c6b338263&")
        await interaction.response.edit_message(content=None, view=makeburger1(bot=self.bot), embed=embed)

class makeburger1(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="add patty")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1191096146937004042/burger_3_00000.png?ex=65a431ba&is=6591bcba&hm=1851c9f38db8dab8c9305e42bfbf422a33d3ffef8260867b91b3c62af2574db3&")
        await interaction.response.edit_message(content=None, view=makeburger2(bot=self.bot), embed=embed)

class makeburger2(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="add cheese")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1191097335455957032/burger_4_00000.png?ex=65a432d6&is=6591bdd6&hm=7f2464c026d8fe81745206c2d81d3daa7e7ee8f038decdd2672ccae22480172c&")
        await interaction.response.edit_message(content=None, view=makeburger3(bot=self.bot), embed=embed)

class makeburger3(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="add lettuce")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1191097582148128788/burger_5_00000.png?ex=65a43311&is=6591be11&hm=d109ebfb3c2b6182ed65c7622d810ce613fd484e0b53f103c1c71d2c18681b7a&")
        await interaction.response.edit_message(content=None, view=makeburger4(bot=self.bot), embed=embed)

class makeburger4(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="add tomato")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1191097966992294010/burger_6_00000.png?ex=65a4336c&is=6591be6c&hm=7e57d6a0bc041e5eeb8a32188c9e5cbf1bdfe4814ed4fcb0a23969501a2234f0&")
        await interaction.response.edit_message(content=None, view=makeburger5(bot=self.bot), embed=embed)

class makeburger5(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="finish burger")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        earnings = random.randint(5354, 5354)
        query = "UPDATE bank SET wallet = wallet + $1 WHERE user = $2"
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, earnings, interaction.user.id)
        embed = discord.Embed(description=f"You earned <a:coin:1192540229727440896> **{earnings}**", color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1191098165089292369/burger_7_00000.png?ex=65a4339c&is=6591be9c&hm=8b801b0f04d0ae6d3029a5736b0b793da2ecb7c6692c596a1eb069271cbd0183&")
        await interaction.response.edit_message(content=None, view=None, embed=embed)
        rantip = ["1","2","3","4"]
        tipran = random.choice(rantip)
        tips = random.randint(100, 1000)
        if tipran == "3":
            query = "UPDATE bank SET wallet = wallet + $1 WHERE user = $2"
            async with self.bot.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(query, tips, interaction.user.id)
                    await interaction.followup.send(f"you have been tipped <a:coin:1192540229727440896> {tips}")

class happymeal(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="start happy meal")
    async def starthm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1192534600052912169/hm1_00000.png?ex=65a96d64&is=6596f864&hm=198a5a97ad8d851f2cecc4d6ee4a3b6d77cb4bed9b561e75c22a05db3074100d&")
        await interaction.response.edit_message(content=None, view=hm2(bot=self.bot), embed=embed)

class hm2(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="add drink")
    async def starthm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1192535857916285090/hm2_00000.png?ex=65a96e90&is=6596f990&hm=8ad9c8ab3c34d0ee4c8cb1f5db4e800dd7e1730af814adfc1b870e5f80b69fb2&")
        await interaction.response.edit_message(content=None, view=hm3(bot=self.bot), embed=embed)

class hm3(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="add fries")
    async def starthm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1192536391553392731/hm3_00000.png?ex=65a96f10&is=6596fa10&hm=c3e0180d3da86a7af1c02f64c58575280a3855e6665cbc126055ef2381c48c39&")
        await interaction.response.edit_message(content=None, view=hm4(bot=self.bot), embed=embed)

class hm4(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="add burger")
    async def starthm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1192536777429352568/hm4_00000.png?ex=65a96f6c&is=6596fa6c&hm=9b5e9a441a7e4c2f1d41d6565f9750f9f7902dd655f56b71302fb0b7312614cf&")
        await interaction.response.edit_message(content=None, view=hm5(bot=self.bot), embed=embed)

class hm5(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="add toy")
    async def starthm(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1192537364304765069/hm5_00000.png?ex=65a96ff7&is=6596faf7&hm=762768a398644f7094ff3ddd26959deadf4f5b0e5755f585ea513149abbf3fe0&")
        await interaction.response.edit_message(content=None, view=hm6(bot=self.bot), embed=embed)

class hm6(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="finish happy meal")
    async def burger(self, interaction: discord.Interaction, button: discord.ui.Button):
        earnings = random.randint(5354, 5354)
        query = "UPDATE bank SET wallet = wallet + $1 WHERE user = $2"
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, earnings, interaction.user.id)
        embed = discord.Embed(description=f"You earned <a:coin:1192540229727440896> **{earnings}**", color=0x2b2d31)
        await interaction.response.edit_message(content=None, view=None, embed=embed)
        rantip = ["1","2","3","4"]
        tipran = random.choice(rantip)
        tips = random.randint(100, 1000)
        if tipran == "3":
            query = "UPDATE bank SET wallet = wallet + $1 WHERE user = $2"
            async with self.bot.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(query, tips, interaction.user.id)
                    await interaction.followup.send(f"you have been tipped <a:coin:1192540229727440896> {tips}")

class pickupshit(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="pickup shit")
    async def starthm(self, interaction: discord.Interaction, button: discord.ui.Button):
        earnings = random.randint(1766, 1766)
        query = "UPDATE bank SET wallet = wallet + $1 WHERE user = $2"
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, earnings, interaction.user.id)
        embed=discord.Embed(title="Job Complete", description=f"You have earnt <a:coin:1192540229727440896> {earnings}", color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1193990123667345579/dogwalker_00000.png?ex=65aeb8f4&is=659c43f4&hm=e2631d448194102a748407bb624e2acf1cd1cc64bf6b701196dae59533ad61ee&")
        await interaction.response.edit_message(content=None, view=None, embed=embed)
        rantip = ["1","2","3","4"]
        tipran = random.choice(rantip)
        tips = random.randint(100, 1000)
        if tipran == "3":
            query = "UPDATE bank SET wallet = wallet + $1 WHERE user = $2"
            async with self.bot.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(query, tips, interaction.user.id)
                    await interaction.followup.send(f"you have been tipped <a:coin:1192540229727440896> {tips}")

class walkdog(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="walk the dog")
    async def starthm(self, interaction: discord.Interaction, button: discord.ui.Button):
        earnings = random.randint(1766, 1766)
        query = "UPDATE bank SET wallet = wallet + $1 WHERE user = $2"
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, earnings, interaction.user.id)
        rangif = gifs[str(random.randrange(len(gifs)))]
        embed=discord.Embed(title="Job Complete", description=f"You have earnt <a:coin:1192540229727440896> {earnings}", color=0x2b2d31)
        embed.set_image(url=rangif[1])
        await interaction.response.edit_message(content=None, view=None, embed=embed)
        rantip = ["1","2","3","4"]
        tipran = random.choice(rantip)
        tips = random.randint(100, 1000)
        if tipran == "3":
            query = "UPDATE bank SET wallet = wallet + $1 WHERE user = $2"
            async with self.bot.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(query, tips, interaction.user.id)
                    await interaction.followup.send(f"you have been tipped <a:coin:1192540229727440896> {tips}")

class Economy(commands.Cog):
    """Commands for the economy system"""
    def __init__(self, bot):
        self.bot = bot
        self.pool = None
        self.bot.loop.create_task(self.init_database())
        self.emoji = "<:tata:1121909389280944169>"

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
            await conn.execute("INSERT INTO bank (user, wallet, bank, maxbank) VALUES (?, 0, 100, 9999999999999999)", (user,))
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

    async def update_max_bank(self, user, maxbank):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE bank SET maxbank = $1 WHERE user = $2", maxbank, user)

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

    def _get_round_avatar(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        circle = Image.open('./assets/circle-mask.png').resize((35, 35)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((35, 35))
        return avatar_image, circle

    @commands.command(hidden=True)
    async def bankmax(self, ctx: commands.Context, member: discord.Member, amount: int):
        await self.update_max_bank(member.id, amount)
        await ctx.reply("all done!")

    @commands.command(aliases=["bal"], description="Check your bank and wallet balance", extras="alias +bal")
    @kanzen_only()
    async def balance(self, ctx, user: discord.Member = None, avatar_size: int = 140, image_size: int = 64) -> BytesIO:
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

    @commands.command(description="Steal coins from other members", extras="+rob @member")
    @commands.cooldown(1, 3600, commands.BucketType.user) 
    async def rob(self, ctx, member: discord.Member):
        titles = ["LOL you stole from someone... naughty naughty", "wow- are you that broke", "well we all need money... mind sharing 🥲"]
        title = random.choice(titles)
        amount = random.randint(0, 50000)
        if amount == 0:
            await ctx.send("No coins taken, as the random amount was 0.")
            return

        wallet_balance, bank_balance = await self.get_balance(member.id)
        bank_to_take = min(amount, bank_balance)
        new_bank_balance = await self.update_balance(member.id, 0, -bank_to_take)
        author_wallet_balance, author_bank_balance = await self.get_balance(ctx.author.id)
        new_author_bank_balance = await self.update_balance(ctx.author.id, 0, bank_to_take)
        embed = discord.Embed(title=title, description=f"You stole <:coin:1167639638123487232> {amount} from {member.display_name}", color=0x2b2d31)
        await ctx.send(embed=embed)

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining = round(error.retry_after)
            if remaining >= 60:
                mins = remaining // 60
                await ctx.send(f"Sorry, you're on a cooldown from using this command. Try again in {mins} minutes.")
            else:
                await ctx.send(f"Sorry, you're on a cooldown from using this command. Try again in {remaining} seconds.")


    @commands.command(aliases=['dep'], description="Deposite money into your bank", extras="+deposit (amount) : alias +dep")
    @kanzen_only()
    async def deposit(self, ctx, amount: int):
        if amount <= 0:
            return await ctx.reply("Amount must be greater than 0.")
        wallet_balance, bank_balance = await self.get_balance(ctx.author.id)
        if wallet_balance < amount:
            return await ctx.reply("You don't have enough coins in your wallet.")
        if bank_balance + amount > 1000000:
            return await ctx.reply("Your bank is full.")
        new_wallet_balance, new_bank_balance = await self.update_balance(ctx.author.id, -amount, amount)
        embed = discord.Embed(title="Deposited Coins <:wallet:1197271492182937670><:arrow10:1197269261211672760><:bank:1197269525138251876>", description=f"You deposited <a:coin:1192540229727440896> **{amount}**", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.add_field(name="<:wallet:1197271492182937670> Wallet Balance", value=f"<a:coin:1192540229727440896> **{new_wallet_balance}**", inline=False)
        embed.add_field(name="<:bank:1197269525138251876> Bank Balance", value=f"<a:coin:1192540229727440896> **{new_bank_balance}**", inline=False)
        await ctx.reply(embed=embed)

    @commands.command(description="Withdraw money from your bank", extras="+withdraw (amount)")
    @kanzen_only()
    async def withdraw(self, ctx, amount: int):
        if amount <= 0:
            return await ctx.send("Amount must be greater than 0.")
        wallet_balance, bank_balance = await self.get_balance(ctx.author.id)
        if bank_balance < amount:
            return await ctx.send("You don't have enough coins in your bank.")
        new_wallet_balance, new_bank_balance = await self.update_balance(ctx.author.id, amount, -amount)
        embed = discord.Embed(title="Withdrew Coins <:bank:1197269525138251876><:arrow10:1197269261211672760><:wallet:1197271492182937670>", description=f"You withdrew <a:coin:1192540229727440896> **{amount}**", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.add_field(name="<:wallet:1197271492182937670> Wallet Balance", value=f"<a:coin:1192540229727440896> **{new_wallet_balance}**", inline=False)
        embed.add_field(name="<:bank:1197269525138251876> Bank Balance", value=f"<a:coin:1192540229727440896> **{new_bank_balance}**", inline=False)
        await ctx.reply(embed=embed)

    @commands.command(description="Donate to ~~the poor~~ other members", extras="+donate @member (amount)")
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
        embed = discord.Embed(title="Donated Coins", description=f"You donated <a:coin:1192540229727440896> **{amount}** to **{user.display_name}**", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.add_field(name=f"<:wallet:1197271492182937670> {user.display_name}'s Wallet Balance", value=f"<a:coin:1192540229727440896> **{new_wallet_balance}**", inline=False)
        embed.add_field(name=f"<:bank:1197269525138251876> {user.display_name}'s Bank Balance", value=f"<a:coin:1192540229727440896> **{new_bank_balance}**", inline=False)
        await ctx.reply(embed=embed)

    @commands.command(description="Beg celebs for coins", extras="+beg")
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
        earnings = random.randint(100000, 10000000000)
        wallet_balance, _ = await self.update_balance(ctx.author.id, earnings, 0)
        embed=discord.Embed(title=celeb_name, description=celeb_line, color=0x2b2d31)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        embed.add_field(name="You received", value=f"<a:coin:1192540229727440896> {earnings}", inline=False)
        embed.add_field(name="Your new wallet balance", value=f"<a:coin:1192540229727440896> {wallet_balance}", inline=False)
        await ctx.reply(embed=embed)

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)
            await ctx.reply(f"You are on cooldown. Try again in {seconds} seconds.")

    @commands.command(description="Search locations for coins", extras="+search | a park")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @kanzen_only()
    async def search(self, ctx):
        search_responses = {
            'park': [
                ("You searched a park and found a squirrel that gave you some coins!", random.randint(1, 500)),
                ("You explored a park and stumbled upon a hidden treasure!", random.randint(1, 500)),
                ("You searched a park and found some loose change!", random.randint(1, 500))
            ],
            'alley': [
                ("You searched an alley and found a wallet with some coins inside!", random.randint(1, 1000)),
                ("You explored a dark alley and found some discarded coins!", random.randint(1, 1000)),
                ("You searched an alley and found nothing but trash.", 0)
            ],
            'dumpster': [
                ("You searched a dumpster and found a valuable item worth some coins!", random.randint(1, 100)),
                ("You rummaged through a dumpster and found some hidden coins!", random.randint(1, 100)),
                ("You searched a dumpster and got dirty for no reward.", 0)
            ],
            'forest': [
                ("You ventured into the forest and found a hidden treasure chest!", random.randint(1, 500)),
                ("You explored the forest and found a friendly forest creature!", random.randint(1, 500)),
                ("You searched the forest, but it seems there was nothing valuable there today.", 0)
            ],
            'cave': [
                ("You entered a dark cave and found a hidden stash of coins!", random.randint(1, 350)),
                ("You explored a mysterious cave and found a rare gemstone!", random.randint(1, 350)),
                ("You searched a cave but found nothing valuable.", 0)
            ]
        }
        random_choices = random.sample(list(search_responses.keys()), 3)
        where = discord.Embed(title="Where would you like to search?", description=f"**{' , '.join(random_choices)}**", color=0x2b2d31)
        where.set_thumbnail(url=ctx.author.display_avatar)
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
            searched.add_field(name="You found", value=f"<a:coin:1192540229727440896> **{earnings}**", inline=False)
            searched.add_field(name="Your new wallet balance", value=f"<a:coin:1192540229727440896> **{wallet_balance}**", inline=False)
            searched.set_thumbnail(url=ctx.author.display_avatar)
            await ctx.reply(embed=searched)
        else:
            await ctx.reply(response)

    @commands.command(description="commit a crime for coins", extras="+crime | shoplifting")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @kanzen_only()
    async def crime(self, ctx):
        crime_responses = {
            'shoplifting': [
                ("You successfully shoplifted and got away with it!", random.randint(100, 1000)),
                ("You were caught shoplifting and had to give back the stolen items.", 0)
            ],
            'trespassing': [
                ("You trespassed and found a valuable item!", random.randint(100, 1000)),
                ("You were caught trespassing and had to leave the premises.", 0)
            ],
            'drug dealing': [
                ("You successfully made a drug deal and earned some money.", random.randint(100, 1500)),
                ("Your drug deal went wrong and you lost your drugs.", 0)
            ],
            'fraud': [
                ("You successfully committed fraud and gained some money.", random.randint(100, 1000)),
                ("Your attempt at fraud failed and you didn't earn anything.", 0)
            ],
            'tax evasion': [
                ("You managed to evade taxes and saved some money.", random.randint(100, 10000)),
                ("Your attempt at tax evasion was discovered, and you had to pay fines.", 0)
            ],
            'arson': [
                ("You successfully set a fire and caused chaos.", random.randint(100, 2000)),
                ("Your attempt at arson failed, and no significant damage was done.", 0)
            ],
            'cyber bullying': [
                ("You successfully cyber bullied someone and felt a sense of power.", random.randint(100, 1000)),
                ("Your attempt at cyber bullying backfired, and you faced backlash.", 0)
            ],
            'hacking': [
                ("You successfully hacked into a system and gained valuable information.", random.randint(100, 3000)),
                ("Your hacking attempt failed, and you couldn't access the desired information.", 0)
            ],
            'identity theft': [
                ("You successfully stole someone's identity and used it to your advantage.", random.randint(100, 5000)),
                ("Your attempt at identity theft failed, and you couldn't gain any benefits.", 0)
            ]
        }
        random_choices = random.sample(list(crime_responses.keys()), 3)
        where = discord.Embed(title="What crime would you like to commit?", description=f"**{' , '.join(random_choices)}**", color=0x2b2d31)
        await ctx.reply(embed=where)
        def check(msg):
            return msg.author == ctx.author and msg.content.lower() in map(str.lower, random_choices)
        try:
            choice_msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            user_choice = choice_msg.content.lower()
        except asyncio.TimeoutError:
            return await ctx.reply("You took too long to choose a location. Try again later.")

        response, earnings = random.choice(crime_responses[user_choice])
        if earnings > 0:
            wallet_balance, _ = await self.update_balance(ctx.author.id, earnings, 0)
            searched = discord.Embed(title=f"You commited {user_choice}", description=response, color=0x2b2d31)
            searched.add_field(name="You got", value=f"<a:coin:1192540229727440896> **{earnings}**", inline=False)
            searched.add_field(name="Your new wallet balance", value=f"<a:coin:1192540229727440896> **{wallet_balance}**", inline=False)
            searched.set_thumbnail(url=ctx.author.display_avatar)
            await ctx.reply(embed=searched)
        else:
            await ctx.reply(response)

    @search.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)
            await ctx.reply(f"You are on cooldown. Try again in {seconds} seconds.")

    @commands.command(description="See the richest kanzen members", extras="+wealth")
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
                    name=f"** **",
                    value=f"**{idx}.** <@!{user.id}>\n<:wallet:1197271492182937670> Wallet: <a:coin:1192540229727440896> {wallet_balance}\n"
                        f"<:bank:1154163938234208367> Bank: <a:coin:1192540229727440896> {bank_balance}",
                    inline=False
                )
                leaderboard_embed.set_footer(text=f"Page {page}", icon_url=ctx.author.avatar)
                leaderboard_embed.set_thumbnail(url=ctx.guild.icon)
            else:
                leaderboard_embed.add_field(
                    name=f"** **",
                    value=f"**{idx}.** User not found\n<a:coin:1192540229727440896> Wallet: {wallet_balance} coins\n"
                        f"<:bank:YOUR_BANK_ICON_ID> Bank: {bank_balance} coins",
                    inline=False
                )

        message = await ctx.send(embed=leaderboard_embed)
        
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return (
                user == ctx.author
                and reaction.message.id == message.id
                and str(reaction.emoji) in ["⬅️", "➡️"]
            )

        while True:
            try:
                reaction, _ = await self.bot.wait_for("reaction_add", check=check, timeout=60.0)
            except TimeoutError:
                break

            if str(reaction.emoji) == "⬅️" and page > 1:
                page -= 1
            elif str(reaction.emoji) == "➡️" and end_idx < len(rows):
                page += 1

            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            leaderboard_embed.clear_fields()
            for idx, (user_id, wallet_balance, bank_balance) in enumerate(rows[start_idx:end_idx], start=start_idx + 1):
                user = self.bot.get_user(user_id)
                if user:
                    leaderboard_embed.add_field(
                        name=f"** **",
                        value=f"**{idx}.** <@!{user.id}>\n<:wallet:1197271492182937670> Wallet: <a:coin:1192540229727440896> {wallet_balance}\n"
                            f"<:bank:1154163938234208367> Bank: <a:coin:1192540229727440896> {bank_balance}",
                        inline=False
                    )
                    leaderboard_embed.set_footer(text=f"Page {page}", icon_url=ctx.author.avatar)
                    leaderboard_embed.set_thumbnail(url=ctx.guild.icon)
                else:
                    leaderboard_embed.add_field(
                        name=f"** **",
                        value=f"**{idx}.** User not found\n<a:coin:1192540229727440896> Wallet: {wallet_balance} coins\n"
                            f"<:bank:1154163938234208367> Bank: {bank_balance} coins",
                        inline=False
                    )

            await message.edit(embed=leaderboard_embed)
            await message.remove_reaction(str(reaction.emoji), ctx.author)

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

    @commands.command(description="See what is in the shop", extras="+shop")
    @kanzen_only()
    async def shop(self, ctx):
        await ctx.reply("The shop is closed right now for updates. Sorryy LOOOOOOOOOOOOOOOOOOOOOOOOL")

    @commands.command(description="Buy items from the shop", extras="+buy cookie (amount)")
    @kanzen_only()
    async def buy(self, ctx, item: str, quantity: int = 1):
        shop_items = {
            "Cookie": 10,
            "Soda": 15,
            "Pizza": 25,
            "Laptop": 500,
            "Fishing_rod": 250,
            "Gaming PC": 5000,
            "Car": 1000000,
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

        embed = discord.Embed(title="Item Purchased", description=f"You have successfully purchased **{quantity}** **{item}(s)** for <a:coin:1192540229727440896> **{price}**", color=0x2b2d31)
        embed.add_field(name="Your new wallet balance", value=f"<a:coin:1192540229727440896> **{wallet_balance}**", inline=False)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await ctx.send(embed=embed)

    @commands.command(description="See what items you have", extras="+inventory")
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
        inventory_embed.set_thumbnail(url=ctx.author.display_avatar)
        await ctx.send(embed=inventory_embed)

    @commands.command(description="Sell your unwanted items", extras="+sell cookie (amount)")
    @kanzen_only()
    async def sell(self, ctx, item: str, quantity: int = 1):
        shop_items = {
            "Cookie": 10,
            "Soda": 15,
            "Pizza": 25,
            "Laptop": 500,
            "Gaming PC": 5000,
            "Car": 100000,
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

        embed = discord.Embed(title="Item Sold", description=f"You have successfully sold  **{quantity}** **{item}(s)** for <a:coin:1192540229727440896> **{price}**", color=0x2b2d31)
        embed.add_field(name="Your new wallet balance", value=f"<a:coin:1192540229727440896> **{wallet_balance}**", inline=False)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await ctx.send(embed=embed)

    async def update_job(self, user, job):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE bank SET job = $1 WHERE user = $2", job, user)

    async def get_job_role(self, user):
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                query = "SELECT job FROM bank WHERE user = ? LIMIT 1"
                result = await conn.execute(query, user)
                row = await result.fetchone()
                if row:
                    return row['job']
                return None

    @commands.command(description="See what jobs are avaliable", extras="+jobs")
    @kanzen_only()
    async def jobs(self, ctx):
        role = await self.get_job_role(ctx.author.id)
        if role == "mcdonalds":
            mcdonalds = "✅"
        else:
            mcdonalds = ""
        if role == "twitch":
            twitch = "✅"
        else:
            twitch = ""
        if role == "amazon":
            amazon = "✅"
        else:
            amazon = ""
        if role == "dog":
            dog = "✅"
        else:
            dog = ""
        if role == "mod":
            mod = "✅"
        else:
            mod = ""
        embed = discord.Embed(title="Kanzen Jobs", description=f"If a job is marked with ✅, that is the job you have selected.\n\n<:CF12:1188186414387568691> [**Mcdonalds worker**](https://instagram.com/kanzengrp) {mcdonalds}\n<:Empty:1188186122350759996> Flip Burgers and make fries\n<:Empty:1188186122350759996> Salary **5,354** per shift\n<:Empty:1188186122350759996> `+apply mcdonalds`\n\n<:CF12:1188186414387568691> [**Twitch Streamer**](https://instagram.com/kanzengrp) {twitch}\n<:Empty:1188186122350759996> Play video games on stream\n<:Empty:1188186122350759996> Salary **7,645** per shift\n<:Empty:1188186122350759996> `COMING SOON`\n\n<:CF12:1188186414387568691> [**Amazon Delivery Driver**](https://instagram.com/kanzengrp) {amazon}\n<:Empty:1188186122350759996> Deliver packages to customers\n<:Empty:1188186122350759996> Salary **2,435** per shift\n<:Empty:1188186122350759996> `+apply amazon`\n\n<:CF12:1188186414387568691> [**Dog Walker**](https://instagram.com/kanzengrp) {dog}\n<:Empty:1188186122350759996> Walk dogs for people in Kanzen's town\n<:Empty:1188186122350759996> Salary **1,766** per shift\n<:Empty:1188186122350759996> `+apply dogwalker`\n\n<:CF12:1188186414387568691> [**Discord Moderator**](https://instagram.com/kanzengrp) {mod}\n<:Empty:1188186122350759996> Deal with shitty people and Discord kittens\n<:Empty:1188186122350759996> Salary **6,454** per shift\n<:Empty:1188186122350759996> `COMING SOON`", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.author.avatar)
        embed.set_footer(text="• Do +apply (job title) to apply for a job", icon_url=ctx.guild.icon)
        await ctx.reply(embed=embed)

    @commands.group(invoke_without_command=True, description="Apply for one of our jobs", extras="+apply (job name)")
    @kanzen_only()
    async def apply(self, ctx: commands.Context):
        await ctx.reply("Please do the command again and say what job role you'd like to apply for\nExample: `+apply`")

    @apply.command(hidden=True)
    @kanzen_only()
    async def amazon(self, ctx):
        await self.update_job(ctx.author.id, "amazon")
        await ctx.reply("Thank you for applying for the position `amazon`\nTo do a shift please do `+work `")

    @apply.command(hidden=True)
    @kanzen_only()
    async def mcdonalds(self, ctx):
        await self.update_job(ctx.author.id, "mcdonalds")
        await ctx.reply("Thank you for applying for the position `mcdonalds`\nTo do a shift please do `+work`")

    @apply.command(hidden=True)
    @kanzen_only()
    async def dogwalker(self, ctx):
        await self.update_job(ctx.author.id, "dogwalker")
        await ctx.reply("Thank you for applying for the position `dogwalker`\nTo do a shift please do `+work`")

    @commands.command(description="Work a shift", extras="+work (twitch/dogwalker/mcdonalds/moderator)")
    @kanzen_only()
    @commands.cooldown(1, 3 * 60 * 60, commands.BucketType.user)
    async def work(self, ctx):
        role = await self.get_job_role(ctx.author.id)
        if role == "twitch":
            await ctx.reply("twitch lol")
        if role == "mcdonalds":
            embed1 = discord.Embed(title="Make a burger", description="Use the buttons below to make a burger!", color=0x2b2d31)
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1191094770244780032/burger_1_00000.png?ex=65a43072&is=6591bb72&hm=f04d2d3b5e9bdd9079fe0256aec99423560227997e8c1eda58be79dccd116509&")
            embed2 = discord.Embed(title="Make a Happy Meal", description="Use the buttons below to make a Happy Meal", color=0x2b2d31)
            embed2.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1191094770244780032/burger_1_00000.png?ex=65a43072&is=6591bb72&hm=f04d2d3b5e9bdd9079fe0256aec99423560227997e8c1eda58be79dccd116509&")
            embedsran = [embed1, embed2]
            ranembeds = random.choice(embedsran)
            if ranembeds == embed1:
                buttons = makeburger(bot=self.bot)
            elif ranembeds == embed2:
                buttons = happymeal(bot=self.bot)
            view = buttons
            await ctx.reply(embed=ranembeds, view=view)
        if role == "dogwalker":
            embed1 = discord.Embed(title="Pick up the dog shit", description="The dog took a massive shit on the side on the road... pick it up", color=0x2b2d31)
            embed1.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1193989944398577855/dogwalker_00000.png?ex=65aeb8ca&is=659c43ca&hm=7154bb7ac9dc38f868474deb66f3ed2f5abf5bee99e2369fc9a22a02e720237e&")
            embed2 = discord.Embed(title="Walk the dog", description="The old lady needs her scruffy dog walked, click the button to walk", color=0x2b2d31)
            rangif = gifs[str(random.randrange(len(gifs)))]
            embed2.set_image(url=rangif[0])
            embedsran = [embed1, embed2]
            ranembeds = random.choice(embedsran)
            if ranembeds == embed1:
                buttons = pickupshit(bot=self.bot)
            elif ranembeds == embed2:
                buttons = walkdog(bot=self.bot)
            view = buttons
            await ctx.reply(embed=ranembeds, view=view)
        if role == "amazon":
            embed = discord.Embed(title="Drop of customer's packages", color=0x2b2d31)
            embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1196001013497344090/amazon1_00000.png?ex=65b609be&is=65a394be&hm=2d3ab0b0aa00e215d5357b6abedc15812f1208c439deca510d66d7ae7c329c37&")
            view = amazon(bot=self.bot)
            await ctx.reply(embed=embed, view=view)

    @work.error
    async def work_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            if error.retry_after > 3600:
                hours = int(error.retry_after // 3600)
                minutes = int((error.retry_after % 3600) // 60)
                await ctx.reply(f"You need to wait {hours} hours and {minutes} minutes before working again!")
            elif error.retry_after > 60:
                minutes = int(error.retry_after // 60)
                await ctx.reply(f"You need to wait {minutes} minutes before working again!")
            else:
                await ctx.reply(f"You need to wait {int(error.retry_after)} seconds before working again!")

    @commands.command(description="gamble your life savings", extras="+gamble (amount)")
    @kanzen_only()
    @commands.cooldown(1, 24 * 60 * 60, commands.BucketType.user)
    async def gamble(self, ctx, amount: str):
        user = ctx.author.id
        wallet_balance, _ = await self.get_balance(ctx.author.id)

        try:
            amount = int(amount)
        except ValueError:
            return await ctx.send("Please enter a valid number for the amount.")

        if wallet_balance < amount:
            return await ctx.send("You don't have enough coins to bet this much")

        doubled = "https://cdn.discordapp.com/attachments/1184208577120960632/1197220330675126322/double.gif?ex=65ba7952&is=65a80452&hm=c8ff676af6ef8368a3a8e540195f9efc6c0e264ec4f2ecfdfa8eeb95681fe7d4&"
        tripled = "https://cdn.discordapp.com/attachments/1184208577120960632/1197220403156885504/triple.gif?ex=65ba7963&is=65a80463&hm=40389da7e1bfa5239b80a441f483be2f4f44e718fd095be0b55d1d0654eeb6ba&"
        gave = "https://cdn.discordapp.com/attachments/1184208577120960632/1197488790252552212/donate.gif?ex=65bb7357&is=65a8fe57&hm=a50ffb7c923c8263582e87f61982979a1d12ef7dde745b61510f6a432871dbf6&"
        lost = "https://cdn.discordapp.com/attachments/1184208577120960632/1197488816412434482/loose.gif?ex=65bb735e&is=65a8fe5e&hm=098beb449ad5f5fe13fbfa396b2d1a1245f456607f69f02559c7934ef42a886c&"
        nothing = "https://cdn.discordapp.com/attachments/1184208577120960632/1197488820086636544/nothing.gif?ex=65bb735e&is=65a8fe5e&hm=7b913ed495bc4b189c7bb2804196cc517c761f3a4255e2fb8cb6fe699e3fb15f&"
        ranwheel = ['triple', 'double','nothing', 'loose']
        wheelran = random.choice(ranwheel)
        newamount = amount

        if wheelran == 'double':
            newamount *= 2
            title = 'YOUR MONEY HAS BEEN DOUBLED!'
            description = f"Your money has been **DOUBLED**! <a:coin:1192540229727440896> {newamount} has been added to your wallet"
            await self.update_balance(user, newamount)
            wheel = doubled
            view=None
            color = 0x5BD437
            editedwheel = "https://cdn.discordapp.com/attachments/1184208577120960632/1197220425114075206/double_image_00000.png?ex=65ba7968&is=65a80468&hm=801eb50b3387d076245c7b513375e34e316d4fe4ba89239f4600a8ef21b7db3d&"
        elif wheelran == 'triple':
            newamount *= 3
            title = 'YOUR MONEY HAS BEEN TRIPLED!!!'
            await self.update_balance(user, newamount)
            color = 0xd4af37
            description = f"Your money has been **TRIPLED**! <a:coin:1192540229727440896> {newamount} has been added to your wallet"
            wheel = tripled
            view=None
            editedwheel = "https://cdn.discordapp.com/attachments/1184208577120960632/1197220443891978250/triple_image_00000.png?ex=65ba796d&is=65a8046d&hm=eec1def1122ae9fcabd817fb5368d165ea928953c078d71c7d20496651e0c3e1&"
        elif wheelran == 'give':
            wheel = gave
            title = 'Someone else got rich'
            color = 0xD11717
            view=None
            description = 'You had to give your money to someone else'
            editedwheel = "https://cdn.discordapp.com/attachments/1184208577120960632/1197489245330350131/donate_image_00000.png?ex=65bb73c4&is=65a8fec4&hm=fd7b1080beecc7a47f9f04b2897fd11da2ac164fdedaff6a6f839ac082c8271d&"
        elif wheelran == 'loose':
            wheel = lost
            title = 'YOU LOST'
            lostamount = amount
            await self.update_balance(user, -lostamount)
            description = 'You lost all your money... rip'
            color = 0xD11717
            view=None
            editedwheel = "https://cdn.discordapp.com/attachments/1184208577120960632/1197489178875809872/loose_image_00000.png?ex=65bb73b4&is=65a8feb4&hm=cd100a25d999ea78a0d650188ec67762e52fba10e26b4084992c970dae2addcb&"
        elif wheelran == 'nothing':
            wheel = nothing
            title = 'Nothing happened'
            view = tryagain(bot=self.bot)
            view.set_amount(amount)
            description = 'You can keep your bet but you win nothing else'
            color = 0xD11717
            editedwheel = "https://cdn.discordapp.com/attachments/1184208577120960632/1197489107526483978/nothing_image_00000.png?ex=65bb73a3&is=65a8fea3&hm=efba6d494aa38301acba36926d41cdccc34176c88ac971a66055ce7dc7248338&"

        embed = discord.Embed(title=f"You gambled <a:coin:1192540229727440896> {amount}", color=0x2b2d31)
        embed.set_image(url=wheel)
        embed.set_footer(text="Goodluck!", icon_url=ctx.author.display_avatar)
        message = await ctx.reply(embed=embed)
        await asyncio.sleep(2.4)
        edited_embed = discord.Embed(title=title, description=description, color=color)
        edited_embed.set_image(url=editedwheel)
        edited_embed.set_footer(text="Thank you for playing!", icon_url=ctx.author.display_avatar)
        await message.edit(embed=edited_embed, view=view)

    @gamble.error
    async def gamble_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            if error.retry_after > 3600:
                hours = int(error.retry_after // 3600)
                minutes = int((error.retry_after % 3600) // 60)
                await ctx.reply(f"You need to wait {hours} hours and {minutes} minutes before working again!")
            elif error.retry_after > 60:
                minutes = int(error.retry_after // 60)
                await ctx.reply(f"You need to wait {minutes} minutes before working again!")
            else:
                await ctx.reply(f"You need to wait {int(error.retry_after)} seconds before working again!")

async def setup(bot):
    await bot.add_cog(Economy(bot))