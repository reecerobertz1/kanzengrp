import discord
from discord.ext import commands
from bot import LalisaBot
from utils.views import VerificationSelectView
import asyncio

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