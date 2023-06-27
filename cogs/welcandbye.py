import discord
from discord.ext import commands

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id == 1121841073673736215:
            embed = discord.Embed(title='Welcome to Kanzen!', color=0x2b2d31, description=f"• Read the [rules](https://discord.com/channels/1121841073673736215/1121913361169391666)\n• Go and get your [roles](https://discord.com/channels/1121841073673736215/1121922077071507476)\n• need help? ping <@&1121842279351590973>!")
            embed.set_footer(text='Hope you enjoy your stay!', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(1121921106706710567)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention}')
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id == 1121841073673736215:
            embed = discord.Embed(title=f"{member.name} has left kanzen!", color=0x2b2d31, description=f"{member.mention} We will miss you!")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again <3')
            channel = self.bot.get_channel(1121921106706710567)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))