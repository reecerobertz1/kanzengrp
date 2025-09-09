import discord
from discord.ext import commands
from bot import LalisaBot
from discord import app_commands

class reviews(discord.ui.View):
    def __init__ (self, bot, username, member, member2):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot
        self.username = username
        self.member = member
        self.member2 = member2

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.Button):
        original_message = interaction.message
        member = self.member2
        if original_message.embeds:
            embed = original_message.embeds[0]
            embed.color = discord.Color(0x248045)
            await original_message.edit(embed=embed, view=None)
        await interaction.response.send_message(f"You accepted **{self.username}**", ephemeral=True)
        embed = discord.Embed(title="WELCOME TO CHROMA", description=f"・Welcome to chroma **{self.username}**!\n・Please use the button below to join our members server.\n・If you have any questions, feel free to ping our @staff or @leads\n・And make sure to read our [rules](https://discord.com/channels/694010548605550675/725373131220320347)!", color=0x2b2d31)
        channel = interaction.client.get_channel(725373131220320347)
        invite = await channel.create_invite(max_age=86400, max_uses=1, unique=True)
        invite_url = str(invite)
        await member.send(invite_url, embed=embed)
        await interaction.client.get_channel(835837557036023819).send(f"https://instagram.com/{self.username}/")
        await self.update_status(status=4, member=self.member)
        await self.update_applied(applied=0, member=self.member)
        await self.update_accepted(accepted=1, member=self.member)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.Button):
        member = self.member2
        attempts = await self.get_attempts(member=self.member)
        original_message = interaction.message
        if original_message.embeds:
            embed = original_message.embeds[0]
            embed.color = discord.Color(0xdc343d)
            await original_message.edit(embed=embed, view=None)
        await interaction.response.send_message(f"You declined **{self.username}**", ephemeral=True)
        if attempts == 2:
            msg = f"Unfortunetly your application was declined.\nYou can re-apply when you are ready!\n\nRemaining attempts: **2**"
        if attempts == 1:
            msg = f"Unfortunetly your application was declined.\nYou can re-apply when you are ready!\n\nRemaining attempts: **1**"
        if attempts == 0:
            msg = f"Unfortunetly your application was declined and you have used all your attempts for this recruit.\nPlease don't be discouraged as we will do more recruits in the future! 🌹"
        await member.send(msg)
        await self.update_status(status=2, member=self.member)
        await self.update_applied(applied=0, member=self.member)

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

    @discord.ui.button(label="Apply", style=discord.ButtonStyle.red)
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

class application(discord.ui.Modal, title='🌹Chroma Applications'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    instagram = discord.ui.TextInput(label="What is your Instagram?", style=discord.TextStyle.short)
    edit = discord.ui.TextInput(label="Send us 1 link to an edit of yours", style=discord.TextStyle.short)
    program = discord.ui.TextInput(label="What editing program or app do you use?", style=discord.TextStyle.short)
    other = discord.ui.TextInput(label="Anything else you want us to know?", style=discord.TextStyle.paragraph, required=False)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🌹Chroma Applications", description="", color=0x2b2d31)
        embed.add_field(name="What is your Instagram?", value=self.instagram.value, inline=False)
        embed.add_field(name="Send us 1 link to an edit of yours", value=self.edit.value, inline=False)
        embed.add_field(name="What editing program or app do you use?", value=self.program.value, inline=False)
        embed.set_thumbnail(url=interaction.guild.icon)
        if self.other.value:
            embed.add_field(name="Anything else you want us to know?", value=self.other.value, inline=False)
        attempts = await self.get_attempts(member=interaction.user.id)
        await interaction.client.get_channel(835497793703247903).send(embed=embed, view=reviews(bot=self.bot, username=self.instagram.value, member=interaction.user.id, member2=interaction.user))
        if attempts == 2:
            await self.update_attempts(member=interaction.user.id, attempts=1)
        elif attempts == 1:
            await self.update_attempts(member=interaction.user.id, attempts=0)
        else:
            await self.add_member(member=interaction.user.id)
        await self.update_status(member=interaction.user.id)
        await interaction.response.send_message(f'Thanks for applying for chromagrp! We will DM you with a response with our bot <@1122150120574681138>', ephemeral=True)

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
        embed=discord.Embed(title="CHROMA APPLICATIONS", description="Welcome to [chromagrp's](https://instagram.com/chromagrp) new era recruit! Please\nread the information below!\n\n**INFORMATION**\n• Make sure you have followed all recruit rules.\n• Click the **Apply** button and fill out the form.\n• Hoshi will DM you with our response.\n⠀— ・You will get a response if you're declined!.\n• You only have 3 attempts to apply.\n• Please make sure your dms are open before applying.\n• The recruit will close on **<t:1758712200:D>**.\n\n-# **Note:** please be patient with us! you will get a response soon!\n-# Ask any questions in <#862624723057508372>.", color=0x2b2d31)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1055168099252437094/1349783735901618317/icon_3.gif?ex=67d45b90&is=67d30a10&hm=c1221982c437df66703f5911604193c8fae740433cb387ae99d6708c16cb027c&")
        await ctx.send(embed=embed, view=apply(bot=self.bot))

async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(applications(bot))