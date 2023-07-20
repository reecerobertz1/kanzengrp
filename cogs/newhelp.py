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
        
        # Create the "About Hoshi" initial embed with fields
        about_hoshi_embed = discord.Embed(title="About Hoshi", description="This is the bot information page.")
        about_hoshi_embed.add_field(name="The coding", value="Hoshi is coded in Python 3.11.4\n[Download Python 3.11.4](https://www.python.org/downloads/)")
        about_hoshi_embed.add_field(name="Owner", value="Hoshi is owned by Reeceroberts\nReece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)")
        about_hoshi_embed.add_field(name="Extra Information", value="Hoshi's prefix is `+`\nHoshi was made for **__Kanzengrp__")
        
        # Create the initial category embed with fields
        initial_category = categories[0]
        embed = discord.Embed(title=initial_category)
        embed.add_field(name="Field 1", value="This is the first field for the first category.")
        embed.add_field(name="Field 2", value="This is the second field for the first category.")
        
        # Create a view to handle the interaction
        view = discord.ui.View()
        view.add_item(dropdown)

        # Send the initial "About Hoshi" embed with the dropdown menu
        message = await ctx.send(embed=about_hoshi_embed, view=view)

        # Function to handle the dropdown selection
        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            if selected_category == initial_category:
                embed.clear_fields()
                embed.add_field(name="Field 1", value="This is the first field for the first category.")
                embed.add_field(name="Field 2", value="This is the second field for the first category.")
            elif selected_category == "Category 2":
                embed.clear_fields()
                embed.add_field(name="Field 1", value="This is the first field for the second category.")
                embed.add_field(name="Field 2", value="This is the second field for the second category.")
            elif selected_category == "Category 3":
                embed.clear_fields()
                embed.add_field(name="Field 1", value="This is the first field for the third category.")
                embed.add_field(name="Field 2", value="This is the second field for the third category.")
            elif selected_category == "Category 4":
                embed.clear_fields()
                embed.add_field(name="Field 1", value="This is the first field for the fourth category.")
                embed.add_field(name="Field 2", value="This is the second field for the fourth category.")
            
            await interaction.response.edit_message(embed=embed)

        # Assign the callback function to the dropdown
        dropdown.callback = dropdown_callback

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(NewHelp(bot))