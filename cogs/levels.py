import asyncio
import json
import discord
from discord.ext import commands

class appnewtest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.questions = [
            {"name": "discord_name", "question": "What is your Discord name? Mention yourself."},
            {"name": "instagram_name", "question": "What is your Instagram name?"},
            {"name": "edit_link", "question": "Link for the edit you want to apply with:"},
            {"name": "activity_level", "question": "How active will you be (1 - 5)?"},
            {"name": "additional_info", "question": "Anything else you want us to know?"}
        ]

        self.application_file = "applications.json"
        self.applications = self.load_applications()

    def load_applications(self):
        try:
            with open(self.application_file, "r") as file:
                applications = json.load(file)
                return applications
        except FileNotFoundError:
            return {}
    
    def save_applications(self):
        with open(self.application_file, "w") as file:
            json.dump(self.applications, file, indent=4)

    @commands.command()
    async def apply(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.message.delete()  # Delete the author's command message

        user_id = str(ctx.author.id)
        if user_id in self.applications:
            await ctx.send("You have already submitted an application.")
            return

        answers = {"discord_id": user_id}

        for question in self.questions:
            question_msg = await ctx.send(question["question"])
            response = await self.bot.wait_for('message', check=check)
            answers[question["name"]] = response.content

            await question_msg.delete()  # Delete the bot's question message
            await response.delete()  # Delete the author's response

        embed = discord.Embed(title="Application Form", color=0x2b2d31)
        embed.add_field(name="Discord ID", value=f"<@{answers['discord_id']}>", inline=False)
        embed.add_field(name="Instagram Name", value=answers.get("instagram_name", "N/A"), inline=False)
        embed.add_field(name="Edit Link", value=answers.get("edit_link", "N/A"), inline=False)
        embed.add_field(name="Activity Level", value=answers.get("activity_level", "N/A"), inline=False)
        embed.add_field(name="Additional Info", value=answers.get("additional_info", "N/A"), inline=False)
        embed.set_footer(text=f"User ID: {answers['discord_id']}")

        channel_id = 1122183100038905908  # Replace with the desired channel ID
        channel = self.bot.get_channel(channel_id)

        if channel:
            await channel.send(embed=embed)
        else:
            await ctx.send("Failed to find the specified channel.")

        confirmation_msg = await ctx.send("Your application has been submitted. Thank you!")

        self.applications[user_id] = answers
        self.save_applications()

        await asyncio.sleep(5)  # Wait for 5 seconds (you can adjust the duration)
        await confirmation_msg.delete()  # Delete the confirmation message

    @commands.command()
    async def resetids(self, ctx):
        if ctx.author.guild_permissions.administrator:
            self.applications = {}
            self.save_applications()
            await ctx.send("Application IDs have been reset.")
        else:
            await ctx.send("You don't have permission to reset application IDs.")

    @commands.command()
    async def viewapplications(self, ctx):
        if ctx.author.guild_permissions.administrator:
            if not self.applications:
                await ctx.send("No applications have been submitted.")
                return

            for application in self.applications.values():
                user_id = application["discord_id"]
                user = self.bot.get_user(int(user_id))

                embed = discord.Embed(title="Application Form", color=0x2b2d31)
                embed.add_field(name="Discord ID", value=f"<@{user_id}>", inline=False)
                embed.add_field(name="Instagram Name", value=application.get("instagram_name", "N/A"), inline=False)
                embed.add_field(name="Edit Link", value=application.get("edit_link", "N/A"), inline=False)
                embed.add_field(name="Activity Level", value=application.get("activity_level", "N/A"), inline=False)
                embed.add_field(name="Additional Info", value=application.get("additional_info", "N/A"), inline=False)
                embed.set_footer(text=f"User ID: {user_id}")

                await ctx.send(f"Application by {user.mention}:")
                await ctx.send(embed=embed)
        else:
            await ctx.send("You don't have permission to view applications.")





async def setup(bot):
    await bot.add_cog(appnewtest(bot))
