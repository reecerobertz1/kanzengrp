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
        self.hidden = True

    @commands.command()
    async def roles(self, ctx):
        select = Select(
            placeholder="Select a role",
            options=[
                discord.SelectOption(label="he/him", value="he/him", emoji="<:_1:1178012295503286423>"),
                discord.SelectOption(label="she/her", value="she/her", emoji="<:_2:1178012298208624651>"),
                discord.SelectOption(label="they/them", value="they/them", emoji="<:_3:1178012301287243786>"),
                discord.SelectOption(label="he/they", value="he/they", emoji="<:_4:1178012304554610688>"),
                discord.SelectOption(label="she/they", value="she/they", emoji="<:_5:1178012281406234674>"),
                discord.SelectOption(label="any/ask", value="any/ask", emoji="<:_6:1178012308035874867>")
            ]
        )
        async def add_role(interaction: discord.Interaction):
            await interaction.response.defer()
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
        view = View(timeout=None)
        view.add_item(select)
        embed = discord.Embed(title="❄ What are your pronouns?", description="Which of the following pronouns do you use? These roles can help other members of the server use the correct pronouns.\n\n<:_1:1178012295503286423> - <@&1131127428668997737> \n<:_2:1178012298208624651> - <@&1131127209952809031> \n<:_3:1178012301287243786> - <@&1131127449753751663> \n<:_4:1178012304554610688> - <@&1131127472142958622> \n<:_5:1178012281406234674> - <@&1131127502396465213> \n<:_6:1178012308035874867> - <@&1131127523456069723>", color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1178017923512668190/extra_00000_00001.png?ex=65749daf&is=656228af&hm=e9425c9f907ad4e0add96d9b12cc1d8df9e543f569c3ea04106162931074b18d&")
        await ctx.send(embed=embed, view=view)
        await ctx.send("<:Empty:1137842301188702239>")

    @commands.command()
    async def roles1(self, ctx):
        select = Select(
            max_values=5,
            min_values=0,
            placeholder="Select a role",
            options=[
                discord.SelectOption(label="qotd", value="qotd", emoji="<:_1:1178012295503286423>"),
                discord.SelectOption(label="events", value="events", emoji="<:_2:1178012298208624651>"),
                discord.SelectOption(label="giveaways", value="giveaways", emoji="<:_3:1178012301287243786>"),
                discord.SelectOption(label="welc", value="welc", emoji="<:_4:1178012304554610688>"),
                discord.SelectOption(label="apps", value="apps", emoji="<:_5:1178012281406234674>"),
                discord.SelectOption(label="hoshi updates", emoji="<:_6:1178012308035874867>")
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
                "apps": 1131127124187684894,
                "hoshi updates": 1141771622785753138
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
        view = View(timeout=None)
        view.add_item(select)

        embed = discord.Embed(title="❄ What server pings would you like?", description="The staff will ping these roles whenever there's something related to these roles happening in the server.\n\n<:_1:1178012295503286423> - <@&1133770119777099866> \n<:_2:1178012298208624651> - <@&1131127168102055996> \n<:_3:1178012301287243786> - <@&1131127104226992208> \n<:_4:1178012304554610688> - <@&1131005057417105418> \n<:_5:1178012281406234674> - <@&1131127124187684894>\n<:_6:1178012308035874867> - <@&1141771622785753138>", color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1178017912959807489/extra_00000_00002.png?ex=65749dac&is=656228ac&hm=6956e40361e24079feced4ced29184e354ceaf6a4cd62e18971b95146c39ef5d&")
        await ctx.send(embed=embed, view=view)
        await ctx.send("<:Empty:1137842301188702239>")

    @commands.command()
    async def roles2(self, ctx):
        select = Select(
            max_values=5,
            min_values=0,
            placeholder="Select a role",
            options=[
                discord.SelectOption(label="collab", value="collab", emoji="<:_1:1178012295503286423>"),
                discord.SelectOption(label="edit help", value="edit help", emoji="<:_2:1178012298208624651>"),
                discord.SelectOption(label="dts", value="dts", emoji="<:_3:1178012301287243786>"),
                discord.SelectOption(label="ops", value="ops", emoji="<:_4:1178012304554610688>"),
                discord.SelectOption(label="chat revive", value="chat revive", emoji="<:_5:1178012281406234674>"),
                discord.SelectOption(label="games", emoji="<:_6:1178012308035874867>")
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
                "chat revive": 1134876934585712773,
                "games": 1141771607501713519,
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
        view = View(timeout=None)
        view.add_item(select)

        embed = discord.Embed(title="❄ What member pings would you like?",
                              description="These roles can be used by anyone in this server to ping other members! Please do not abuse these roles!\n\n<:_1:1178012295503286423> - <@&1131130157160206396>\n<:_2:1178012298208624651> - <@&1131127084379549757>\n<:_3:1178012301287243786> - <@&1131130102328078336>\n<:_4:1178012304554610688> - <@&1131127146186821685>\n<:_5:1178012281406234674> - <@&1134876934585712773>\n<:_6:1178012308035874867> - <@&1141771607501713519>",
                              color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1178017885021536303/extra_00000_00003.png?ex=65749da6&is=656228a6&hm=767c1e5226b89cc0af7e362dd3e4ef0b42d125b692a5e96e788de311a8f44691&")
        await ctx.send(embed=embed, view=view)
        await ctx.send("<:Empty:1137842301188702239>")

    @commands.command()
    async def roles3(self, ctx):
        select = Select(
            max_values=2,
            min_values=0,
            placeholder="Select a role",
            options=[
                discord.SelectOption(label="vent", value="vent", emoji="<:_1:1178012295503286423>"),
                discord.SelectOption(label="partner mute", value="partner mute", emoji="<:_2:1178012298208624651>")
            ]
        )
        async def add_role(interaction: discord.Interaction):
            await interaction.response.defer()
            role_ids = {
                "vent": 1141780367808925717,
                "partner mute": 1131127183159590953
            }
            
            member = interaction.user
            selected_value = interaction.data["values"][0]
            selected_role_id = role_ids.get(selected_value)
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
        view = View(timeout=None)
        view.add_item(select)

        embed = discord.Embed(title="❄ What extra roles do you want?", description="Which of the following roles do you want? These roles are for other access to extra channels in the  server!\n\n<:_1:1178012295503286423> - <@&1141780367808925717>\n<:_2:1178012298208624651> - <@&1131127183159590953>", color=0x2b2d31)
        await ctx.send("https://cdn.discordapp.com/attachments/1131006428631539773/1178017933138608279/extra_00000_00000.png?ex=65749db1&is=656228b1&hm=3139cf8969deb5d2ed095591940d181d7f63aeb7bd6fcf9f9af6d79c01e48000&")
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Roles(bot))