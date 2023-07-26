import asyncio
import platform
import time
from typing import Optional
import humanize
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import aiohttp

class MemberInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_banner_url(self, user):
        headers = {
            'Authorization': f'Bot {self.bot.http.token}',
            'User-Agent': 'DiscordBot (https://github.com/yourusername/yourbot, 1.0)'
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'https://discord.com/api/v9/users/{user.id}') as response:
                data = await response.json()

                if 'banner' in data and data['banner']:
                    return f"https://cdn.discordapp.com/banners/{user.id}/{data['banner']}.png?size=2048"

        return None

    async def get_user_data(self, user_id):
        # Function to get user data. Replace with your data retrieval logic.
        # Example:
        return {
            "last_seen": None,
            "online_since": None
        }

    def get_badges(self, member: discord.Member, user: discord.User, flags: str, badgeslist: list) -> None:
        if "hypesquad_balance" in str(flags):
            badgeslist.append("<:balance:1122699998635753532> HypeSquad Balance")
        elif "hypesquad_bravery" in str(flags):
            badgeslist.append("<:6601hypesquadbravery:1122699733186654248> HypeSquad Bravery")
        elif "hypesquad_brilliance" in str(flags):
            badgeslist.append("<:brilliance:1122700238361206816> HypeSquad Brilliance")
        if "active_developer" in str(flags):
            badgeslist.append("<:7011activedeveloperbadge:1122700402442383450> Active Developer")
        if member.avatar.is_animated():
            badgeslist.append("<:nitro:1122703008220860468> Nitro")
        elif member.discriminator == "0001":
            badgeslist.append("<:nitro:1122703008220860468> Nitro")
        elif member.premium_since is not None:
            badgeslist.append("<:nitro:1122703008220860468> Nitro")
        elif user.banner is not None:
            badgeslist.append("<:nitro:1122703008220860468> Nitro")
        if member.premium_since is not None:
            badgeslist.append("<a:938021210984419338:1122702983277330512> Booster")

    @commands.command()
    async def userinfo(self, ctx, member: Optional[discord.Member] = None):
        if member is None:
            member = ctx.author

        createdat = member.created_at
        joinedat = member.joined_at
        created = time.mktime(createdat.timetuple())
        joined = time.mktime(joinedat.timetuple())
        flags = member.public_flags.all()
        badgeslist = []
        user = await self.bot.fetch_user(member.id)
        self.get_badges(member, user, flags, badgeslist)
        badges = ' \n'.join([str(elem) for elem in badgeslist])

        embed = discord.Embed(title=member.name, color=0x2b2d31)
        if user.banner is not None:
            embed.set_image(url=user.banner)
        embed.set_thumbnail(url=member.avatar.url)

        data = await self.get_user_data(member.id)
        try:
            if data['last_seen'] is None:
                embed.add_field(name="<:status_online:998595341450481714> Activity",
                                value=f'Active for **{humanize.precisedelta(discord.utils.utcnow() - data["online_since"], minimum_unit="seconds", format="%0.0f")}**',
                                inline=False)
            else:
                embed.add_field(name="<:status_offline:998595266062061653> Activity",
                                value=f'Went offline {discord.utils.format_dt(data["last_seen"], "R")}',
                                inline=False)
        except Exception as error:
            if str(error) == "'NoneType' object is not subscriptable":
                return
            else:
                print(error)

        embed.add_field(name="<:1faaa:1122701643536937011> Nickname:", value=member.nick, inline=False)
        embed.add_field(name="<:concoursdiscordcartesvoeuxfortni:1122702096085549076> Joined Discord:", value=f"<t:{int(created)}:D> (<t:{int(created)}:R>)", inline=False)
        embed.add_field(name=f"<:dash:1123654552843993099> Joined {ctx.guild.name}", value=f"<t:{int(joined)}:D> (<t:{int(joined)}:R>)", inline=False)

        # Extract Instagram account from the nickname
        if member.nick:
            instagram_account = member.nick.split("|")[-1].strip()
            embed.add_field(name="<:instagram:1128753024718872717> Instagram",
                            value=f"[{instagram_account}](https://www.instagram.com/{instagram_account})", inline=False)

        if len(badgeslist) > 0:
            embed.add_field(name="<a:badges:938023584142622791> Badges", value=f"{badges}", inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["hoshiinfo", "about"])
    async def abouthoshi(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        days, hours = divmod(hours, 24)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(title="About Hoshi", description=f"Hoshi is a multi-purpose bot made for [kanzengrp](https://instagram.com/kanzengrp)\nFor help with commands, do `+help`\n", color=0x2b2d31)
        embed.add_field(name="** **", value=f"** Hoshi was made on:** {discord.utils.format_dt(self.bot.user.created_at, 'D')}", inline=False)
        embed.add_field(name="** **", value=f"**Last reboot:** {discord.utils.format_dt(self.bot.launch_time, 'D')}", inline=False)
        embed.add_field(name="** **", value=f"**Uptime:** {days} days, {hours} hours, {minutes} minutes, {seconds} seconds", inline=False)
        embed.add_field(name="** **", value=f"**Total users:** {sum(g.member_count for g in self.bot.guilds)}", inline=False)
        embed.add_field(name="** **", value=f"**Total Servers:** {len(ctx.bot.guilds)}")
        embed.add_field(name="** **", value=f"**Python version:** {platform.python_version()}", inline=False)
        embed.add_field(name='** **', value=f"**Discord.py version:** {discord.__version__}", inline=False)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Made by {self.bot.application.owner.name}")

        message = await ctx.send(embed=embed)

        # Simulate some action that takes time
        await asyncio.sleep(1)

        # Update the embed with the latency as the ping value
        latency = round(self.bot.latency * 1000, 2)
        embed.set_field_at(5, name="** **", value=f"**Latency:** {latency}ms", inline=False)

        # Edit the message with the updated embed
        await message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(MemberInfo(bot))