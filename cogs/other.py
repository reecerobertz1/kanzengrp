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

    @commands.command()
    async def botinfo(self, ctx):
        app = await self.bot.application_info()
        if isinstance(app.owner, discord.Team):
            owner = app.team.owner
        else:
            owner = app.owner
        total_members = sum(guild.member_count for guild in self.bot.guilds)
        
        embed = discord.Embed(title=f"{self.bot.user.name} Info", color=self.color)
        embed.add_field(name="Owner", value="<@1077841960691322921>", inline=False)
        embed.add_field(name="Prefix", value="+", inline=False)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=False)
        embed.add_field(name="Total Members", value=total_members, inline=False)
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=False)
        embed.add_field(name="Name", value=self.bot.user.name, inline=False)
        embed.add_field(name="Created At", value=self.bot.user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Library", value="discord.py", inline=False)
        embed.add_field(name="Python Version", value="3.11", inline=False)
        embed.add_field(name="Uptime", value=str(self.bot.launch_time), inline=False)
        embed.add_field(name="Coded by", value="<@1077841960691322921> & <@609515684740988959>", inline=False)
        embed.set_footer(text=f"CHRT_OS // BOTINFO_v1.01", icon_url=self.bot.user.avatar.url)
        
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        if self.bot.user.banner:
            embed.set_image(url=self.bot.user.banner.url)
        else:
            embed.set_image(url=self.bot.user.avatar.url)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(other(bot))