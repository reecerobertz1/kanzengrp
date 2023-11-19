import datetime
import random
import discord
from discord.ext import commands

class welc(discord.ui.View):
    def __init__ (self, member):
        super().__init__(timeout=None)
        self.value = None
        self.member = member

    @discord.ui.button(label=f"Wave", emoji="<:brazy_milksip:958479364184490075>")
    async def guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        gifs = [
            "https://tenor.com/view/bts-jin-suga-j-hope-rm-gif-15564709",
            "https://tenor.com/view/bts-hello-bts-hello-bts-wave-wave-gif-23901650",
            "https://tenor.com/view/jimin-bts-wave-korean-korean-entertainment-gif-11065936",
            "https://tenor.com/view/bts-bangtan-boys-bangtan-sonyeondan-kpop-rm-gif-17936283",
            "https://tenor.com/view/jikook-jimin-jungkook-wave-bts-gif-18607625",
            "https://tenor.com/view/bts-jhope-bts-hobi-hobi-wave-hobi-bye-gif-24841251",
            "https://tenor.com/view/bts-hello-yoongi-wave-bye-gif-14546847",
            "https://tenor.com/view/bts-bangtan-boys-bangtan-sonyeondan-bts-v-kim-taehyung-gif-17366668",
            "https://tenor.com/view/hi-hello-cute-so-hobi-gif-12926594",
            "https://tenor.com/view/jimin-bts-hi-wave-gif-13871104",
            "https://tenor.com/view/bts-hello-wave-hi-hey-gif-10308098",
            "https://tenor.com/view/taehyung-bts-wave-wink-gif-22711528",
            "https://tenor.com/view/bts-rm-namjoon-wave-hi-gif-15366897",
            "https://tenor.com/view/bts-k-pop-ccg-bangtan-sonyeondan-tae-gif-14767559",
            "https://tenor.com/view/kookie-jungkook-bts-vlive-funny-gif-21382895",
            "https://tenor.com/view/min-yoongi-suga-rapper-bts-suga-bts-gif-17828015",
           "https://tenor.com/view/bts-jhope-hobi-hoseok-hello-gif-12444850",
            "https://tenor.com/view/jungkook-hi-hello-wave-gif-14290086",
            "https://tenor.com/view/bts-bangtan-boys-bangtan-sonyeondan-rap-monster-kim-namjoon-gif-17180284",
            "https://tenor.com/view/bts-suga-big-hit-entertainment-bangtan-boys-kpop-gif-16055359",
            "https://tenor.com/view/bts-jin-wave-cute-kpop-gif-13657754",
            "https://tenor.com/view/pjmtii-jungkook-wave-bts-gif-22905798",
            "https://tenor.com/view/bts-bts-hi-wave-kpop-gif-22929533",
            "https://tenor.com/view/wave-gif-18897262",
            "https://tenor.com/view/blackpink-lisa-lilifilm-vlog-with-jisoo-wave-gif-21466675",
            "https://tenor.com/view/blackpink-jisoo-wave-gif-19354205",
            "https://tenor.com/view/blackpink-wave-jisoo-ros%C3%A9-jennie-gif-19710205",
            "https://tenor.com/view/blackpink-lisa-photobook-wave-gif-21164172",
            "https://tenor.com/view/blackpink-wave-gif-19335519",
            "https://tenor.com/view/jennie-kim-jennie-blow-kiss-hi-black-pink-gif-15906924",
            "https://tenor.com/view/blackpink-happy-smile-kimjisoo-jisoo-gif-13226528",
            "https://tenor.com/view/blackpink-ros%C3%A9-chaeyoung-ya-hello-gif-21069665",
            "https://tenor.com/view/blackpink-jennie-wave-the-show-vlog-gif-20310411",
            "https://tenor.com/view/hi-hello-wave-lisa-lalisa-gif-14924995",
            "https://tenor.com/view/blackpink-wave-bye-love-gif-19335534",
            "https://tenor.com/view/jennie-jennie-wave-jennie-hi-jennie-hello-blackpink-hi-gif-26445042",
            "https://tenor.com/view/blackpink-jennie-wave-smile-smiling-gif-19975699",
            "https://tenor.com/view/blackpink-jisoo-wave-kiss-smile-gif-20086330",
            "https://tenor.com/view/blackpink-touch-cute-jisoo-jennie-gif-13625042",
            "https://tenor.com/view/blackpink-jennie-wave-smile-gif-19975801",
            "https://tenor.com/view/rose-roseanne-park-blackpink-kpop-cute-gif-15535366",
            "https://tenor.com/view/sushichaeng-blackpink-jennie-jennie-kim-jennie-cute-gif-21481445",
            "https://tenor.com/view/blackpink-wave-bye-jennie-flying-kiss-gif-15741931",
            "https://tenor.com/view/blackpink-lisoo-lisa-jisoo-wave-gif-21466840",
            "https://tenor.com/view/lisa-lisa-manoban-hello-cute-smile-gif-15880375",
            "https://tenor.com/view/blackpink-curly-hair-wave-hands-gif-13323734",
            "https://tenor.com/view/lesserafim-yunjin-blows-kiss-with-candy-lesserafim-yunjin-huh-yunjin-mwah-gif-26468116",
            "https://tenor.com/view/kazuha-lesserafim-kazuha-lesserafim-nakamura-kazuha-gif-387759147393748565",
            "https://tenor.com/view/kazuha-nakamura-kazuha-lesserafim-le-sserafim-wave-gif-7028135244005719993",
            "https://tenor.com/view/le-sserafim-chaewon-kpop-lesserafim-k-pop-gif-5305875374031120683",
            "https://tenor.com/view/izone-sakura-izone-miyawaki-sakura-sakura-miyawaki-bye-bye-gif-18000800"
        ]
        welcomer = interaction.user.name
        hello = random.choice(gifs)
        await interaction.response.send_message(f"{welcomer} has welcomed {self.member} to Kanzengrp!")
        await interaction.followup.send(f"{hello}")

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
        self.server1_id = 1121841073673736215
        self.server1_welcome_channel_id = 1121921106706710567
        self.server2_id = 957987670787764224
        self.server2_welcome_channel_id = 1123274964406120479
        self.server6_id = 1131003330810871979
        self.server6_channel = 1133767338588639323
        self.hidden = True

    @commands.Cog.listener()
    async def on_member_join(self ,member: discord.Member):
        if member.guild.id == self.server1_id:
            embed = discord.Embed(title='<a:kanzenflower:1128154723262943282> Welcome to Kanzen!', color=0x2b2d31, description=f"Welcome to kanzen {member.name}!\n<a:bounceyarrow:1128155233437106187> Read our [information](https://discord.com/channels/1121841073673736215/1121913361169391666)\n<a:bounceyarrow:1128155233437106187> Get your roles [here](https://discord.com/channels/1121841073673736215/1139958872279359518)\n<a:bounceyarrow:1128155233437106187> Logos and hashtag are [here](https://discord.com/channels/1121841073673736215/1121913361169391666)")
            embed.set_footer(text='Need help? ping @lead or @staff', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server1_welcome_channel_id)
            channel2 = self.bot.get_channel(1125053619893440653)
            role = discord.utils.get(member.guild.roles, id=1121842393994494082)
            embed.set_thumbnail(url=member.display_avatar.url)
            view = welc(member)
            await channel2.send(f"<a:kanzenflower:1128154723262943282> {member.mention} Welcome to **Kanzengrp!**\nTalk to other zennies in this channel\nNeed help? ping Lead or Staff", view=view)
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
            member_count = len(member.guild.members) 
            embed = discord.Embed(color=0x2b2d31, description=f"<a:arrowlightpink:1141452054716489789> [read infortmation](https://discord.com/channels/1131003330810871979/1131005271502753812)\n<a:arrowlightpink:1141452054716489789> [get roles](https://discord.com/channels/1131003330810871979/1133730290221715487)\n<a:arrowlightpink:1141452054716489789> [apply here](https://discord.com/channels/1131003330810871979/1133771634793250847)")
            role = member.guild.get_role(1141442504881864765)  
            channel = self.bot.get_channel(self.server6_channel)
            timestamp = datetime.datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"Member Count: {member_count}")  
            embed.set_author(name=f"{member.display_name}", icon_url=member.display_avatar.url)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'Welcome {member.mention} <@&1131005057417105418>', embed=embed)
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