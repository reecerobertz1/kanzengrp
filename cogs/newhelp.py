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
        categories = ["Fun Commands", "Category 2", "Category 3", "Category 4"]
        dropdown = discord.ui.Select(placeholder="Select a category...", options=[discord.SelectOption(label=category) for category in categories])
        
        # Create the "About Hoshi" initial embed
        about_hoshi_embed = discord.Embed(title="> <a:Lumi_penguin_fall:1122607666578063531> : About Hoshi", description="**The coding**\nHoshi is coded in Python 3.11.4\n[Download Python 3.11.4](https://www.python.org/downloads/)\n\n**Owner**\nHoshi is owned by Reeceroberts\nReece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)\n\n**Extra Information**\nHoshi's prefix is `+`\nHoshi was made for **__Kanzengrp__**")
        
        # Create the initial category embed
        initial_category = categories[0]
        embed = discord.Embed(title=initial_category, description="This is the description for the first category.")
        
        # Create a view to handle the interaction
        view = discord.ui.View()
        view.add_item(dropdown)

        # Send the initial "About Hoshi" embed with the dropdown menu
        message = await ctx.send(embed=about_hoshi_embed, view=view)

        # Function to handle the dropdown selection
        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            if selected_category == initial_category:
                embed.description = "**+dog**\n<:reply:1125269313432059904> Sends you a random photo of a dog.\n\n**+cat**\n<:reply:1125269313432059904> Sends you a random photo of a cat.\n\n**+jail**\n<:reply:1125269313432059904> Put someone or yourself in jail\n\n**+pride**\n<:reply:1125269313432059904> Puts the pride flag on someones avatar.\n\n**+memberinfo**\n<:reply:1125269313432059904> View info for yourself or others\n\n**+kiss**\n<:reply:1125269313432059904> Mention someone to kiss, or don't mention anyone for Hoshi to kiss you\n\n**+hug**\n<:reply:1125269313432059904> Mention someone to hug, or don't mention anyone for Hoshi to hug you\n\n**+slap**\n<:reply:1125269313432059904> Mention someone to slap, or don't mention anyone for Hoshi to slap you"
            elif selected_category == "Category 2":
                embed.description = "This is the description for the second category."
            elif selected_category == "Category 3":
                embed.description = "This is the description for the third category."
            elif selected_category == "Category 4":
                embed.description = "This is the description for the fourth category."
            
            await interaction.response.edit_message(embed=embed)

        # Assign the callback function to the dropdown
        dropdown.callback = dropdown_callback

    # Add other commands and functions for the cog, if needed.

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(NewHelp(bot))