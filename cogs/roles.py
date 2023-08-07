from discord import ui, Embed
from discord.interactions import Interaction
from collections import deque
from typing import List
from discord.ui import View, Select
import discord
from discord.ext import commands
from discord.utils import get


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        select = Select(
            placeholder="Select a role",
            options=[
                discord.SelectOption(label="he/him", value="he/him", emoji="<:1:1137455321028251708>"),
                discord.SelectOption(label="she/her", value="she/her", emoji="<:2:1137455517577531565>"),
                discord.SelectOption(label="they/them", value="they/them", emoji="<:3:1137455658258673704>"),
                discord.SelectOption(label="he/they", value="he/they", emoji="<:4:1137455776877781107>"),
                discord.SelectOption(label="she/they", value="she/they", emoji="<:5:1137455941609078824>"),
                discord.SelectOption(label="any/ask", value="any/ask", emoji="<:6:1137456046978383892>")
            ]
        )
        async def add_role(interaction: discord.Interaction):
            await interaction.response.defer()
            if select.values[0] == "he/him":
                member = interaction.user
                role_id = 1131127428668997737
                role = interaction.guild.get_role(role_id)
                await member.add_roles(role)
            elif select.values[0] == "she/her":
                member = interaction.user
                role_id = 1131127209952809031
                role = interaction.guild.get_role(role_id)
                await member.add_roles(role)
            elif select.values[0] == "they/them":
                role_id = 1131127449753751663
                role = interaction.guild.get_role(role_id)
                member = interaction.user
                await member.add_roles(role)
            elif select.values[0] == "he/they":
                role_id = 1131127472142958622
                role = interaction.guild.get_role(role_id)
                member = interaction.user
                await member.add_roles(role)
            elif select.values[0] == "she/they":
                role_id = 1131127502396465213
                role = interaction.guild.get_role(role_id)
                member = interaction.user
                await member.add_roles(role)
            elif select.values[0] == "any/ask":
                role_id = 1131127523456069723
                role = interaction.guild.get_role(role_id)
                member = interaction.user
                await member.add_roles(role)
            await interaction.followup.send(f"You selected {select.values[0]}", ephemeral=True)
        select.callback = add_role
        view = View()
        view.add_item(select)

        embed = discord.Embed(title="<:leaf:1137454366886993950> What are your pronouns?", description="Which of the following pronouns do you use? These roles can help other members of the server use the correct pronouns.\n\n<:1:1137455321028251708> - <@&1131127428668997737> \n<:2:1137455517577531565> - <@&1131127209952809031> \n<:3:1137455658258673704> - <@&1131127449753751663> \n<:4:1137455776877781107> - <@&1131127472142958622> \n<:5:1137455941609078824> - <@&1131127502396465213> \n<:6:1137456046978383892> - <@&1131127523456069723>", color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1138222545187909713/pronouns_new_00000_2.png")
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Roles(bot))