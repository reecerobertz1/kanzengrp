import asyncio
from io import BytesIO
import random
import aiohttp
import discord
from discord.ext import commands
from discord import ui
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

class jobpick(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=30.0)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="mcdonalds")
    async def mcdonalds(self, interaction: discord.Interaction, button: discord.ui.Button):
        job = "mcdonalds"
        query = "UPDATE bank SET job = $1 WHERE user = $2"
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, job, interaction.user.id)
        await interaction.response.send_message("Congrats on your new job! you now work at mcdonalds\nTo work do `+work`", ephemeral=True)

    @discord.ui.button(label="amazon driver")
    async def amazon(self, interaction: discord.Interaction, button: discord.ui.Button):
        job = "amazon"
        query = "UPDATE bank SET job = $1 WHERE user = $2"
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, job, interaction.user.id)
        await interaction.response.send_message("Congrats on your new job! you now work at amazon\nTo work do `+work`", ephemeral=True)

    @discord.ui.button(label="dog walker")
    async def doggy(self, interaction: discord.Interaction, button: discord.ui.Button):
        job = "dogwalker"
        query = "UPDATE bank SET job = $1 WHERE user = $2"
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, job, interaction.user.id)
        await interaction.response.send_message("Congrats on your new job! you now work as a dog walker\nTo work do `+work`", ephemeral=True)

    @discord.ui.button(label="nurse", disabled=True)
    async def nurse(self, interaction: discord.Interaction, button: discord.ui.Button):
        job = "nurse"
        query = "UPDATE bank SET job = $1 WHERE user = $2"
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, job, interaction.user.id)
        await interaction.response.send_message("Congrats on your new job! you now work as a dog walker\nTo work do `+work`", ephemeral=True)

    @discord.ui.button(label="twitch streamer", disabled=True)
    async def streamer(self, interaction: discord.Interaction, button: discord.ui.Button):
        job = "twitch"
        query = "UPDATE bank SET job = $1 WHERE user = $2"
        async with self.bot.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, job, interaction.user.id)
        await interaction.response.send_message("Congrats on your new job! you now work as a dog walker\nTo work do `+work`", ephemeral=True)

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
                child.style = discord.ButtonStyle.red
        self.stop()

class toolbuy(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=30.0)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="hunting rifle", emoji="<:rifle:1199405381630308572>", style=discord.ButtonStyle.blurple)
    async def huntingrife(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:rifle:1199405381630308572>Hunting rifle"
        quantity = 1

        price = 100000 * quantity
        wallet_balance, _ = await self.get_balance(interaction.user.id)
        if wallet_balance < price:
            return await interaction.response.send_message("You don't have enough coins to buy this item.", ephemeral=True)

        new_wallet_balance, _ = await self.update_balance(interaction.user.id, -price, 0)
        await self.buy_item(interaction.user.id, item, quantity)

        await interaction.response.send_message(
            f"Successfully bought <:rifle:1199405381630308572> hunting rifle for <a:coin:1192540229727440896> **100,000**",
            ephemeral=True
        )

    @discord.ui.button(label="knife", emoji="<:knife:1199405378216144947>", style=discord.ButtonStyle.blurple)
    async def knife(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:knife:1199405378216144947>knife"
        quantity = 1

        price = 115000 * quantity
        wallet_balance, _ = await self.get_balance(interaction.user.id)
        if wallet_balance < price:
            return await interaction.response.send_message("You don't have enough coins to buy this item.", ephemeral=True)

        new_wallet_balance, _ = await self.update_balance(interaction.user.id, -price, 0)
        await self.buy_item(interaction.user.id, item, quantity)

        await interaction.response.send_message(
            f"Successfully bought <:knife:1199405378216144947> knife for <a:coin:1192540229727440896> **115,000**",
            ephemeral=True
        )

    @discord.ui.button(label="fishing rod", emoji="<:frod:1199405376320323664>", style=discord.ButtonStyle.blurple)
    async def frod(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:frod:1199405376320323664>fishing rod"
        quantity = 1

        price = 125000 * quantity
        wallet_balance, _ = await self.get_balance(interaction.user.id)
        if wallet_balance < price:
            return await interaction.response.send_message("You don't have enough coins to buy this item.", ephemeral=True)

        new_wallet_balance, _ = await self.update_balance(interaction.user.id, -price, 0)
        await self.buy_item(interaction.user.id, item, quantity)

        await interaction.response.send_message(
            f"Successfully bought <:frod:1199405376320323664> fishing rod for <a:coin:1192540229727440896> **125,000**",
            ephemeral=True
        )

    @discord.ui.button(label="pickaxe", emoji="<:paxe:1199405372524478664>", style=discord.ButtonStyle.blurple)
    async def pickaxe(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:paxe:1199405372524478664>pickaxe"
        quantity = 1

        price = 150000 * quantity
        wallet_balance, _ = await self.get_balance(interaction.user.id)
        if wallet_balance < price:
            return await interaction.response.send_message("You don't have enough coins to buy this item.", ephemeral=True)

        new_wallet_balance, _ = await self.update_balance(interaction.user.id, -price, 0)
        await self.buy_item(interaction.user.id, item, quantity)

        await interaction.response.send_message(
            f"Successfully bought <:paxe:1199405372524478664> pickaxe for <a:coin:1192540229727440896> **150,000**",
            ephemeral=True
        )

    async def buy_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] + quantity
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO inventory (user, item, quantity) VALUES (?, ?, ?)", (user, item, quantity))
                    await conn.commit()

    async def buy_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] + quantity
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO inventory (user, item, quantity) VALUES (?, ?, ?)", (user, item, quantity))
                    await conn.commit()

    async def create_account(self, user):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("INSERT INTO bank (user, wallet, bank, maxbank) VALUES (?, 0, 100, 9999999999999999)", (user,))
            await conn.commit()

    async def get_balance(self, user):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT wallet, bank FROM bank WHERE user = ?", (user,))
                row = await cursor.fetchone()
                if row is None:
                    await self.create_account(user)
                    return 0, 0
                return row[0], row[1]

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

class toolsell(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=30.0)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Hunting Rifle", emoji="<:rifle:1199405381630308572>", style=discord.ButtonStyle.blurple)
    async def rifle(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:rifle:1199405381630308572>Huntingrifle"
        quantity = 1

        price = 100000 * quantity
        sell_price = int(price * 0.7)

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, sell_price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:rifle:1199405381630308572> hunting rifle for <a:coin:1192540229727440896> **{sell_price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="Knife", emoji="<:knife:1199405378216144947>", style=discord.ButtonStyle.blurple)
    async def knife(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:knife:1199405378216144947>knife"
        quantity = 1

        price = 115000 * quantity
        sell_price = int(price * 0.7)

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, sell_price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:knife:1199405378216144947> knife for <a:coin:1192540229727440896> **{sell_price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="Fishing rod", emoji="<:frod:1199405376320323664>", style=discord.ButtonStyle.blurple)
    async def frod(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:frod:1199405376320323664>fishing rod"
        quantity = 1

        price = 125000 * quantity
        sell_price = int(price * 0.7)

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, sell_price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:frod:1199405376320323664> fishing rod for <a:coin:1192540229727440896> **{sell_price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="Pickaxe", emoji="<:paxe:1199405372524478664>", style=discord.ButtonStyle.blurple)
    async def paxe(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:paxe:1199405372524478664>pickaxe"
        quantity = 1

        price = 150000 * quantity
        sell_price = int(price * 0.7)

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, sell_price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:paxe:1199405372524478664> pickaxe for <a:coin:1192540229727440896> **{sell_price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    async def buy_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] + quantity
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO inventory (user, item, quantity) VALUES (?, ?, ?)", (user, item, quantity))
                    await conn.commit()

    async def sell_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] - quantity
                    if new_quantity <= 0:
                        await cursor.execute("DELETE FROM inventory WHERE user = ? AND item = ?", (user, item))
                    else:
                        await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()

    async def check_inventory(self, user_id, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user_id, item))
                row = await cursor.fetchone()

        return row and row[0] >= quantity

    async def create_account(self, user):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("INSERT INTO bank (user, wallet, bank, maxbank) VALUES (?, 0, 100, 9999999999999999)", (user,))
            await conn.commit()

    async def get_balance(self, user):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT wallet, bank FROM bank WHERE user = ?", (user,))
                row = await cursor.fetchone()
                if row is None:
                    await self.create_account(user)
                    return 0, 0
                return row[0], row[1]

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

class animalsell(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=30.0)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Turkey", emoji="🦃", style=discord.ButtonStyle.red)
    async def turkey(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🦃turkey"
        quantity = 1

        price = 50000 * quantity
        sell_price = int(price * 0.7)

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, sell_price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🦃 turkey for <a:coin:1192540229727440896> **{sell_price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="rabbit", emoji="🐇", style=discord.ButtonStyle.red)
    async def rabbit(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🐇rabbit"
        quantity = 1

        price = 35000 * quantity
        sell_price = int(price * 0.7)

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, sell_price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🐇 rabbit for <a:coin:1192540229727440896> **{sell_price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="moose", emoji="🫎", style=discord.ButtonStyle.red)
    async def moose(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🫎moose"
        quantity = 1

        price = 100000 * quantity
        sell_price = int(price * 0.7)

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, sell_price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🫎 moose for <a:coin:1192540229727440896> **{sell_price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="deer", emoji="🦌", style=discord.ButtonStyle.red)
    async def deer(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🦌deer"
        quantity = 1

        price = 100000 * quantity
        sell_price = int(price * 0.7)

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, sell_price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🦌 deer for <a:coin:1192540229727440896> **{sell_price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    async def buy_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] + quantity
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO inventory (user, item, quantity) VALUES (?, ?, ?)", (user, item, quantity))
                    await conn.commit()

    async def sell_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] - quantity
                    if new_quantity <= 0:
                        await cursor.execute("DELETE FROM inventory WHERE user = ? AND item = ?", (user, item))
                    else:
                        await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()

    async def check_inventory(self, user_id, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user_id, item))
                row = await cursor.fetchone()

        return row and row[0] >= quantity

    async def create_account(self, user):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("INSERT INTO bank (user, wallet, bank, maxbank) VALUES (?, 0, 100, 9999999999999999)", (user,))
            await conn.commit()

    async def get_balance(self, user):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT wallet, bank FROM bank WHERE user = ?", (user,))
                row = await cursor.fetchone()
                if row is None:
                    await self.create_account(user)
                    return 0, 0
                return row[0], row[1]

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

class fishsell(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=30.0)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Regular Fish", emoji="🐟", style=discord.ButtonStyle.blurple)
    async def regular(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🐟regular fish"
        quantity = 1

        price = 3000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🐟 regular fish for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="shrimp", emoji="🦐", style=discord.ButtonStyle.blurple)
    async def shrimp(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🦐shrimp"
        quantity = 1

        price = 3150 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🦐 shrimp for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="crab", emoji="🦀", style=discord.ButtonStyle.blurple)
    async def crab(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🦀crab"
        quantity = 1

        price = 5000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🦀 crab for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="lobster", emoji="🦞", style=discord.ButtonStyle.blurple)
    async def lobster(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🦞lobster"
        quantity = 1

        price = 5250 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🦞 lobster for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="tropical fish", emoji="🐠", style=discord.ButtonStyle.blurple)
    async def tfish(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🐠tropical fish"
        quantity = 1

        price = 7000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🐠 tropical fish for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="pufferfish", emoji="🐡", style=discord.ButtonStyle.blurple)
    async def pfish(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🐡pufferfish"
        quantity = 1

        price = 7500 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🐡 pufferfish for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="squid", emoji="🦑", style=discord.ButtonStyle.blurple)
    async def squid(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🦑squid"
        quantity = 1

        price = 10000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🦑 squid for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="shark", emoji="🦈", style=discord.ButtonStyle.blurple)
    async def shark(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "🦈shark"
        quantity = 1

        price = 25000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold 🦈 shark for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    async def buy_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] + quantity
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO inventory (user, item, quantity) VALUES (?, ?, ?)", (user, item, quantity))
                    await conn.commit()

    async def sell_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] - quantity
                    if new_quantity <= 0:
                        await cursor.execute("DELETE FROM inventory WHERE user = ? AND item = ?", (user, item))
                    else:
                        await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()

    async def check_inventory(self, user_id, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user_id, item))
                row = await cursor.fetchone()

        return row and row[0] >= quantity

    async def create_account(self, user):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("INSERT INTO bank (user, wallet, bank, maxbank) VALUES (?, 0, 100, 9999999999999999)", (user,))
            await conn.commit()

    async def get_balance(self, user):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT wallet, bank FROM bank WHERE user = ?", (user,))
                row = await cursor.fetchone()
                if row is None:
                    await self.create_account(user)
                    return 0, 0
                return row[0], row[1]

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

class oresell(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=30.0)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="coal", emoji="<:coal16581529:1199747331143249940>", style=discord.ButtonStyle.green)
    async def coal(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:coal16581529:1199747331143249940>coal"
        quantity = 1

        price = 5000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:coal16581529:1199747331143249940> coal for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="quartz", emoji="<:Nether_Quartz_JE2_BE2:1199747191653269595>", style=discord.ButtonStyle.green)
    async def quartz(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:Nether_Quartz_JE2_BE2:1199747191653269595>quartz"
        quantity = 1

        price = 13000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:Nether_Quartz_JE2_BE2:1199747191653269595> quartz for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="copper", emoji="<:Raw_Copper_JE3_BE2:1199747183759597570>", style=discord.ButtonStyle.green)
    async def copper(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:Raw_Copper_JE3_BE2:1199747183759597570>copper"
        quantity = 1

        price = 25000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:Raw_Copper_JE3_BE2:1199747183759597570> copper for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="redstone", emoji="<:Redstone_Dust_JE2_BE2:1199747189203808366>", style=discord.ButtonStyle.green)
    async def redstone(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:Redstone_Dust_JE2_BE2:1199747189203808366>redstone"
        quantity = 1

        price = 50000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:Redstone_Dust_JE2_BE2:1199747189203808366> redstone for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="iron", emoji="<:Iron_Ingot_JE3_BE2:1199747187777749062>", style=discord.ButtonStyle.green)
    async def iron(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:Iron_Ingot_JE3_BE2:1199747187777749062>iron"
        quantity = 1

        price = 75000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:Iron_Ingot_JE3_BE2:1199747187777749062> iron for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="gold", emoji="<:Gold_Ingot_JE4_BE2:1199747185529598012>", style=discord.ButtonStyle.green)
    async def gold(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:Gold_Ingot_JE4_BE2:1199747185529598012>gold"
        quantity = 1

        price = 100000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:Gold_Ingot_JE4_BE2:1199747185529598012> gold for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="diamond", emoji="<:Diamond_JE3_BE3:1199747180848758824>", style=discord.ButtonStyle.green)
    async def diamond(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:Diamond_JE3_BE3:1199747180848758824>diamond"
        quantity = 1

        price = 200000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:Diamond_JE3_BE3:1199747180848758824> diamond for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    @discord.ui.button(label="emerald", emoji="<:Emerald_JE3_BE3:1199747182195130458>", style=discord.ButtonStyle.green)
    async def emerald(self, interaction: discord.Interaction, button: discord.ui.Button):
        item = "<:Emerald_JE3_BE3:1199747182195130458>emerald"
        quantity = 1

        price = 250000 * quantity

        wallet_balance, _ = await self.get_balance(interaction.user.id)
        new_wallet_balance, _ = await self.update_balance(interaction.user.id, price, 0)

        if await self.check_inventory(interaction.user.id, item, quantity):
            await self.sell_item(interaction.user.id, item, quantity)
            await interaction.response.send_message(
                f"Successfully sold <:Emerald_JE3_BE3:1199747182195130458> emerald for <a:coin:1192540229727440896> **{price}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"You don't have enough of this item to sell.",
                ephemeral=True
            )

    async def buy_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] + quantity
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO inventory (user, item, quantity) VALUES (?, ?, ?)", (user, item, quantity))
                    await conn.commit()

    async def sell_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] - quantity
                    if new_quantity <= 0:
                        await cursor.execute("DELETE FROM inventory WHERE user = ? AND item = ?", (user, item))
                    else:
                        await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()

    async def check_inventory(self, user_id, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user_id, item))
                row = await cursor.fetchone()

        return row and row[0] >= quantity

    async def create_account(self, user):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("INSERT INTO bank (user, wallet, bank, maxbank) VALUES (?, 0, 100, 9999999999999999)", (user,))
            await conn.commit()

    async def get_balance(self, user):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT wallet, bank FROM bank WHERE user = ?", (user,))
                row = await cursor.fetchone()
                if row is None:
                    await self.create_account(user)
                    return 0, 0
                return row[0], row[1]

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

class balbuttons(discord.ui.View):
    def __init__(self, pool):
        super().__init__(timeout=30)
        self.pool = pool
        self.value = None

    @discord.ui.button(label="withdraw")
    async def withdraw(self, interaction: discord.Interaction, button: discord.ui.Button):
        withdraw_modal = withdraw()
        await withdraw_modal.init_database()
        await interaction.response.send_modal(withdraw_modal)

    @discord.ui.button(label="deposit")
    async def deposit(self, interaction: discord.Interaction, button: discord.ui.Button):
        deposit_modal = deposit()
        await deposit_modal.init_database()
        await interaction.response.send_modal(deposit_modal)

    @discord.ui.button(label="help", style=discord.ButtonStyle.blurple)
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="", description="<:CF12:1188186414387568691> **balance:**\n<:Empty:1188186122350759996> This command shows you how many coins you have in your\n<:Empty:1188186122350759996> bank and allows you to withdraw inti or deposit coins out of\n<:Empty:1188186122350759996> your bank.\n\n<:CF12:1188186414387568691> **withdraw and deposit:**\n<:Empty:1188186122350759996> To withdraw coins, click the `withdraw` button and enter the\n<:Empty:1188186122350759996> the amount of coins you want to take out of your bank.\n<:Empty:1188186122350759996> To deposit coins, click the `deposit` button and enter the\n<:Empty:1188186122350759996> the amount of coins you want to put into your bank.", color=0x2b2d31)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
        embed.set_thumbnail(url=interaction.user.display_avatar)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
                child.style = discord.ButtonStyle.red
        self.stop()

class withdraw(ui.Modal, title='Withdraw Coins'):
    amount = ui.TextInput(label='How much would you like to withdraw?', placeholder="Enter amount here....", style=discord.TextStyle.short)

    async def init_database(self):
        self.pool = await asqlite.create_pool('databases/levels.db')
        async with self.pool.acquire() as conn:
            await conn.execute('''CREATE TABLE IF NOT EXISTS bank (
                user INTEGER PRIMARY KEY,
                wallet INTEGER,
                bank INTEGER,
                maxbank INTEGER
            )''')

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user.id
        await interaction.response.defer()
        amount = int(self.amount.value)

        if not hasattr(self, 'pool'):
            await self.init_database()

        async with self.pool.acquire() as conn:
            await conn.execute("""UPDATE bank SET wallet = wallet + ?, bank = bank - ? WHERE user = ?""", (amount, amount, user))
            await conn.commit()

        await interaction.followup.send(f"You have withdrawn <a:coin:1192540229727440896> **{amount}** from your bank", ephemeral=True)

class deposit(ui.Modal, title='Deposit Coins'):
    amount = ui.TextInput(label='How much would you like to deposit?', placeholder="Enter amount here....", style=discord.TextStyle.short)

    async def init_database(self):
        self.pool = await asqlite.create_pool('databases/levels.db')
        async with self.pool.acquire() as conn:
            await conn.execute('''CREATE TABLE IF NOT EXISTS bank (
                user INTEGER PRIMARY KEY,
                wallet INTEGER,
                bank INTEGER,
                maxbank INTEGER
            )''')

    async def on_submit(self, interaction: discord.Interaction):
        user = interaction.user.id
        await interaction.response.defer()
        amount = int(self.amount.value)

        if not hasattr(self, 'pool'):
            await self.init_database()

        async with self.pool.acquire() as conn:
            await conn.execute("""UPDATE bank SET wallet = wallet - ?, bank = bank + ? WHERE user = ?""", (amount, amount, user))
            await conn.commit()

        await interaction.followup.send(f"You have deposited <a:coin:1192540229727440896> **{amount}** from your bank", ephemeral=True)

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

    @commands.command(hidden=True)
    async def bankmax(self, ctx: commands.Context, member: discord.Member, amount: int):
        await self.update_max_bank(member.id, amount)
        await ctx.reply("all done!")

    @commands.command(aliases=["bal"], description="Check your bank and wallet balance", extras="+balance : alias +bal")
    @kanzen_only()
    async def balance(self, ctx, user: discord.Member = None) -> BytesIO:
        async with ctx.typing():
            user = user or ctx.author
            wallet_balance, bank_balance = await self.get_balance(user.id)
            embed = discord.Embed(color=0x2b2d31)
            embed.add_field(name="`👛` purse", value=f"<a:coin:1199052296995209237> **{wallet_balance}**", inline=False)
            embed.add_field(name="`🏦` bank", value=f"<a:coin:1199052296995209237> **{bank_balance}**", inline=False)
            embed.set_footer(text="Would you like to deposit or withdraw money?")
            embed.set_author(name=user.name, icon_url=user.display_avatar)
            embed.set_thumbnail(url=user.display_avatar)
            view = balbuttons(pool=self.pool)
            await ctx.send(embed=embed, view=view)

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
            "Taylor Swift",
            "Dwayne 'The Rock' Johnson",
            "Ariana Grande",
            "BTS",
            "BLACKPINK",
            "Ed Sheeran",
            "Beyoncé",
            "Justin Bieber",
            "Rihanna",
            "Lady Gaga",
            "Katy Perry",
            "Selena Gomez",
        ]
        earnings = random.randint(1, 25000)
        celeb_lines = {
            "Taylor Swift": [
                f"Taylor Swift hands you <a:coin:1192540229727440896> **{earnings}** with a smile.",
                f"'<a:coin:1192540229727440896> **{earnings}** for the fans!'",
                f"You get <a:coin:1192540229727440896> **{earnings}** from the pop sensation, Taylor Swift."
            ],
            "Dwayne 'The Rock' Johnson": [
                f"'Can you smell what The Rock is giving?' <a:coin:1192540229727440896> **{earnings}**",
                f"The Rock shares some of his success with you in coins. <a:coin:1192540229727440896> **{earnings}**",
                f"You receive a 'Rock'-solid amount of coins from Dwayne Johnson. <a:coin:1192540229727440896> **{earnings}**"
            ],
            "Ariana Grande": [
                f"Ariana Grande tosses <a:coin:1192540229727440896> **{earnings}** while saying 'Yuh'",
                f"'Here's a little something for you, sweetener.' <a:coin:1192540229727440896> **{earnings}**",
                f"You receive <a:coin:1192540229727440896> **{earnings}** from the queen of pop, Ariana Grande."
            ],
            "BTS": [
                f"BTS members dance their way to you and drop <a:coin:1192540229727440896> **{earnings}**!",
                f"'Bangtan Sonyeondan, giving you some love and <a:coin:1192540229727440896> **{earnings}**.'",
                f"You get <a:coin:1192540229727440896> **{earnings}** from your favorite kpop idols."
            ],
            "BLACKPINK": [
                f"BLACKPINK members share <a:coin:1192540229727440896> **{earnings}** and say 'Hit you with that ddu-du ddu-du!'",
                f"'Pretty Savage! Here are <a:coin:1192540229727440896> **{earnings}** for you.'",
                f"You receive <a:coin:1192540229727440896> **{earnings}** from the queens of K-pop, BLACKPINK."
            ],
            "Ed Sheeran": [
                f"Ed Sheeran strums his guitar and gives you <a:coin:1192540229727440896> **{earnings}**.",
                f"'Shape of you and <a:coin:1192540229727440896> **{earnings}** for you!'",
                f"You receive <a:coin:1192540229727440896> **{earnings}** from the talented singer-songwriter, Ed Sheeran."
            ],
            "Beyoncé": [
                f"Beyoncé graciously donates <a:coin:1192540229727440896> **{earnings}** with a smile.",
                f"'Queen Bey sending you <a:coin:1192540229727440896> **{earnings}**!'",
                f"You get <a:coin:1192540229727440896> **{earnings}** from the queen herself, Beyoncé."
            ],
            "Justin Bieber": [
                f"Justin Bieber hands you <a:coin:1192540229727440896> **{earnings}** and says 'Never say never!'",
                f"'Beliebers deserve <a:coin:1192540229727440896> **{earnings}** too.'",
                f"You receive <a:coin:1192540229727440896> **{earnings}** from the pop sensation, Justin Bieber."
            ],
            "Rihanna": [
                f"Rihanna shares <a:coin:1192540229727440896> **{earnings}** and says 'Shine bright like a diamond!'",
                f"'Umbrella, ella, ella, here's <a:coin:1192540229727440896> **{earnings}**.'",
                f"You get <a:coin:1192540229727440896> **{earnings}** from the iconic singer, Rihanna."
            ],
            "Lady Gaga": [
                f"Lady Gaga donates <a:coin:1192540229727440896> **{earnings}** and says 'Just dance!'",
                f"'Little monsters, here's <a:coin:1192540229727440896> **{earnings}** for you.'",
                f"You get <a:coin:1192540229727440896> **{earnings}** from the legendary Lady Gaga."
            ],
            "Katy Perry": [
                f"Katy Perry generously donates <a:coin:1192540229727440896> **{earnings}** and says 'Roar for these coins!'",
                f"'California Gurls, here's <a:coin:1192540229727440896> **{earnings}**' for you.'",
                f"You get <a:coin:1192540229727440896> **{earnings}** from the pop icon, Katy Perry."
            ],
            "Selena Gomez": [
                f"Selena Gomez smiles and hands you <a:coin:1192540229727440896> **{earnings}**.",
                f"'Wolves, hands, and <a:coin:1192540229727440896> **{earnings}** for you!'",
                f"You receive <a:coin:1192540229727440896> **{earnings}** from the talented Selena Gomez."
            ],
        }

        celeb_name = random.choice(celeb_names)
        celeb_line = random.choice(celeb_lines.get(celeb_name, ["No coins for you."]))
        wallet_balance, _ = await self.update_balance(ctx.author.id, earnings, 0)
        embed = discord.Embed(title=celeb_name, description=f"{celeb_line}", color=0x2b2d31)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
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
                ("searched a park and found a squirrel that gave you some coins!", random.randint(100, 1500)),
                ("explored a park and stumbled upon a hidden treasure!", random.randint(100, 1500)),
                ("searched a park and found some loose change!", random.randint(100, 1500))
            ],
            'alley': [
                ("searched an alley and found a wallet with some coins inside!", random.randint(100, 2500)),
                ("explored a dark alley and found some discarded coins!", random.randint(100, 2500)),
                ("searched an alley and found nothing but trash.", 0)
            ],
            'dumpster': [
                ("searched a dumpster and found a valuable item worth some coins!", random.randint(100, 1000)),
                ("rummaged through a dumpster and found some hidden coins!", random.randint(100, 1000)),
                ("searched a dumpster and got dirty for no reward.", 0)
            ],
            'forest': [
                ("ventured into the forest and found a hidden treasure chest!", random.randint(100, 1500)),
                ("explored the forest and found a friendly forest creature!", random.randint(100, 1500)),
                ("searched the forest, but it seems there was nothing valuable there today.", 0)
            ],
            'cave': [
                ("entered a dark cave and found a hidden stash of coins!", random.randint(100, 3500)),
                ("explored a mysterious cave and found a rare gemstone!", random.randint(100, 3500)),
                ("searched a cave but found nothing valuable.", 0)
            ],
            'beach': [
                ("strolled along the beach and discovered buried pirate treasure!", random.randint(100, 2000)),
                ("searched the shoreline and found a message in a bottle with coins!", random.randint(100, 2000)),
                ("built sandcastles on the beach and found coins hidden in the sand!", random.randint(100, 2000))
            ],
            'city': [
                ("explored the city streets and found coins dropped by passersby!", random.randint(100, 2500)),
                ("visited a bustling market and haggled your way into extra coins!", random.randint(100, 2500)),
                ("searched city landmarks and found coins overlooked by tourists!", random.randint(100, 2500))
            ],
            'mountain': [
                ("climbed a mountain and found a hidden cave with coins inside!", random.randint(100, 3000)),
                ("explored mountain trails and found coins hidden in the rocks!", random.randint(100, 3000)),
                ("searched a snowy mountain peak and discovered ancient treasure!", random.randint(100, 3000))
            ],
            'hospital': [
                ("searched a hospital and found coins in a sick person's purse... why are you going through a sick person's purse?", random.randint(100, 500)),
                ("explored a hospital and found a doctor's stash of coins!", random.randint(100, 500)),
                ("searched a hospital and found a vending machine that dispenses coins instead of snacks!", random.randint(100, 500))
            ],
            'haunted house': [
                ("entered a haunted house and got scared to death... found no coins. Rest in peace.", 0),
                ("explored a spooky graveyard and encountered restless spirits... found no coins. Rest in peace.", 0),
                ("searched a cursed tomb and triggered a trap... found no coins. Rest in peace.", 0)
            ],
            'ocean': [
                ("dived to the bottom of the ocean and got lost... found no coins. Rest in peace.", 0),
                ("explored a sunken ship and encountered a sea monster... found no coins. Rest in peace.", 0),
                ("searched a mysterious underwater cave and got trapped... found no coins. Rest in peace.", 0)
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
            searched = discord.Embed(description=f"{ctx.author.name} {response}\nYou found: <a:coin:1192540229727440896> **{earnings}**", color=0x2b2d31)
            await ctx.reply(embed=searched)
        else:
            none = discord.Embed(description=response, color=0x2b2d31)
            await ctx.reply(embed=none)

    def is_staff():
        async def predicate(ctx):
            role_id = 1135244903165722695
            role = ctx.guild.get_role(role_id)
            return role in ctx.author.roles
        return commands.check(predicate)

    @commands.command(hidden=True)
    @is_staff()
    async def removecoins(self, ctx, member: discord.Member, amount: str):
        amount = int(amount)
        wallet_balance, _ = await self.get_balance(member.id)
        coins_to_take = min(amount, wallet_balance)
        new_wallet_balance = await self.update_balance(member.id, -coins_to_take, 0)
        author_wallet_balance, _ = await self.get_balance(ctx.author.id)
        new_author_wallet_balance = await self.update_balance(ctx.author.id, coins_to_take, 0)
        await ctx.send(f"Removed {coins_to_take} coins from {member.mention}'s wallet.")

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
            ],
            'vandalism': [
                ("You successfully vandalized public property and left your mark.", random.randint(100, 2000)),
                ("Your attempt at vandalism failed, and you were caught by authorities.", 0)
            ],
            'bribery': [
                ("You successfully bribed someone and got what you wanted.", random.randint(100, 3000)),
                ("Your attempt at bribery failed, and the person reported you.", 0)
            ],
            'kidnapping': [
                ("You successfully kidnapped someone and demanded a ransom.", random.randint(100, 5000)),
                ("Your attempt at kidnapping failed, and the person escaped.", 0)
            ],
            'assault': [
                ("You successfully assaulted someone and took their belongings.", random.randint(100, 2000)),
                ("Your attempt at assault failed, and the person fought back.", 0)
            ],
            'smuggling': [
                ("You successfully smuggled illegal goods and earned a hefty sum.", random.randint(100, 4000)),
                ("Your smuggling attempt failed, and authorities seized the goods.", 0)
            ],
            'counterfeiting': [
                ("You successfully counterfeited money and added fake coins to your wallet.", random.randint(100, 5000)),
                ("Your counterfeiting attempt failed, and the fake coins were easily detected.", 0)
            ],
            'embezzlement': [
                ("You successfully embezzled funds and transferred them to your account.", random.randint(100, 8000)),
                ("Your embezzlement attempt failed, and you were caught by the company.", 0)
            ],
            'street racing': [
                ("You successfully participated in an illegal street race and won some money.", random.randint(100, 3000)),
                ("Your street racing attempt failed, and you crashed your vehicle.", 0)
            ],
            'espionage': [
                ("You successfully engaged in espionage and obtained valuable secrets.", random.randint(100, 6000)),
                ("Your espionage attempt failed, and you were exposed as a spy.", 0)
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

    async def get_wallet_balance(self, user):
        user_id = user.id
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

    @commands.command(description="Steal coins from other members", extras="+rob @member")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @kanzen_only()
    async def rob(self, ctx, user: discord.Member = None):
        inventory = await self.check_inventory(ctx.author.id)
        knife = "<:knife:1199405378216144947>knife"

        if knife.lower() in (item.lower() for item in inventory):
            user = user or ctx.author
            titles = ["LOL you stole from someone... naughty naughty", "wow- are you that broke", "well we all need money... mind sharing "]
            title = random.choice(titles)
            amount = random.randint(1, 50000)

            bank_balance = await self.get_bank_balance(user.id)
            bank_to_take = min(+amount, bank_balance)

            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("UPDATE bank SET bank = bank - ? WHERE user = ?", (bank_to_take, user.id))
                    await cursor.execute("UPDATE bank SET bank = bank + ? WHERE user = ?", (bank_to_take, ctx.author.id))
                    await conn.commit()

            embed = discord.Embed(title=title, description=f"You stole <:coin:1167639638123487232> {bank_to_take} from {user.display_name}", color=0x2b2d31)
            await ctx.send(embed=embed)
        else:
            await ctx.reply("Hey you cannot rob this person without a threat... Buy a knife from the shop")

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining = round(error.retry_after)
            if remaining >= 60:
                mins = remaining // 60
                await ctx.send(f"Sorry, you're on a cooldown from using this command. Try again in {mins} minutes.")
            else:
                await ctx.send(f"Sorry, you're on a cooldown from using this command. Try again in {remaining} seconds.")

    @commands.command(description="Visit the store to see what we have in stock", extras="+shop")
    @kanzen_only()
    async def shop(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        wallet_balance = await self.get_wallet_balance(user)
        categories = [
            "tools"
        ]
        emojis = [
            "⚒️"
        ]
        descriptions = [
            "Includes all the tools you need!"
        ]
        tool_buy_view = toolbuy(bot=self.bot)
        dropdown = discord.ui.Select(
            placeholder="Select a category",
            options=[discord.SelectOption(label=category, emoji=emoji, description=description) for category, emoji, description in zip(categories, emojis, descriptions)]
        )

        tools = discord.Embed(title="Hoshi's Shop", description="> Welcome to the shop, Here you can find all sorts of items to buy\n> Use the dropdown menu below to select a category\n\n**__Categories:__**\n`⚒️` [**tools**](https://instagram.com/kanzengrp/)\n<:1166196258499727480:1188190249768210582> Includes all the tools you need!", color=0x2b2d31)
        tools.set_thumbnail(url=ctx.guild.icon)
        view = discord.ui.View()
        view.add_item(dropdown)
        message = await ctx.send(embed=tools, view=view)

        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            for item in view.children:
                if not isinstance(item, discord.ui.Select):
                    view.remove_item(item)

            if selected_category == categories[0]:
                for item in tool_buy_view.children:
                    view.add_item(item)
                embed = discord.Embed(title="Hoshi's Shop - Tools", description=f"> Use the buttons below to buy the items you want\n\n<a:coin:1192540229727440896> **{wallet_balance}**", color=0x2b2d31)
                embed.set_image(url="https://cdn.discordapp.com/attachments/1111567760745574401/1199316979991982170/shop_tools_00000.png?ex=65c219fa&is=65afa4fa&hm=f6aeffe9777e3defafa21d14b62cd39924f75bc4e6a7caa51a6ef7095c6fa91f&")
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="• Use the buttons below to buy an item (clicking it twice will give you another)", icon_url=ctx.author.avatar)
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")

            await interaction.response.edit_message(embed=embed, view=view)

        dropdown.callback = dropdown_callback

    @commands.command(description="Sell your useless/unwanted items", extras="+sell")
    @kanzen_only()
    async def sell(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        wallet_balance = await self.get_wallet_balance(user)
        categories = [
            "tools",
            "animals",
            "fish",
            "mining ores"
        ]
        emojis = [
            "⚒️",
            "🦌",
            "🐠",
            "<:Emerald_JE3_BE3:1199747182195130458>"
        ]
        descriptions = [
            "Sell the tools you no longer need!",
            "Sell the animals you got from hunting",
            "Sell the fish you got from fishing",
            "Sell the ores you got from mining"
        ]
        tool_sell_view = toolsell(bot=self.bot)
        animal_sell_view = animalsell(bot=self.bot)
        fish_sell_view = fishsell(bot=self.bot)
        ores_sell_view = oresell(bot=self.bot)
        dropdown = discord.ui.Select(
            placeholder="Select a category",
            options=[discord.SelectOption(label=category, emoji=emoji, description=description) for category, emoji, description in zip(categories, emojis, descriptions)]
        )

        tools = discord.Embed(title="Sell Items", description="> Want to sell some items? Well you came to the right place!\n> Use the dropdown menu below to select a category\n\n**__Categories:__**\n`⚒️` [**tools**](https://instagram.com/kanzengrp/)\n<:1166196258499727480:1188190249768210582> Includes all the tools you need!\n`🦌` [**animals**](https://instagram.com/kanzengrp/)\n<:1166196258499727480:1188190249768210582> Sell the animals you got from hunting!\n`🐠` [**fish**](https://instagram.com/kanzengrp/)\n<:1166196258499727480:1188190249768210582> Sell the fish you got from fishing!\n`💎` [**minging ores**](https://instagram.com/kanzengrp/)\n<:1166196258499727480:1188190249768210582> Sell the ores you got from mining!", color=0x2b2d31)
        tools.set_thumbnail(url=ctx.guild.icon)
        view = discord.ui.View()
        view.add_item(dropdown)
        message = await ctx.send(embed=tools, view=view)

        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            for item in view.children:
                if not isinstance(item, discord.ui.Select):
                    view.remove_item(item)

            if selected_category == categories[0]:
                for item in tool_sell_view.children:
                    view.add_item(item)
                embed = discord.Embed(title="Sell Items - Tools", description=f"> Use the buttons below to sell the items you don't want", color=0x2b2d31)
                embed.set_image(url="https://cdn.discordapp.com/attachments/1111567760745574401/1199699889110646894/shop_tools_00000.png?ex=65c37e96&is=65b10996&hm=f690dcb564c714b8940599f25bdc6223f94778c4c2ad0aa51a44d2026f51c1ea&")
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="• Use the buttons below to sell an item (you can click an item again to sell another)", icon_url=ctx.author.avatar)
            elif selected_category == categories[1]:
                for item in animal_sell_view.children:
                    view.add_item(item)
                embed = discord.Embed(title="Sell Items - Animals", description=f"> Use the buttons below to sell the items you don't want", color=0x2b2d31)
                embed.set_image(url="https://cdn.discordapp.com/attachments/1111567760745574401/1199699514299256892/shop_tools_00000.png?ex=65c37e3d&is=65b1093d&hm=f1a8625582c0ad1289f239b783f4fe27d4ef4793481914ad480d14147e77f2d9&")
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="• Use the buttons below to sell an item (you can click an item again to sell another)", icon_url=ctx.author.avatar)
            elif selected_category == categories[2]:
                for item in fish_sell_view.children:
                    view.add_item(item)
                embed = discord.Embed(title="Sell Items - Fish", description=f"> Use the buttons below to sell the items you don't want", color=0x2b2d31)
                embed.set_image(url="https://cdn.discordapp.com/attachments/1111567760745574401/1199741155412295720/shop_tools_00000.png?ex=65c3a505&is=65b13005&hm=5573e72ecc09593214a467a43526c20b920eec2161c00971e607ceb8a8cc628f&")
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="• Use the buttons below to sell an item (you can click an item again to sell another)", icon_url=ctx.author.avatar)
            elif selected_category == categories[3]:
                for item in ores_sell_view.children:
                    view.add_item(item)
                embed = discord.Embed(title="Sell Items - Ores", description=f"> Use the buttons below to sell the items you don't want", color=0x2b2d31)
                embed.set_image(url="https://cdn.discordapp.com/attachments/1111567760745574401/1199747757611688037/shop_tools_00000.png?ex=65c3ab2b&is=65b1362b&hm=0183ca16615099687d5a69c0d54da1320914fce6ffeb8cddb4e0d0e3f4122f68&")
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="• Use the buttons below to sell an item (you can click an item again to sell another)", icon_url=ctx.author.avatar)
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")

            await interaction.response.edit_message(embed=embed, view=view)

        dropdown.callback = dropdown_callback

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
        if role == "dogwalker":
            dog = "✅"
        else:
            dog = ""
        if role == "mod":
            mod = "✅"
        else:
            mod = ""
        embed = discord.Embed(title="Kanzen Jobs", description=f"If a job is marked with ✅, that is the job you have selected.\n\n<:CF12:1188186414387568691> [**Mcdonalds worker**](https://instagram.com/kanzengrp) {mcdonalds}\n<:Empty:1188186122350759996> Flip Burgers and make fries\n<:Empty:1188186122350759996> Salary **5,354** per shift\n<:Empty:1188186122350759996> `+apply mcdonalds`\n\n<:CF12:1188186414387568691> [**Twitch Streamer**](https://instagram.com/kanzengrp) {twitch}\n<:Empty:1188186122350759996> Play video games on stream\n<:Empty:1188186122350759996> Salary **7,645** per shift\n<:Empty:1188186122350759996> `COMING SOON`\n\n<:CF12:1188186414387568691> [**Amazon Delivery Driver**](https://instagram.com/kanzengrp) {amazon}\n<:Empty:1188186122350759996> Deliver packages to customers\n<:Empty:1188186122350759996> Salary **2,435** per shift\n<:Empty:1188186122350759996> `+apply amazon`\n\n<:CF12:1188186414387568691> [**Dog Walker**](https://instagram.com/kanzengrp) {dog}\n<:Empty:1188186122350759996> Walk dogs for people in Kanzen's town\n<:Empty:1188186122350759996> Salary **1,766** per shift\n<:Empty:1188186122350759996> `+apply dogwalker`\n\n<:CF12:1188186414387568691> [**Discord Moderator**](https://instagram.com/kanzengrp) {mod}\n<:Empty:1188186122350759996> Deal with shitty people and Discord kittens\n<:Empty:1188186122350759996> Salary **6,454** per shift\n<:Empty:1188186122350759996> `COMING SOON`", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.author.avatar)
        embed.set_footer(text="• To apply for a job click the buttons below!", icon_url=ctx.guild.icon)
        view=jobpick(bot=self.bot)
        await ctx.reply(embed=embed, view=view)

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

    @commands.command(description="Go hunting for animals and sell them for profit", extras="+hunt")
    @commands.cooldown(1, 3 * 60 * 60, commands.BucketType.user)
    async def hunt(self, ctx):
        inventory = await self.check_inventory(ctx.author.id)
        rifle = "<:rifle:1199405381630308572>Hunting rifle"

        if rifle.lower() in (item.lower() for item in inventory):
            animals = ['🫎moose', '🐇rabbit', '🦌deer', '🦃turkey']
            animal = random.choice(animals)
            item = f"{animal}"
            quantity = 1
            await self.buy_item(ctx.author.id, item, quantity)

            await ctx.reply(f"You went hunting and brought back a **{animal}**")
        else:
            await ctx.reply("Hey! You can't go hunting without a <:rifle:1199405381630308572> hunting rifle!\nGo to the shop to buy one.")

    async def buy_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] + quantity
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO inventory (user, item, quantity) VALUES (?, ?, ?)", (user, item, quantity))
                    await conn.commit()

    @hunt.error
    async def hunt_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            if error.retry_after > 3600:
                hours = int(error.retry_after // 3600)
                minutes = int((error.retry_after % 3600) // 60)
                await ctx.reply(f"You need to wait {hours} hours and {minutes} minutes before hunting again!")
            elif error.retry_after > 60:
                minutes = int(error.retry_after // 60)
                await ctx.reply(f"You need to wait {minutes} minutes before hunting again!")
            else:
                await ctx.reply(f"You need to wait {int(error.retry_after)} seconds before hunting again!")

    @commands.command(description="Go fishing for fish and sell them for profit", extras="+fish")
    @commands.cooldown(1, 1 * 60 * 60, commands.BucketType.user)
    async def fish(self, ctx):
        inventory = await self.check_inventory(ctx.author.id)
        rifle = "<:frod:1199405376320323664>fishing rod"

        if rifle.lower() in (item.lower() for item in inventory):
            animals = ['🦈shark', '🐡pufferfish', '🦑squid', '🐟regular fish', '🐠tropical fish', '🦀crab', '🦐shrimp', '🦞lobster']
            animal = random.choice(animals)
            item = f"{animal}"
            quantity = 1
            await self.buy_item(ctx.author.id, item, quantity)

            await ctx.reply(f"You went fishing and caught a **{animal}**")
        else:
            await ctx.reply("Hey! You can't go fishing without a <:frod:1199405376320323664> fishing rod!\nGo to the shop to buy one.")

    async def buy_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] + quantity
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO inventory (user, item, quantity) VALUES (?, ?, ?)", (user, item, quantity))
                    await conn.commit()

    @fish.error
    async def fish_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            if error.retry_after > 3600:
                hours = int(error.retry_after // 3600)
                minutes = int((error.retry_after % 3600) // 60)
                await ctx.reply(f"You need to wait {hours} hours and {minutes} minutes before fishing again!")
            elif error.retry_after > 60:
                minutes = int(error.retry_after // 60)
                await ctx.reply(f"You need to wait {minutes} minutes before fishing again!")
            else:
                await ctx.reply(f"You need to wait {int(error.retry_after)} seconds before fishing again!")

    @commands.command(description="Go mining for min and sell them for profit", extras="+mine")
    @commands.cooldown(1, 1 * 60 * 60, commands.BucketType.user)
    async def mine(self, ctx):
        inventory = await self.check_inventory(ctx.author.id)
        rifle = "<:paxe:1199405372524478664>pickaxe"

        if rifle.lower() in (item.lower() for item in inventory):
            animals = ['<:coal16581529:1199747331143249940>coal', '<:Nether_Quartz_JE2_BE2:1199747191653269595>quartz', '<:Raw_Copper_JE3_BE2:1199747183759597570>copper', '<:Redstone_Dust_JE2_BE2:1199747189203808366>redstone', '<:Iron_Ingot_JE3_BE2:1199747187777749062>iron', '<:Gold_Ingot_JE4_BE2:1199747185529598012>gold', '<:Diamond_JE3_BE3:1199747180848758824>diamond', '<:Emerald_JE3_BE3:1199747182195130458>emerald']
            animal = random.choice(animals)
            item = f"{animal}"
            quantity = 1
            await self.buy_item(ctx.author.id, item, quantity)

            await ctx.reply(f"You went mining and found **{animal}**")
        else:
            await ctx.reply("Hey! You can't go mining without a <:paxe:1199405372524478664> pickaxe!\nGo to the shop to buy one.")

    async def buy_item(self, user, item, quantity):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT quantity FROM inventory WHERE user = ? AND item = ?", (user, item))
                row = await cursor.fetchone()

        if row:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    new_quantity = row[0] + quantity
                    await cursor.execute("UPDATE inventory SET quantity = ? WHERE user = ? AND item = ?", (new_quantity, user, item))
                    await conn.commit()
        else:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("INSERT INTO inventory (user, item, quantity) VALUES (?, ?, ?)", (user, item, quantity))
                    await conn.commit()

    @mine.error
    async def mine_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            if error.retry_after > 3600:
                hours = int(error.retry_after // 3600)
                minutes = int((error.retry_after % 3600) // 60)
                await ctx.reply(f"You need to wait {hours} hours and {minutes} minutes before mining again!")
            elif error.retry_after > 60:
                minutes = int(error.retry_after // 60)
                await ctx.reply(f"You need to wait {minutes} minutes before mining again!")
            else:
                await ctx.reply(f"You need to wait {int(error.retry_after)} seconds before mining again!")

async def setup(bot):
    await bot.add_cog(Economy(bot))