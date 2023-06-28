import asyncio
import discord
from discord.ext import commands

class qna(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.question_channel_id = 1123696501441450107
        self.answer_channel_id = 1123696762985656451

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 1123696243911164054:
            await self.process_question(message)

    async def process_question(self, message):
        question_channel = self.bot.get_channel(self.question_channel_id)
        answer_channel = self.bot.get_channel(self.answer_channel_id)

        # Delete the question message
        await message.delete()

        # Create an embed with the question and user information
        embed = discord.Embed(title="Question", description=message.content, color=discord.Color.blue())
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)

        # Send the embed to the question channel
        question_msg = await question_channel.send(embed=embed)

        # Add a reaction to the question message for easier answering
        await question_msg.add_reaction("✉️")

        # Wait for an answer
        def check_answer(reaction, user):
            return (
                reaction.message.id == question_msg.id
                and str(reaction.emoji) == "✉️"
                and user != self.bot.user
            )

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=300.0, check=check_answer)
            answer_content = reaction.message.content

            # Create an embed with the answer and user information
            answer_embed = discord.Embed(title="Answer", description=answer_content, color=discord.Color.green())
            answer_embed.set_author(name=user.name, icon_url=user.avatar_url)

            # Ping the user who asked the question and send the answer embed to the answer channel
            answer_embed.set_footer(text=f"In response to {message.author.name}")
            await answer_channel.send(f"<@{message.author.id}>", embed=answer_embed)
        except asyncio.TimeoutError:
            await question_channel.send("No answer received within 5 minutes.")

async def setup(bot):
    await bot.add_cog(qna(bot))