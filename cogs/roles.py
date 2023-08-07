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
            
            # Define the role IDs and their corresponding labels
            role_ids = {
                "he/him": 1131127428668997737,
                "she/her": 1131127209952809031,
                "they/them": 1131127449753751663,
                "he/they": 1131127472142958622,
                "she/they": 1131127502396465213,
                "any/ask": 1131127523456069723
            }
            
            member = interaction.user
            selected_value = interaction.data["values"][0]
            selected_role_id = role_ids.get(selected_value)
            
            # Remove existing pronoun roles from the user
            for role_id in role_ids.values():
                role = interaction.guild.get_role(role_id)
                if role and role in member.roles:
                    await member.remove_roles(role)
            
            if selected_role_id:
                role = interaction.guild.get_role(selected_role_id)
                if role:
                    await member.add_roles(role)
                    await interaction.followup.send(f"You selected {selected_value}", ephemeral=True)
                else:
                    await interaction.followup.send("Role not found. Please contact a server admin.", ephemeral=True)
            else:
                await interaction.followup.send("Invalid role selection. Please try again.", ephemeral=True)

        select.callback = add_role
        view = View()
        view.add_item(select)

        embed = discord.Embed(title="<:leaf:1137454366886993950> What are your pronouns?", description="Which of the following pronouns do you use? These roles can help other members of the server use the correct pronouns.\n\n<:1:1137455321028251708> - <@&1131127428668997737> \n<:2:1137455517577531565> - <@&1131127209952809031> \n<:3:1137455658258673704> - <@&1131127449753751663> \n<:4:1137455776877781107> - <@&1131127472142958622> \n<:5:1137455941609078824> - <@&1131127502396465213> \n<:6:1137456046978383892> - <@&1131127523456069723>", color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1138222545187909713/pronouns_new_00000_2.png")
        await ctx.send(embed=embed, view=view)
        await ctx.send("<:Empty:1137842301188702239>")

    @commands.command()
    async def roles1(self, ctx):
        select = Select(
            max_values=5,
            min_values=0,
            placeholder="Select a role",
            options=[
                discord.SelectOption(label="qotd", value="qotd", emoji="<:1:1137455321028251708>"),
                discord.SelectOption(label="events", value="events", emoji="<:2:1137455517577531565>"),
                discord.SelectOption(label="giveaways", value="giveaways", emoji="<:3:1137455658258673704>"),
                discord.SelectOption(label="welc", value="welc", emoji="<:4:1137455776877781107>"),
                discord.SelectOption(label="apps", value="apps", emoji="<:5:1137455941609078824>"),
            ]
        )
        async def add_role(interaction: discord.Interaction):
            await interaction.response.defer()
            selected_values = interaction.data["values"]

            role_mapping = {
                "qotd": 1133770119777099866,
                "events": 1131127168102055996,
                "giveaways": 1131127104226992208,
                "welc": 1131005057417105418,
                "apps": 1131127124187684894
            }

            member = interaction.guild.get_member(interaction.user.id)

            roles_to_add = []
            roles_to_remove = []

            for selected_value in role_mapping:
                role_id = role_mapping[selected_value]
                role = interaction.guild.get_role(role_id)

                if selected_value in selected_values:
                    if role:
                        if role in member.roles:
                            roles_to_remove.append(role)
                        else:
                            roles_to_add.append(role)

            if roles_to_add:
                await member.add_roles(*roles_to_add)
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)

            if roles_to_add or roles_to_remove:
                if roles_to_add and roles_to_remove:
                    operation_msg = f"You have updated roles: added {', '.join(role.name for role in roles_to_add)} and removed {', '.join(role.name for role in roles_to_remove)}."
                elif roles_to_add:
                    operation_msg = f"You have updated roles: added {', '.join(role.name for role in roles_to_add)}."
                else:
                    operation_msg = f"You have updated roles: removed {', '.join(role.name for role in roles_to_remove)}."

                await interaction.followup.send(operation_msg, ephemeral=True)
            else:
                await interaction.followup.send("No changes were made to your roles.", ephemeral=True)

        select.callback = add_role
        view = View()
        view.add_item(select)

        embed = discord.Embed(title="<:leaf:1137454366886993950> What server pings would you like?", description="The staff will ping these roles whenever there's something related to these roles happening in the server.\n\n<:1:1137455321028251708> - <@&1133770119777099866> \n<:2:1137455517577531565> - <@&1131127168102055996> \n<:3:1137455658258673704> - <@&1131127104226992208> \n<:4:1137455776877781107> - <@&1131005057417105418> \n<:5:1137455941609078824> - <@&1131127124187684894>", color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1138225991446179930/pings_new_00000.png")
        await ctx.send(embed=embed, view=view)
        await ctx.send("<:Empty:1137842301188702239>")

    @commands.command()
    async def roles2(self, ctx):
        select = Select(
            max_values=5,
            min_values=0,
            placeholder="Select a role",
            options=[
                discord.SelectOption(label="collab", value="collab", emoji="<:1:1137455321028251708>"),
                discord.SelectOption(label="edit help", value="edit help", emoji="<:2:1137455517577531565>"),
                discord.SelectOption(label="dts", value="dts", emoji="<:3:1137455658258673704>"),
                discord.SelectOption(label="ops", value="ops", emoji="<:4:1137455776877781107>"),
                discord.SelectOption(label="chat revive", value="chat revive", emoji="<:5:1137455941609078824>"),
            ]
        )
        async def add_role(interaction: discord.Interaction):
            await interaction.response.defer()
            selected_values = interaction.data["values"]

            role_mapping = {
                "collab": 1131130157160206396,
                "edit help": 1131127084379549757,
                "dts": 1131130102328078336,
                "ops": 1131127146186821685,
                "chat revive": 1134876934585712773
            }

            member = interaction.guild.get_member(interaction.user.id)

            roles_to_add = []
            roles_to_remove = []

            for selected_value in role_mapping:
                role_id = role_mapping[selected_value]
                role = interaction.guild.get_role(role_id)

                if selected_value in selected_values:
                    if role:
                        if role in member.roles:
                            roles_to_remove.append(role)
                        else:
                            roles_to_add.append(role)

            if roles_to_add:
                await member.add_roles(*roles_to_add)
            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)

            if roles_to_add or roles_to_remove:
                if roles_to_add and roles_to_remove:
                    operation_msg = f"You have updated roles: added {', '.join(role.name for role in roles_to_add)} and removed {', '.join(role.name for role in roles_to_remove)}."
                elif roles_to_add:
                    operation_msg = f"You have updated roles: added {', '.join(role.name for role in roles_to_add)}."
                else:
                    operation_msg = f"You have updated roles: removed {', '.join(role.name for role in roles_to_remove)}."

                await interaction.followup.send(operation_msg, ephemeral=True)
            else:
                await interaction.followup.send("No changes were made to your roles.", ephemeral=True)

        select.callback = add_role
        view = View()
        view.add_item(select)

        embed = discord.Embed(title="<:leaf:1137454366886993950> What member pings would you like?",
                              description="These roles can be used by anyone in this server to ping other members! Please do not abuse these roles!\n\n<:1:1137455321028251708> - <@&1131130157160206396>\n<:2:1137455517577531565> - <@&1131127084379549757>\n<:3:1137455658258673704> - <@&1131130102328078336>\n<:4:1137455776877781107> - <@&1131127146186821685>\n<:5:1137455941609078824> - <@&1134876934585712773>",
                              color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1138232205261422682/member_pings_new_00000.png")
        await ctx.send(embed=embed, view=view)
        await ctx.send("<:Empty:1137842301188702239>")

async def setup(bot):
    await bot.add_cog(Roles(bot))