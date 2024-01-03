import datetime
import random
import discord
from discord.ext import commands

class welc(discord.ui.View):
    def __init__ (self, member):
        super().__init__(timeout=None)
        self.value = None
        self.member = member

    @discord.ui.button(label=f"Wave", emoji="<a:jkwave:1179680953501753466>")
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
        await interaction.response.send_message(f"{welcomer} has welcomed {self.member} to {interaction.guild.name}!")
        await interaction.followup.send(f"{hello}")

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
        self.server1_id = 1121841073673736215
        self.server1_welcome_channel_id = 1121921106706710567
        self.server6_id = 1131003330810871979
        self.server6_channel = 1133767338588639323
        self.server7_id = 748021504830341330
        self.server7_channel = 748021504830341334
        self.daegu = 896619762354892821
        self.daegu_welc = 896924663819694132
        self.hidden = True
        self.emoji = "<:shooky:1121909564799987722>"

    @commands.Cog.listener()
    async def on_member_join(self ,member: discord.Member):
        if member.guild.id == self.server1_id:
            embed = discord.Embed(title='<a:kanzenflower:1128154723262943282> Welcome to Kanzen!', color=0x2b2d31, description=f"Welcome to kanzen {member.name}!\n<a:Arrow_1:1145603161701224528> Read our [information](https://discord.com/channels/1121841073673736215/1148042725950767138)\n<a:Arrow_1:1145603161701224528> Logos and hashtag are [here](https://discord.com/channels/1121841073673736215/1148042725950767138)")
            embed.set_footer(text='Need help? ping @lead or @staff', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.server1_welcome_channel_id)
            channel2 = self.bot.get_channel(1125053619893440653)
            role = discord.utils.get(member.guild.roles, id=1121842393994494082)
            bronze = discord.utils.get(member.guild.roles, id=1187508597761003572)
            main = discord.utils.get(member.guild.roles, id=1187909432168955905)
            ranks = discord.utils.get(member.guild.roles, id=1187910861537427627)
            extra = discord.utils.get(member.guild.roles, id=1187912377388236820)
            embed.set_thumbnail(url=member.display_avatar.url)
            view = welc(member)
            await channel2.send(f"<a:kanzenflower:1128154723262943282> {member.mention} Welcome to **Kanzengrp!**\nTalk to other zennies in this channel\nNeed help? ping Lead or Staff", view=view)
            await channel.send(f'{member.mention} Welcome to Kanzengrp!', embed=embed)
            await member.add_roles(role)
            await member.add_roles(bronze)
            await member.add_roles(main)
            await member.add_roles(ranks)
            await member.add_roles(extra)
            """DAEGUTOWN SERVER"""
        elif member.guild.id == self.daegu:
            embed = discord.Embed(title=f'✦ {member.name} joined daegu!', color=0x2b2d31, description=f"- read our [information](https://discord.com/channels/896619762354892821/896924663819694132/1158304340147179570)\n- get your [roles](https://discord.com/channels/896619762354892821/896924663819694132/1158304340147179570) and [bias roles](https://discord.com/channels/896619762354892821/896924663819694132/1158304340147179570)\n- logos and hashtag are [here](https://discord.com/channels/896619762354892821/896924663819694132/1158304340147179570)")
            embed.set_footer(text='Need help? ping @lead or @staff', icon_url=member.display_avatar.url)
            channel = self.bot.get_channel(self.daegu_welc)
            channel2 = self.bot.get_channel(1064806374992785469)
            role = discord.utils.get(member.guild.roles, id=896925970672549958)
            embed.set_thumbnail(url=member.display_avatar.url)
            view = welc(member)
            await channel2.send(f"✦ Welcome to Daegutown {member.name}!\nThank you for joining", view=view)
            await channel.send(f'{member.mention}', embed=embed)
            await member.add_roles(role)
            """EDITORS BLOCK SERVER"""
        elif member.guild.id == self.server6_id:
            member_count = len(member.guild.members) 
            embed = discord.Embed(color=0x2b2d31, description=f"<a:arrowlightpink:1141452054716489789> [read infortmation](https://discord.com/channels/1131003330810871979/1131005271502753812)\n<a:arrowlightpink:1141452054716489789> [apply here](https://discord.com/channels/1131003330810871979/1133771634793250847)")
            role = member.guild.get_role(1131016147282710679)  
            channel = self.bot.get_channel(self.server6_channel)
            timestamp = datetime.datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"Member Count: {member_count}")  
            embed.set_author(name=f"{member.display_name}", icon_url=member.display_avatar.url)
            embed.set_thumbnail(url=member.display_avatar.url)
            view = welc(member)
            await channel.send(f'Welcome {member.mention} <@&1131005057417105418>', embed=embed, view=view)
            await member.add_roles(role)
            """ASTER SERVER"""
        elif member.guild.id == self.server7_id:
            member_count = len(member.guild.members) 
            embed = discord.Embed(color=0x2b2d31,title="ASTER", description=f"¹﹒[regulations](https://discord.com/channels/748021504830341330/786982725579833394).\n²﹒[booster perks](https://discord.com/channels/748021504830341330/1036575005598826627).\n³﹒[personal profile](https://discord.com/channels/748021504830341330/792121849856393257).")
            channel = self.bot.get_channel(self.server7_channel)
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(f'<a:astersheart:1028181292342312970> welcome {member.display_name} ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _ <@&1060732335156367450> {member.mention}', embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.id == self.server1_id:
            embed = discord.Embed(title=f"{member.display_name} has left Kanzen!", color=0x2b2d31, description="We will miss you !")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again <3')
            channel = self.bot.get_channel(self.server1_welcome_channel_id)
            await channel.send(f'{member.mention}', embed=embed)
        elif member.guild.id == self.daegu:
            embed = discord.Embed(title=f"{member.display_name} has left daegu!", color=0x2b2d31, description="We will miss you !")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text='Hope to see you again <3')
            channel = self.bot.get_channel(self.daegu_welc)
            await channel.send(f'{member.mention}', embed=embed)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))