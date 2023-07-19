import asyncio
import json
import discord
from discord.ext import commands

class applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.questions = [
            {"name": "discord_name", "question": f"What is your Discord name?"},
            {"name": "instagram_name", "question": f"What is your Instagram name?"},
            {"name": "edit_link", "question": f"Link for the edit you want to apply with (instagram only!)"},
            {"name": "activity_level", "question": f"How active will you be (1 - 5)?"},
            {"name": "additional_info", "question": f"Anything else you want us to know?"}
        ]
        self.application_file = "applications.json"
        self.applications = self.load_applications()

    def load_applications(self):
        try:
            with open(self.application_file, "r") as file:
                applications = json.load(file)
                return applications
        except FileNotFoundError:
            return {}
    
    def save_applications(self):
        with open(self.application_file, "w") as file:
            json.dump(self.applications, file, indent=4)

    @commands.command()
    async def app(self, ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.message.delete()  # Delete the author's command message

        user_id = str(ctx.author.id)
        if user_id in self.applications:
            await ctx.send("You have already submitted an application.")
            return

        answers = {"discord_id": user_id}

        for question in self.questions:
            question_msg = await ctx.send(question["question"])
            response = await self.bot.wait_for('message', check=check)
            answers[question["name"]] = response.content

            await question_msg.delete()  # Delete the bot's question message
            await response.delete()  # Delete the author's response

        embed = discord.Embed(title="Application Form", color=0x2b2d31)
        embed.add_field(name="Discord ID", value=f"<@{answers['discord_id']}>", inline=False)
        embed.add_field(name="Instagram Name", value=answers.get("instagram_name", "N/A"), inline=False)
        embed.add_field(name="Edit Link", value=answers.get("edit_link", "N/A"), inline=False)
        embed.add_field(name="Activity Level", value=answers.get("activity_level", "N/A"), inline=False)
        embed.add_field(name="Additional Info", value=answers.get("additional_info", "N/A"), inline=False)
        embed.set_footer(text=f"User ID: {answers['discord_id']}")

        if ctx.guild.id == 1122181605591621692:
            channel_id = 1122183100038905908  # Channel ID for server 1122181605591621692
            invite_server_id = 1121841073673736215  # Invite Server ID for server 1122181605591621692
            add_role_id = 1122191098006224906  # Role ID to add for server 1122181605591621692
            remove_role_id = 1122191119430733835  # Role ID to remove for server 1122181605591621692
            embed_color = 0x00FF00  # Green color for the embed
        elif ctx.guild.id == 1123347338841313331:
            channel_id = 1123353889228468305  # Channel ID for server 1123347338841313331
            invite_server_id = 957987670787764224  # Invite Server ID for server 1123347338841313331
            add_role_id = 1123356130970701878  # Role ID to add for server 1123347338841313331
            remove_role_id = 1123356165246566491  # Role ID to remove for server 1123347338841313331
            embed_color = 0xFF0000  # Red color for the embed
        elif ctx.guild.id == 901409710572466217:
            channel_id = 901410829218492456  # Channel ID for server 901409710572466217
            invite_server_id = 896619762354892821  # Invite Server ID for server 901409710572466217
            add_role_id = 1119012138640494594  # Role ID to add for server 901409710572466217
            remove_role_id = 901412966241554462  # Role ID to remove for server 901409710572466217
            embed_color = 0x0000FF  # Blue color for the embed
        else:
            await ctx.send("You can't apply with this command in this group!")
            return

        channel = self.bot.get_channel(channel_id)

        if channel:
            await channel.send(embed=embed)
        else:
            await ctx.send("Failed to find the specified channel.")

        confirmation_msg = await ctx.send("Your application has been submitted. Thank you!")

        self.applications[user_id] = answers
        self.save_applications()

        await asyncio.sleep(5)  # Wait for 5 seconds (you can adjust the duration)
        await confirmation_msg.delete()  # Delete the confirmation message

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def resetapps(self, ctx):
        if ctx.author.guild_permissions.administrator:
            self.applications = {}
            self.save_applications()
            await ctx.send("Application IDs have been reset.")
        else:
            await ctx.send("You don't have permission to reset application IDs.")

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

async def setup(bot):
    await bot.add_cog(applications(bot))
