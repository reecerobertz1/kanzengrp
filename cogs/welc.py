import datetime
import random
import discord
from discord.ext import commands
from discord.ui import View, Button

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
        self.kanzen_id = 1134736053803159592
        self.kanzen_welcome = 1134746303390302238
        self.hidden = True
        self.emoji = "<:shooky:1121909564799987722>"

    @commands.Cog.listener()
    async def on_member_join(self ,member: discord.Member):
        public = 835498963418480650
        role = 694016195090710579
        stored_guild_id = 694010548605550675
        scout_guild_id = 835495688832811039
        chromatica_guild_id = 1462079847433244799
        # CHROMA MEMBERS WELCOME EMBED
        if member.guild.id == stored_guild_id:
            await member.add_roles(member.guild.get_role(role))
            embed = discord.Embed(title='ᯓ Welcome to Chromagrp ༝ ⁺', color=0x2b2d31, description=f"**{member.name}** has joined !\n-# ・Please read our [rules](https://discord.com/channels/694010548605550675/725373131220320347)\n-# ・Introduce yourself in [this channel](https://discord.com/channels/694010548605550675/727875317439528982)\n-#  ⠀⠀—・⋆ Need help? Ping @leads or @staff")
            embed.set_footer(text="Thank you for joining Chroma ★ ₊ ۫ ּ")
            channel = self.bot.get_channel(725389930607673384)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention}', embed=embed)
            channel2 = self.bot.get_channel(694010549532360726)
            await channel2.send(f"{member.mention} welcome to chroma!\n• get roles in <id:customize>\n・ Our logos are in <#725373131220320347>\n・ Introduce yourself in <#727875317439528982>\n・ Please set your server nickname as `name | username` !\nAny questions, ping staff or leads <a:3b56330f710c3a978f27c9cc7e099180:836940737123057705>")
            await self.add_member(member.id)
        # CHROMA COMMUNITY WELCOME EMBED
        elif member.guild.id == scout_guild_id:
            guild = self.bot.get_guild(694010548605550675)
            guild2 = self.bot.get_guild(835495688832811039)
            embed2 = discord.Embed(color=0x2b2d31, description=f"## ᯓ Welcome {member.name} ༝ ⁺\n・ Please make sure to [verify](https://discord.com/channels/835495688832811039/1341728546946682941)\n・ Read our [rules](https://discord.com/channels/835495688832811039/1283439723053977730)\n・ Come and get your [roles](https://discord.com/channels/835495688832811039/1340656462342393918)")
            embed2.set_footer(text='Thanks for joining Chroma Community', icon_url=member.guild.icon)
            embed2.set_thumbnail(url=member.display_avatar.url)
            channel2 = self.bot.get_channel(836251337649160256)
            await channel2.send(f'{member.mention}', embed=embed2)
            member2 = guild.get_member(member.id)
            if member2 is None:
                await member.add_roles(member.guild.get_role(public))
            else:
                await member.add_roles(member.guild.get_role(836244165637046283))
        # CHROMATICA WELCOME EMBED
        elif member.guild.id == chromatica_guild_id:
            embed2 = discord.Embed(title=f'†    WELCOME ： {member.name}', description=f"\n・⠀01 : [Grab some roles](https://discord.com/channels/1462079847433244799/1462139108515254294)\n・⠀02 : [Apply for Chromatica](https://discord.com/channels/1462079847433244799/1462096191096361205)\n・⠀03 : [Chat to other members](https://discord.com/channels/1462079847433244799/1462281588099387432)")
            embed2.set_footer(text='CHRT_OS // MEMBER_ADDED_v1.01')
            embed2.set_thumbnail(url=member.display_avatar.url)
            view = View()
            button = Button(label="・⠀Verify here to enter", url="https://discord.com/channels/1462079847433244799/1462096750964641927", style=discord.ButtonStyle.link)
            view.add_item(button)
            
            channel3 = self.bot.get_channel(1462849510504923220)
            await channel3.send(f'{member.mention}', embed=embed2, view=view)
            member2 = guild.get_member(member.id)
            if member2 is None:
                await member.add_roles(member.guild.get_role(1462092433637773322))

    async def add_member(self, member_id: int, xp=5) -> None:
        query = '''INSERT INTO levelling (member_id, xp, messages, color) VALUES (?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, xp, 1, '#c45a72'))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def remove_member(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('DELETE FROM levelling WHERE member_id = $1', member_id)
                await conn.commit()
            await self.bot.pool.release(conn)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        stored_guild_id = 694010548605550675
        aster = 748021504830341330
        # CHROMA LEAVE MESSAGE
        if member.guild.id == stored_guild_id:
            channel = self.bot.get_channel(725389930607673384)
            await channel.send(f"**{member.display_name}** has left Chroma\n-# ・⋆  We will miss you ")
            await self.remove_member(member.id)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))