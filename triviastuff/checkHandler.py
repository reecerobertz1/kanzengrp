from triviastuff.getQuestions import getQuestions
import discord

async def checkHandler(userAnswer, currentAnswer, score, lives, interaction, view):
    if userAnswer == currentAnswer:
        score += 1
    else:
        lives -= 1
    if lives == 0:
        await interaction.response.edit_message(content = f">>> GAME OVER! You have no lives left. \nYour total score is {score}", view=None)
    else:
        embed, answer = await getQuestions()
        currentAnswer = answer
        await interaction.response.edit_message(content = f"Your current score is: **{score}**\nYou have ❤**{lives}** lives left.", embed=embed, view=view)
        return score, lives, currentAnswer
    
class buttonHandler(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.score = 0
        self. lives = 3
        self.userAns = None
        self.currentAns = None

    @discord.ui.button(label = "A", style = discord.ButtonStyle.gray)
    async def A(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.userAns = "A"
        self.score, self. lives, self.currentAns = await checkHandler (self.userAns, self.currentAns, self.score, self.lives, interaction, self)

    @discord.ui.button(label = "B", style = discord.ButtonStyle.gray)
    async def B(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.userAns = "B"
        self.score, self.lives, self.currentAns = await checkHandler(self.userAns, self.currentAns, self.score, self.lives, interaction, self)

    @discord.ui.button(label = "C", style = discord.ButtonStyle.gray)
    async def C(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.userAns = "C"
        self.score, self. lives, self.currentAns = await checkHandler (self.userAns, self.currentAns, self.score, self.lives, interaction, self)

    @discord.ui.button(label = "D", style = discord.ButtonStyle.gray)
    async def D(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.userAns = "D"
        self.score, self.lives, self.currentAns = await checkHandler(self.userAns, self.currentAns, self.score, self.lives, interaction, self)
    
    @discord.ui.button(label="X", style=discord.ButtonStyle.red)
    async def X(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content= f"You Gave Up! \nYour total score is {self.score}", view = None)

    