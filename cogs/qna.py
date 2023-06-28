import asyncio
import discord
from discord.ext import commands

class qna(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_messages_channel_id = 1123696501441450107
        self.answer_channel_id = 1123696762985656451

    @commands.command(hidden=True)
    async def answer(self, ctx, *, response: str):
        reference = ctx.message.reference
        if reference and reference.message_id:
            msg = await ctx.channel.fetch_message(reference.message_id)
            if "|" in msg.content:
                question, asker = msg.content.split("| ")
                user = await self.bot.fetch_user(int(asker))
                answer_channel = self.bot.get_channel(self.answer_channel_id)

                embed = discord.Embed(title="kanzen q&n", color=0x2b2d31, description=f"**question:** {question}**\nanswer:** {response}")
                embed.set_footer(text=f"asked by {user.display_name} | answered by {ctx.author.display_name}")

                await answer_channel.send(user.mention)
                await answer_channel.send(embed=embed)
                return

        await ctx.send("Failed to retrieve the question or the question format is incorrect.")

    @commands.command()
    async def qna(self, ctx, *, question: str):
        deleted_messages_channel = self.bot.get_channel(self.deleted_messages_channel_id)

        q = await ctx.reply("Your question has been sent to the lead!")

        message = f"{question} | {ctx.author.id}"
        await deleted_messages_channel.send(message)

        await asyncio.sleep(3)
        await ctx.message.delete()
        await q.delete()




async def setup(bot):
    await bot.add_cog(qna(bot))