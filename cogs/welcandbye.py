import datetime
import random
import discord
from discord.ext import commands

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
        self.kanzen_id = 1121841073673736215
        self.kanzen_welcome = 1121921106706710567
        self.editors_block_id = 1131003330810871979
        self.editors_block_channel = 1133767338588639323
        self.hidden = True
        self.emoji = "<:shooky:1121909564799987722>"

    @commands.Cog.listener()
    async def on_member_join(self ,member: discord.Member):
        if member.guild.id == self.kanzen_id:
            embed = discord.Embed(title='<a:kanzenflower:1128154723262943282> Welcome to Kanzen!', color=0x2b2d31, description=f"Welcome to kanzen {member.name}!\n<a:Arrow_1:1145603161701224528> Read our [information](https://discord.com/channels/1121841073673736215/1148042725950767138)\n<a:Arrow_1:1145603161701224528> Logos and hashtag are [here](https://discord.com/channels/1121841073673736215/1148042725950767138)")
            embed.set_footer(text='Need help? ping @lead or @staff', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.kanzen_welcome)
            channel2 = self.bot.get_channel(1125053619893440653)
            role = discord.utils.get(member.guild.roles, id=1121842393994494082)
            bronze = discord.utils.get(member.guild.roles, id=1187508597761003572)
            main = discord.utils.get(member.guild.roles, id=1187909432168955905)
            ranks = discord.utils.get(member.guild.roles, id=1187910861537427627)
            extra = discord.utils.get(member.guild.roles, id=1187912377388236820)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel2.send(f"<a:kanzenflower:1128154723262943282> {member.mention} Welcome to **Kanzengrp!**\nTalk to other zennies in this channel\nNeed help? ping Lead or Staff")
            await channel.send(f'{member.mention} Welcome to Kanzengrp!', embed=embed)
            await member.add_roles(role)
            await member.add_roles(bronze)
            await member.add_roles(main)
            await member.add_roles(ranks)
            await member.add_roles(extra)
            """KANZEN FORMS SERVER"""
        elif member.guild.id == self.editors_block_id:
            member_count = len(member.guild.members) 
            embed = discord.Embed(color=0x2b2d31, description=f"### 🌕 Welcome to Kanzen Forms\n<:1166196254141861979:1215213912623161364> Please read out [information](https://discord.com/channels/1131003330810871979/1131005271502753812)\n<:1166196254141861979:1215213912623161364> Apply for kanzengrp [here](https://discord.com/channels/1131003330810871979/1214940420946272316)\n<:1166196258499727480:1215213896256724992> Get roles in <id:customize>")
            role = member.guild.get_role(1131016147282710679)  
            channel = self.bot.get_channel(self.editors_block_channel)
            timestamp = datetime.datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"Thank you for joining! We are at {member_count} members!")  
            embed.set_author(name=f"{member.display_name}", icon_url=member.display_avatar.url)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention} <@&1131005057417105418>', embed=embed)
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id == self.kanzen_id:
            embed = discord.Embed(title=f"{member.display_name} has left Kanzen!", color=0x2b2d31, description="We will miss you !")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again <3')
            channel = self.bot.get_channel(self.kanzen_welcome)
            await channel.send(f'{member.mention}', embed=embed)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))