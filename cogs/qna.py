import asyncio
import discord
from discord.ext import commands

class qna(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_messages_channels = {
            1123347338841313331: 1123696501441450107,  # Server 1 
            1122181605591621692: 1123719751479341107  # Server 2 
        }
        self.answer_channels = {
            1123347338841313331: 1123696762985656451,  # Server 1
            1122181605591621692: 2345678901  # Server 2
        }

    @commands.command(hidden=True)
    async def answer(self, ctx, *, response: str):
        reference = ctx.message.reference
        if reference and reference.message_id:
            msg = await ctx.channel.fetch_message(reference.message_id)
            if "^" in msg.content:
                question, asker = msg.content.split("^ ")
                user = await self.bot.fetch_user(int(asker))
                deleted_messages_channel_id = self.deleted_messages_channels.get(ctx.guild.id)
                answer_channel_id = self.answer_channels.get(ctx.guild.id)

                if deleted_messages_channel_id and answer_channel_id:
                    deleted_messages_channel = self.bot.get_channel(deleted_messages_channel_id)
                    answer_channel = self.bot.get_channel(answer_channel_id)

                    embed = discord.Embed(title="kanzen q&n", color=0x2b2d31, description=f"**question:** {question}**\nanswer:** {response}")
                    embed.set_footer(text=f"asked by {user.display_name} | answered by {ctx.author.display_name}")

                    await answer_channel.send(user.mention)
                    await answer_channel.send(embed=embed)
                    return

        await ctx.send("Failed to retrieve the question or the question format is incorrect.")

    @commands.command()
    async def qna(self, ctx, *, question: str):
        deleted_messages_channel_id = self.deleted_messages_channels.get(ctx.guild.id)

        if deleted_messages_channel_id:
            deleted_messages_channel = self.bot.get_channel(deleted_messages_channel_id)

            q = await ctx.reply("Your question has been sent to the lead!")

            message = f"{question} ^ {ctx.author.id}"
            await deleted_messages_channel.send(message)

            await asyncio.sleep(3)
            await ctx.message.delete()
            await q.delete()



async def setup(bot):
    await bot.add_cog(qna(bot))