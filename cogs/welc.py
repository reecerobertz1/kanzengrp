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
        chromatica_guild_id = 1462079847433244799
        if member.guild.id == chromatica_guild_id:
            embed2 = discord.Embed(title=f'†    WELCOME ： {member.name.upper()}', description=f"\n・⠀01 : [Grab some roles](https://discord.com/channels/1462079847433244799/1462139108515254294)\n・⠀02 : [Apply for Chromatica](https://discord.com/channels/1462079847433244799/1462096191096361205)\n・⠀03 : [Chat to other members](https://discord.com/channels/1462079847433244799/1462281588099387432)")
            embed2.set_footer(text='CHRT_OS // MEMBER_ADDED_v1.01')
            embed2.set_thumbnail(url=member.display_avatar.url)
            view = View()
            button = Button(label="・⠀Verify here to enter", url="https://discord.com/channels/1462079847433244799/1462096750964641927", style=discord.ButtonStyle.link)
            view.add_item(button)
            
            channel3 = self.bot.get_channel(1462849510504923220)
            await channel3.send(f'{member.mention}', embed=embed2, view=view)
            await member.add_roles(member.guild.get_role(1462092433637773322))

    async def add_member(self, member_id: int, xp=5) -> None:
        query = '''INSERT INTO levelling (member_id, xp, messages, color) VALUES (?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, xp, 1, '#c45a72'))
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