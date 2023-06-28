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

        # Create an embed with the deleted message and user information
        embed = discord.Embed(title="Deleted Question", color=discord.Color.red())
        embed.add_field(name="Content", value=message.content)
        embed.add_field(name="User ID", value=message.author.id)

        # Send the embed to the deleted messages channel
        await deleted_messages_channel.send(embed=embed)

        # Delete the question message
        await message.delete()

    async def process_answer(self, message):
        answer_channel = self.bot.get_channel(self.answer_channel_id)
        deleted_messages_channel = self.bot.get_channel(self.deleted_messages_channel_id)

        # Create an embed with the deleted message and user information
        embed = discord.Embed(title="Deleted Answer", color=discord.Color.red())
        embed.add_field(name="Content", value=message.content)
        embed.add_field(name="User ID", value=message.author.id)

        # Send the embed to the deleted messages channel
        await deleted_messages_channel.send(embed=embed)

        # Delete the answer message
        await message.delete()


async def setup(bot):
    await bot.add_cog(qna(bot))