import discord
from discord.ext import commands
from datetime import datetime, timezone
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

                if 'banner' in data:
                    return f"https://cdn.discordapp.com/banners/{user.id}/{data['banner']}.png?size=2048"

        return None

    def get_badges(self, member: discord.Member, user: discord.User, flags: str, badgeslist: list) -> None:
        if "hypesquad_balance" in str(flags):
            badgeslist.append("<:balance_icon:937770399880585287> HypeSquad Balance")
        elif "hypesquad_bravery" in str(flags):
            badgeslist.append("<:bravery_icon:937767201094631444> HypeSquad Bravery")
        elif "hypesquad_brilliance" in str(flags):
            badgeslist.append("<:brilliance_icon:937770447838281758> HypeSquad Brilliance")
        if "active_developer" in str(flags):
            badgeslist.append("<:active_dev:1078684899172692020> Active Developer")
        if member.avatar.is_animated():
            badgeslist.append("<:nitro_icon:937770475625525289> Nitro")
        elif member.discriminator == "0001":
            badgeslist.append("<:nitro_icon:937770475625525289> Nitro")
        elif member.premium_since is not None:
            badgeslist.append("<:nitro_icon:937770475625525289> Nitro")
        elif user.banner is not None:
            badgeslist.append("<:nitro_icon:937770475625525289> Nitro")
        if member.premium_since is not None:
            badgeslist.append("<a:boost:938021210984419338> Booster")

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

        embed = discord.Embed(title=f"{member.name}", color=0x2b2d31)
        embed.add_field(name="Activity", value=f"Active for the **{online_days} days, {online_hours} hours**", inline=False)
        embed.add_field(name="Joined Discord", value=discord_join_date, inline=False)
        embed.add_field(name="Joined", value=server_join_date, inline=False)
        embed.add_field(name="Nickname", value=nickname, inline=False)
        embed.add_field(name="Badges", value=' '.join(str(badge) for badge in badgeslist) if badgeslist else "None", inline=False)

        if avatar_url:
            embed.set_thumbnail(url=avatar_url)

        if banner_url:
            embed.set_image(url=banner_url)

        await ctx.reply(embed=embed)

    async def get_banner_url(self, user):
        # Placeholder implementation for getting banner URL
        return None

            

        await ctx.reply(embed=embed)



async def setup(bot):
    await bot.add_cog(MemberInfo(bot))