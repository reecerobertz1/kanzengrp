import datetime
import random
import discord
from discord.ext import commands

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
        self.kanzen_id = 1131003330810871979
        self.kanzen_welcome = 1258713117366681711
        self.hidden = True
        self.emoji = "<:shooky:1121909564799987722>"

    @commands.Cog.listener()
    async def on_member_join(self ,member: discord.Member):
        if member.guild.id == self.kanzen_id:
            embed = discord.Embed(title="welcome to kanzengrp!", color=0xb4d4b4, description=f"> • make sure to read our [server rules](https://discord.com/channels/1131003330810871979/1131005271502753812)\n> • apply for kanzen [here](https://discord.com/channels/1131003330810871979/1131005271502753812)\n> • get roles in <id:customize>")
            role = member.guild.get_role(1131016147282710679)  
            channel = self.bot.get_channel(self.kanzen_welcome)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_image(url="https://cdn.discordapp.com/attachments/1254095017878753281/1258717183203344435/welcome_image_00000.png?ex=66890f3a&is=6687bdba&hm=aa21f03c690969b974af3ed268705cb0a81ba4a5d94af30fc36495d9a34a6eb7&")
            await channel.send(f'{member.mention} <@&1131005057417105418>', embed=embed)
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id == self.kanzen_id:
            embed = discord.Embed(title=f"{member.display_name} has left Kanzen!", color=0x5e9d5e, description="We will miss you !")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again <3')
            channel = self.bot.get_channel(self.kanzen_welcome)
            await channel.send(f'{member.mention}', embed=embed)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))