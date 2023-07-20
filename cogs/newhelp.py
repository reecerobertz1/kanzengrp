from typing import Any
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import View, Select

class NewHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newhelp(self, ctx):
        # Create the dropdown menu with different categories
        categories = [
            "> About Hoshi",
            "> Fun commands",
            "> Editing commands",
            "> Other commands",
            "> Kanzen only commands",
            "> Levels commands",
            "> Moderation commands",
            "> Application commands"
        ]
        dropdown = discord.ui.Select(placeholder="Select a category...", options=[discord.SelectOption(label=category) for category in categories])

        # Create the initial "About Hoshi" embed with fields
        about_hoshi_embed = discord.Embed(title="About Hoshi")
        about_hoshi_embed.add_field(name="The coding", value="Hoshi is coded in Python 3.11.4\n[Download Python 3.11.4](https://www.python.org/downloads/)", inline=False)
        about_hoshi_embed.add_field(name="Owner", value="Hoshi is owned by Reeceroberts\nReece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)", inline=False)
        about_hoshi_embed.add_field(name="Extra Information", value="Hoshi's prefix is `+`\nHoshi was made for **__Kanzengrp__", inline=False)

        # Create a view to handle the interaction
        view = discord.ui.View()
        view.add_item(dropdown)

        # Send the initial "About Hoshi" embed with the dropdown menu
        message = await ctx.send(embed=about_hoshi_embed, view=view)

        # Function to handle the dropdown selection
        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            if selected_category == categories[0]:
                embed = discord.Embed(title="About Hoshi", description="This is the bot information page.")
                embed.add_field(name="Bot Name", value="Hoshi Bot")
                embed.add_field(name="Author", value="YourName#1234")
                embed.add_field(name="Version", value="1.0.0")
            elif selected_category == categories[1]:
                embed = discord.Embed(title="Fun commands")
                embed.add_field(name="+dog", value="<:reply:1125269313432059904> Sends you a random photo of a dog", inline=False)
                embed.add_field(name="+cat", value="<:reply:1125269313432059904> Sends you a random photo of a cat", inline=False)
                embed.add_field(name="+jail", value="<:reply:1125269313432059904> Put someone or yourself in jail", inline=False)
                embed.add_field(name="+pride", value="<:reply:1125269313432059904> Puts the pride flag on someones avatar", inline=False)
                embed.add_field(name="+memberinfo", value="<:reply:1125269313432059904> View info for yourself or others", inline=False)
                embed.add_field(name="+kiss", value="<:reply:1125269313432059904> Mention someone to kiss, or don't mention anyone for Hoshi to kiss you", inline=False)
                embed.add_field(name="+hug", value="<:reply:1125269313432059904> Mention someone to hug, or don't mention anyone for Hoshi to hug you", inline=False)
                embed.add_field(name="+slap", value="<:reply:1125269313432059904> Mention someone to slap, or don't mention anyone for Hoshi to slap you", inline=False)
                embed.add_field(name="+roast", value="<:reply:1125269313432059904> Get a roast from Hoshi", inline=False)
                embed.add_field(name="+compliment", value="<:reply:1125269313432059904> Get a compliment from Hoshi", inline=False)
                embed.add_field(name="+say", value="<:reply:1125269313432059904> Make Hoshi say exactly what you say", inline=False)
                embed.add_field(name="+8ball", value="<:reply:1125269313432059904> Ask Hoshi a question and get an answer", inline=False)
                embed.add_field(name="+ship", value="<:reply:1125269313432059904> Mention 2 members to see if Hoshi ships them (+ship @mention @mention)", inline=False)
                embed.add_field(name="+trivia", value="<:reply:1125269313432059904> Hoshi will ask you a question, make sure to answer correctly (answer with numbers 1-4)", inline=False)
                embed.add_field(name="+avatar", value="<:reply:1125269313432059904> Get a photo of your avatar or someone elses", inline=False)
                # Add more fun commands fields here
                embed.add_field(name="", value="`[page 2/8]`", inline=True)
            elif selected_category == categories[2]:
                embed = discord.Embed(title="Editing commands")
                embed.add_field(name="+transition", value="<:reply:1125269313432059904> Get a random transition to use in your edit", inline=False)
                embed.add_field(name="+audio", value="<:reply:1125269313432059904> Get an audio added by a member to use for your edit", inline=False)
                # Add more editing commands fields here
                embed.add_field(name="", value="`[page 3/8]`", inline=True)
            elif selected_category == categories[3]:
                embed = discord.Embed(title="Other commands")
                embed.add_field(name="+ia", value="<:reply:1125269313432059904> Send us an inactivity message if you go inactive", inline=False)
                embed.add_field(name="/ia", value="<:reply:1125269313432059904> Send us an inactivity message if you go inactive (kanzengrp only)", inline=False)
                # Add more other commands fields here
                embed.add_field(name="", value="`[page 4/8]`", inline=True)
            # Add more categories and their fields here
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")

            await interaction.response.edit_message(embed=embed)

        # Assign the callback function to the dropdown
        dropdown.callback = dropdown_callback

    # Add other commands and functions for the cog, if needed.


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(NewHelp(bot))