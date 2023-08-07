from discord import ui, Embed
from discord.interactions import Interaction
from collections import deque
from typing import List
from discord.ui import View, Select
import discord
from discord.ext import commands

class RoleView(discord.ui.View):
    def __init__(self, category):
        super().__init__()
        self.category = category

    async def on_select(self, interaction: discord.Interaction, role_name: str):
        role = discord.utils.get(interaction.guild.roles, name=role_name)
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

        embed = discord.Embed(title="Pronouns", description="Please select your pronouns:")
        for pronoun in pronouns:
            embed.add_field(name=pronoun, value=f"React with ✅ to choose {pronoun}", inline=False)

        view = RoleView("pronouns")
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def serverpings(self, ctx):
        server_pings = ["Announcements", "Events", "Updates", "Giveaways", "Polls", "None"]

        embed = discord.Embed(title="Server Pings", description="Please select your server ping:")
        for ping in server_pings:
            embed.add_field(name=ping, value=f"React with ✅ to choose {ping}", inline=False)

        view = RoleView("server_pings")
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def memberpings(self, ctx):
        member_pings = ["Game Nights", "Movie Nights", "Study Group", "Meme Chat", "Art Chat", "None"]

        embed = discord.Embed(title="Member Pings", description="Please select your member ping:")
        for ping in member_pings:
            embed.add_field(name=ping, value=f"React with ✅ to choose {ping}", inline=False)

        view = RoleView("member_pings")
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Roles(bot))