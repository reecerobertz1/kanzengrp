import discord
from discord.ext import commands
from typing import Optional

class pickup(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Pick up")
    async def pick(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description=f"**{interaction.user.name}** Has picked up the candy!", color=0x2b2d31)
        await self.update_candy(member_id=interaction.user.id)
        await interaction.response.edit_message(embed=embed, view=None)

    async def update_candy(self, member_id: int) -> None:
        query = '''UPDATE inventory SET candy = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                candy = await self.candy(member_id)
                await cursor.execute(query, (candy + 2, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def candy(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT candy FROM inventory WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

class clear(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Remove Decoration")
    async def yes(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description=f"Are you sure you'd like to clear your equipped rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, view=confirmclear(bot=self.bot), ephemeral=True)

class confirmclear(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Yes")
    async def yes(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description=f"Okay your equipped rank decoration has been cleared", color=0x2b2d31)
        await self.update_selected(interaction.user.id, number=None)
        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="No")
    async def no(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description="Okay! I have not cleared your equipped rank decoration", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=None)

    async def update_selected(self, member_id: int, number: int):
        update_query = '''UPDATE inventory SET selected = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(update_query, (number, member_id))
            return "Selected rank decoration updated!"

class confirm(discord.ui.View):
    def __init__(self, bot, number, price):
        super().__init__(timeout=None)
        self.bot = bot
        self.number = int(number)
        self.price = int(price)

    @discord.ui.button(label="Yes")
    async def yes(self, interaction: discord.Interaction, button: discord.Button):
        candy = await self.candy(interaction.user.id)
        decors = await self.get_rank_decors(interaction.user.id)
        if self.number in decors:
            alreadybought = discord.Embed(description=f"Seems like you have already purchased this decoration\nDo **+equip {self.number}** to equip!",color=0x2b2d31)
            await interaction.response.edit_message(embed=alreadybought, view=None)
        elif candy < self.price:
            ohnoembed = discord.Embed(description="Oh no... you don't have enough to buy this rank decoration",color=0x2b2d31)
            await interaction.response.edit_message(embed=ohnoembed, view=None)
        else:
            embed = discord.Embed(description=f"Okay, you purchased rank decoration **{self.number}**", color=0x2b2d31)
            await self.add_decor(interaction.user.id, self.number)
            await self.remove_candy(interaction.user.id, self.price)
            await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="No")
    async def no(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description="Okay! Purchase has been cancelled", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=None)

    async def get_rank_decors(self, member_id: int):
        query = '''SELECT rank_decors FROM inventory WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                row = await cursor.fetchone()
        
        if row:
            if isinstance(row[0], str):
                # Return as a list of integers
                return [int(x) for x in row[0].split(',') if x]
            elif isinstance(row[0], int):
                # Return as a single-item list if it's an integer
                return [row[0]]  
        
        return []  # Return an empty list if not found

    async def candy(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT candy FROM inventory WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

    async def remove_candy(self, member_id: int, price: int) -> None:
        query = '''UPDATE inventory SET candy = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                candy = await self.candy(member_id)
                await cursor.execute(query, (candy - price, member_id))
                await conn.commit()

    async def add_decor(self, member_id: int, new_decor: int):
        rank_decors = await self.get_rank_decors(member_id)
        
        # Ensure rank_decors is a list
        if isinstance(rank_decors, list):
            rank_decors.append(new_decor)  # Add the new decor
        else:
            rank_decors = [new_decor]  # Create a new list with the new decor
        
        # Convert the list back to a string if needed
        updated_rank_decors = ",".join(map(str, rank_decors))
        
        # Update the database with the new rank_decors
        query = '''UPDATE inventory SET rank_decors = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (updated_rank_decors, member_id))
                await conn.commit()

class shop1(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="1")
    async def one(self, interaction: discord.Interaction, button: discord.Button):
        number = "1"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="2")
    async def two(self, interaction: discord.Interaction, button: discord.Button):
        number = "2"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="3")
    async def three(self, interaction: discord.Interaction, button: discord.Button):
        number = "3"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="4")
    async def four(self, interaction: discord.Interaction, button: discord.Button):
        number = "4"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="5")
    async def five(self, interaction: discord.Interaction, button: discord.Button):
        number = "5"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="6")
    async def six(self, interaction: discord.Interaction, button: discord.Button):
        number = "6"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="Next Page")
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        candy = await self.candy(interaction.user.id)
        embed = discord.Embed(title="Event Shop",description=f"Welcome to our __limited time__ event shop!\n• You are able to purchase rank decorations to decorate your rank cards\n• In the image below you can preview all the different designs and their prices!\n• Use the buttons below to purchase your rank decorations with candy\n• Once purchased, you will keep them __forever__!\n\n🍬**{candy}**\nEvent ends: <t:1730478420:D>" ,color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/849724031723634688/1295394092234309632/shop_view_00000.png?ex=670e7d42&is=670d2bc2&hm=d14543036a44976241ccbb9b8ec6941d3790d34ed5ea3034951f52576bc3720a&")
        await interaction.response.edit_message(embed=embed, view=shop2(bot=self.bot))

    async def candy(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT candy FROM inventory WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

class shop2(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="7")
    async def one(self, interaction: discord.Interaction, button: discord.Button):
        number = "7"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="8")
    async def two(self, interaction: discord.Interaction, button: discord.Button):
        number = "8"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="9")
    async def three(self, interaction: discord.Interaction, button: discord.Button):
        number = "9"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="10")
    async def four(self, interaction: discord.Interaction, button: discord.Button):
        number = "10"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="11")
    async def five(self, interaction: discord.Interaction, button: discord.Button):
        number = "11"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="12")
    async def six(self, interaction: discord.Interaction, button: discord.Button):
        number = "12"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="Previous Page")
    async def last(self, interaction: discord.Interaction, button: discord.Button):
        candy = await self.candy(interaction.user.id)
        embed = discord.Embed(title="Event Shop",description=f"Welcome to our __limited time__ event shop!\n• You are able to purchase rank decorations to decorate your rank cards\n• In the image below you can preview all the different designs and their prices!\n• Use the buttons below to purchase your rank decorations with candy\n• Once purchased, you will keep them __forever__!\n\n🍬**{candy}**\nEvent ends: <t:1730478420:D>" ,color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/849724031723634688/1295392795326156932/shop_view_00000.png?ex=670e7c0d&is=670d2a8d&hm=bdc38d5f5ad66da268987f79f2cf5b4b30cfcbff56ebcd2024c3ae0c7d33a00e&")
        await interaction.response.edit_message(embed=embed, view=shop1(bot=self.bot))

    @discord.ui.button(label="Next Page")
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        candy = await self.candy(interaction.user.id)
        embed = discord.Embed(title="Event Shop",description=f"Welcome to our __limited time__ event shop!\n• You are able to purchase rank decorations to decorate your rank cards\n• In the image below you can preview all the different designs and their prices!\n• Use the buttons below to purchase your rank decorations with candy\n• Once purchased, you will keep them __forever__!\n\n🍬**{candy}**\nEvent ends: <t:1730478420:D>" ,color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248039148888129647/1295404920467619890/shop_view_00000.png?ex=670e8758&is=670d35d8&hm=48ba1f4cb487d2b5f36cc3d8bc6858c90d907a8e4aae435c5a4d27df9474e36c&")
        await interaction.response.edit_message(embed=embed, view=shop3(bot=self.bot))

    async def candy(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT candy FROM inventory WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

class shop3(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="13")
    async def one(self, interaction: discord.Interaction, button: discord.Button):
        number = "13"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="14")
    async def two(self, interaction: discord.Interaction, button: discord.Button):
        number = "14"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="15")
    async def three(self, interaction: discord.Interaction, button: discord.Button):
        number = "15"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="16")
    async def four(self, interaction: discord.Interaction, button: discord.Button):
        number = "16"
        price = "4"
        embed = discord.Embed(description="Are you sure you'd like to purchase this rank decoration?", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=confirm(bot=self.bot, number=number, price=price))

    @discord.ui.button(label="Previous Page")
    async def last(self, interaction: discord.Interaction, button: discord.Button):
        candy = await self.candy(interaction.user.id)
        embed = discord.Embed(title="Event Shop",description=f"Welcome to our __limited time__ event shop!\n• You are able to purchase rank decorations to decorate your rank cards\n• In the image below you can preview all the different designs and their prices!\n• Use the buttons below to purchase your rank decorations with candy\n• Once purchased, you will keep them __forever__!\n\n🍬**{candy}**\nEvent ends: <t:1730478420:D>" ,color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/849724031723634688/1295394092234309632/shop_view_00000.png?ex=670e7d42&is=670d2bc2&hm=d14543036a44976241ccbb9b8ec6941d3790d34ed5ea3034951f52576bc3720a&")
        await interaction.response.edit_message(embed=embed, view=shop2(bot=self.bot))

    async def candy(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT candy FROM inventory WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_staff():
        async def predicate(ctx):
            role_id = 753678720119603341
            role = ctx.guild.get_role(role_id)
            return role in ctx.author.roles
        return commands.check(predicate)

    async def candy(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT candy FROM inventory WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

    async def get_selected(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = '''SELECT selected FROM inventory WHERE member_id = ?'''
                await cursor.execute(query, (member_id,))
                row = await cursor.fetchone()

                if row:
                    selected_value = row[0]
                    return selected_value
                else:
                    return None

    async def update_selected(self, member_id: int, number: int):
        query = '''SELECT rank_decors, selected FROM inventory WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                row = await cursor.fetchone()
            if row:
                rank_decors = row['rank_decors']
                if str(number) in str(rank_decors).split(','):
                    update_query = '''UPDATE inventory SET selected = ? WHERE member_id = ?'''
                    async with conn.cursor() as cursor:
                        await cursor.execute(update_query, (number, member_id))

    async def get_rank_decors(self, member_id: int):
        query = '''SELECT rank_decors FROM inventory WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                row = await cursor.fetchone()
            if row and row[0]:
                rank_decors = [int(x) for x in row[0].split(',')]
                return rank_decors
            else:
                return []

    @commands.command()
    async def shop(self, ctx):
        candy = await self.candy(ctx.author.id)
        embed = discord.Embed(title="Event Shop",description=f"Welcome to our __limited time__ event shop!\n• You are able to purchase rank decorations to decorate your rank cards\n• In the image below you can preview all the different designs and their prices!\n• Use the buttons below to purchase your rank decorations with candy\n• Once purchased, you will keep them __forever__!\n\n🍬**{candy}**\nEvent ends: <t:1730478420:D>" ,color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/849724031723634688/1295392795326156932/shop_view_00000.png?ex=670e7c0d&is=670d2a8d&hm=bdc38d5f5ad66da268987f79f2cf5b4b30cfcbff56ebcd2024c3ae0c7d33a00e&")
        await ctx.reply(embed=embed, view=shop1(bot=self.bot))

    @commands.command()
    async def equip(self, ctx, number: Optional[int]):
        if number:
            await self.update_selected(ctx.author.id, number)
            await ctx.reply(f"Okay! you have equipped rank decoration **{number}**")
        else:
            decors = await self.get_rank_decors(ctx.author.id)
            embed = discord.Embed(title="Decoration Equip",description=f"Here you can see all the rank decorations you have!\nTo select a rank decoration, redo this command but enter the number of the decoration you want!\n> **eg. +equip 1**\n\nTo remove your equipped rank decoration, click the button below!\n\nCurrent unlocked rank decorations: {decors}" ,color=0x2b2d31)
            await ctx.reply(embed=embed, view=clear(bot=self.bot))

    async def update_candy(self, member_id: int) -> None:
        query = '''UPDATE inventory SET candy = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                candy = await self.candy(member_id)
                await cursor.execute(query, (candy + 2, member_id, ))
                await conn.commit()
            await self.bot.pool.release(conn)

    @commands.command()
    async def addcandy(self, ctx, member: discord.Member):
        await self.update_candy(member.id)
        await ctx.reply("yup")

    @commands.command()
    @is_staff()
    async def drop(self, ctx):
        embed = discord.Embed(title="Dropped Candy!", description=f"**{ctx.author.name}** has dropped 🍬**2**\nQuick pick it up before someone steals it")
        await ctx.send(embed=embed, view=pickup(bot=self.bot))

async def setup(bot):
    await bot.add_cog(event(bot))