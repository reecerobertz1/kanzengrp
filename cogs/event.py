from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = None

    @app_commands.command(name="shop", description="Hoshi's limited time event shop")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Hoshi Event Shop", description="Welcome to Hoshi's __limited time__ event shop!"
        "\n<:bulletpoint:1304247536021667871>Here you can buy rank decorations."
        "\n<:bulletpoint:1304247536021667871>Rank decorations overlay on top of your rank cards."
        "\n<:bulletpoint:1304247536021667871>Decorations are limited-time sales but last forever once purchased."
        "\n<:bulletpoint:1304247536021667871>Decorations are available for both Lyra and Chroma."
        "\n<:bulletpoint:1304247536021667871>If you buy a decoration in Chroma, you don't need to repurchase it in Lyra."
        "\n<:bulletpoint:1304247536021667871>You can have a different decoration for Lyra and Chroma."
        "\n\nBelow are all the available rank decorations!"
        "\nUse the buttons below to purchase one"
        "\n<:candy_cane:1306439693658750976>**10**", color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/849724031723634688/1295392795326156932/shop_view_00000.png?ex=6736090d&is=6734b78d&hm=bb38406eb6cdc09c4e73443c50c11ca1011969ec4a250968e347ba788fd2c2e1&")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(event(bot))