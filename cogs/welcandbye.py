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
        self.server6_id = 1131003330810871979
        self.server6_channel = 1133767338588639323

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id == self.server1_id:
            embed = discord.Embed(title='<a:kanzenflower:1128154723262943282> Welcome to Kanzen!', color=0x2b2d31, description=f"Welcome to kanzen {member.name}!\n<a:bounceyarrow:1128155233437106187> Read our [information](https://discord.com/channels/1121841073673736215/1121913361169391666)\n<a:bounceyarrow:1128155233437106187> Get your roles [here](https://discord.com/channels/1121841073673736215/1139958872279359518)\n<a:bounceyarrow:1128155233437106187> Logos and hashtag are [here](https://discord.com/channels/1121841073673736215/1121913361169391666)")
            embed.set_footer(text='Need help? ping @lead or @staff', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server1_welcome_channel_id)
            channel2 = self.bot.get_channel(1125053619893440653)
            role = discord.utils.get(member.guild.roles, id=1121842393994494082)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel2.send(f"<a:kanzenflower:1128154723262943282> {member.mention} Welcome to **Kanzengrp!**\nTalk to other zennies in this channel\nNeed help? ping Lead or Staff")
            await channel.send(f'{member.mention} Welcome to Kanzengrp!', embed=embed)
            await member.add_roles(role)
            """AURA GRP WELCOME"""
        elif member.guild.id == self.server2_id:
            embed = discord.Embed(title=f'<:brazy_milksip:958479364184490075> : {member.name} has joined aura!', color=0x64a875, description=f"<a:greenarrow:1123286634629169203> Make sure you read our [rules](https://discord.com/channels/957987670787764224/958026887379173396)\n<a:greenarrow:1123286634629169203> Go and get your [roles](https://discord.com/channels/957987670787764224/1122304274408423566)\n<a:greenarrow:1123286634629169203> need help? ping <@&957993316794917024> or <@&965970726597296148>")
            embed.set_footer(text='Have fun! Thank you for joining', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server2_welcome_channel_id)
            role = discord.utils.get(member.guild.roles, id=1122253152192831549)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention}', embed=embed)
            await member.add_roles(role)
            """EDITORS BLOCK SERVER"""
        elif member.guild.id == self.server6_id:
            embed = discord.Embed(title=f'<a:bearhugz:1131122693085868172> `Welcome {member.name}`', color=0x2b2d31, description=f"<a:arrowpink:1134860720777990224> Read [infortmation](https://discord.com/channels/1131003330810871979/1131005271502753812)\n<a:arrowpink:1134860720777990224> get [roles](https://discord.com/channels/1131003330810871979/1133730290221715487)\n<a:arrowpink:1134860720777990224> apply [here](https://discord.com/channels/1131003330810871979/1133771634793250847)")
            embed.set_footer(text='Need help? ping @leads or @staff', icon_url=member.display_avatar.url)
            role = discord.utils.get(member.guild.roles, id=1141442504881864765)
            channel = self.bot.get_channel(self.server6_channel)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'{member.mention} <@&1131005057417105418>', embed=embed)
            await member.add_roles(role)

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

    @commands.Cog.listener()
    async def on_member_boost(self, member):
        server_id = member.guild.id
        channel_id = None

        if server_id == 957987670787764224:  # auragrp
            channel_id = 1123752383101542441  # aura channel
        elif server_id == 1121841073673736215:  # kanzengrp
            channel_id = 1123649005147127818  # kanzen channel
        elif server_id == 1123347338841313331:  # aura forms
            channel_id = 1123752056772104252  # aura forms channel
        elif server_id == 1122181605591621692:  # kanzengrp forms
            channel_id = 1123755909089337364  # kanzen forms channel
        elif server_id == 1131003330810871979:  # editors block
            channel_id = 1133772140915732511  # boost editors block

        if channel_id:
            channel = self.bot.get_channel(channel_id)
            embed = discord.Embed(title=f"{member.name} thank you for boosting!", description='<a:greenarrow:1123286634629169203> do `+perks` to get the booster perks!\n<a:greenarrow:1123286634629169203> dm a lead or co lead for your custom role\n<a:greenarrow:1123286634629169203> we really appreciate the support', color=0x2b2d31)
            await channel.send(f'{member.mention}', embed=embed)

    @commands.command()
    async def perks(self, ctx):
        server_id = ctx.guild.id

        if server_id in [957987670787764224, 1123347338841313331]:
            channel_ids = [1122994947444973709, 1123991454788894820]  
            message = discord.Embed(title="Perks command has been used!", description=f"`{ctx.author.display_name}` has used the perks command!", color=0x2b2d31)
            message.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
            for channel_id in channel_ids:
                channel = self.bot.get_channel(channel_id)
                await channel.send(embed=message)

            embed = discord.Embed(title="Aura Perks", description="Thank you for boosting aura!\n[Click here for the booster pack!](https://mega.nz/folder/QpkzFIRB#FHWAnwOGU6-0vZQ_AjDn8g)", color=0x2b2d31)
            embed.add_field(name="Remqsi's pack", value="<a:greenarrow:1123286634629169203> Remqsi's colouring packs 1 & 2\n<a:greenarrow:1123286634629169203> BTS Photos\n<a:greenarrow:1123286634629169203> Enhypen Photos\n<a:greenarrow:1123286634629169203> Blackpink Photos", inline=False)
            embed.add_field(name="Yoongiaeps pack", value="<a:greenarrow:1123286634629169203> AE effects\n<a:greenarrow:1123286634629169203> AE shakes\n<a:greenarrow:1123286634629169203> BTS photos\n<a:greenarrow:1123286634629169203> Itzy photos\n<a:greenarrow:1123286634629169203> Kep1er photos\n<a:greenarrow:1123286634629169203> Twice photos", inline=False)
            embed.set_footer(text="We really appreciate the support!")

            if ctx.author.premium_since:
                await ctx.author.send(embed=embed)
            else:
                await ctx.send("Sorry, this command is only available for server boosters")

        elif server_id in [1121841073673736215, 1122181605591621692]:
            channel_ids = [1122627075682078720, 1123991325763711096]  
            message = discord.Embed(title="Perks command has been used!", description=f"`{ctx.author.display_name}` has used the perks command!", color=0x2b2d31)
            message.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.display_avatar)
            for channel_id in channel_ids:
                channel = self.bot.get_channel(channel_id)
                await channel.send(embed=message)

            embed = discord.Embed(title="Kanzen Perks", description="Thank you for boosting kanzengrp!\n[Click here for the booster pack!](https://mega.nz/folder/N1tgSLqD#DZ73U23GXk1LqyZKUpdNww)", color=0x2b2d31)
            embed.add_field(name="Remqsi's pack", value="<a:bounceyarrow:1126865547255091343> Remqsi's colouring packs 1 & 2\n<a:bounceyarrow:1126865547255091343> BTS Photos\n<a:bounceyarrow:1126865547255091343> Enhypen Photos\n<a:bounceyarrow:1126865547255091343> Blackpink Photos\n<a:bounceyarrow:1126865547255091343> Break your heart project file\n<a:bounceyarrow:1126865547255091343> Lisa candy project file", inline=False)
            embed.set_footer(text="We really appreciate the support!")

            if ctx.author.premium_since:
                await ctx.author.send(embed=embed)
            else:
                await ctx.send("Sorry, this command is only available for server boosters")

async def setup(bot):
    await bot.add_cog(welcandleave(bot))