import asyncio
import random
import discord
from discord.ext import commands
from discord import app_commands
from gtcstuff.celebs import easy

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

    @commands.hybrid_command(name="guesstheceleb", description="Play guess the celebrity")
    async def guesstheceleb(self, ctx):
        embed = discord.Embed(title="Guess the Celeb", description="Please pick a mode to play!\n<a:Arrow_1:1145603161701224528> Easy\n<a:Arrow_1:1145603161701224528> Medium (coming soon)\n<a:Arrow_1:1145603161701224528> Hard (coming soon)", color=0x2b2d31)
        view = modes()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(celeb(bot))