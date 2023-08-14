import datetime
import discord
from discord.ext import tasks
from discord.ext import commands

class QOTD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.qotd_schedule_channel_id = 1131018131813441696  # Replace with your channel ID
        self.qotd_schedule = {}

    @commands.command(name='qotdschedule')
    async def qotd_schedule(self, ctx):
        embed = discord.Embed(title='QOTD Schedule', color=0x2b2d31)
        for author, data in self.qotd_schedule.items():
            date = data['date']
            question = data['question']
            embed.add_field(name=f'{author}', value=f"{date}\n\n**question**:\n{question}", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='qotd')
    async def add_qotd(self, ctx, *, qotd_info):
        qotd_parts = qotd_info.split('|')
        if len(qotd_parts) == 3:
            question, date, author = map(str.strip, qotd_parts)
            self.qotd_schedule[author] = {'date': date, 'question': question}
            await ctx.send(f"Added QOTD for {author} on {date}: {question}")
        else:
            await ctx.send("Invalid input format. Use: +qotd question | date | author")

    # Add a task to check the schedule daily and send reminders
    @tasks.loop(hours=24)
    async def check_qotd_schedule(self):
        current_date = datetime.datetime.now().strftime('%B %d')
        for author, data in self.qotd_schedule.items():
            if data['date'] == current_date:
                channel = self.bot.get_channel(self.qotd_schedule_channel_id)
                if channel is not None:
                    question = data['question']
                    await channel.send(f"{author}, today is your day to post the Question of the Day!\nYour question: {question}")

    @check_qotd_schedule.before_loop
    async def before_check_qotd_schedule(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(QOTD(bot))