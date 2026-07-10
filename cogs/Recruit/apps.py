import discord
from discord.ext import commands

class LeadReviewView(discord.ui.View):
    def __init__(self, applicant_id: int, username: str, edit: str, program: str, platform: str, reviewer: int, bot: commands.Bot):
        super().__init__(timeout=None)
        self.applicant_id = applicant_id
        self.username = username
        self.edit = edit
        self.program = program
        self.platform = platform
        self.bot = bot
        self.reviewer = reviewer

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.client.get_user(self.applicant_id)
        await interaction.response.send_message(f"You have accepted {self.username}'s application!", ephemeral=True)
        await interaction.message.edit(view=AcceptReviewVerify())
        review_channel = interaction.client.get_channel(1477653138185126100)
        embed = discord.Embed(title="CHROMATICA APPLICATIONS", description=f"Hello **{self.username}**,\n・⠀We wanted to let you know your application was **__ACCEPTED__**\n・⠀Congrats and welcome to Chromaticagp!\n・⠀Please make sure to read our Resonator [Handbook](https://discord.com/channels/1462079847433244799/1462134516456882249).\n・⠀And claim a name colour from our [Palette](https://discord.com/channels/1462079847433244799/1462138569572352030).\n\n-# **Note:** If you have any questions, feel free to ask a lead or a staff member!")
        main_server = interaction.client.get_guild(1462079847433244799)
        embed.set_thumbnail(url=main_server.icon.url)
        await member.send(embed=embed)
        await self.update_status(user_id=self.applicant_id, new_status=3)
        resonator_role = main_server.get_role(1462092411122749732)
        echoes_roles = main_server.get_role(1462092433637773322)
        guild_member = main_server.get_member(self.applicant_id)
        if resonator_role and guild_member:
            await guild_member.add_roles(resonator_role, reason="Accepted into Chromatica")
            await guild_member.remove_roles(echoes_roles, reason="Accepted into Chromatica")
        if review_channel:
            await review_channel.send(f"{self.reviewer} has accepted {self.username}'s application.")

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, custom_id="decline")
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        attempts = await self.get_attempts(user_id=self.applicant_id)
        member = interaction.client.get_user(self.applicant_id)
        main_server = interaction.client.get_guild(1462079847433244799)
        await interaction.response.send_message(f"You have declined {self.username}'s application.", ephemeral=True)
        await interaction.message.edit(view=DeclineReviewVerify())
        if attempts == 2:
            description = f"Hello **{self.username}**,\n・⠀Your application has unfortunetly been declined.\n・⠀You still have **1 attempt** left! \n⠀ ⠀ Make sure to re-apply again before the end of this recruit.\n\n-# **Note:** Feedback for declines is not available during Chromatica recruits. But if you'd like opinions on your edit, feel free to ask in <#1462851173777150097>"
        else:
            attempt = "0"
            description = f"Hello **{self.username}**,\n・⠀Your application has unfortunetly been declined.\n・⠀You also used both your attempts for this recruit.\n\n-# **Note:** Feedback for declines is not available during Chromatica recruits. But if you'd like opinions on your edit, feel free to ask in <#1462851173777150097>"
        embed = discord.Embed(title="CHROMATICA APPLICATIONS", description=description)
        embed.set_thumbnail(url=main_server.icon.url)
        await member.send(embed=embed)

        if attempts == 2:
            attempt = "first attempt, they can apply one more time"
        else:
            attempt = "second attempt, they cannot apply again"

        if attempts == 2:
            await self.update_attempts(user_id=self.applicant_id, new_attempts=1)
        if attempts == 1:
            await self.update_attempts(user_id=self.applicant_id, new_attempts=3)

        review_channel = interaction.client.get_channel(1477653138185126100)
        await self.update_status(user_id=self.applicant_id, new_status=0)
        if review_channel:
            await review_channel.send(f"-# {interaction.user.display_name} has declined {self.username}'s application.\n-# **This is {self.username}'s {attempt}**")

# --- DATABASE ---

    async def update_status(self, user_id: int, new_status: int):
        query = 'UPDATE recruit SET status = ? WHERE member_id = ?'
        async with self.bot.pool.acquire() as conn:
            await conn.execute(query, (new_status, user_id))
            await conn.commit()

    async def update_attempts(self, user_id: int, new_attempts: int):
        query = 'UPDATE recruit SET attempts = ? WHERE member_id = ?'
        async with self.bot.pool.acquire() as conn:
            await conn.execute(query, (new_attempts, user_id))
            await conn.commit()

    async def get_attempts(self, user_id: int):
        query = 'SELECT attempts FROM recruit WHERE member_id = ?'
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (user_id,))
                row = await cursor.fetchone()
                if row:
                    return int(row[0])
                else:
                    return 0

class AcceptReviewVerify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Accepted", style=discord.ButtonStyle.green, disabled=True)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"{self.username}'s application has already been accepted!", ephemeral=True)

class DeclineReviewVerify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Declined", style=discord.ButtonStyle.red, disabled=True)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"{self.username}'s application has already been declined.", ephemeral=True)

class ReviewView(discord.ui.View):
    def __init__(self, applicant_id: int, username: str, edit: str, program: str, platform: str, bot: commands.Bot):
        super().__init__(timeout=None)
        self.applicant_id = applicant_id
        self.username = username
        self.edit = edit
        self.program = program
        self.platform = platform
        self.bot = bot

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        application = discord.Embed(title="CHROMATICA APPLICATIONS")
        application.add_field(name="Username", value=self.username, inline=False)
        application.add_field(name="Edit", value=self.edit, inline=False)
        application.add_field(name="Program", value=self.program, inline=False)
        await interaction.response.send_message(f"You have accepted {self.username}'s application!", ephemeral=True)
        await interaction.message.edit(view=AcceptReviewVerify())
        reviewer = interaction.user.id
        accept_channel = interaction.client.get_channel(1477653120723980300)
        if accept_channel:
            await accept_channel.send(content=f"<@{reviewer}> has requested to accept {self.username}", embed=application, view=LeadReviewView(bot=self.bot, applicant_id=self.applicant_id, username=self.username, edit=self.edit, program=self.program, platform=self.platform, reviewer=interaction.user.display_name))

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, custom_id="decline")
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        attempts = await self.get_attempts(user_id=self.applicant_id)
        member = interaction.client.get_user(self.applicant_id)
        main_server = interaction.client.get_guild(1462079847433244799)
        await interaction.response.send_message(f"You have declined {self.username}'s application.", ephemeral=True)
        await interaction.message.edit(view=DeclineReviewVerify())
        if attempts == 2:
            description = f"Hello **{self.username}**,\n・⠀Your application has unfortunetly been declined.\n・⠀You still have **1 attempt** left! \n⠀ ⠀ Make sure to re-apply again before the end of this recruit.\n\n-# **Note:** Feedback for declines is not available during Chromatica recruits. But if you'd like opinions on your edit, feel free to ask in <#1462851173777150097>"
        else:
            attempt = "0"
            description = f"Hello **{self.username}**,\n・⠀Your application has unfortunetly been declined.\n・⠀You also used both your attempts for this recruit.\n\n-# **Note:** Feedback for declines is not available during Chromatica recruits. But if you'd like opinions on your edit, feel free to ask in <#1462851173777150097>"
        embed = discord.Embed(title="CHROMATICA APPLICATIONS", description=description)
        embed.set_thumbnail(url=main_server.icon.url)
        await member.send(embed=embed)

        if attempts == 2:
            attempt = "first attempt, they can apply one more time"
        else:
            attempt = "second attempt, they cannot apply again"

        if attempts == 2:
            await self.update_attempts(user_id=self.applicant_id, new_attempts=1)
        if attempts == 1:
            await self.update_attempts(user_id=self.applicant_id, new_attempts=3)

        review_channel = interaction.client.get_channel(1477653138185126100)
        await self.update_status(user_id=self.applicant_id, new_status=0)
        if review_channel:
            await review_channel.send(f"-# {interaction.user.display_name} has declined {self.username}'s application.\n-# **This is {self.username}'s {attempt}**")

# --- DATABASE ---

    async def update_status(self, user_id: int, new_status: int):
        query = 'UPDATE recruit SET status = ? WHERE member_id = ?'
        async with self.bot.pool.acquire() as conn:
            await conn.execute(query, (new_status, user_id))
            await conn.commit()

    async def update_attempts(self, user_id: int, new_attempts: int):
        query = 'UPDATE recruit SET attempts = ? WHERE member_id = ?'
        async with self.bot.pool.acquire() as conn:
            await conn.execute(query, (new_attempts, user_id))
            await conn.commit()

    async def get_attempts(self, user_id: int):
        query = 'SELECT attempts FROM recruit WHERE member_id = ?'
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (user_id,))
                row = await cursor.fetchone()
                if row:
                    return int(row[0])
                else:
                    return 0

class AcceptReviewVerify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Accepted", style=discord.ButtonStyle.green, disabled=True)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"application has already been accepted!", ephemeral=True)

class DeclineReviewVerify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Declined", style=discord.ButtonStyle.red, disabled=True)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"application has already been declined.", ephemeral=True)

class ApplyView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Apply Now", style=discord.ButtonStyle.blurple, custom_id="apply")
    async def apply(self, interaction: discord.Interaction, button: discord.ui.Button):
        attempts = await self.get_attempts(user_id=interaction.user.id)
        status = await self.get_status(member_id=interaction.user.id)
        if status == 1:
            await interaction.response.send_message("You have already applied and your application is awaiting review. Please be patient while we review your application.", ephemeral=True)
            return
        if status == 3:
            await interaction.response.send_message("Congratulations! Your application has already been accepted. Welcome to Chromatica!", ephemeral=True)
            return
        if attempts == 3:
            msg = "You have already used both of your attempts to apply for Chromatica. Unfortunately, you cannot apply again at this time. We hope to see you apply again in the future!"
            await interaction.response.send_message(msg, ephemeral=True)
            return
        else:
            await interaction.response.send_modal(ApplicationModal(user=interaction.user.id, bot=self.bot))

    @discord.ui.button(label="Status", style=discord.ButtonStyle.gray, custom_id="status")
    async def status(self, interaction: discord.Interaction, button: discord.ui.Button):
        status = await self.get_status(member_id=interaction.user.id)
        if status == 1:
            status_message = "Your application has been submitted and is awaiting review."
        if status == 2:
            status_message = "Your application is currently being reviewed. We will get back to you soon."
        if status == 3:
            status_message = "Your application has been accepted! Welcome to Chromatica."
        if status == 0:
            status_message = "You have not applied yet. Please click the 'Apply Now' button to submit your application."
        
        await interaction.response.send_message(status_message, ephemeral=True)

# --- DATABASE ---

    async def get_status(self, member_id: int):
        query = '''SELECT status FROM recruit WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                row = await cursor.fetchone()
                if row:
                    return int(row[0])
                else:
                    return 0

    async def get_attempts(self, user_id: int):
        query = 'SELECT attempts FROM recruit WHERE member_id = ?'
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (user_id,))
                row = await cursor.fetchone()
                if row:
                    return int(row[0])
                else:
                    return 0

# --- MODALS ---

class ApplicationModal(discord.ui.Modal, title="Chromatica Application"):
    def __init__(self, user: int, bot: commands.Bot):
        super().__init__(timeout=None)
        self.user = user
        self.bot = bot

    name = discord.ui.TextInput(label="What's your username?", placeholder="Enter your Instagram or TikTok username", required=True)
    edit = discord.ui.TextInput(label="Edit you're applying with.", placeholder="Instagram or TikTok link", required=True)
    program = discord.ui.TextInput(label="What editing program do you use?", placeholder="e.g., Videostar, After Effects, Alight Motion etc", style=discord.TextStyle.short, required=True)
    platform = discord.ui.TextInput(label="Which platform do you post on?", placeholder="Instagram, TikTok or both", style=discord.TextStyle.short, required=True)
    anything = discord.ui.TextInput(label="Anything else you'd like to add?", placeholder="Feel free to share any additional information", style=discord.TextStyle.paragraph, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        application = discord.Embed(title="CHROMATICA APPLICATIONS")
        application.add_field(name="Username", value=self.name.value, inline=False)
        application.add_field(name="Edit", value=self.edit.value, inline=False)
        application.add_field(name="Program", value=self.program.value, inline=False)
        application.add_field(name="Platform", value=self.platform.value, inline=False)
        if self.anything.value:
            application.add_field(name="Anything Else?", value=self.anything.value, inline=False)
        application.set_footer(text=f"User ID: {self.user} : {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        main_server = interaction.client.get_guild(1462079847433244799)
        application.set_thumbnail(url=main_server.icon.url)

        channel = interaction.client.get_channel(1477653100247646389)
        if channel:
            await channel.send(embed=application, view=ReviewView(bot=self.bot, applicant_id=self.user, username=self.name.value, edit=self.edit.value, program=self.program.value, platform=self.platform.value))
            await self.add_app(user_id=self.user)
        await interaction.response.send_message("Thank you for applying! We will review your application and get back to you soon.", ephemeral=True)

    async def add_app(self, user_id: int):
        check_query = 'SELECT member_id FROM recruit WHERE member_id = ?'
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(check_query, (user_id,))
                row = await cursor.fetchone()
                if row:
                    update_query = 'UPDATE recruit SET status = 1 WHERE member_id = ?'
                    await conn.execute(update_query, (user_id,))
                    await conn.commit()
                    return
                insert_query = 'INSERT INTO recruit (member_id, attempts, status) VALUES (?, ?, ?)'
                await conn.execute(insert_query, (user_id, 2, 1))
                await conn.commit()
    
    # Statuses: 1 = application submitted, 2 = being reviewed, 3 = accepted
    # Attempts: number of times the user has applied, max 2 attempts

class Recruit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='apply')
    async def apply(self, ctx):
        embed1 = discord.Embed(title="CHROMATICA RECRUITMENT", description="Welcome to [Chromaticagp's](https://www.instagram.com/chromaticagp/) comeback recruitment!\nPlease read the information below before applying.")
        embed2 = discord.Embed(title="INFORMATION",description="・⠀Make sure you have followed all recruit rules.\n・⠀No edits older than **4 months**.\n・⠀Remakes, heavy ib & velocity are auto declined.\n・⠀You get **2 attempts** to apply for Chromatica.\n⠀⠀・⠀You will get a response if you're declined!.\n・⠀No feedback will be given during our recruits.\n・⠀Any style, program & fandoms are accepted!\n・⠀Only Streamable, TikTok or Instagram links.\n\n-# **Note:** Please be patient with us! Ask any questions\n-# in <#1462097184487903337>.")
        await ctx.send(embeds=[embed1, embed2], view=ApplyView(self.bot))

    @commands.command(name='clearapps')
    @commands.has_permissions(administrator=True)
    async def clearapps(self, ctx):
        msg = await ctx.send("Are you sure you want to clear all applications from the database? This action cannot be undone.\n✅ Confirm\n❌ Cancel")
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == "✅":
                query = 'DELETE FROM recruit'
                async with self.bot.pool.acquire() as conn:
                    await conn.execute(query)
                    await conn.commit()
                await ctx.send("All applications have been cleared from the database.")
            else:
                await ctx.send("Clear operation cancelled.")
        except TimeoutError:
            await ctx.send("Clear operation timed out. No action taken.")

    @commands.command(name="fixuser")
    @commands.has_permissions(administrator=True)
    async def fixuser(self, ctx, member: discord.Member, attempts: int = None):
        status_query = 'UPDATE recruit SET status = 0 WHERE member_id = ?'

        async with self.bot.pool.acquire() as conn:
            await conn.execute(status_query, (member.id,))

            if attempts is not None:
                attempts_query = 'UPDATE recruit SET attempts = ? WHERE member_id = ?'
                await conn.execute(attempts_query, (attempts, member.id))

            await conn.commit()

        await ctx.send(
            f"✅ Reset **{member.display_name}**'s application.\n"
            f"• Status → `0` (can apply again)\n"
            f"{f'• Attempts → `{attempts}`' if attempts is not None else ''}"
        )

async def setup(bot):
    await bot.add_cog(Recruit(bot))