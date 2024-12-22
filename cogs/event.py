from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

class standard2(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.bot = bot

    @discord.ui.button(label="🏠︎", style=discord.ButtonStyle.blurple, row=2)
    async def back(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description="Welcome to Hoshi's shop!"
        "\n<:bulletpoint:1304247536021667871>Here you can buy rank decorations."
        "\n<:bulletpoint:1304247536021667871>Rank decorations overlay on top of your rank cards."
        "\n<:bulletpoint:1304247536021667871>Decorations are available for both Lyra and Chroma."
        "\n<:bulletpoint:1304247536021667871>If you buy a decoration in Chroma, you don't need to repurchase it in Lyra."
        "\n<:bulletpoint:1304247536021667871>You can have a different decoration for Chroma and Lyra.", color=0xC7D9E5)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1202385683134812210/1316858495395434568/home_page_yuh_00000.png?ex=675c938b&is=675b420b&hm=75571d2c24b722ba1dafacc62a89c549dc8faa860c67c08191ea140e377d2220&")
        await interaction.response.edit_message(embed=embed, view=categories(bot=self.bot))

    @discord.ui.button(label="Page 1", row=1)
    async def page1(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Standard Collection", description=f"`・` Use the **Buy** button below and enter the number of the decoration you want.\n`・` These decorations are available forever.\n\n`🪙{currency} coins`", color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 1 of 4")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1316865713394421820/standard_collection_1500x500_00000.png?ex=676877c4&is=67672644&hm=7064d41c336c29191297514a63af2d41c18df7c1480b5af295eaa858c3921042&")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Page 2", row=1)
    async def page2(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Standard Collection", description=f"`・` Use the **Buy** button below and enter the number of the decoration you want.\n`・` These decorations are available forever.\n\n`🪙{currency} coins`", color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 2 of 4")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1316867102052716565/standard_collection_1500x500_00000.png?ex=6768790f&is=6767278f&hm=52aac649652c56016cb480227045731700dacd9e3c262d7b836b4e7abd2d59ee&")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Page 3", row=1)
    async def page3(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Standard Collection", description=f"`・` Use the **Buy** button below and enter the number of the decoration you want.\n`・` These decorations are available forever.\n\n`🪙{currency} coins`", color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 3 of 4")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1320164845089456180/standard_collection_1500x500_00000.png?ex=67689ad2&is=67674952&hm=73f399b1aeaa93f279e4e75f657f97c127f6d1c6b53545e889fd513f8ce993e1&")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Page 4", row=1)
    async def page4(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Standard Collection", description=f"`・` Use the **Buy** button below and enter the number of the decoration you want.\n`・` These decorations are available forever.\n\n`🪙{currency} coins`", color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 4 of 4")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1320165188279861389/standard_collection_1500x500_00000.png?ex=67689b24&is=676749a4&hm=f044f727307d2490288ddb8aca39ccb7e3d44636d2b858270c70115afd34e0b1&")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Buy", row=2)
    async def buy(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(buy(bot=self.bot))

    @discord.ui.button(label="Switch Format", row=3, style=discord.ButtonStyle.blurple)
    async def format(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Standard Collection", description=f"`・` Use the **Buy** button below and enter the number of the decoration you want.\n`・` These decorations are available forever.\n\n`🪙{currency} coins`", color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 1 of 2")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1316860437567897641/standard_collection_1080x1080_00000.png?ex=6765271a&is=6763d59a&hm=5b5814ed863877d35a254ef67f64de127be00285c1caa1b275b26f7dfa3eaafe&")
        await interaction.response.edit_message(embed=embed, view=standard1(bot=self.bot))

    @discord.ui.button(label="2nd format selected", row=3, disabled=True)
    async def formats(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("hdfg")

    async def get_currency(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT currency FROM decors WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

class standard1(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.bot = bot

    @discord.ui.button(label="🏠︎", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description="Welcome to Hoshi's shop!"
        "\n<:bulletpoint:1304247536021667871>Here you can buy rank decorations."
        "\n<:bulletpoint:1304247536021667871>Rank decorations overlay on top of your rank cards."
        "\n<:bulletpoint:1304247536021667871>Decorations are available for both Lyra and Chroma."
        "\n<:bulletpoint:1304247536021667871>If you buy a decoration in Chroma, you don't need to repurchase it in Lyra."
        "\n<:bulletpoint:1304247536021667871>You can have a different decoration for Chroma and Lyra.", color=0xC7D9E5)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1202385683134812210/1316858495395434568/home_page_yuh_00000.png?ex=675c938b&is=675b420b&hm=75571d2c24b722ba1dafacc62a89c549dc8faa860c67c08191ea140e377d2220&")
        await interaction.response.edit_message(embed=embed, view=categories(bot=self.bot))

    @discord.ui.button(label="<")
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Standard Collection", description=f"`・` Use the **Buy** button below and enter the number of the decoration you want.\n`・` These decorations are available forever.\n\n`🪙{currency} coins`", color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 1 of 2")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1316860437567897641/standard_collection_1080x1080_00000.png?ex=6765271a&is=6763d59a&hm=5b5814ed863877d35a254ef67f64de127be00285c1caa1b275b26f7dfa3eaafe&")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label=">")
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Standard Collection", description=f"`・` Use the **Buy** button below and enter the number of the decoration you want.\n`・` These decorations are available forever.\n\n`🪙{currency} coins`", color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 2 of 2")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248039148888129647/1320189667248967720/standard_collection_1080x1080_00000.png?ex=6768b1f0&is=67676070&hm=fa0138fea3115f684bed74dae02166c4dbd0e165485fd54c31295adeb85c9a4f&")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Buy")
    async def buy(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(buy(bot=self.bot))

    @discord.ui.button(label="Switch Format", row=2, style=discord.ButtonStyle.blurple)
    async def format(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Standard Collection", description=f"`・` Use the **Buy** button below and enter the number of the decoration you want.\n`・` These decorations are available forever.\n\n`🪙{currency} coins`", color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 1 of 4")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1316865713394421820/standard_collection_1500x500_00000.png?ex=67652c04&is=6763da84&hm=a66dbf9e7733b1b65fea7195407cd26405db84460c357f38e43ee895163b59c4&")
        await interaction.response.edit_message(embed=embed, view=standard2(bot=self.bot))

    @discord.ui.button(label="1st format selected", row=2, disabled=True)
    async def formats(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("hdfg")

    async def get_currency(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT currency FROM decors WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

class limitedtime(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.bot = bot

    @discord.ui.button(label="🏠︎", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description="Welcome to Hoshi's shop!"
        "\n<:bulletpoint:1304247536021667871>Here you can buy rank decorations."
        "\n<:bulletpoint:1304247536021667871>Rank decorations overlay on top of your rank cards."
        "\n<:bulletpoint:1304247536021667871>Decorations are available for both Lyra and Chroma."
        "\n<:bulletpoint:1304247536021667871>If you buy a decoration in Chroma, you don't need to repurchase it in Lyra."
        "\n<:bulletpoint:1304247536021667871>You can have a different decoration for Chroma and Lyra.", color=0xC7D9E5)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1202385683134812210/1316858495395434568/home_page_yuh_00000.png?ex=675c938b&is=675b420b&hm=75571d2c24b722ba1dafacc62a89c549dc8faa860c67c08191ea140e377d2220&")
        await interaction.response.edit_message(embed=embed, view=categories(bot=self.bot))

    @discord.ui.button(label="<")
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Limited Decorations", description="`・` Use the **Buy** button below and enter the number of the decoration you want."
        "\n`・` These decorations are only available until <t:1735768020:D>."
        f"\n\n`🪙{currency} coins`" ,color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 1 of 2")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1316870629651251362/standard_collection_1500x500_00000.png?ex=67609358&is=675f41d8&hm=b6f3268bb49869360058caf61312ee8dfd63bc90a70bef2b7e8fb7ab9c1d2161&")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label=">")
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Limited Decorations", description="`・` Use the **Buy** button below and enter the number of the decoration you want."
        "\n`・` These decorations are only available until <t:1735768020:D>."
        f"\n\n`🪙{currency} coins`" ,color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 2 of 2")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1316871013203443732/standard_collection_1500x500_00000.png?ex=676530f3&is=6763df73&hm=37966e0db36b9542e2fb6cf9216db4e028de33e9c6b0738f731357390d3de686&")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Buy")
    async def buy(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(buy(bot=self.bot))

    async def get_currency(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT currency FROM decors WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

class categories(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.bot = bot

    @discord.ui.button(label="Limited Collection", style=discord.ButtonStyle.blurple)
    async def limited(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Limited Decorations", description="`・` Use the **Buy** button below and enter the number of the decoration you want."
        "\n`・` These decorations are only available until <t:1735768020:D>."
        f"\n\n`🪙{currency} coins`" ,color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 1 of 2")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1316870629651251362/standard_collection_1500x500_00000.png?ex=67609358&is=675f41d8&hm=b6f3268bb49869360058caf61312ee8dfd63bc90a70bef2b7e8fb7ab9c1d2161&")
        await interaction.response.edit_message(embed=embed, view=limitedtime(bot=self.bot))

    @discord.ui.button(label="Standard Collection")
    async def standard(self, interaction: discord.Interaction, button: discord.Button):
        currency = await self.get_currency(interaction.user.id)
        embed=discord.Embed(title="Standard Collection", description=f"`・` Use the **Buy** button below and enter the number of the decoration you want.\n`・` These decorations are available forever.\n\n`🪙{currency} coins`", color=0x2b2d31)
        embed.set_footer(icon_url=interaction.guild.icon, text="Page 1 of 2")
        embed.set_image(url="https://cdn.discordapp.com/attachments/1248991619026391122/1316860437567897641/standard_collection_1080x1080_00000.png?ex=6765271a&is=6763d59a&hm=5b5814ed863877d35a254ef67f64de127be00285c1caa1b275b26f7dfa3eaafe&")
        await interaction.response.edit_message(embed=embed, view=standard1(bot=self.bot))

    async def get_currency(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT currency FROM decors WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

class equip(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="Equip a rank decoration")
        self.bot = bot

    deocration = discord.ui.TextInput(label="Enter the decoration ID", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        decors = await self.get_rank_decors(interaction.user.id)
        chosen = int(self.deocration.value)
        if chosen not in decors:
            await interaction.response.send_message("It looks like you do not own this rank decoration...\nPlease do /decorations again to see your owned decorations!", ephemeral=True)
        else:
            await self.update_equiped(interaction.user.id, chosen=chosen)
            await interaction.response.send_message(f'You have equipped **Decoration {chosen}**', ephemeral=True)

    async def update_equiped(self, member_id: int, chosen: int) -> None:
        query = '''UPDATE decors SET selected = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (chosen, member_id))
                await conn.commit()

    async def get_rank_decors(self, member_id: int):
        query = '''SELECT unlocked FROM decors WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                row = await cursor.fetchone()
        
        if row:
            if isinstance(row[0], str):
                return [int(x) for x in row[0].split(',') if x]
            elif isinstance(row[0], int):
                return [row[0]]  
        
        return []

class buy(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="Purchase a rank decoration")
        self.bot = bot

    deocration = discord.ui.TextInput(label="Enter the decoration ID", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        currency = await self.get_currency(interaction.user.id)
        decors = await self.get_rank_decors(interaction.user.id)
        chosen = int(self.deocration.value)
        if chosen in decors:
            await interaction.response.send_message("It looks like you have already purchased this decoration.\nDo /equip to equip it!", ephemeral=True)
        elif currency < 10:
            await interaction.response.send_message("You don't have enough coins to purchase this decoration :(", ephemeral=True)
        else:
            await self.add_decor(interaction.user.id, chosen)
            await self.remove_currency(interaction.user.id, price=10)
            await interaction.response.send_message(f'You have bought **Decoration {chosen}**', ephemeral=True)

    async def remove_currency(self, member_id: int, price: int) -> None:
        query = '''UPDATE decors SET currency = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                currency = await self.get_currency(member_id)
                await cursor.execute(query, (currency - price, member_id))
                await conn.commit()

    async def add_decor(self, member_id: int, new_decor: int):
        rank_decors = await self.get_rank_decors(member_id)
        if isinstance(rank_decors, list):
            rank_decors.append(new_decor)
        else:
            rank_decors = [new_decor]
        updated_rank_decors = ",".join(map(str, rank_decors))
        query = '''UPDATE decors SET unlocked = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (updated_rank_decors, member_id))
                await conn.commit()

    async def get_rank_decors(self, member_id: int):
        query = '''SELECT unlocked FROM decors WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                row = await cursor.fetchone()
        
        if row:
            if isinstance(row[0], str):
                return [int(x) for x in row[0].split(',') if x]
            elif isinstance(row[0], int):
                return [row[0]]  
        
        return []

    async def get_currency(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT currency FROM decors WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

    async def add_decor(self, member_id: int, chosen: int):
        rank_decors = await self.get_rank_decors(member_id)
        if isinstance(rank_decors, list):
            rank_decors.append(chosen)
        else:
            rank_decors = [chosen]
        updated_rank_decors = ",".join(map(str, rank_decors))
        query = '''UPDATE decors SET unlocked = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (updated_rank_decors, member_id))
                await conn.commit()

    async def remove_currency(self, member_id: int, price: 10) -> None:
        query = '''UPDATE decors SET currency = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                currency = await self.get_currency(member_id)
                await cursor.execute(query, (currency - price, member_id))
                await conn.commit()

class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = None

    async def add_member(self, member_id: int, currency: int) -> None:
        query_check = '''SELECT 1 FROM decors WHERE member_id = ?'''
        query_insert = '''INSERT INTO decors (member_id, currency, unlocked, selected) VALUES (?, ?, ?, ?)'''

        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query_check, (member_id,))
                result = await cursor.fetchone()
                if result:
                    print(f"Member {member_id} already exists in the database.")
                else:
                    await cursor.execute(query_insert, (member_id, currency, 0, 0))
                    await conn.commit()

    @app_commands.command(name="shop", description="Hoshi's shop")
    async def shop(self, interaction: discord.Interaction):
        required_roles = {694016195090710579, 1134797882420117544}
        member_roles = {role.id for role in interaction.user.roles}
        if required_roles.isdisjoint(member_roles):
            await interaction.response.send_message("Sorry, this command is only available for members.", ephemeral=True)
            return
        
        embed = discord.Embed(description="Welcome to Hoshi's shop!"
        "\n<:bulletpoint:1304247536021667871>Here you can buy rank decorations."
        "\n<:bulletpoint:1304247536021667871>Rank decorations overlay on top of your rank cards."
        "\n<:bulletpoint:1304247536021667871>Decorations are available for both Lyra and Chroma."
        "\n<:bulletpoint:1304247536021667871>If you buy a decoration in Chroma, you don't need to repurchase it in Lyra."
        "\n<:bulletpoint:1304247536021667871>You can have a different decoration for Chroma and Lyra.", color=0xC7D9E5)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1202385683134812210/1316858495395434568/home_page_yuh_00000.png?ex=675c938b&is=675b420b&hm=75571d2c24b722ba1dafacc62a89c549dc8faa860c67c08191ea140e377d2220&")
        await self.add_member(interaction.user.id, currency=10)
        await interaction.response.send_message(embed=embed, view=categories(bot=self.bot))

    async def get_currency(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT currency FROM decors WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

    async def add_currency(self, member_id: int) -> None:
        query = '''UPDATE decors SET currency = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                currency = await self.get_currency(member_id)
                await cursor.execute(query, (currency + 10, member_id))
                await conn.commit()

    @commands.command()
    async def abc(self, ctx):
        await self.add_currency(ctx.author.id)
        await ctx.reply("yes")

    async def get_rank_decors(self, member_id: int):
        query = '''SELECT unlocked FROM decors WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                row = await cursor.fetchone()
        
        if row:
            if isinstance(row[0], str):
                return [int(x) for x in row[0].split(',') if x]
            elif isinstance(row[0], int):
                return [row[0]]  
        
        return []

    @app_commands.command(name="decorations", description="View the decorations you own")
    async def decorations(self, interation: discord.Interaction):
        decors = await self.get_rank_decors(interation.user.id)
        await interation.response.send_message(f"{decors}")

    @app_commands.command(name="equip", description="equip a decoration")
    async def equip(self, interation: discord.Interaction):
        await interation.response.send_modal(equip(bot=self.bot))

async def setup(bot):
    await bot.add_cog(event(bot))