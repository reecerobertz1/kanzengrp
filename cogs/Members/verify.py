import discord
from discord.ext import commands
from bot import LalisaBot
import asyncio
from discord import ui, Embed, ButtonStyle, SelectOption
from discord.interactions import Interaction
from typing import List
import random
import string

class VerificationSelectView(ui.View):
    def __init__(self, cog):
        self.cog = cog
        super().__init__(timeout=300)

    @ui.select(
        placeholder="Choose a verification method...",
        options=[
            SelectOption(label="Type the correct code Hoshi sends", value="code", emoji="<:ice:1477655182048231749>", description="Hoshi will send a code into this chat. You will need to copy the code correctly to verify."),
            SelectOption(label="List the 5 colours in order", value="colours", emoji="<:ice:1477655182048231749>", description="List the 5 colours in order as Hoshi sends them."),
            SelectOption(label="Press the buttons in the correct order", value="buttons", emoji="<:ice:1477655182048231749>", description="5 icons will appear in an image, please use the buttons given to put them in order."),
        ]
    )
    async def select_method(self, interaction: Interaction, select: ui.Select):
        choice = select.values[0]
        if choice == "code":
            code_list = random.choices(string.ascii_uppercase, k=4) + random.choices(string.digits, k=4)
            random.shuffle(code_list)
            code = ''.join(code_list)
            self.cog.pending_codes[interaction.user.id] = code
            await interaction.response.send_message(f"The code is: `{code}`\nType this code in the chat (all caps).", ephemeral=True)
        elif choice == "colours":
            colour_view = ColourView()
            code_str = ' '.join(colour_view.code)
            await interaction.response.send_message(f"Select the 5 colours in order\n{code_str}", view=colour_view, ephemeral=True)
        elif choice == "buttons":
            order_view = OrderView()
            code_str = ' '.join(map(str, order_view.code))
            await interaction.response.send_message(f"Press the buttons in the correct order\n`{code_str}`", view=order_view, ephemeral=True)

class ColourView(ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.colours = ['<:dot_red:1462461718092447985>', '<:dot_yellow:1462461752766894223>', '<:dot_green:1462461796215685293>', '<:dot_blue:1462461830399135855>', '<:dot_pink:1462461868051267635>']
        self.code = random.sample(self.colours, 5)
        self.input = []

    async def handle_button(self, interaction: Interaction, button: ui.Button, colour: str):
        self.input.append(colour)
        button.disabled = True
        
        if len(self.input) == 5:
            if self.input == self.code:
                role = interaction.guild.get_role(1462163311540961433)
                if role:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message("Verification successful! Role added.", ephemeral=True)
                else:
                    await interaction.response.send_message("Error: Role not found.", ephemeral=True)
            else:
                new_view = ColourView()
                code_str = ' '.join(new_view.code)
                await interaction.response.edit_message(content=f"Incorrect order.\nTry again: {code_str}", view=new_view)
        else:
            await interaction.response.edit_message(view=self)

    @ui.button(emoji='<:dot_red:1462461718092447985>')
    async def red_button(self, interaction: Interaction, button: ui.Button):
        await self.handle_button(interaction, button, "<:dot_red:1462461718092447985>")

    @ui.button(emoji='<:dot_yellow:1462461752766894223>')
    async def yellow_button(self, interaction: Interaction, button: ui.Button):
        await self.handle_button(interaction, button, "<:dot_yellow:1462461752766894223>")
    @ui.button(emoji='<:dot_green:1462461796215685293>')
    async def green_button(self, interaction: Interaction, button: ui.Button):
        await self.handle_button(interaction, button, "<:dot_green:1462461796215685293>")

    @ui.button(emoji='<:dot_blue:1462461830399135855>')
    async def blue_button(self, interaction: Interaction, button: ui.Button):
        await self.handle_button(interaction, button, "<:dot_blue:1462461830399135855>")

    @ui.button(emoji='<:dot_pink:1462461868051267635>')
    async def purple_button(self, interaction: Interaction, button: ui.Button):
        await self.handle_button(interaction, button, "<:dot_pink:1462461868051267635>")

class OrderView(ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.code = random.sample(range(1, 6), 5)
        self.input = []

    async def handle_button(self, interaction: Interaction, button: ui.Button, number: int):
        self.input.append(number)
        button.disabled = True
        
        if len(self.input) == 5:
            if self.input == self.code:
                role = interaction.guild.get_role(1462163311540961433)
                if role:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message("Verification successful! Role added.", ephemeral=True)
                else:
                    await interaction.response.send_message("Error: Role not found.", ephemeral=True)
            else:
                new_view = OrderView()
                code_str = ' '.join(map(str, new_view.code))
                await interaction.response.edit_message(content=f"Incorrect order. Try again: {code_str}", view=new_view)
        else:
            await interaction.response.edit_message(view=self)

    @ui.button(label="1")
    async def button_1(self, interaction: Interaction, button: ui.Button):
        await self.handle_button(interaction, button, 1)

    @ui.button(label="2")
    async def button_2(self, interaction: Interaction, button: ui.Button):
        await self.handle_button(interaction, button, 2)

    @ui.button(label="3")
    async def button_3(self, interaction: Interaction, button: ui.Button):
        await self.handle_button(interaction, button, 3)

    @ui.button(label="4")
    async def button_4(self, interaction: Interaction, button: ui.Button):
        await self.handle_button(interaction, button, 4)

    @ui.button(label="5")
    async def button_5(self, interaction: Interaction, button: ui.Button):
        await self.handle_button(interaction, button, 5)

class verify(commands.Cog):
    def __init__(self, bot: LalisaBot):
        self.bot = bot
        self.pending_codes = {}

    @commands.command(name="verify")
    async def verify(self, ctx: commands.Context):
        embed = discord.Embed(title="†    CHROMATICA ： VERIFICATION", description="Select one of 3 options to verify yourself to join the Chromatica server.\n> -# ・⠀01 : Type the correct code Hoshi sends you.\n> -# ・⠀02 : List the 5 colours in order.\n> -# ・⠀03 : Press the buttons in the correct order.")
        embed.set_footer(text="Use the dropdown menu below to select a verification option.")
        view = VerificationSelectView(self)
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id in self.pending_codes:
            expected = self.pending_codes[message.author.id]
            if message.content == expected:
                role = message.guild.get_role(1462163311540961433)
                if role:
                    await message.author.add_roles(role)
                await message.delete()
                confirm_msg = await message.channel.send(f"{message.author.mention} Verification successful! Role added.", ephemeral=True)
                await asyncio.sleep(3)
                await confirm_msg.delete()
                del self.pending_codes[message.author.id]
            else:
                await message.delete()
                try_msg = await message.channel.send(f"{message.author.mention} Incorrect code. Try verifying with another option!.", ephemeral=True)
                await asyncio.sleep(5)
                await try_msg.delete()

async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(verify(bot))