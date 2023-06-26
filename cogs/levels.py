import discord
from discord.ext import commands

class appnewtest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def apply(self, ctx):
        # Create a modal with questions
        questions = [
            {"name": "discord_name", "question": "What is your Discord name?"},
            {"name": "instagram_name", "question": "What is your Instagram name?"},
            {"name": "edit_link", "question": "Link for the edit you want to apply with:"},
            {"name": "activity_level", "question": "How active will you be (1 - 5)?"},
            {"name": "additional_info", "question": "Anything else you want us to know?"}
        ]

        # Initialize responses dictionary
        responses = {}

        # Send the modal
        for question in questions:
            response_msg = await ctx.send(question["question"])
            response = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            responses[question["name"]] = response.content

            await response_msg.delete()  # Delete the question message

        # Create the embed with the submitted information
        embed = discord.Embed(title="Application Form", color=0x2b2d31)
        embed.add_field(name="Discord Name", value=responses.get("discord_name", "N/A"), inline=False)
        embed.add_field(name="Instagram Name", value=responses.get("instagram_name", "N/A"), inline=False)
        embed.add_field(name="Edit Link", value=responses.get("edit_link", "N/A"), inline=False)
        embed.add_field(name="Activity Level", value=responses.get("activity_level", "N/A"), inline=False)
        embed.add_field(name="Additional Info", value=responses.get("additional_info", "N/A"), inline=False)

        channel_id = 1122183100038905908  # Replace with the desired channel ID
        channel = self.bot.get_channel(channel_id)

        if channel:
            await channel.send(embed=embed)
        else:
            await ctx.send("Failed to find the specified channel.")

        # Optionally, you can also send a confirmation message to the user
        await ctx.send("Your application has been submitted. Thank you!")


async def setup(bot):
    await bot.add_cog(appnewtest(bot))
