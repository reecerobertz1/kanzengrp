import datetime
import random
import discord
from discord.ext import commands

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
        if member.guild.id == self.kanzen_id:
            embed = discord.Embed(title="Welcome to lyra!", color=0xFEF7E5, description=f"• Read the rules in <#1134744553425993799>\n• Get some roles in <#1134771998896181289>")
            role = member.guild.get_role(1134797836135964723)  
            channel = self.bot.get_channel(self.kanzen_welcome)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_image(url="https://cdn.discordapp.com/attachments/1134736054637838490/1137359950750961724/form_gfx_w_grains.png?ex=66b0c3ff&is=66af727f&hm=a8f1172d9b51a678101b5632b16bab4160228bd1fcfd9120c0d9fdc64ea78844&")
            await channel.send(f'{member.mention}', embed=embed)
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id == self.kanzen_id:
            embed = discord.Embed(title=f"Thank you for joining lyra", color=0x5e9d5e, description="We hope to see you again soon")
            embed.set_thumbnail(url=member.display_avatar.url)
            channel = self.bot.get_channel(self.kanzen_welcome)
            await channel.send(f'{member.mention}', embed=embed)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))