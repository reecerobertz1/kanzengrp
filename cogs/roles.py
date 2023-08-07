from discord import ui, Embed
from discord.interactions import Interaction
from collections import deque
from typing import List
from discord.ui import View, Select
import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        pronouns = ["He/Him", "She/Her", "They/Them", "He/They", "She/They", "Any"]
        server_pings = ["Announcements", "Events", "Updates", "Giveaways", "Polls", "None"]
        member_pings = ["Game Nights", "Movie Nights", "Study Group", "Meme Chat", "Art Chat", "None"]

        # Create a select menu for pronouns
        pronouns_menu = discord.ui.Select(placeholder="Please select your pronouns:", options=[
            discord.SelectOption(label=pronoun, value=f"pronoun_{pronoun}") for pronoun in pronouns
        ])

        # Create a select menu for server pings
        server_pings_menu = discord.ui.Select(placeholder="Please select your server ping:", options=[
            discord.SelectOption(label=server_ping, value=f"server_ping_{server_ping}") for server_ping in server_pings
        ])

        # Create a select menu for member pings
        member_pings_menu = discord.ui.Select(placeholder="Please select your member ping:", options=[
            discord.SelectOption(label=member_ping, value=f"member_ping_{member_ping}") for member_ping in member_pings
        ])

        await ctx.send("Please select your roles:", view=pronouns_menu)

        # Wait for the user to make a selection
        interaction = await self.bot.wait_for('select_option', check=lambda i: i.user == ctx.author)

        role_type, role_name = interaction.values[0].split("_")

        # Add the corresponding role to the member
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await ctx.author.add_roles(role)
            await ctx.send(f"You selected the role: {role_name}")
        else:
            await ctx.send("Oops, something went wrong. Please try again later.")

async def setup(bot):
    await bot.add_cog(Roles(bot))