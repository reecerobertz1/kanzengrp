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
        public = 835498963418480650
        role = 694016195090710579
        stored_guild_id = 694010548605550675
        scout_guild_id = 835495688832811039
        if member.guild.id == self.kanzen_id:
            embed = discord.Embed(title="Welcome to lyra!", color=0xFEF7E5, description=f"• Read our [rules](https://discord.com/channels/1134736053803159592/1134744553425993799) and get some [roles](https://discord.com/channels/1134736053803159592/1134771998896181289)\n• Chat with other members [here](https://discord.com/channels/1134736053803159592/1134742133421658193)\n• Get to know our [leads](https://discord.com/channels/1134736053803159592/1207118201897492480) & [staff](https://discord.com/channels/1134736053803159592/1134802970031161355)")
            role = member.guild.get_role(1134797836135964723)  
            channel = self.bot.get_channel(self.kanzen_welcome)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_image(url="https://cdn.discordapp.com/attachments/1134736054637838490/1137359950750961724/form_gfx_w_grains.png?ex=66b0c3ff&is=66af727f&hm=a8f1172d9b51a678101b5632b16bab4160228bd1fcfd9120c0d9fdc64ea78844&")
            await channel.send(f'{member.mention}', embed=embed)
            await member.add_roles(role)
        elif member.guild.id == stored_guild_id:
            await member.add_roles(member.guild.get_role(role))
            embed = discord.Embed(title='<a:shookylove:1082786001958744224> __Welcome to chroma!__', color=0x2b2d31, description=f"{member.name} has joined!\n> • Please make sure to read [our rules](https://discord.com/channels/694010548605550675/725373131220320347)\n> • Introduce yourself [here](https://discord.com/channels/694010548605550675/727875317439528982)\n> • Questions? ping <@&753678720119603341> or <@&739513680860938290>\nEnjoy your time here in chroma!")
            channel = self.bot.get_channel(725389930607673384)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention}', embed=embed)
            channel2 = self.bot.get_channel(694010549532360726)
            await channel2.send(f"{member.mention} welcome to chroma!\n• get roles in <id:customize>\n• Our logos are in <#725373131220320347>\n• Introduce yourself in <#727875317439528982>\nAny questions, ping staff or leads <a:3b56330f710c3a978f27c9cc7e099180:836940737123057705>")
        elif member.guild.id == scout_guild_id:
            guild = self.bot.get_guild(694010548605550675)
            guild2 = self.bot.get_guild(835495688832811039)
            embed2 = discord.Embed(title="welcome!", color=0x303136, description=f"{member.mention} has joined the server!\n\n• read the <#835495896727814164>!\n• get editing help in <#862656708059594782>\n• talk to other editors <#836647673595428925>")
            embed2.set_footer(text='thanks for wanting to join chroma! <3', icon_url=member.display_avatar.url)
            embed2.set_thumbnail(url=member.display_avatar.url)
            channel2 = self.bot.get_channel(836251337649160256)
            await channel2.send(f'{member.mention}', embed=embed2)
            member2 = guild.get_member(member.id)
            if member2 is None:
                await member.add_roles(member.guild.get_role(public))
            else:
                await member.add_roles(member.guild.get_role(836244165637046283))

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        stored_guild_id = 694010548605550675
        if member.guild.id == self.kanzen_id:
            embed = discord.Embed(title=f"Thank you for joining lyra", color=0xFEF7E5, description="We hope to see you again soon")
            embed.set_thumbnail(url=member.display_avatar.url)
            channel = self.bot.get_channel(self.kanzen_welcome)
            await channel.send(f'{member.mention}', embed=embed)
        elif member.guild.id == stored_guild_id:
            embed = discord.Embed(title="Member left!", color=0x2b2d31, description=f"{member.mention} has left the discord.")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='i hope to see you again!', icon_url='https://cdn.discordapp.com/attachments/799984745772875786/800015677653909504/yaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.png')
            channel = self.bot.get_channel(725389930607673384)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))