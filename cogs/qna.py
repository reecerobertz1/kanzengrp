import asyncio
import discord
from discord.ext import commands

class qna(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.question_channel_id = 1123696243911164054
        self.answer_channel_id = 1123696762985656451
        self.deleted_messages_channel_id = 1123696501441450107

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.question_channel_id:
            await self.process_question(message)
        elif message.channel.id == self.answer_channel_id:
            await self.process_answer(message)

    async def process_question(self, message):
        question_channel = self.bot.get_channel(self.question_channel_id)
        deleted_messages_channel = self.bot.get_channel(self.deleted_messages_channel_id)

        # Send the deleted question content and user ID to the deleted messages channel
        deleted_message = f"Deleted Question\nContent: {message.content}\nUser ID: {message.author.id}"
        await deleted_messages_channel.send(deleted_message)

        # Delete the question message
        await message.delete()

    async def process_answer(self, message):
        answer_channel = self.bot.get_channel(self.answer_channel_id)
        deleted_messages_channel = self.bot.get_channel(self.deleted_messages_channel_id)

        # Send the deleted answer content and user ID to the deleted messages channel
        deleted_message = f"questions: {message.content}\nid: {message.author.id}"
        await deleted_messages_channel.send(deleted_message)

        # Delete the answer message
        await message.delete()

    @commands.command()
    async def answer(self, ctx, message_id: int):
        deleted_messages_channel = self.bot.get_channel(self.deleted_messages_channel_id)
        answer_channel = self.bot.get_channel(self.answer_channel_id)

        # Fetch the message using the provided message ID
        try:
            message = await deleted_messages_channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("Invalid message ID.")
            return

        if "Deleted Question" in message.content:
            # Extract the question content and user ID from the deleted message
            lines = message.content.split("\n")
            content = lines[1].split(": ")[1]
            user_id = lines[2].split(": ")[1]

            # Fetch the user who asked the question
            user = await self.bot.fetch_user(int(user_id))

            # Create an embed with the question and answer
            embed = discord.Embed(title="Answer", color=discord.Color.green())
            embed.add_field(name="Question", value=content)
            embed.add_field(name="Answer", value=ctx.message.content)

            # Send the answer embed to the answer channel
            await answer_channel.send(f"<@{user.id}>")
            await answer_channel.send(embed=embed)

            # Notify the user who asked the question
            await ctx.send(f"Answer sent to {user.mention} in {answer_channel.mention}.")
        else:
            await ctx.send("The specified message is not a deleted question.")




async def setup(bot):
    await bot.add_cog(qna(bot))