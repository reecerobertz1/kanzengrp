import asyncio
import platform
import time
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
    async def memberinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        now = datetime.now(timezone.utc)
        joined_at_utc = member.joined_at.replace(tzinfo=timezone.utc)

        online_duration = now - joined_at_utc
        online_days = online_duration.days
        online_hours = online_duration.seconds // 3600

        discord_join_date = member.created_at.strftime("%A, %B %d %Y")
        server_join_date = member.joined_at.strftime("%A, %B %d")

        nickname = member.nick
        badges = member.public_flags.all()

        user = member
        avatar_url = user.avatar.url if user.avatar else None
        banner_url = await self.get_banner_url(user)

        badgeslist = []
        self.get_badges(member, user, badges, badgeslist)

        # Extract Instagram account from the member nickname
        instagram_account = nickname.split("|")[-1].strip()

        embed = discord.Embed(title=f"{member.name}", color=0x2b2d31)
        embed.add_field(name="<:instagram:1128753024718872717> Instagram", value=f"[{instagram_account}](https://www.instagram.com/{instagram_account})", inline=False)
        embed.add_field(name="<:concoursdiscordcartesvoeuxfortni:1122702096085549076> Joined Discord", value=discord_join_date, inline=False)
        embed.add_field(name="<:dash:1123654552843993099> Joined", value=server_join_date, inline=False)
        embed.add_field(name="<:1faaa:1122701643536937011> Nickname", value=nickname, inline=False)
        embed.set_footer(text=f'Member ID {user.id}')
        if badgeslist:
            embed.add_field(name="<a:938023584142622791:1122700150641528873> Badges", value='\n'.join(badgeslist), inline=False)
        else:
            embed.add_field(name="<a:938023584142622791:1122700150641528873> Badges", value="None", inline=False)

        if avatar_url:
            embed.set_thumbnail(url=avatar_url)

        if banner_url:
            embed.set_image(url=banner_url)

        await ctx.reply(embed=embed)

        self.start_time = datetime.utcnow()

    @commands.command(aliases=["hoshiinfo", "about"])
    async def abouthoshi(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        days, hours = divmod(hours, 24)
        minutes, seconds = divmod(remainder, 60)

        embed = discord.Embed(title="About Hoshi", description=f"Hoshi is a multi-purpose bot made for [kanzengrp](https://instagram.com/kanzengrp)\nFor help with commands, do `+help`\n", color=0x2b2d31)
        embed.add_field(name="Hoshi was made on", value=f"{discord.utils.format_dt(self.bot.user.created_at, 'D')}", inline=False)
        embed.add_field(name="Last reboot", value=f"{discord.utils.format_dt(self.bot.launch_time, 'D')}", inline=False)
        embed.add_field(name="Uptime", value=f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds", inline=False)
        embed.add_field(name="Total users", value=f"{sum(g.member_count for g in self.bot.guilds)}", inline=False)
        embed.add_field(name="Python version", value=f"{platform.python_version()}", inline=False)
        embed.add_field(name="Discord.py version", value=f"{discord.__version__}", inline=False)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"Made by {self.bot.application.owner.name}")

        message = await ctx.send(embed=embed)

        # Simulate some action that takes time
        await asyncio.sleep(1)

        # Update the embed with the latency as the ping value
        latency = round(self.bot.latency * 1000, 2)
        embed.set_field_at(5, name="Latency", value=f"{latency}ms", inline=False)

        # Edit the message with the updated embed
        await message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(MemberInfo(bot))