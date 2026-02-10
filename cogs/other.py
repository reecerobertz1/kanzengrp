import discord
from discord.ext import commands
from discord import ui

class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.color = 0x2b2d31

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.type == discord.MessageType.premium_guild_subscription:
            embed = discord.Embed(
                title="SERVER BOOST",
                description=(
                    f"Thank you for boosting {message.author.name}!"
                    "\n・⠀01 : [Claim our booster perks here!](https://discord.com/channels/1462079847433244799/1465475407342997718)"
                    "\n・⠀02 : [Preview our perks here!](https://discord.com/channels/1462079847433244799/1465475615103783074)"
                    "\n・⠀03 : Your support is greatly appreciated!"
                )
            )
            embed.set_footer(
                text=f"CHRT_OS // BOOSTER_LOG_v1.01 | {message.guild.premium_subscription_count} BOOSTS ADDED",
                icon_url=message.guild.icon.url if message.guild.icon else None
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)

            if message.guild.id == 1462079847433244799:
                await message.channel.send(f"{message.author.mention}", embed=embed)
            else:
                pass

async def setup(bot):
    await bot.add_cog(other(bot))