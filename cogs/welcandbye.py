import discord
from discord.ext import commands

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.server1_id = 1121841073673736215
        self.server1_welcome_channel_id = 1121921106706710567
        self.server2_id = 123456789012345678
        self.server2_welcome_channel_id = 123456789012345678

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id == self.server1_id:
            embed = discord.Embed(title='Welcome to Kanzen!', color=0x2b2d31, description=f"• Read the [rules](https://discord.com/channels/1121841073673736215/1121913361169391666)\n• Go and get your [roles](https://discord.com/channels/1121841073673736215/1121922077071507476)\n• Need help? Ping <@&1121842279351590973>!")
            embed.set_footer(text='Hope you enjoy your stay!', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server1_welcome_channel_id)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention}')
            await channel.send(embed=embed)
        elif member.guild.id == self.server2_id:
            embed = discord.Embed(title='Welcome to Server2!', color=0x2b2d31, description=f"Welcome to Server2, {member.mention}!")
            embed.set_footer(text='Enjoy your time here!', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server2_welcome_channel_id)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention}')
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id == self.server1_id:
            embed = discord.Embed(title=f"{member.name} has left Kanzen!", color=0x2b2d31, description=f"{member.mention}, we will miss you!")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again <3')
            channel = self.bot.get_channel(self.server1_welcome_channel_id)
            await channel.send(embed=embed)
        elif member.guild.id == self.server2_id:
            embed = discord.Embed(title=f"{member.name} has left Server2!", color=0x2b2d31, description=f"{member.mention}, we'll miss you!")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Farewell <3')
            channel = self.bot.get_channel(self.server2_welcome_channel_id)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))