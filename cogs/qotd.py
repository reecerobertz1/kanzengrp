import datetime
import json
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
        
        for author_id, data_list in self.qotd_schedule.items():
            for data in data_list:
                author = data['author']
                date = data['date']
                question = data['question']
                embed.add_field(name="Scheduled Question", value=f"Author: {author}\nDate: {date}\nQuestion: {question}", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name='qotd')
    async def add_qotd(self, ctx, *, qotd_info):
        try:
            author, date, question = map(str.strip, qotd_info.split('|'))
        except ValueError:
            await ctx.send("Invalid format. Please use: +qotd question | date (e.g., +qotd What is your favorite movie? | Tuesday August 15th)")
            return

        if str(ctx.author.id) not in self.qotd_schedule:
            self.qotd_schedule[str(ctx.author.id)] = []

        self.qotd_schedule[str(ctx.author.id)].append({
            'author': ctx.author.display_name,
            'date': date,
            'question': question
        })

        with open("qotd_schedule.json", "w") as file:
            json.dump(self.qotd_schedule, file, indent=4)

        await ctx.send("Question added to the QOTD schedule!")

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