import asyncio
import json
import discord
from discord.ext import commands

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


    @commands.command()
    async def taccept(self, ctx):
        if ctx.message.reference is not None:
            try:
                # Fetch the replied message
                replied_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)

                if replied_msg.embeds:
                    embed = replied_msg.embeds[0]
                    content = embed.description.lower()  # Convert to lowercase to make it case-insensitive

                    # Mapping of keywords to group names
                    group_mapping = {
                        "kanzen": "Kanzen",
                        "daegu": "Daegu",
                        "aura": "Aura",
                    }

                    groups = []  # List to store accepted groups

                    # Check if the content contains any of the keywords and get the associated group name
                    for keyword, group_name in group_mapping.items():
                        if keyword in content:
                            groups.append(group_name)

                    if groups:
                        # React with a tick emoji
                        await ctx.message.add_reaction("✅")

                        # Send a message in the specified channel with the accepted groups
                        channel_id = 1131006361921130526
                        channel = self.bot.get_channel(channel_id)
                        mention = ctx.author.mention
                        groups_text = ", ".join(groups)
                        await channel.send(f"{mention} was accepted into {groups_text}")

            except discord.errors.NotFound:
                await ctx.send("The replied message was not found.")
        else:
            await ctx.send("You need to reply to a message with an embed to use this command.")


    @commands.command()
    async def acceptt(self, ctx):
        def check_author(m):
            return m.author == ctx.author

        # Wait for the user to reply with the embed information
        await ctx.send("Please provide the embed information.")
        msg = await self.bot.wait_for('message', check=check_author)

        # Check if the words 'kanzen', 'aura', or 'daegu' are in the embed
        grps = msg.embeds[0].fields[0].value.lower()
        user_id = msg.embeds[0].fields[1].value.strip()
        accepted_server_id = None
        if "kanzen" in grps:
            accepted_server_id = 1121841073673736215
        elif "aura" in grps:
            accepted_server_id = 957987670787764224
        elif "daegu" in grps:
            accepted_server_id = 896619762354892821
        else:
            await ctx.send("Sorry, the server name (kanzen, aura, or daegu) was not found in the embed.")
            return

        # DM the user with the invite link
        user = self.bot.get_user(int(user_id))
        if user is not None:
            invite = await self.bot.get_guild(accepted_server_id).create_invite(max_uses=1, unique=True)
            await user.send(f"Here is your invite to the server: {invite}")

            # Edit the original embed to show the accepted status
            embed = msg.embeds[0]
            embed.add_field(name="Status", value="Accepted ✅")
            await ctx.message.add_reaction("✅")
            await msg.edit(embed=embed)
        else:
            await ctx.send("Unable to find the user. Please make sure the provided ID is correct.")


async def setup(bot):
    await bot.add_cog(applications(bot))
