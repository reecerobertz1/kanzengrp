import discord
from discord.ext import commands
from discord import app_commands, ui

class acceptordecline(discord.ui.View):
    def __init__(self, bot, member, instagram):
        super().__init__(timeout=None)
        self.value= None
        self.bot = bot
        self.member = member
        self.instagram = instagram

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.blurple)
    async def accept(self, interaction: discord.Interaction, button: discord.Button):
        member = self.member
        member_id = member.id
        guild_id = 1121841073673736215
        channel_id = 1148042725950767138
        guild = interaction.client.get_guild(guild_id)
        if not guild:
            await interaction.response.send_message("Guild not found.", ephemeral=True)
            return

        channel = guild.get_channel(channel_id)
        if not channel:
            await interaction.response.send_message("Channel not found.", ephemeral=True)
            return
        try:
            invite = await channel.create_invite(max_age=0, max_uses=1, unique=True)
            link = invite.url
        except Exception as e:
            await interaction.response.send_message(f"Failed to create invite.\n{e}", ephemeral=True)
            return

        accept_embed = discord.Embed(description=f"## __Welcome to Kanzengrp!__\nYou have been accepted from our applications!", color=0x2b2d31)
        accept_embed.set_thumbnail(url=interaction.guild.icon)
        await self.update_accepted_status(member.id)
        button = discord.ui.Button(label="Click to join!", url=f"{link}")
        view = discord.ui.View()
        view.add_item(button)
        await member.send(embed=accept_embed, view=view)
        await interaction.response.edit_message(content="ACCEPTED", view=None)
        embed = discord.Embed(description=f"## {self.member} was accepted\nTheir instagram is {self.instagram}", color=0x2b2d31)
        embed.set_thumbnail(url=member.avatar)
        button2 = discord.ui.Button(label=f"Follow {self.instagram}", url=f"https://instagram.com/{self.instagram}/")
        view2 = discord.ui.View()
        view2.add_item(button2)
        channel = interaction.client.get_channel(1131006361921130526)
        await channel.send(embed=embed, view=view2)

    async def update_accepted_status(self, member_id: int, status="yes"):
        query = '''UPDATE apps SET accepted = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (status, member_id))
                await conn.commit()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.Button):
        member = self.member
        member_id = member.id
        apps = await self.get_apps(member.id)
        if apps == 1:
            appcount = "You have **1** application left, you can apply one more time!"
        else:
            appcount = "You cannot apply anymore times, you have used both your applications"
        declineembed = discord.Embed(description=f"## __Your application has been declined!__\nYou have been declined from our applications...\n{appcount}", color=0x2b2d31)
        declineembed.set_thumbnail(url=interaction.guild.icon)
        await self.update_applied(member.id, "false")
        await member.send(embed=declineembed)
        await interaction.response.edit_message(content="# DECLINED", view=None)

    async def update_applied(self, member_id: int, text: str):
        query = '''UPDATE apps SET applied = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (text, member_id))
                await conn.commit()

    async def get_apps(self, member_id):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT apps FROM apps WHERE member_id = $1", member_id)
                row = await cursor.fetchone()
                return row['apps'] if row else 0

class applicationsview(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.value= None
        self.bot = bot

    @discord.ui.button(label="Apply", style=discord.ButtonStyle.blurple)
    async def apply(self, interaction: discord.Interaction, button: discord.Button):
        await self.add_member(interaction.user.id)
        apps = await self.get_apps(interaction.user.id)
        applied = await self.get_applied(interaction.user.id)
        accepted = await self.get_accepted(interaction.user.id)
        if accepted == "yes":
            await interaction.response.send_message("You have been accepted! Please check your dms from Hoshi if you haven't already", ephemeral=True)
        if applied == "true":
            await interaction.response.send_message("You have already applied... please wait for a response before applying again", ephemeral=True)
        if apps == 0:
            await interaction.response.send_message("You cannot apply anymore since you have no applications left...", ephemeral=True)
        else:
            await interaction.response.send_modal(apply(bot=self.bot))

    @discord.ui.button(label="Check", style=discord.ButtonStyle.grey)
    async def check(self, interaction: discord.Interaction, button: discord.Button):
        apps = await self.get_apps(interaction.user.id)
        await self.add_member(interaction.user.id)
        if apps == 0:
            attempts = "You have **0** attempts left"
        elif apps:
            attempts = f"You have **{apps}** application attempts left!"
        else:
            attempts = "Please try again... An error occurred"
        await interaction.response.send_message(attempts, ephemeral=True)

    async def get_applied(self, member_id: int) -> str:
        query = '''SELECT applied FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return None

    async def get_accepted(self, member_id: int) -> str:
        query = '''SELECT accepted FROM apps WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return None

    async def update_apps(self, member_id: int, value=1):
        query = '''UPDATE apps SET apps = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def get_apps(self, member_id):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT apps FROM apps WHERE member_id = $1", member_id)
                row = await cursor.fetchone()
                return row['apps'] if row else 0

    async def add_member(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT member_id FROM apps WHERE member_id = ?", (member_id,))
                existing_member = await cursor.fetchone()
                if existing_member:
                    return

                query = '''INSERT INTO apps (member_id, apps, applied) VALUES (?, ?, ?)'''
                await cursor.execute(query, (member_id, 2, "false"))
                await conn.commit()

class answerbuttons(discord.ui.View):
    def __init__(self, member, question):
        super().__init__(timeout=None)
        self.value = None
        self.member = member
        self.question = question

    @discord.ui.button(label="Answer", style=discord.ButtonStyle.green)
    async def qna(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(answer(member=self.member, question=self.question))

class qnabuttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ask us anything!", emoji="🌙")
    async def qna(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(feedback())

class information(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Server Guide", emoji="🚀")
    async def guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="## Kanzen Forms\n<#1131007362895970414> - Server announcements are made here!\n<#1131005271502753812> - Server information\n<#1137115456642232340> - Our partners! (check them out too)\n<#1214943234711617568> - Our amazing supporters\n<#1214943332774453328> - Some stuff for your support\n\n## Apply\n<#1214940420946272316> - Apply for kanzen here!\n<#1214940450541273140> - Ask us anything here!\n<#1214940513589919774> - Answers to previous Q&A\n\n## Main\n<#1133767338588639323> - Come say hi to the community\n<#1214940039335641089> - General chat for other languages\n<#1214940115433168987> - Suggest anything for us to add here\n<#1214940316520677386> - General voice chat\n\n## Editing\n<#1214940632112570468> Ask for help with editing here\n<#1214940886526328944> - Promote your edits here (and only here)\n<#1214940947729874975> - Voice chat to share your screen while editing\n\n## Extra\n<#1214940622293835818> - Use kanzen's custom bot Hoshi!\n<#1214940722529181756> - Spam other bots here\n<#1214940812933333033> - Count with other server members!", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Partner Info", emoji="⭐")
    async def partnerinfo(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description="## `⭐` Partner Information\n\n- Advertisement with ping \n<a:purplearrow:1214948087861084171> Must follow Discord's TOS and Guidelines\n<a:purplearrow:1214948087861084171> Must have 200+ server members\nIf you meet our requirements, please message one of our owners\n\n- Advertisement with ping \n<a:purplearrow:1214948087861084171> Must follow Discord's TOS and Guidelines\n<a:purplearrow:1214948087861084171> Must have 150+ server members\nIf you meet our requirements, please message one of our owners", color=0x2b2d31)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class feedback(ui.Modal, title='Kanzen Forms Q&A'):
    rate = ui.TextInput(label='What is your question?', placeholder="Enter your question here", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(description=f"## `🌙` Q&A\nTheir question:\n{self.rate.value}", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text=f"Sent from {interaction.user.name}", icon_url=interaction.user.display_avatar)
        channel = interaction.client.get_channel(1214940489883717662)
        view = answerbuttons(member=interaction.user.id, question=self.rate.value)
        await channel.send(embed=embed, view=view)
        await interaction.followup.send(f"Thank you {interaction.user.display_name} your question has been sent!", ephemeral=True)

class answer(ui.Modal, title='Kanzen Forms Q&A'):
    def __init__(self, member, question):
        super().__init__()
        self.member = member
        self.question = question

    rate = ui.TextInput(label='What is your answer?', placeholder="Enter your answer here", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(description=f"## `🌙` Q&A\nQuestion:\n{self.question}\n\nAnswer:\n{self.rate.value}", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text=f"Answered by {interaction.user.name}", icon_url=interaction.user.display_avatar)

        answered = discord.Embed(title="This question has been answered", description=f"## `🌙` Q&A\nQuestion:\n{self.question}\n\nAnswer:\n{self.rate.value}", color=0x2B765E)
        answered.set_thumbnail(url=interaction.guild.icon)
        answered.set_footer(text=f"Answered by {interaction.user.name}", icon_url=interaction.user.display_avatar)
        channel = interaction.client.get_channel(1214940513589919774)
        await channel.send(f"<@{self.member}>", embed=embed)
        await interaction.followup.send(f"Thank you {interaction.user.display_name} the answer has been sent to <#1214940513589919774>!", ephemeral=True)
        await interaction.edit_original_response(embed=answered, view=None)

class apply(ui.Modal, title="Apply for Kanzengrp"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    instagram = ui.TextInput(label="What is your Instagram username?", placeholder="Enter your username here...", style=discord.TextStyle.short)
    activity = ui.TextInput(label="How active will you be in kanzengrp?", placeholder="On a scale of 1-10", style=discord.TextStyle.short)
    pastmember = ui.TextInput(label="Where you a past member?", placeholder="Yes or No", style=discord.TextStyle.short)
    edit = ui.TextInput(label="The link to the edit you're applying with", placeholder="Paste link here", style=discord.TextStyle.short)
    other = ui.TextInput(label="Anything else you want us to know?", placeholder="Anything else?", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(description=f"`☄️` Kanzen Forms\nSent from [**{self.instagram.value}**](https://instagram.com{self.instagram.value})\n\nHow active will they be?\n> {self.activity.value}\n\nWere they a past member?\n> {self.pastmember.value}\n\nThe edit they applied with\n> {self.edit.value}\n\nAnything Else?\n> {self.other.value}", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text=f"Sent from {interaction.user.name} | {interaction.user.id}")
        channel=interaction.client.get_channel(1131006328207327294)
        await channel.send(embed=embed, view = acceptordecline(bot=self.bot, member=interaction.user, instagram=self.instagram.value))
        await self.add_member(interaction.user.id)
        await self.update_applied(interaction.user.id, "true")
        apps = await self.get_apps(interaction.user.id)
        if apps == 2:
            await self.update_apps(interaction.user.id)
        if apps == 1:
            await self.update_apps2(interaction.user.id)
        await interaction.followup.send(f"Thank you {interaction.user.name} for applying! Please wait for a response", ephemeral=True)

    async def get_apps(self, member_id):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT apps FROM apps WHERE member_id = $1", member_id)
                row = await cursor.fetchone()
                return row['apps'] if row else 0

    async def add_member(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT member_id FROM apps WHERE member_id = ?", (member_id,))
                existing_member = await cursor.fetchone()
                if existing_member:
                    return

                query = '''INSERT INTO apps (member_id, apps, applied) VALUES (?, ?, ?)'''
                await cursor.execute(query, (member_id, 2, "false"))
                await conn.commit()

    async def update_applied(self, member_id: int, text: str):
        query = '''UPDATE apps SET applied = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (text, member_id))
                await conn.commit()

    async def update_apps(self, member_id: int, value=1):
        query = '''UPDATE apps SET apps = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_apps2(self, member_id: int, value=0):
        query = '''UPDATE apps SET apps = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def formsinfo(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(description="## 🪐 Kanzen Forms\n`-` Welcome to kanzen forms! This is a server made for [@kanzengrp](https://instagram.com/kanzengrp)!\n`-` Please feel free to ask our staff any questions orgo to  [# Q&A](https://discord.com/channels/1131003330810871979/1214940450541273140)\n`-` If you're confused on our server layout, click `Server Guide`", color=0x2b2d31)
        embed2 = discord.Embed(description="## Server Rules\n<a:purplearrow:1214948087861084171> Follow Discord's tos and guidelines\n<a:purplearrow:1214948087861084171> No NSFW talk is allowed in this server!!\n<a:purplearrow:1214948087861084171> Be nice and respectful to everyone!\n<a:purplearrow:1214948087861084171> No impersonation of other editors\n<a:purplearrow:1214948087861084171> Use channels for their intended purpose\n<a:purplearrow:1214948087861084171> No spamming pings, you will be warned/kicked\n<a:purplearrow:1214948087861084171> No trash talk of other people", color=0x483b6e)
        embed2.set_image(url="https://cdn.discordapp.com/attachments/1214944837451780116/1214951135723528242/welc_banner_00000_00000.png?ex=65fafa6b&is=65e8856b&hm=ef421a6b4e4e7d9a2717fe556207e7b6da2eebbd42cea400d6c61c718732c3eb&")
        embed2.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2, view=information())

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def qnayuh(self, ctx):
        await ctx.message.delete()
        embed=discord.Embed(description="## `🌙` Q&A\n<a:purplearrow:1214948087861084171> Ask us anything about the server or Kanzengrp\n<a:purplearrow:1214948087861084171> The answers to your questions will be sent [here](https://discord.com/channels/1131003330810871979/1214940513589919774)\n<a:purplearrow:1214948087861084171> A form will pop up where you can enter your question\n<a:purplearrow:1214948087861084171> No question is dumb, you can ask us anything and we will try and help\n\n## `🌕` Q&A Information\n<a:purplearrow:1214948087861084171>  Any inappropriate questions will be skipped!\n<a:purplearrow:1214948087861084171>  We are not active 24/7 to see your questions, be patient\n<a:purplearrow:1214948087861084171>  If you spam questions we will ignore you", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        view=qnabuttons()
        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def apps(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(description="### `☄️` __Application Information__\n<a:purplearrow:1214948087861084171> Click the `Apply` button and fill out the form, then submit\n<a:purplearrow:1214948087861084171> You will get a dm from Hoshi saying if you got accepted or not\n<a:purplearrow:1214948087861084171> You only get 2 applications, so use them wisely\n<a:purplearrow:1214948087861084171> Click the `Check` button to see how many times you've applied\n<a:purplearrow:1214948087861084171> Once you have applied twice, you no longer can app again\n<a:purplearrow:1214948087861084171> Please be patient with us! you will get a response soon", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed, view=applicationsview(bot=self.bot))

    async def get_accepted_members(self):
        query = '''SELECT member_id FROM apps WHERE accepted LIKE '%yes%' '''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                members = await cursor.fetchall()
        return [member[0] for member in members]

    @commands.command()
    async def accepted(self, ctx):
        accepted_members = await self.get_accepted_members()
        if accepted_members:
            member_list = '\n'.join(f"<@{member}>" for member in accepted_members)
            embed = discord.Embed(
                title="Accepted Members",
                description=member_list,
                color=0x2b2d31
            )
            embed.set_thumbnail(url=ctx.guild.icon)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No members have been accepted yet!")

    async def clear_database(self):
        query = '''DELETE FROM apps'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                await conn.commit()

    @commands.command()
    async def clearapps(self, ctx):
        await self.clear_database()
        await ctx.send("The database has been cleared.")

async def setup(bot):
    await bot.add_cog(Forms(bot))