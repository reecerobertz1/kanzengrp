import discord
from discord.ext import commands

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member, ctx):
        channel_id = 1121921106706710567  
        channel = self.bot.get_channel(channel_id)
        if channel:
            mention = member.mention
            await channel.send(f"{mention}")
            
            embed = discord.Embed(title=f"Welcome to Kanzen {member.name}!", description=f"Welcome {mention} to the kanzen!\n﹒Please read the [Rules](https://discord.com/channels/1121841073673736215/1121913361169391666)\n﹒Go get your [Roles](https://discord.com/channels/1121841073673736215/1121922077071507476)\n﹒The logos are [here](https://discord.com/channels/1121841073673736215/1121922101708857344)", color=0x2b2d31)
            embed.set_thumbnail(url=f'{member.avatar}')
            embed.set_footer(text='Have fun! Thank you for joining <3')
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel_id = 1121921106706710567  
        channel = self.bot.get_channel(channel_id)
        if channel:
            mention = member.mention
            await channel.send(f"{mention}")
            
            embed = discord.Embed(title="Goodbye!", description=f"Goodbye {mention}! We'll miss you!", color=0x2b2d31)
            embed.set_thumbnail(url=f'{member.avatar}')
            embed.set_footer(text='Hope to see you again soon <3')
            await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(welcandleave(bot))