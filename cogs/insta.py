import discord
from discord.ext import commands
import instaloader

class instagram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loader = instaloader.Instaloader()

    @commands.command()
    async def insta(self, ctx, username: str):
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)

            embed = discord.Embed(title=f"{profile.username}", color=0x2b2d31)
            embed.set_thumbnail(url=profile.profile_pic_url)

            embed.add_field(name="Posts", value=profile.mediacount, inline=True)
            embed.add_field(name="Followers", value=profile.followers, inline=True)
            embed.add_field(name="Following", value=profile.followees, inline=True)

            await ctx.send(embed=embed)
        except instaloader.exceptions.ProfileNotExistsException:
            await ctx.send("This Instagram user does not exist.")

async def setup(bot):
    await bot.add_cog(instagram(bot))