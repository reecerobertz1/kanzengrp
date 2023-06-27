import discord
from discord.ext import commands

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        aura = 835498963418480650
        kanzen = 1122253152192831549
        stored_guild_id = 1121841073673736215
        scout_guild_id = 957987670787764224
        if member.guild.id == stored_guild_id:
            embed = discord.Embed(title='Welcome to Kanzen!', color=0x2b2d31, description=f"• Read the [rules](https://discord.com/channels/1121841073673736215/1121913361169391666)\n• Go and get your [roles](https://discord.com/channels/1121841073673736215/1121922077071507476)\n• need help? ping <@&1121842279351590973>!")
            embed.set_footer(text='Hope you enjoy your stay!', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(1121921106706710567)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention}')
            await channel.send(embed=embed)
        elif member.guild.id == scout_guild_id:
            guild = self.bot.get_guild(1121841073673736215)
            guild2 = self.bot.get_guild(957987670787764224)
            embed2 = discord.Embed(title="welcome!", color=0x303136, description=f"• Read the [rules](https://discord.com/channels/1121841073673736215/1121913361169391666)\n• Go and get your [roles](https://discord.com/channels/1121841073673736215/1121922077071507476)\n• need help? ping <@&1121842279351590973>!")
            embed2.set_footer(text='Hope you enjoy your stay!', icon_url=member.display_avatar.url)
            channel2 = self.bot.get_channel(1123274964406120479)
            await channel2.send(f'{member.mention}')
            await channel2.send(embed=embed2)
            member2 = guild.get_member(member.id)
            if member2 is None:
                await member.add_roles(member.guild.get_role(aura))
            else:
                await member.add_roles(member.guild.get_role(kanzen))

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member, ctx):
        stored_guild_id = 1121841073673736215
        if member.guild.id == stored_guild_id:
            embed = discord.Embed(title="Member left!", color=0x96bfff, description=f"{member.mention} has left the discord.")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='i hope to see you again!', icon_url=ctx.guild.icon_url)
            channel = self.bot.get_channel(1123274964406120479)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))