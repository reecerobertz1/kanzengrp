import asyncio
import json
import discord
from discord.ext import commands
import re

class applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def accept(self, ctx, member: discord.Member):
        if ctx.guild.id == 1123347338841313331:  # Aura
            invite_server_id = 957987670787764224
            accepted_channel_id = 1123588246614577213
            add_role_id = 1123356130970701878
            remove_role_id = 1123356165246566491
            embed_color = 0x2b2d31
        elif ctx.guild.id == 1122181605591621692:  # Kanzen
            invite_server_id = 1121841073673736215
            accepted_channel_id = 1123588044180684800
            add_role_id = 1122191098006224906
            remove_role_id = 1122191119430733835
            embed_color = 0x2b2d31
        elif ctx.guild.id == 901409710572466217:  # daegu
            invite_server_id = 896619762354892821  
            accepted_channel_id = 901410829218492456
            add_role_id = 1119012138640494594
            remove_role_id = 901412966241554462
            embed_color = 0x2b2d31
        else:
            await ctx.reply("You can only use this command in specific servers.")
            return

        accepted_channel = self.bot.get_channel(accepted_channel_id)
        if accepted_channel:
            await accepted_channel.send(f"{member.mention} has been accepted.")
            await ctx.message.add_reaction("✅")
        else:
            await ctx.reply("Failed to find the specified channel.")

        invite = await self.generate_invite(invite_server_id)

        # Create server-specific embeds
        embed1 = discord.Embed(color=embed_color)
        embed1.set_image(url='https://cdn.discordapp.com/attachments/1121841074512605186/1128394231115948072/theme_3_00000.png')
        embed1.add_field(name="You have been accepted into Kanzen!", value=f"[**Click here to join**]({invite})")
        embed2 = discord.Embed(color=embed_color)
        embed2.set_image(url='https://cdn.discordapp.com/banners/957987670787764224/3b81da990294e7cf80a6b53d3ee98a1f.png?size=1024')
        embed2.add_field(name="You have been accepted into Auragrp!", value=f"[**Click here to join**]({invite})")
        embed3 = discord.Embed(color=embed_color)
        embed3.set_image(url='https://cdn.discordapp.com/banners/896619762354892821/906d72346deed85c1abe719216180be0.png?size=1024')
        embed3.add_field(name="You have been accepted into Daegu!", value=f"[**Click here to join**]({invite})")

        guild = self.bot.get_guild(ctx.guild.id)
        role_to_add = guild.get_role(add_role_id)
        role_to_remove = guild.get_role(remove_role_id)

        if role_to_add:
            await member.add_roles(role_to_add)
        else:
            await ctx.reply("Failed to find the role to add.")

        if role_to_remove:
            await member.remove_roles(role_to_remove)
        else:
            await ctx.reply("Failed to find the role to remove.")

        if ctx.guild.id == 1122181605591621692:
            await member.send(embed=embed1)
        elif ctx.guild.id == 1123347338841313331:
            await member.send(embed=embed2)
        elif ctx.guild.id == 901409710572466217:
            await member.send(embed=embed3)

    async def generate_invite(self, server_id):
        server = self.bot.get_guild(server_id)
        if server:
            invites = await server.invites()
            if invites:
                return invites[0].url
            else:
                invite = await server.text_channels[0].create_invite()
                return invite.url
        else:
            raise ValueError("Failed to find the specified server.")


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def decline(self, ctx, mention_or_id):
        guild_id = ctx.guild.id
        if guild_id == 1122181605591621692:
            server_name = "Kanzen"
            decline_channel_id = 1123588044180684800
        elif guild_id == 1123347338841313331:
            server_name = "Auragrp"
            decline_channel_id = 1123588246614577213
        elif guild_id == 901409710572466217:
            server_name = "Daegutown"
            decline_channel_id = 901410829218492456
        else:
            await ctx.reply("This command is not available in this server.")
            return

        decline_channel = self.bot.get_channel(decline_channel_id)
        if decline_channel:
            try:
                member = await commands.MemberConverter().convert(ctx, mention_or_id)
            except commands.MemberNotFound:
                try:
                    member = await self.bot.fetch_user(int(mention_or_id))
                except (ValueError, discord.NotFound):
                    await ctx.reply("Invalid mention or user ID.")
                    return

            await decline_channel.send(f"{member.mention} has been declined.")
            await ctx.send(f"Decline message has been sent to {member.name}.")
            await member.send(f"Hey, you have been declined in {server_name}. Please don't be upset or discouraged! We will have more recruitments in the future. <3")
        else:
            await ctx.reply(f"Failed to find the decline channel.")

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
    async def acceptt(self, ctx):
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

                # DM the user with the invite links
                embed = discord.Embed(title="Congratulations! You have been accepted!", color=0x2b2d31)
                for group, server_id in accepted_server_ids:
                    invite_link = await self.create_invite(server_id)
                    if invite_link:
                        embed.add_field(name=group.capitalize(), value=f"[Join Here]({invite_link})", inline=True)

                user = self.bot.get_user(user_id)
                if user:
                    await user.send(embed=embed)

                # Edit the original embed to show the accepted status
                embed = msg.embeds[0]
                embed.add_field(name="Status", value="Accepted ✅")
                await ctx.message.add_reaction("✅")
                await msg.edit(embed=embed)
            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply with the embed you want to process.")


async def setup(bot):
    await bot.add_cog(applications(bot))
