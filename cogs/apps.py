import discord
from discord.ext import commands
from bot import LalisaBot
from discord import app_commands

class answerfeedback(discord.ui.View):
    def __init__(self, bot, username, member, member2, app_message, reviewer):
        super().__init__(timeout=None)
        self.bot = bot
        self.username = username
        self.member = member
        self.member2 = member2
        self.app_message = app_message
        self.reviewer = reviewer

    @discord.ui.button(label="Give Feedback")
    async def feedback(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(
            AnswerFeedback(
                bot=self.bot,
                member2=self.member2,
                member=self.member,
                username=self.username,
                app_message=self.app_message,
                reviewer=self.reviewer
            )
        )

class feedback(discord.ui.View):
    def __init__(self, bot, username, member, member2, app_message, reviewer):
        super().__init__(timeout=None)
        self.bot = bot
        self.username = username
        self.member = member
        self.member2 = member2
        self.app_message = app_message
        self.reviewer = reviewer

    @discord.ui.button(label="Request Feedback")
    async def feedback(self, interaction: discord.Interaction, button: discord.Button):
        view=answerfeedback(self.bot, self.username, self.member, self.member2, self.app_message, reviewer=self.reviewer)
        channel = interaction.client.get_channel(1409916083627888661)
        app_url = f"https://discord.com/channels/{self.app_message.guild.id}/{self.app_message.channel.id}/{self.app_message.id}"
        embed = discord.Embed(title="Feedback Requested", description=f"{self.member2} has requested feedback!\n[click here]({app_url}) to view their application!\n\n-# Please only give feedback to requests that ping you.\n-# Please react to this message once feedback has been given!")
        await channel.send(f"<@{self.reviewer}>", embed=embed, view=view)
        await interaction.response.send_message("Okay! Feedback has been requested.\nYour feedback will be sent here when a staff member responds!")
        await interaction.edit_original_response(view=None)

class areyousuredecline(discord.ui.View):
    def __init__(self, bot, username, member, member2, app_message):
        super().__init__(timeout=None)
        self.bot = bot
        self.username = username
        self.member = member
        self.member2 = member2
        self.app_message = app_message

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.Button):
        member = self.member2
        attempts = await self.get_attempts(member=self.member)
        if self.app_message and self.app_message.embeds:
            embed = self.app_message.embeds[0]
            embed.color = discord.Color(0xdc343d)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1055168099252437094/1406644414809378886/Comp_1_00001.png"
            )
            await self.app_message.edit(embed=embed, view=None)

        await interaction.response.send_message(f"You declined **{self.username}**", ephemeral=True)
        if attempts == 2:
            msg = "Unfortunately your application was declined.\nYou can re-apply when you are ready!\n\nRemaining attempts: **2**\n\nYou can now request feedback during chroma recruits!\nClick the button below to get feedback on your edit."
            view=feedback(self.bot, self.username, self.member, self.member2, self.app_message, reviewer=interaction.user.id)
        elif attempts == 1:
            msg = "Unfortunately your application was declined.\nYou can re-apply when you are ready!\n\nRemaining attempts: **1**"
            view=feedback(self.bot, self.username, self.member, self.member2, self.app_message, reviewer=interaction.user.id)
        else:
            msg = "Unfortunately your application was declined and you have used all your attempts for this recruit.\nPlease don't be discouraged as we will do more recruits in the future!\n\nUnfortunetly you're not able to receive feedback now."
            view=None
        await member.send(msg, view=view)

        await self.update_status(status=2, member=self.member)
        await self.update_applied(applied=0, member=self.member)
        await interaction.message.delete()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Okay I have cancelled the decline!", ephemeral=True)
        await interaction.message.delete()

    async def update_status(self, member, status):
        query = '''UPDATE apps SET status = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (status, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_accepted(self, member, accepted):
        query = '''UPDATE apps SET accepted = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (accepted, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_applied(self, member, applied):
        query = '''UPDATE apps SET applied = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (applied, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_attempts(self, member):
        query = '''SELECT attempts FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member,))
                row = await cursor.fetchone()
                return int(row[0]) if row else 0


class areyousureaccept(discord.ui.View):
    def __init__(self, bot, username, member, member2, app_message):
        super().__init__(timeout=None)
        self.bot = bot
        self.username = username
        self.member = member
        self.member2 = member2
        self.app_message = app_message

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.Button):
        member = self.member2
        if self.app_message and self.app_message.embeds:
            embed = self.app_message.embeds[0]
            embed.color = discord.Color(0x248045)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/1055168099252437094/1406644414360846407/Comp_1_00000.png"
            )
            await self.app_message.edit(embed=embed, view=None)

        await interaction.response.send_message(f"You accepted **{self.username}**", ephemeral=True)

        embed = discord.Embed(
            title="WELCOME TO CHROMA",
            description=f"・Welcome to chroma **{self.username}**!\n・Please use the button below to join our members server.\n・If you have any questions, feel free to ping our @staff or @leads\n・And make sure to read our [rules](https://discord.com/channels/694010548605550675/725373131220320347)!",
            color=0x2b2d31,
        )
        channel = interaction.client.get_channel(725373131220320347)
        invite = await channel.create_invite(max_age=86400, max_uses=1, unique=True)
        await member.send(str(invite), embed=embed)

        await interaction.client.get_channel(835837557036023819).send(
            f"https://instagram.com/{self.username}/"
        )

        await self.update_status(status=4, member=self.member)
        await self.update_applied(applied=0, member=self.member)
        await self.update_accepted(accepted=1, member=self.member)
        await interaction.message.delete()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Okay I have cancelled the accept!", ephemeral=True)
        await interaction.message.delete()

    async def update_status(self, member, status):
        query = '''UPDATE apps SET status = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (status, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_accepted(self, member, accepted):
        query = '''UPDATE apps SET accepted = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (accepted, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_applied(self, member, applied):
        query = '''UPDATE apps SET applied = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (applied, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_attempts(self, member):
        query = '''SELECT attempts FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member,))
                row = await cursor.fetchone()
                return int(row[0]) if row else 0

class reviews(discord.ui.View):
    def __init__(self, bot, username, member, member2, app_message):
        super().__init__(timeout=None)
        self.bot = bot
        self.username = username
        self.member = member
        self.member2 = member2
        self.app_message = app_message

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(
            f"Are you sure you'd like to accept {self.username}?",
            view=areyousureaccept(self.bot, self.username, self.member, self.member2, self.app_message),
            ephemeral=True
        )

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(
            f"Are you sure you'd like to decline {self.username}?",
            view=areyousuredecline(self.bot, self.username, self.member, self.member2, self.app_message),
            ephemeral=True
        )

    @discord.ui.button(label="Send to voting")
    async def vote(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message(f"Okay! I have sent **{self.username}'s** edit", ephemeral=True)
        voting_channel = interaction.client.get_channel(1067235666917859348)
        if not voting_channel:
            return await interaction.followup.send("Failed to find the voting channel.", ephemeral=True)

        original_message = interaction.message
        original_message_link = f"https://discord.com/channels/{interaction.guild_id}/{original_message.channel.id}/{original_message.id}"
        vote_message = await voting_channel.send(f"**{interaction.user.name}** has sent **{self.username}'s** application.\n{original_message_link}")
        thread = await vote_message.create_thread(name=f"Discuss {self.username}'s edit")
        if original_message.embeds:
            embed = original_message.embeds[0]
            embed.color = discord.Color(0xECE2E2)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1055168099252437094/1406644415107436644/Comp_1_00002.png?ex=68a33732&is=68a1e5b2&hm=8d7e97621bdca9a68763a2a5f6c7c6591a2e5c103155a155e26ceb937b04cba7&")
            await original_message.edit(embed=embed)
        await vote_message.add_reaction("<:accept:974433091412189184>")
        await vote_message.add_reaction("<:DECLINE:974433189055594586>")
        await vote_message.add_reaction("❓")
        await self.update_status(status=3, member=self.member)

    async def update_status(self, member, status):
        query = '''UPDATE apps SET status = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (status, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_accepted(self, member, accepted):
        query = '''UPDATE apps SET accepted = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (accepted, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_applied(self, member, applied):
        query = '''UPDATE apps SET applied = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (applied, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def get_attempts(self, member):
        query = '''SELECT attempts FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member,))
                row = await cursor.fetchone()
                if row:
                    return int(row[0])
                else:
                    return 0

class apply(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Apply")
    async def apply(self, interaction: discord.Interaction, button: discord.Button):
        attempts = await self.get_attempts(member=interaction.user.id)
        applied = await self.if_applied(member=interaction.user.id)
        accepted = await self.if_accepted(member=interaction.user.id)
        if applied == 1:
            await interaction.response.send_message(
                "It seems like you have already applied. Please wait for a response from us before applying again!\n**Note:** You can do `/status` to see your application status.",
                ephemeral=True,
            )
            return

        elif attempts == 0 and applied is not None:
            await interaction.response.send_message(
                "Sorry, but you have used all your attempts this recruit :(\nKeep a lookout for future recruits to retry!",
                ephemeral=True,
            )
            return

        elif accepted == 1:
            await interaction.response.send_message(
                "It looks like we already accepted you to Chroma.\nPlease check your DMs from <@1122150120574681138> for our member server link!!",
                ephemeral=True,
            )
            return

        await interaction.response.send_modal(application(bot=self.bot))

    @discord.ui.button(label="Status")
    async def status(self, interaction: discord.Interaction, button: discord.Button):
        status = await self.get_status(member=interaction.user.id)
        attempts = await self.get_attempts(member=interaction.user.id)

        if status == 1:
            statuses = "Your application is currently **pending**.\nWe have not yet seen it. Please wait for a response in your DMs <3"
        if status == 2:
            if attempts == 2:
                statuses = "Unfortunately, your application has been **declined**.\nYou still have **2** more attempts to re-apply."
            elif attempts == 1:
                statuses = "Unfortunately, your application has been **declined**.\nYou still have **1** more attempt to re-apply."
            else:
                statuses = "Unfortunately, your application has been **declined**, and you have no more attempts left to re-apply."
        if status == 3:
            statuses = "Your application is currently being reviewed by our staff members. Please be patient with us and wait for our response! <3"
        if status == 4:
            statuses = "Congrats! You have been accepted into Chromagrp!\nPlease check your DMs from our bot <@1122150120574681138> for the member server link!"
        if status == 0:
            statuses = "You have not applied yet! Go to <#1252726042964136026> to start your application."

        await interaction.response.send_message(statuses, ephemeral=True)

    async def get_status(self, member):
        query = '''SELECT status FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member,))
                row = await cursor.fetchone()
                if row:
                    return int(row[0])
                else:
                    return 0

    async def if_applied(self, member):
        query = '''SELECT applied FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member,))
                row = await cursor.fetchone()
                if row is not None:
                    return int(row[0])
                return None

    async def if_accepted(self, member):
        query = '''SELECT accepted FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member,))
                row = await cursor.fetchone()
                if row is not None:
                    return int(row[0])
                return None

    async def get_attempts(self, member):
        query = '''SELECT attempts FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member,))
                row = await cursor.fetchone()
                if row is not None:
                    return int(row[0])
                return None

class application(discord.ui.Modal, title='Chroma Applications'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    instagram = discord.ui.TextInput(label="What is your Instagram?", style=discord.TextStyle.short)
    edit = discord.ui.TextInput(label="Link one edit (Insta + Streamable only)", style=discord.TextStyle.short)
    program = discord.ui.TextInput(label="What editing program or app do you use?", style=discord.TextStyle.short)
    other = discord.ui.TextInput(label="Anything else you want us to know?", style=discord.TextStyle.paragraph, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        valid_domains = ["https://www.instagram.com", "https://instagram.com", "https://streamable.com"]
        if not any(self.edit.value.startswith(domain) for domain in valid_domains):
            return await interaction.response.send_message(
                "Please provide a valid **Instagram** or **Streamable** link.",
                ephemeral=True
            )

        embed = discord.Embed(title="Chroma Applications", color=0x2b2d31)
        embed.add_field(name="What is your Instagram?", value=self.instagram.value, inline=False)
        embed.add_field(name="Link one edit", value=self.edit.value, inline=False)
        embed.add_field(name="What editing program or app do you use?", value=self.program.value, inline=False)
        embed.set_thumbnail(url=interaction.guild.icon)

        if self.other.value:
            embed.add_field(name="Anything else you want us to know?", value=self.other.value, inline=False)

        attempts = await self.get_attempts(member=interaction.user.id)
        channel = interaction.client.get_channel(835497793703247903)
        app_message = await channel.send(
            embed=embed,
            view=reviews(bot=self.bot, username=self.instagram.value, member=interaction.user.id, member2=interaction.user, app_message=None)
        )

        reviews_view = reviews(bot=self.bot, username=self.instagram.value, member=interaction.user.id, member2=interaction.user, app_message=app_message)
        await app_message.edit(view=reviews_view)

        if attempts == 2:
            await self.update_attempts(member=interaction.user.id, attempts=1)
        elif attempts == 1:
            await self.update_attempts(member=interaction.user.id, attempts=0)
        else:
            await self.add_member(member=interaction.user.id)

        await self.update_status(member=interaction.user.id)
        await interaction.response.send_message(
            f'Thanks for applying for chromagrp! We will DM you with a response with our bot <@1122150120574681138>',
            ephemeral=True
        )

    async def get_attempts(self, member):
        query = '''SELECT attempts FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member,))
                row = await cursor.fetchone()
                if row:
                    return int(row[0])
                else:
                    return 0

    async def update_status(self, member, status=1):
        query = '''UPDATE apps SET status = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (status, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def update_attempts(self, member, attempts):
        query = '''UPDATE apps SET attempts = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (attempts, member))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def add_member(self, member, attempts=2, applied=1):
        query_check = '''SELECT 1 FROM apps WHERE member_id = ?'''
        query_insert = '''INSERT INTO apps (member_id, attempts, applied, accepted, status) VALUES (?, ?, ?, ?, ?)'''
        
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query_check, (member,))
                existing_member = await cursor.fetchone()

                if existing_member:
                    return
                
                await cursor.execute(query_insert, (member, attempts, applied, "0", "1"))
                await conn.commit()
            
            await self.bot.pool.release(conn)

class AnswerFeedback(discord.ui.Modal, title="Chroma Application Feedback"):
    def __init__(self, bot, member2, member, username, app_message, reviewer):
        super().__init__()
        self.bot = bot
        self.member2 = member2
        self.member = member
        self.username = username
        self.app_message = app_message
        self.reviewer = reviewer

    givenfeedback = discord.ui.TextInput(
        label="What is your feedback?",
        style=discord.TextStyle.long
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.client.get_channel(1409994437261787332)
        embed = discord.Embed(title="Chroma Application Feedback", color=0x2b2d31)
        embed.add_field(name="Response:", value=self.givenfeedback.value, inline=False)
        embed.set_thumbnail(url=interaction.guild.icon)

        logs = discord.Embed(title="Feedback Logs", description=f"**Feedback**:\n{self.givenfeedback.value}\n\n"f"Sent from {interaction.user.mention} to {self.member2}")
        await interaction.response.send_message(f"Okay I have sent your feedback to {self.member2}", ephemeral=True)
        await channel.send(embed=logs)
        await self.member2.send(embed=embed)

class applications(commands.Cog):
    def __init__(self, bot: LalisaBot):
        self.bot = bot

    async def get_status(self, member):
        query = '''SELECT status FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member,))
                row = await cursor.fetchone()
                if row:
                    return int(row[0])
                else:
                    return 0

    async def get_attempts(self, member):
        query = '''SELECT attempts FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member,))
                row = await cursor.fetchone()
                if row:
                    return int(row[0])
                else:
                    return 0

    @app_commands.command(name="status", description="Check your current status for your application")
    async def status(self, interaction: discord.Interaction):
        status = await self.get_status(member=interaction.user.id)
        attempts = await self.get_attempts(member=interaction.user.id)

        if status == 1:
            statuses = "Your application is currently **pending**.\nWe have not yet seen it. Please wait for a response in your DMs <3"
        if status == 2:
            if attempts == 2:
                statuses = "Unfortunately, your application has been **declined**.\nYou still have **2** more attempts to re-apply."
            elif attempts == 1:
                statuses = "Unfortunately, your application has been **declined**.\nYou still have **1** more attempt to re-apply."
            else:
                statuses = "Unfortunately, your application has been **declined**, and you have no more attempts left to re-apply."
        if status == 3:
            statuses = "Your application is currently being reviewed by our staff members. Please be patient with us and wait for our response! <3"
        if status == 4:
            statuses = "Congrats! You have been accepted into Chromagrp!\nPlease check your DMs from our bot <@1122150120574681138> for the member server link!"
        if status == 0:
            statuses = "You have not applied yet! Go to <#1252726042964136026> to start your application."

        await interaction.response.send_message(statuses, ephemeral=True)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def openapps(self, ctx):
        image=discord.Embed(color=0x2b2d31)
        image.set_image(url="https://cdn.discordapp.com/attachments/1055168099252437094/1404752434076844082/welc_banner_00000_00000_00000_00000_00000.png?ex=689c5527&is=689b03a7&hm=36d9529dbac9c55fab855ba37596287458991beba4c926c0bbc3ec892b697df1&")
        embed=discord.Embed(title="CHROMA APPLICATIONS", description="Welcome to [chromagrp's](https://instagram.com/chromagrp) recruitment!! Please read \nthe information below!", color=0x2b2d31)
        info=discord.Embed(description="**INFORMATION**\n• Make sure you have followed all recruit rules.\n• Click the **Apply** button and fill out the form.\n• Hoshi will DM you with our response.\n⠀— ・You will get a response if you're declined!.\n⠀— ・You can request for feedback.\n• You only have 3 attempts to apply.\n• Please make sure your dms are open.\n• The recruit will close on **<t:1758712200:D>**.⠀⠀\n\n-# **Note:** Please be patient with us! You'll get a response.\n-# Ask any questions in <#862624723057508372>.",color=0x2b2d31)
        await ctx.send(embeds=[image, embed, info], view=apply(bot=self.bot))

    @commands.command(name="clearapps")
    @commands.has_permissions(administrator=True)
    async def clearapps(self, ctx: commands.Context):
        query = '''DELETE FROM apps'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                await conn.commit()
            await self.bot.pool.release(conn)

        await ctx.send("✅ All application data has been cleared from the database.", delete_after=10)

    @clearapps.error
    async def clearapps_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don’t have permission to use this command.", delete_after=10)
        else:
            raise error

    @commands.command(name="getapp")
    @commands.has_permissions(administrator=True)
    async def getapp(self, ctx, user_id: int):
        """Fetch an application from the DB and rebuild it with working buttons."""
        query = '''SELECT * FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (user_id,))
                row = await cursor.fetchone()
            await self.bot.pool.release(conn)

        if not row:
            return await ctx.send("❌ No application found for that user ID.")

        applicant_id = row[0]
        reviewer_id = row[1]

        applicant = await self.bot.fetch_user(applicant_id)

        embed = discord.Embed(
            title="Application",
            description=f"Application from {applicant}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Applicant ID", value=applicant_id)
        embed.add_field(name="Reviewer ID", value=reviewer_id)

        view = reviews(self.bot, applicant_id, reviewer_id)

        await ctx.send(embed=embed, view=view)

    @commands.command(name="deleteapp")
    @commands.has_permissions(administrator=True)
    async def deleteapp(self, ctx: commands.Context, user_id: int = None):
        if not user_id:
            return await ctx.send("Please provide a user ID.", delete_after=10)

        query = '''DELETE FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (user_id,))
                await conn.commit()
            await self.bot.pool.release(conn)

        await ctx.send(f"✅ Application data for user ID `{user_id}` has been deleted.", delete_after=10)

    @deleteapp.error
    async def deleteapp_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don’t have permission to use this command.", delete_after=10)
        else:
            raise error

async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(applications(bot))