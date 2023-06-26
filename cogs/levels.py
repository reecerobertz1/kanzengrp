import asyncio
import discord
from discord.ext import commands

class appnewtest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.questions = [
            {"name": "discord_name", "question": "What is your Discord name?"},
            {"name": "instagram_name", "question": "What is your Instagram name?"},
            {"name": "edit_link", "question": "Link for the edit you want to apply with:"},
            {"name": "activity_level", "question": "How active will you be (1 - 5)?"},
            {"name": "additional_info", "question": "Anything else you want us to know?"}
        ]

    @commands.command()
    async def apply(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        answers = {}

        for question in self.questions:
            await ctx.send(question["question"])
            response = await self.bot.wait_for('message', check=check)
            answers[question["name"]] = response.content

            await response.delete()  # Delete the author's response

        embed = discord.Embed(title="Application Form", color=0x2b2d31)
        embed.add_field(name="Discord Name", value=answers.get("discord_name", "N/A"), inline=False)
        embed.add_field(name="Instagram Name", value=answers.get("instagram_name", "N/A"), inline=False)
        embed.add_field(name="Edit Link", value=answers.get("edit_link", "N/A"), inline=False)
        embed.add_field(name="Activity Level", value=answers.get("activity_level", "N/A"), inline=False)
        embed.add_field(name="Additional Info", value=answers.get("additional_info", "N/A"), inline=False)

        channel_id = 1122183100038905908  # Replace with the desired channel ID
        channel = self.bot.get_channel(channel_id)

        if channel:
            await channel.send(embed=embed)
        else:
            await ctx.send("Failed to find the specified channel.")

        confirmation_msg = await ctx.send("Your application has been submitted. Thank you!")

        await asyncio.sleep(5)  # Wait for 5 seconds (you can adjust the duration)
        await confirmation_msg.delete()  # Delete the confirmation message



async def setup(bot):
    await bot.add_cog(appnewtest(bot))
