import discord
from discord.ext import commands
import random
from tof.questions import questions

async def getQuestions():
    randomCeleb = questions[str(random.randrange(len(questions)))]
    embed = discord.Embed(title=randomCeleb[0],
                          description=randomCeleb[1],
                          color=0x2b2d31)
    embed.set_footer(text="Use the X button to stop the game")
    answer = randomCeleb[2]
    return embed, answer