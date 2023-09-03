import discord
import random

from triviastuff.questions import questions

async def getQuestions():
    randomQuestion = questions[str(random.randrange(len(questions)))]
    embed = discord.Embed(title=randomQuestion[0],
                          description=randomQuestion[1],
                          color=0x2b2d31)
    embed.set_footer(text="Use the X button to stop the game")
    answer = randomQuestion[2]
    return embed, answer