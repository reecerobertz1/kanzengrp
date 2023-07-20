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
        categories = ["About Hoshi", "Fun Commands", "Moderation Commands", "Kanzen Only"]
        dropdown = discord.ui.Select(placeholder="Select a category...", options=[discord.SelectOption(label=category) for category in categories])
        
        # Create the initial embed
        initial_category = categories[0]
        embed = discord.Embed(title=initial_category, description="**The coding**\nHoshi is coded in Python 3.11.4\n[Download Python 3.11.4](https://www.python.org/downloads/)\n\n**Owner**\nHoshi is owned by Reeceroberts\nReece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)\n\n**Extra Information**\nHoshi's prefix is `+`\nHoshi was made for **__Kanzengrp__")
        
        # Create a view to handle the interaction
        view = discord.ui.View()
        view.add_item(dropdown)

        # Send the initial embed with the dropdown menu
        message = await ctx.send(embed=embed, view=view)

        # Function to handle the dropdown selection
        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            if selected_category == initial_category:
                embed.description = "This is the description for the first category."
            elif selected_category == "Category 2":
                embed.description = "This is the description for the second category."
            elif selected_category == "Category 3":
                embed.description = "This is the description for the third category."
            elif selected_category == "Category 4":
                embed.description = "This is the description for the fourth category."
            
            await interaction.response.edit_message(embed=embed)

        # Assign the callback function to the dropdown
        dropdown.callback = dropdown_callback

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(NewHelp(bot))