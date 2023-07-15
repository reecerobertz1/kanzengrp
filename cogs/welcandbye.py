import discord
from discord.ext import commands

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.server1_id = 1121841073673736215
        self.server1_welcome_channel_id = 1121921106706710567
        self.server2_id = 957987670787764224
        self.server2_welcome_channel_id = 1123274964406120479
        self.server3_id = 1123347338841313331
        self.server3_channel = 1123347339797594144
        self.server4_id = 1122181605591621692
        self.server4_channel = 1123334440727367730
        self.server5_id = 896619762354892821
        self.server5_channel = 896924663819694132

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id == self.server1_id:
            embed = discord.Embed(title='Welcome to Kanzen!', color=0x2b2d31, description=f"<a:bounceyarrow:1128155233437106187> Read the [rules](https://discord.com/channels/1121841073673736215/1121913361169391666)\n<a:bounceyarrow:1128155233437106187> Go and get your [roles](https://discord.com/channels/1121841073673736215/1121922077071507476)\n<a:bounceyarrow:1128155233437106187> Need help? Ping <@&1121842279351590973>!")
            embed.set_footer(text='Hope you enjoy your stay!', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server1_welcome_channel_id)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'<a:kanzenflower:1128154723262943282> {member.mention} welcome to kanzen!', embed=embed)
            """AURA GRP WELCOME"""
        elif member.guild.id == self.server2_id:
            embed = discord.Embed(title=f'<:brazy_milksip:958479364184490075> : {member.name} has joined aura!', color=0x64a875, description=f"<a:greenarrow:1123286634629169203> Make sure you read our [rules](https://discord.com/channels/957987670787764224/958026887379173396)\n<a:greenarrow:1123286634629169203> Go and get your [roles](https://discord.com/channels/957987670787764224/1122304274408423566)\n<a:greenarrow:1123286634629169203> need help? ping <@&957993316794917024> or <@&965970726597296148>")
            embed.set_footer(text='Have fun! Thank you for joining', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server2_welcome_channel_id)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention}', embed=embed)
            """AURA FORMS"""
        elif member.guild.id == self.server3_id:
            embed = discord.Embed(title=f'<:brazy_milksip:958479364184490075> : {member.name} has joined the server!', color=0x64a875, description=f"<a:greenarrow:1123286634629169203> Make sure you read our [rules](https://discord.com/channels/1123347338841313331/1123351779158016060)\n<a:greenarrow:1123286634629169203> Go and get your [roles](https://discord.com/channels/1123347338841313331/1123351943549562950)\n<a:greenarrow:1123286634629169203> apply [here!](https://discord.com/channels/1123347338841313331/1123352172143329331)\n<a:greenarrow:1123286634629169203> need help? ping <@&1123347897715527802> or <@&1123347913964269718>")
            embed.set_footer(text='Have fun! Thank you for joining', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server3_channel)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention} <@&1123361940895445032>', embed=embed)
            """KANZEN FORMS"""
        elif member.guild.id == self.server4_id:
            embed = discord.Embed(title=f'<:brazy_milksip:958479364184490075> : {member.name} has joined the server!', color=0x2b2d31, description=f"• Make sure you read our [rules](https://discord.com/channels/1122181605591621692/1122195332516810873)\n• Go and get your [roles](https://discord.com/channels/1122181605591621692/1123334720969789521)\n• apply [here!](https://discord.com/channels/1122181605591621692/1122195260735500348)\n• need help? ping <@609515684740988959>")
            embed.set_footer(text='Have fun! Thank you for joining', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server4_channel)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'<a:kanzenflower:1128154723262943282> {member.mention} <@&1123374988808962099>', embed=embed)
            """DAEGU"""
        elif member.guild.id == self.server5_id:
            embed = discord.Embed(title=f'<:members:1119069738493026364> : {member.name} has joined the server!', color=0x2b2d31, description=f"• Make sure you read our [server info](https://discord.com/channels/896619762354892821/896924214311911476)\n• Go and get your [roles](https://discord.com/channels/896619762354892821/1062169874748686386) + [biases](https://discord.com/channels/896619762354892821/1044478054258458685)\n• need help? ping <@&896881532671754260>, <@&1119948686550630410> or <@&903955975000698922>")
            embed.set_footer(text='Have fun! Thank you for joining', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server5_channel)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention}', embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id == self.server1_id:
            embed = discord.Embed(title=f"{member.display_name} has left Kanzen!", color=0x2b2d31, description="We will miss you !")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again <3')
            channel = self.bot.get_channel(self.server1_welcome_channel_id)
            await channel.send(f'{member.mention}', embed=embed)
            """AURA GRP LEAVE"""
        elif member.guild.id == self.server2_id:
            embed = discord.Embed(title=f"{member.display_name} has left Aura!", color=0x6475a8, description="We will miss you !")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again soon !!')
            channel = self.bot.get_channel(self.server2_welcome_channel_id)
            await channel.send(f'{member.mention}', embed=embed)
            """DAEGU LEAVE"""
        elif member.guild.id == self.server5_id:
            embed = discord.Embed(title=f"{member.display_name} has left Daegu!", color=0x2b2d31, description="We will miss you !")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again soon !!')
            channel = self.bot.get_channel(self.server5_channel)
            await channel.send(f'{member.mention}', embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.premium_since and after.premium_since:
            server_id = after.guild.id
            channel_id = None
            
            if server_id == 957987670787764224: # auragrp
                channel_id = 1123752383101542441 #aura channel
            elif server_id == 1121841073673736215: # kanzengrp
                channel_id = 1123649005147127818 #kanzen channel
            elif server_id == 1123347338841313331: #aura forms
                channel_id = 1123752056772104252 #aura forms channel
            elif server_id == 1122181605591621692: #kanzengrp forms
                channel_id = 1123755909089337364 #kanzen forms channel
            
            if channel_id:
                channel = self.bot.get_channel(channel_id)
                embed = discord.Embed(title=f"{after.name} thank you for boosting!",description='<a:greenarrow:1123286634629169203> do `+perks` to get the booster perks!\n<a:greenarrow:1123286634629169203> dm a lead or co lead for your custom role\n<a:greenarrow:1123286634629169203> we really appriciate the support', color=0x2b2d31)
                await channel.send(f'{after.mention}')
                await channel.send(embed=embed)

    @commands.command()
    async def perks(self, ctx):
        server_id = ctx.guild.id

        if server_id in [957987670787764224, 1123347338841313331]:
            channel_ids = [1122994947444973709, 1123991454788894820]  
            message = f"{ctx.author.mention} has used the perks command!"
            for channel_id in channel_ids:
                channel = self.bot.get_channel(channel_id)
                await channel.send(message)

            embed = discord.Embed(title="Aura Perks", description="Thank you for boosting aura!", color=0x2b2d31)
            embed.add_field(name="Remqsi's pack", value="", inline=False)
            embed.add_field(name="Perk 2", value="Perk 2 description", inline=False)
            embed.set_footer(text="We really appreciate the support!")

            if ctx.author.premium_since:
                await ctx.author.send(embed=embed)
            else:
                await ctx.send("Sorry, this command is only available for server boosters")

        elif server_id in [1121841073673736215, 1122181605591621692]:
            channel_ids = [1122627075682078720, 1123991325763711096]  
            message = f"{ctx.author.mention} has used the perks command!"
            for channel_id in channel_ids:
                channel = self.bot.get_channel(channel_id)
                await channel.send(message)

            embed = discord.Embed(title="Kanzen Perks", description="Thank you for boosting kanzengrp!", color=0x2b2d31)
            embed.add_field(name="Perk 3", value="Perk 3 description", inline=False)
            embed.add_field(name="Perk 4", value="Perk 4 description", inline=False)
            embed.set_footer(text="We really appreciate the support!")

            if ctx.author.premium_since:
                await ctx.author.send(embed=embed)
            else:
                await ctx.send("Sorry, this command is only available for server boosters")



async def setup(bot):
    await bot.add_cog(welcandleave(bot))