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
        pronouns_menu = discord.ui.Select(placeholder="Please select your pronouns:", min_values=1, max_values=1)
        pronouns_menu.add_option(label="She/Her", value="she_her")
        pronouns_menu.add_option(label="He/Him", value="he_him")
        pronouns_menu.add_option(label="They/Them", value="they_them")

        server_pings_menu = discord.ui.Select(placeholder="Please select your server pings:", min_values=1, max_values=1)
        server_pings_menu.add_option(label="Announcements", value="announcements")
        server_pings_menu.add_option(label="Events", value="events")
        server_pings_menu.add_option(label="Giveaways", value="giveaways")

        member_pings_menu = discord.ui.Select(placeholder="Please select your member pings:", min_values=1, max_values=1)
        member_pings_menu.add_option(label="Group Updates", value="group_updates")
        member_pings_menu.add_option(label="Group Auditions", value="group_auditions")
        member_pings_menu.add_option(label="Collab Requests", value="collab_requests")

        await ctx.send("Please select your pronouns:", view=pronouns_menu)
        await ctx.send("Please select your server pings:", view=server_pings_menu)
        await ctx.send("Please select your member pings:", view=member_pings_menu)

    @commands.Cog.listener()
    async def on_select_option(self, interaction: discord.Interaction):
        if interaction.custom_id == "pronouns_menu":
            pronouns = interaction.values[0]
            role_id = 1122635691487137884  # Replace with the role ID for the selected pronoun
            role = discord.utils.get(interaction.guild.roles, id=role_id)
            if role:
                await interaction.user.add_roles(role)
        elif interaction.custom_id == "server_pings_menu":
            # Handle server pings role assignment here
            pass
        elif interaction.custom_id == "member_pings_menu":
            # Handle member pings role assignment here
            pass

async def setup(bot):
    await bot.add_cog(Roles(bot))