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

        # Send the first message with pronouns
        pronouns_embed = discord.Embed(title="Pronouns", description="Please select your pronouns:")
        pronouns_menu = RolesMenu()
        for pronoun in pronouns:
            pronouns_menu.add_item(RolesButton(label=pronoun, custom_id=f"pronoun_{pronoun}"))

        pronouns_message = await ctx.send(embed=pronouns_embed, view=pronouns_menu)

        # Send the second message with server pings
        server_pings_embed = discord.Embed(title="Server Pings", description="Please select your server ping:")
        server_pings_menu = RolesMenu()
        for server_ping in server_pings:
            server_pings_menu.add_item(RolesButton(label=server_ping, custom_id=f"server_ping_{server_ping}"))

        server_pings_message = await ctx.send(embed=server_pings_embed, view=server_pings_menu)

        # Send the third message with member pings
        member_pings_embed = discord.Embed(title="Member Pings", description="Please select your member ping:")
        member_pings_menu = RolesMenu()
        for member_ping in member_pings:
            member_pings_menu.add_item(RolesButton(label=member_ping, custom_id=f"member_ping_{member_ping}"))

        member_pings_message = await ctx.send(embed=member_pings_embed, view=member_pings_menu)

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        if isinstance(interaction.data, discord.MessageComponent):
            if interaction.custom_id.startswith("pronoun_"):
                pronoun = interaction.custom_id[8:]
                member = interaction.author
                role = discord.utils.get(member.guild.roles, name=pronoun)

                if role:
                    await member.add_roles(role)
                    await interaction.response.send_message(f"You selected the pronoun: {pronoun}", ephemeral=True)
                else:
                    await interaction.response.send_message("Oops, something went wrong. Please try again later.", ephemeral=True)

class RolesButton(discord.ui.Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        view.clear_items()
        await interaction.message.edit(view=view)

class RolesMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def on_timeout(self):
        self.clear_items()

async def setup(bot):
    await bot.add_cog(Roles(bot))