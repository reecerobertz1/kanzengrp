import asyncio
import random
import discord
from discord.ext import commands
from discord import app_commands

easy = {'0': ["https://cdn.discordapp.com/attachments/1121841074512605186/1147752445406089216/lisa_00000.png","```A. Blackpink Lisa\nB. BIBI\nC. (G)Idle Minnie\nD. Blackpink Jennie```","A","https://cdn.discordapp.com/attachments/1121841074512605186/1148809817947902012/lisa_00000.png"],'1':["https://cdn.discordapp.com/attachments/1121841074512605186/1147752444827283516/ariana_00000.png","```A. Ariana Grande\nB. Selena Gomez\nC. Demi Lovato\nD. Taylor Swift```","A","https://cdn.discordapp.com/attachments/1121841074512605186/1148809671218577439/ariana_00000.png"],'2':["https://cdn.discordapp.com/attachments/1121841074512605186/1147752445074735185/jisoo_00001.png","```A. Itzy chaeryeong\nB. Blackpink Jisoo\nC. Somi\nD. Demi Lovato```","B","https://cdn.discordapp.com/attachments/1121841074512605186/1148809959597940809/jisoo_00000.png"],'3':["https://cdn.discordapp.com/attachments/1121841074512605186/1147752445674532925/rose_00000.png","```A. Miley Cyrus\nB. Blackpink Rosé\nC. Somi\nD. (G)Idle Mi-yeon```","B","https://cdn.discordapp.com/attachments/1121841074512605186/1148810165668302909/rose_00000.png"],'4':["https://cdn.discordapp.com/attachments/1121841074512605186/1147752445968121886/jennie_00000.png","```A. Ella Gross\nB. Aespa Ningning\nC. Ariana Grande\nD. Blackpink Jennie```","D","https://cdn.discordapp.com/attachments/1121841074512605186/1148810166062559242/jennie_00000.png"],'5':["https://cdn.discordapp.com/attachments/1121841074512605186/1147769723065466910/hoseok_00000.png","```A. TXT Soobin\nB. Enhypen Jay\nC. P1harmony Intak\nD. BTS Hoseok```","D","https://cdn.discordapp.com/attachments/1121841074512605186/1148808398964531252/ezgif-5-34eed441e9.png"], '6':["https://cdn.discordapp.com/attachments/1121841074512605186/1147769723434573824/jimin_00000.png","```A. TXT Yeonjun\nB. Stray Kids Han\nC. BTS Jimin\nD. EXO Kai```","C","https://cdn.discordapp.com/attachments/1121841074512605186/1148808398624800828/unnamed.jpg"], '7':["https://cdn.discordapp.com/attachments/1121841074512605186/1147769723828830218/jin_00001.png","```A. BTS Taehyung\nB. P1harmony Theo\nC. BTS Jin\nD. EXO Chanyeol```","C","https://cdn.discordapp.com/attachments/1121841074512605186/1148808734403985559/EzbU8NUWYAQDgOW.jpeg"], '8':["https://cdn.discordapp.com/attachments/1121841074512605186/1147769724193755216/jungkook_00000.png","```A. BTS Jin\nB. TXT Yeonjun\nC. BTS Taehyung\nD. BTS Jungkook```","D","https://cdn.discordapp.com/attachments/1121841074512605186/1148808398389903371/ezgif-5-9f7fa2d9f3.png"], '9':["https://cdn.discordapp.com/attachments/1121841074512605186/1147769724558647356/namjoon_00000.png","```A. BTS Namjoon\nB. P1harmony Jiung\nC. Stray Kids Bang Chan\nD. Enhypen Jake```","A","https://cdn.discordapp.com/attachments/1121841074512605186/1148808397920157718/kim-namjoon-16842982443x2.png"], '10':["https://cdn.discordapp.com/attachments/1121841074512605186/1147769724843872286/taehyung_00000.png","```A. Astro Eunwoo\nB. P1harmony Keeho\nC. BTS Jungkook\nD. BTS Taehyung```","D","https://cdn.discordapp.com/attachments/1121841074512605186/1148808398167613520/a68bd02419f53af77a5577444a047b30.jpg"], '11':["https://cdn.discordapp.com/attachments/1121841074512605186/1147769725154238474/yoongi_00000.png","```A. Astro JinJin\nB. EXO Chanyeol\nC. BTS Yoongi\nD. EXO Sehun```","C","https://cdn.discordapp.com/attachments/1121841074512605186/1148808397689454612/2115d19119734e606bf16aaa02c743b3.jpg"],'12':["https://cdn.discordapp.com/attachments/1121841074512605186/1148892895999443034/Comp_2_00000.png","```A. BTS Seokjin\nB. P1harmony Theo\nC. Enhypen Sunoo\nD. TXT Kai```","C","https://cdn.discordapp.com/attachments/1121841074512605186/1148892759734886481/Comp_2_00000.png"],'13':["https://cdn.discordapp.com/attachments/1121841074512605186/1148892896657936445/Comp_2_00001.png","```A. BTS Taehyung\nC. P1harmony Keeho\nC. TXT Yeonjun\nD. Enhypen Sunghoon```","D","https://cdn.discordapp.com/attachments/1121841074512605186/1148892760141746216/Comp_2_00001.png"],'14':["https://cdn.discordapp.com/attachments/1121841074512605186/1148892896972517416/Comp_2_00002.png","```A. Enhypen Jungwon\nB. BTS Seokjin\nC. P1harmony Jiung\nD. Enhypen Sunoo```","A","https://cdn.discordapp.com/attachments/1121841074512605186/1148892760439537664/Comp_2_00002.png"],'15':["https://cdn.discordapp.com/attachments/1121841074512605186/1148892897257734176/Comp_2_00003.png","```A. BTS Namjoon\nB. Seventeen Jun\nC. Enhypen Jay\nD. BTS Jimin```","C","https://cdn.discordapp.com/attachments/1121841074512605186/1148892760867348520/Comp_2_00003.png"],'16':["https://cdn.discordapp.com/attachments/1121841074512605186/1148892897530351667/Comp_2_00004.png","```A. TXT Soobin\nB. P1harmony Jongseob\nC. BTS Taehyung\nD. Enhypen Jake```","D","https://cdn.discordapp.com/attachments/1121841074512605186/1148892761207099463/Comp_2_00004.png"],'17':["https://cdn.discordapp.com/attachments/1121841074512605186/1148892897832349777/Comp_2_00005.png","```A. Enhypen Ni-Ki\nB. BTS Jimin\nC. TXT Taehyun\nD. Stray Kids Hyunjin```","A","https://cdn.discordapp.com/attachments/1121841074512605186/1148892761651683328/Comp_2_00005.png"],'18':["https://cdn.discordapp.com/attachments/1121841074512605186/1149220850957025320/Comp_2_00001.png","```A. Enhypen Ni-Ki\nB. BTS Jimin\nC. TXT Taehyun\nD. Stray Kids Hyunjin```","C","https://cdn.discordapp.com/attachments/1121841074512605186/1149220775438590023/Comp_2_00001.png"],'19':["https://cdn.discordapp.com/attachments/1121841074512605186/1149220851275808808/Comp_2_00002.png","```A. TXT Soobin\nB. Seventeen Hoshi\nC. BTS Yoongi\nD. Stray Kids Han```","A","https://cdn.discordapp.com/attachments/1121841074512605186/1149220775837040640/Comp_2_00002.png"],'20':["https://cdn.discordapp.com/attachments/1121841074512605186/1149220850676011048/Comp_2_00000.png","```A. Enhypen Jake\nB. BTS Seokjin\nC. Seventeen Seungkwan\nD. TXT Yeonjun```","D","https://cdn.discordapp.com/attachments/1121841074512605186/1149220774754922566/Comp_2_00000.png"],'21':["https://cdn.discordapp.com/attachments/1121841074512605186/1149220851514871888/Comp_2_00003.png","```A. Stray Kids Minho\nB. BTS Jimin\nC. TXT Kai\nD. BTS Jungkook```","C","https://cdn.discordapp.com/attachments/1121841074512605186/1149220776428445786/Comp_2_00003.png"],'22':["https://cdn.discordapp.com/attachments/1121841074512605186/1149220851758137354/Comp_2_00004.png","```A. TXT Beomgyu\nB. BTS Seokjin\nC. TXT Kai\nD. Stray Kids Hyunjin```","A","https://cdn.discordapp.com/attachments/1121841074512605186/1149220776885628938/Comp_2_00004.png"],'23':["https://cdn.discordapp.com/attachments/1121841074512605186/1149224666817376346/Comp_2_00000.png""```A. Taylor Swift\nB. Margot Robbie\nC. Miley Cyrus\nD. Jennifer Lawrence```","A","https://cdn.discordapp.com/attachments/1121841074512605186/1149224574337155082/Comp_2_00000.png"],'24':["https://cdn.discordapp.com/attachments/1121841074512605186/1149224667501035541/Comp_2_00001.png","```A. Jennifer Aniston\nB. Kristen Stewart\nC. Taylor Swift\nD. Margot Robbie```","D","https://cdn.discordapp.com/attachments/1121841074512605186/1149224574664331284/Comp_2_00001.png"],'25':["https://cdn.discordapp.com/attachments/1121841074512605186/1149224667798839338/Comp_2_00002.png","```A. Margot Robbie\nB. Miley Cyrus\nC. Kristen Stewart\nD. Jennifer Aniston```","B","https://cdn.discordapp.com/attachments/1121841074512605186/1149224574970503208/Comp_2_00002.png"],'26':["https://cdn.discordapp.com/attachments/1121841074512605186/1149225798750978129/Comp_2_00000.png","```A. Rihanna\nB. Nicki Minaj\nC. Ice Spice\nD. Beyonce```","A","https://cdn.discordapp.com/attachments/1121841074512605186/1149225854862368798/Comp_2_00000.png"],'27':["https://cdn.discordapp.com/attachments/1121841074512605186/1149224667798839338/Comp_2_00002.png","```A. Keke Palmer\nB. Zendaya\nC. Beyonce\nD. Ice Spice```","D","https://cdn.discordapp.com/attachments/1121841074512605186/1149225855298580480/Comp_2_00001.png"],'28':["https://cdn.discordapp.com/attachments/1121841074512605186/1149225799304618025/Comp_2_00002.png","```A. Zendaya\nB. Keke Palmer\nC. Nicki Minaj\nD. Ice Spice```","C","https://cdn.discordapp.com/attachments/1121841074512605186/1149225855810277376/Comp_2_00002.png"]}

class modes(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="easy", style=discord.ButtonStyle.green)
    async def easy(self, interaction: discord.Interaction, button: discord.Button):
        randomCeleb = easy[str(random.randrange(len(easy)))]
        embed = discord.Embed(title="Guess the celeb",
            description=f"easy mode\n{randomCeleb[1]}",
                            color=0x2b2d31)
        embed.set_footer(text="Use the X button to stop the game")
        embed.set_image(url=randomCeleb[0])
        
        correct_answer = randomCeleb[2]
        answer_image = randomCeleb[3]
        view = easybuttons(correct_answer, answer_image)
        await interaction.response.send_message(embed=embed, view=view)

class easybuttons(discord.ui.View):
    def __init__(self, correct_answer, answer_image):
        super().__init__()
        self.value = None
        self.userAns = None
        self.currentAns = None
        self.correct_answer = correct_answer
        self.image = answer_image

    def set_user_answer(self, answer):
        self.userAns = answer

    @discord.ui.button(label="A", style=discord.ButtonStyle.gray)
    async def A(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = easyplayagain()
        self.set_user_answer("A")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)
    
    @discord.ui.button(label = "B", style = discord.ButtonStyle.gray)
    async def B(self, interaction:discord.Interaction, button: discord.ui.Button):
        view = easyplayagain()
        self.set_user_answer("B")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)

    @discord.ui.button(label = "C", style = discord.ButtonStyle.gray)
    async def C(self, interaction:discord.Interaction, button: discord.ui.Button):
        view = easyplayagain()
        self.set_user_answer("C")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)

    @discord.ui.button(label = "D", style = discord.ButtonStyle.gray)
    async def D(self, interaction:discord.Interaction, button: discord.ui.Button):
        view = easyplayagain()
        self.set_user_answer("D")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)

    @discord.ui.button(label = "X", style = discord.ButtonStyle.red)
    async def X(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content= f"You Gave Up!", embed=None, view=None)

class mediumbuttons(discord.ui.View):
    def __init__(self, correct_answer, answer_image):
        super().__init__()
        self.value = None
        self.userAns = None
        self.currentAns = None
        self.correct_answer = correct_answer
        self.image = answer_image

    def set_user_answer(self, answer):
        self.userAns = answer

    @discord.ui.button(label="A", style=discord.ButtonStyle.gray)
    async def A(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = mediumplayagain()
        self.set_user_answer("A")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)
    
    @discord.ui.button(label = "B", style = discord.ButtonStyle.gray)
    async def B(self, interaction:discord.Interaction, button: discord.ui.Button):
        view = mediumplayagain()
        self.set_user_answer("B")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)

    @discord.ui.button(label = "C", style = discord.ButtonStyle.gray)
    async def C(self, interaction:discord.Interaction, button: discord.ui.Button):
        view = mediumplayagain()
        self.set_user_answer("C")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)

    @discord.ui.button(label = "D", style = discord.ButtonStyle.gray)
    async def D(self, interaction:discord.Interaction, button: discord.ui.Button):
        view = mediumplayagain()
        self.set_user_answer("D")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)

    @discord.ui.button(label = "X", style = discord.ButtonStyle.red)
    async def X(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content= f"You Gave Up!", embed=None, view=None)

class mediumplayagain(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Play Again?", style=discord.ButtonStyle.gray)
    async def Again(self, interaction: discord.Interaction, button: discord.Button):
        randomCeleb = easy[str(random.randrange(len(easy)))]
        embed = discord.Embed(title="Guess the celeb",
                            description=randomCeleb[1],
                            color=0x2b2d31)
        embed.set_footer(text="Use the X button to stop the game")
        embed.set_image(url=randomCeleb[0])
        
        correct_answer = randomCeleb[2]
        answer_image = randomCeleb[3]
        view = easybuttons(correct_answer, answer_image)
        await interaction.response.send_message(embed=embed, view=view)

class hardbuttons(discord.ui.View):
    def __init__(self, correct_answer, answer_image):
        super().__init__()
        self.value = None
        self.userAns = None
        self.currentAns = None
        self.correct_answer = correct_answer
        self.image = answer_image

    def set_user_answer(self, answer):
        self.userAns = answer

    @discord.ui.button(label="A", style=discord.ButtonStyle.gray)
    async def A(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = hardplayagain()
        self.set_user_answer("A")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)
    
    @discord.ui.button(label = "B", style = discord.ButtonStyle.gray)
    async def B(self, interaction:discord.Interaction, button: discord.ui.Button):
        view = hardplayagain()
        self.set_user_answer("B")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)

    @discord.ui.button(label = "C", style = discord.ButtonStyle.gray)
    async def C(self, interaction:discord.Interaction, button: discord.ui.Button):
        view = hardplayagain()
        self.set_user_answer("C")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)

    @discord.ui.button(label = "D", style = discord.ButtonStyle.gray)
    async def D(self, interaction:discord.Interaction, button: discord.ui.Button):
        view = hardplayagain()
        self.set_user_answer("D")
        if self.userAns == self.correct_answer:
            correct = discord.Embed(title="Your answer was correct!", color=0x11ff00)
            correct.set_image(url=self.image)
            await interaction.response.edit_message(embed=correct, view=view)
        else:
            wrong = discord.Embed(title="Your answer was wrong!", color=0xff0000)
            wrong.set_image(url=self.image)
            await interaction.response.edit_message(embed=wrong, view=view)

    @discord.ui.button(label = "X", style = discord.ButtonStyle.red)
    async def X(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content= f"You Gave Up!", embed=None, view=None)

class hardplayagain(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Play Again?", style=discord.ButtonStyle.gray)
    async def Again(self, interaction: discord.Interaction, button: discord.Button):
        randomCeleb = easy[str(random.randrange(len(easy)))]
        embed = discord.Embed(title="Guess the celeb",
                            description=randomCeleb[1],
                            color=0x2b2d31)
        embed.set_footer(text="Use the X button to stop the game")
        embed.set_image(url=randomCeleb[0])
        
        correct_answer = randomCeleb[2]
        answer_image = randomCeleb[3]
        view = easybuttons(correct_answer, answer_image)
        await interaction.response.send_message(embed=embed, view=view)

class easyplayagain(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Play Again?", style=discord.ButtonStyle.gray)
    async def Again(self, interaction: discord.Interaction, button: discord.Button):
        randomCeleb = easy[str(random.randrange(len(easy)))]
        embed = discord.Embed(title="Guess the celeb",
                            description=randomCeleb[1],
                            color=0x2b2d31)
        embed.set_footer(text="Use the X button to stop the game")
        embed.set_image(url=randomCeleb[0])
        
        correct_answer = randomCeleb[2]
        answer_image = randomCeleb[3]
        view = easybuttons(correct_answer, answer_image)
        await interaction.response.send_message(embed=embed, view=view)

class celeb(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.hidden = True
        self.emoji = "<:tata:1121909389280944169>"

    @commands.hybrid_command(name="guesstheceleb", description="Play guess the celebrity")
    async def guesstheceleb(self, ctx):
        embed = discord.Embed(title="Guess the Celeb", description="Please pick a mode to play!\n<a:Arrow_1:1145603161701224528> Easy\n<a:Arrow_1:1145603161701224528> Medium (coming soon)\n<a:Arrow_1:1145603161701224528> Hard (coming soon)", color=0x2b2d31)
        view = modes()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(celeb(bot))