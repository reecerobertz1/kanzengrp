import discord
from discord.ext import commands, tasks
from bot import LalisaBot
import asyncio
import random
import datetime

SERVER_SETTINGS = {
    835495688832811039: {  # Chroma Community
        "channel_id": 1352458069866582056,
        "role_id": 1352456467256574013
    },
    694010548605550675: {  # Chroma
        "channel_id": 1352448775943229582,
        "role_id": 1352451309822804098
    }
}

class QOTD(commands.Cog):
    def __init__(self, bot: LalisaBot):
        self.bot = bot
        self.questions = []
        self.daily_qotd.start()

    @commands.command()
    async def addquestions(self, ctx, *, question_list: str):
        new_questions = question_list.split(",")
        self.questions.extend(new_questions)
        await ctx.send(f"Added {len(new_questions)} questions for this month!")

    @tasks.loop(hours=24)
    async def daily_qotd(self):
        """Sends the Question of the Day at 12:00 PM server time."""
        now = datetime.datetime.now()
        target_time = datetime.time(12, 0)
        run_time = datetime.datetime.combine(now.date(), target_time)

        if now.time() > target_time:
            run_time += datetime.timedelta(days=1)

        delay = (run_time - now).total_seconds()
        await asyncio.sleep(delay)

        if not self.questions:
            print("No questions left today.")
            return

        question = self.questions.pop(0)

        for server_id, settings in SERVER_SETTINGS.items():
            channel = self.bot.get_channel(settings["channel_id"])  # Fetch channel object
            role_id = settings["role_id"]

            if channel:
                mention = f"<@&{role_id}>"
                message = await channel.send(f"**Question of the Day:** {question} {mention}")
                thread = await message.create_thread(name=f"QOTD Discussion: {datetime.date.today()}")
                if thread:
                    await thread.send("Answer today's question here!")

    @daily_qotd.before_loop
    async def before_daily_qotd(self):
        """Ensures the bot is ready before starting the loop."""
        await self.bot.wait_until_ready()

async def setup(bot: LalisaBot):
    await bot.add_cog(QOTD(bot))