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
        if message.content.lower() == "chroma":
            if message.author.id == 756361726257004625:
                await message.channel.send(f"OMG RYAN WE LOVE YOU TOO!!!!!!!!!")
            else:
                await message.channel.send(f"**{message.author.name}** loves chroma\n-# <:1166196258499727480:1325926576042410094> we love you too! **<3**")
        if message.type == discord.MessageType.premium_guild_subscription:
            chromaembed = discord.Embed(
                title="Thank you for boosting",
                description=(
                    f"Thank you {message.author.name} for boosting!\n"
                    "・Your support is greatly appreciated\n"
                    "・Head to <#865516313065947136> to claim our perks"
                ),
                color=0x2b2d31
            )
            chromaembed.set_footer(
                text=f"We now have {message.guild.premium_subscription_count} boosts!",
                icon_url=message.guild.icon.url if message.guild.icon else None
            )
            chromaembed.set_thumbnail(url=message.author.display_avatar.url)

            chroma2embed = discord.Embed(
                title="Thank you for boosting",
                description=(
                    f"Thank you {message.author.name} for boosting!\n"
                    "・Your support is greatly appreciated\n"
                    "・Head to <#853241710658584586> to claim our perks"
                ),
                color=0x2b2d31
            )
            chroma2embed.set_footer(
                text=f"We now have {message.guild.premium_subscription_count} boosts!",
                icon_url=message.guild.icon.url if message.guild.icon else None
            )
            chroma2embed.set_thumbnail(url=message.author.display_avatar.url)

            if message.guild.id == 835495688832811039:
                await message.channel.send(f"{message.author.mention}", embed=chromaembed)
            elif message.guild.id == 694010548605550675:
                await message.channel.send(f"{message.author.mention}", embed=chroma2embed)
            else:
                pass

async def setup(bot):
    await bot.add_cog(other(bot))