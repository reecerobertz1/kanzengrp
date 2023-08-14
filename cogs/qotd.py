import discord
from discord.ext import commands

class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.qotd_schedule_channel_id = 1131018131813441696  # Replace with your channel ID

    @commands.command(name='qotdschedule')
    async def qotd_schedule(self, ctx):
        embed = discord.Embed(title='QOTD Schedule', color=0x2b2d31)
        # Add fields for each person with their name, date, and question
        # Example: embed.add_field(name='Person', value='John Doe', inline=True)
        #          embed.add_field(name='Date', value='August 15th', inline=True)
        #          embed.add_field(name='Question', value='What is your favorite movie?', inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='qotd')
    async def add_qotd(self, ctx, *, qotd_info):
        # Parse the input: +qotd question | date | author
        question, date, author = map(str.strip, qotd_info.split('|'))
        
        # Update the qotd_schedule_channel on the specified date
        channel = self.bot.get_channel(self.qotd_schedule_channel_id)
        if channel is not None:
            await channel.send(f"{author}, today is your day to post the Question of the Day!\nYour question: {question}")
        else:
            await ctx.send("QOTD schedule channel not found. Please set the correct channel ID.")

async def setup(bot):
    await bot.add_cog(QOTD(bot))