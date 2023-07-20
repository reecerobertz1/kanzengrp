from typing import Any
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import View, Select

class NewHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

"""    @commands.command()
    async def newhelp(self, ctx):
        # Create the dropdown menu with different categories
        categories = [
            "Fun commands",
            "Editing commands",
            "Other commands",
            "Kanzen only commands",
            "Levels commands",
            "Moderation commands",
            "Application commands"
        ]
        dropdown = discord.ui.Select(placeholder="Select a category...", options=[discord.SelectOption(label=category) for category in categories])

        # Create the initial "About Hoshi" embed with fields
        about_hoshi_embed = discord.Embed(title="> <a:kanzenflower:1128154723262943282>: About Hoshi", color=0x2b2d31)
        about_hoshi_embed.add_field(name="The coding", value="Hoshi is coded in Python 3.11.4\n[Download Python 3.11.4](https://www.python.org/downloads/)", inline=False)
        about_hoshi_embed.add_field(name="Owner", value="Hoshi is owned by Reeceroberts\nReece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)", inline=False)
        about_hoshi_embed.add_field(name="Extra Information", value="Hoshi's prefix is `+`\nHoshi was made for **__Kanzengrp__**", inline=False)

        # Create a view to handle the interaction
        view = discord.ui.View()
        view.add_item(dropdown)

        # Send the initial "About Hoshi" embed with the dropdown menu
        message = await ctx.send(embed=about_hoshi_embed, view=view)

        # Function to handle the dropdown selection
        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            if selected_category == categories[0]:
                embed = discord.Embed(title="> Fun commands", color=0x2b2d31)
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
            elif selected_category == categories[1]:
                embed = discord.Embed(title="> Editing commands", color=0x2b2d31)
                embed.add_field(name="+transition", value="<:reply:1125269313432059904> Get a random transition to use in your edit", inline=False)
                embed.add_field(name="+audio", value="<:reply:1125269313432059904> Get an audio added by a member to use for your edit", inline=False)
                embed.add_field(name="+addaudio", value="<:reply:1125269313432059904> Add an audio from SoundCloud for others to use", inline=False)
                embed.add_field(name="+addedit", value="<:reply:1125269313432059904> Add your own edit to Hoshi (must be a streamable link)", inline=False)
                embed.add_field(name="+edits", value="<:reply:1125269313432059904> Watch edits added from members of, Aura, Kanzen and Daegu", inline=False)
                embed.add_field(name="+effects", value="<:reply:1125269313432059904> Get a random effect to use in your edit", inline=False)
                embed.add_field(name="+colorscheme", value="<:reply:1125269313432059904> Get a random color scheme to use in your edit", inline=False)
            elif selected_category == categories[2]:
                embed = discord.Embed(title="> Other commands", color=0x2b2d31)
                embed.add_field(name="+ia", value="<:reply:1125269313432059904> Send us an inactivity message if you go inactive", inline=False)
                embed.add_field(name="/ia", value="<:reply:1125269313432059904> Send us an inactivity message if you go inactive (kanzengrp only)", inline=False)
            elif selected_category == categories[3]:
                embed = discord.Embed(title="> Kanzen only commands", color=0x2b2d31)
                embed.add_field(name="+newcmd", value="<:reply:1125269313432059904> Make your own command! `+newcmd (command name) (hoshi's responce)`", inline=False)
                embed.add_field(name="+listcmds", value="<:reply:1125269313432059904> See all the commands other zennies have added", inline=False)
                embed.add_field(name="+removecmd", value="<:reply:1125269313432059904> Made a mistake in your command? do `+removecmd (+commandname)`", inline=False)
            elif selected_category == categories[4]:
                embed = discord.Embed(title="> Levels commands", color=0x2b2d31)
                embed.add_field(name="+rank", value="<:reply:1125269313432059904> See your rank, or someone elses", inline=False)
                embed.add_field(name="+levels", value="<:reply:1125269313432059904> See the level leaderboard for the server", inline=False)
                embed.add_field(name="+rankcolor", value="<:reply:1125269313432059904> Set your rank color with a hex code", inline=False)
                embed.add_field(name="+xp add", value="<:reply:1125269313432059904> Add xp to a member (admin only command)", inline=False)
                embed.add_field(name="+xp remove", value="<:reply:1125269313432059904> Remove xp from a member (admin only command)", inline=False)
                embed.add_field(name="+reset add", value="<:reply:1125269313432059904> Resets xp for everyone (admin only)", inline=False)
                embed.add_field(name="+levelling on", value="<:reply:1125269313432059904> Enables the levelling system for the server (admin only)", inline=False)
                embed.add_field(name="+levelling off", value="<:reply:1125269313432059904> Disables the levelling system for the server (admin only)", inline=False)
                embed.add_field(name="+levelling setrole", value="<:reply:1125269313432059904> Set the top 20 active role", inline=False)
            elif selected_category == categories[5]:
                embed = discord.Embed(title="> Moderation commands", color=0x2b2d31)
                embed.add_field(name="+kick", value="<:reply:1125269313432059904> Kick a member from the server", inline=False)
                embed.add_field(name="+ban", value="<:reply:1125269313432059904> Ban a member from the server", inline=False)
                embed.add_field(name="+addrole", value="<:reply:1125269313432059904> Add a role to a member (+addrole @role @mention)", inline=False)
                embed.add_field(name="+removerole", value="<:reply:1125269313432059904> Remove a role from a member (+removerole @role @mention)", inline=False)
                embed.add_field(name="+buildembed", value="<:reply:1125269313432059904> Create an embed", inline=False)
                embed.add_field(name="+suggest", value="<:reply:1125269313432059904> Suggest what we can do in the group (+suggest [suggestion])", inline=False)
                embed.add_field(name="+uptime", value="<:reply:1125269313432059904> See how long the bot has been online for", inline=False)
                embed.add_field(name="+ping", value="<:reply:1125269313432059904> See the bots ping", inline=False)
            elif selected_category == categories[6]:
                embed = discord.Embed(title="> Application commands", color=0x2b2d31)
                embed.add_field(name="/apply", value="<:reply:1125269313432059904> Apply for kanzengrp", inline=False)
                embed.add_field(name="/app", value="<:reply:1125269313432059904> Apply for auragrp", inline=False)
                embed.add_field(name="+accept @mention", value="<:reply:1125269313432059904> Accepts member into kanzen", inline=False)
                embed.add_field(name="+decline @mention", value="<:reply:1125269313432059904> Declines a member from kanzen", inline=False)
                embed.add_field(name="+resetapps", value="<:reply:1125269313432059904> Resets all IDs from forms", inline=False)
                embed.add_field(name="+viewapps", value="<:reply:1125269313432059904> See all applications sent", inline=False)
                embed.add_field(name="+qna", value="<:reply:1125269313432059904> Ask the lead a question", inline=False)
                embed.add_field(name="+answer", value="<:reply:1125269313432059904> Answer a question sent", inline=False)
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")

            await interaction.response.edit_message(embed=embed)

        # Assign the callback function to the dropdown
        dropdown.callback = dropdown_callback

    # Add other commands and functions for the cog, if needed."""


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(NewHelp(bot))