from discord import ui, Embed
from discord.interactions import Interaction
from collections import deque
from typing import List
from discord.ui import View, Select
import discord
from discord.ext import commands

class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__()

    async def on_select(self, interaction: discord.Interaction, role_type: str, role_name: str):
        role_id = {
            "pronoun_He/Him": 1122635691487137881,
            "pronoun_She/Her": 1122635691487137884,
            "pronoun_They/Them": 1122635691487137886,
            "pronoun_He/They": 1122635691487137882,
            "pronoun_She/They": 1122635691487137885,
            "pronoun_Any": 1122635691487137880,
            "server_ping_Announcements": YOUR_SERVER_PING_ROLE_ID,
            "server_ping_Events": YOUR_SERVER_PING_ROLE_ID,
            # Add the role IDs for other server ping options
            "member_ping_Game Nights": YOUR_MEMBER_PING_ROLE_ID,
            "member_ping_Movie Nights": YOUR_MEMBER_PING_ROLE_ID,
            # Add the role IDs for other member ping options
        }

        role = discord.utils.get(interaction.guild.roles, id=role_id.get(role_name))
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You selected the role: {role_name}", ephemeral=True)
        else:
            await interaction.response.send_message("Oops, something went wrong. Please try again later.", ephemeral=True)

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pronouns(self, ctx):
        pronouns = ["He/Him", "She/Her", "They/Them", "He/They", "She/They", "Any"]
        pronouns_menu = discord.ui.Select(custom_id="pronouns_select", placeholder="Please select your pronouns:")

        for pronoun in pronouns:
            pronouns_menu.add_option(label=pronoun, value=f"pronoun_{pronoun}")

        view = RoleView()
        view.add_item(pronouns_menu)

        await ctx.send("Please select your pronouns:", view=view)

    @commands.command()
    async def serverpings(self, ctx):
        server_pings = ["Announcements", "Events", "Updates", "Giveaways", "Polls", "None"]
        server_pings_menu = discord.ui.Select(custom_id="server_pings_select", placeholder="Please select your server ping:")

        for server_ping in server_pings:
            server_pings_menu.add_option(label=server_ping, value=f"server_ping_{server_ping}")

        view = RoleView()
        view.add_item(server_pings_menu)

        await ctx.send("Please select your server ping:", view=view)

    @commands.command()
    async def memberpings(self, ctx):
        member_pings = ["Game Nights", "Movie Nights", "Study Group", "Meme Chat", "Art Chat", "None"]
        member_pings_menu = discord.ui.Select(custom_id="member_pings_select", placeholder="Please select your member ping:")

        for member_ping in member_pings:
            member_pings_menu.add_option(label=member_ping, value=f"member_ping_{member_ping}")

        view = RoleView()
        view.add_item(member_pings_menu)

        await ctx.send("Please select your member ping:", view=view)

async def setup(bot):
    await bot.add_cog(Roles(bot))