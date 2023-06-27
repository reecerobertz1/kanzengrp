import discord
from discord.ext import commands

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.server1_id = 1121841073673736215
        self.server1_welcome_channel_id = 1121921106706710567
        self.server2_id = 957987670787764224
        self.server2_welcome_channel_id = 1123274964406120479

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
            embed = discord.Embed(title=f'<:brazy_milksip:958479364184490075> : {member.name} has joined aura!', color=0x64a875, description=f"<a:greenarrow:1123286634629169203> Make sure you read our [rules](https://discord.com/channels/957987670787764224/958026887379173396)\n<a:greenarrow:1123286634629169203> Go and get your [roles](https://discord.com/channels/957987670787764224/1122304274408423566)\n<a:greenarrow:1123286634629169203> need help? ping <@&957993316794917024> or <@&965970726597296148>")
            embed.set_footer(text='Have fun! Thank you for joining', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server2_welcome_channel_id)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention}')
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id == self.server1_id:
            embed = discord.Embed(title=f"{member.name} has left Kanzen!", color=0x2b2d31, description="We will miss you !")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again <3')
            channel = self.bot.get_channel(self.server1_welcome_channel_id)
            await channel.send(embed=embed)
            """AURA GRP LEAVE"""
        elif member.guild.id == self.server2_id:
            embed = discord.Embed(title=f"{member.name} has left Aura!", color=0x6475a8, description="We will miss you !")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again soon !!')
            channel = self.bot.get_channel(self.server2_welcome_channel_id)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))