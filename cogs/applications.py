import asyncio
import json
import discord
from discord.ext import commands
import re

class applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

"""    def is_judge():
        async def predicate(ctx):
            role_id = 1135216335652143104
            role = ctx.guild.get_role(role_id)
            return role in ctx.author.roles
        return commands.check(predicate)

    async def create_invite(self, guild_id):
        try:
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                raise ValueError("Invalid server ID")

            invite = await guild.text_channels[0].create_invite(max_uses=1, unique=True)
            return invite.url
        except Exception as e:
            print(f"Failed to create invite: {e}")
            return None

    @commands.command()
    @is_judge()
    async def accept(self, ctx):
        if ctx.message.reference is not None:
            try:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                embed = msg.embeds[0]
                group_field = next((field for field in embed.fields if field.name == 'Group(s) they want to be in:'), None)
                user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)
                insta_field = next((field for field in embed.fields if field.name == 'Instagram Account Link:'), None)

                if not group_field or not user_id_field or not insta_field:
                    await ctx.send("Invalid embed format. Please make sure the embed contains fields 'Group(s) they want to be in:' and 'Discord ID'.")
                    return

                grps = group_field.value.lower()
                groups = [group.strip() for group in re.split(r'[,\s]+', grps)]

                insta = insta_field.value.lower()
                insta = [insta.strip() for insta in re.split(r'[,\s]+', insta)]

                user_id = int(re.search(r'\d+', user_id_field.value).group())  # Extract the user ID from the field value
                accepted_server_ids = []

                for group in groups:
                    if "kanzen" in group:
                        accepted_server_ids.append((group, 1121841073673736215))
                    elif "aura" in group:
                        accepted_server_ids.append((group, 957987670787764224))
                    elif "daegu" in group:
                        accepted_server_ids.append((group, 896619762354892821))

                if not accepted_server_ids:
                    await ctx.send("Sorry, I could not find a group name in this embed...")
                    return

                embed = discord.Embed(title="Congratulations! You have been accepted!", color=0x2b2d31)
                for group, server_id in accepted_server_ids:
                    invite_link = await self.create_invite(server_id)  # Implement this function to generate the invite link
                    if invite_link:
                        embed.add_field(name=group.capitalize(), value=f"[Join Here]({invite_link})", inline=True)

                user = discord.utils.get(ctx.guild.members, id=user_id)
                if user:
                    await user.send(embed=embed)

                    channel = ctx.guild.get_channel(1131006361921130526)
                    if channel:
                        await channel.send(f"{user.mention} was accepted")

                    instachannel = ctx.guild.get_channel(1137423800623960116)
                    if instachannel:
                        await instachannel.send(f"You need to follow {', '.join(insta)}\nThey were accepted into {', '.join(groups)}")

                embed = msg.embeds[0]
                embed.add_field(name="Status", value="Accepted ✅")
                await ctx.message.add_reaction("✅")
                await msg.edit(embed=embed)

            except Exception as e:
                await ctx.send(f"An error occurred: {e}")

                guild = ctx.guild
                role_to_add = guild.get_role(1131016215754715166)
                if role_to_add:
                    await user.add_roles(role_to_add)

                role_to_remove = guild.get_role(1131016147282710679)
                if role_to_remove:
                    await user.remove_roles(role_to_remove)

            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply with the embed you want to process.")

    @commands.command()
    @is_judge()
    async def decline(self, ctx):
        if ctx.message.reference is not None:
            try:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                embed = msg.embeds[0]
                group_field = next((field for field in embed.fields if field.name == 'Group(s) they want to be in:'), None)
                user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)

                if not group_field or not user_id_field:
                    await ctx.send("Invalid embed format. Please make sure the embed contains fields 'Group(s) they want to be in:' and 'Discord ID'.")
                    return

                grps = group_field.value.lower()
                groups = [group.strip() for group in re.split(r'[,\s]+', grps)]

                user_id = user_id_field.value.strip()

                # DM the user with the decline message
                user = self.bot.get_user(int(user_id))
                if user:
                    decline_message = f"Hey! You have been declined from {', '.join(groups)}. Please don't be upset or discouraged! We will have more recruitments in the future. <3"
                    await user.send(decline_message)

                    channel = ctx.guild.get_channel(1131006361921130526)
                    if channel:
                        await channel.send(f"{user.mention} was declined")

                # Edit the original embed to show the declined status
                embed = msg.embeds[0]
                embed.add_field(name="Status", value="Declined ❌")
                await ctx.message.add_reaction("✅")
                await msg.edit(embed=embed)
            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply with the embed you want to process.")

    @commands.command(aliases=['sa'])
    @commands.has_permissions(manage_guild=True)
    async def staffaccept(self, ctx):
        if ctx.message.reference is not None:
            try:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                embed = msg.embeds[0]
                user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)

                if user_id_field:
                    user_id = user_id_field.value.strip()

                    # DM the user with the decline message
                    user = await ctx.guild.fetch_member(int(user_id))
                    if user:
                        decline_message = f"Hey! you have been accepted as a new staff member for Kanzengrp\nPlease go into <#1135247559431032833> for more information"
                        await user.send(decline_message)

                        # Edit the original embed to show the declined status
                        embed = msg.embeds[0]
                        embed.add_field(name="Status", value="Accepted ✅")
                        await ctx.message.add_reaction("✅")
                        await msg.edit(embed=embed)

                        role_to_add = ctx.guild.get_role(1135244903165722695)
                        if role_to_add:
                            await user.add_roles(role_to_add)
                    else:
                        await ctx.send("Failed to find the user.")
                else:
                    await ctx.send("Failed to find the Discord ID field in the embed.")
            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply with the embed you want to process.")"""

async def setup(bot):
    await bot.add_cog(applications(bot))
