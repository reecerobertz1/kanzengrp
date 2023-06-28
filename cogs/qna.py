import asyncio
import discord
from discord.ext import commands

class qna(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server1_deleted_messages_channel_id = 1123696501441450107
        self.server1_answer_channel_id = 1123696762985656451
        self.server2_deleted_messages_channel_id = 1123719751479341107
        self.server2_answer_channel_id = 1123719714594639922

    @commands.command(hidden=True)
    async def answer(self, ctx, *, response: str):
        reference = ctx.message.reference
        if reference and reference.message_id:
            msg = await ctx.channel.fetch_message(reference.message_id)
            if "|" in msg.content:
                question, asker = msg.content.split("| ")
                user = await self.bot.fetch_user(int(asker))
                if ctx.guild.id == 1122181605591621692:  # Server 1
                    answer_channel = self.bot.get_channel(self.server1_answer_channel_id)
                elif ctx.guild.id == 1123347338841313331:  # Server 2
                    answer_channel = self.bot.get_channel(self.server2_answer_channel_id)
                else:
                    return

                embed = discord.Embed(title="Q&A", color=0x2b2d31, description=f"**question:** {question}**\nanswer:** {response}")
                embed.set_footer(text=f"asked by {user.display_name} | answered by {ctx.author.display_name}")

                await answer_channel.send(user.mention)
                await answer_channel.send(embed=embed)
                return

        await ctx.send("Failed to retrieve the question or the question format is incorrect.")

    @commands.command()
    async def qna(self, ctx, *, question: str):
        if ctx.guild.id == 1122181605591621692:  # Server 1
            deleted_messages_channel = self.bot.get_channel(self.server1_deleted_messages_channel_id)
        elif ctx.guild.id == 1123347338841313331:  # Server 2
            deleted_messages_channel = self.bot.get_channel(self.server2_deleted_messages_channel_id)
        else:
            return

        q = await ctx.reply("Your question has been sent to the lead!")

        message = f"{question} | {ctx.author.id}"
        await deleted_messages_channel.send(message)

        await asyncio.sleep(3)
        await ctx.message.delete()
        await q.delete()




async def setup(bot):
    await bot.add_cog(qna(bot))