from tof.getQuestions import getQuestions
import discord
import asyncio

async def celebHandler(userAnswer, currentAnswer, score, lives, interaction, view):
    if userAnswer == currentAnswer:
        score += 1
        response_message = f"✅ That's correct!\nYour current score is: **{score}**\nYou have ❤**{lives}** lives left."
    else:
        lives -= 1
        response_message = f"❌ That's incorrect.\nYour current score is: **{score}**\nYou have ❤**{lives}** lives left."

    if lives <= 0:
        await interaction.response.edit_message(content=f">>> GAME OVER! You have no lives left. \nYour total score is {score}", embed=None, view=None)
        return

    embed, answer = await getQuestions()
    currentAnswer = answer
    await interaction.response.edit_message(content=response_message, embed=embed, view=view)
    return score, lives, currentAnswer

class buttonHandler(discord.ui.View):
    def __init__(self, message):
        super().__init__()
        self.score = 0
        self.lives = 3
        self.userAns = None
        self.currentAns = None
        self.timeout = False
        self.message = message

    async def on_timeout(self):
        self.timeout = True
        await self.message.edit(content=f">>> TIMEOUT! Your score was {self.score}", embed=None, view=None)

    @discord.ui.button(label="True", style=discord.ButtonStyle.gray)
    async def A(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.timeout:
            return
        self.userAns = "True"
        result = await celebHandler(self.userAns, self.currentAns, self.score, self.lives, interaction, self)
        if result:
            self.score, self.lives, self.currentAns = result

    @discord.ui.button(label="False", style=discord.ButtonStyle.gray)
    async def B(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.timeout:
            return
        self.userAns = "False"
        result = await celebHandler(self.userAns, self.currentAns, self.score, self.lives, interaction, self)
        if result:
            self.score, self.lives, self.currentAns = result

    @discord.ui.button(label="X", style=discord.ButtonStyle.red)
    async def X(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.timeout:
            return
        await interaction.response.edit_message(content=f"You Gave Up! \nYour total score is {self.score}", embed=None, view=None)