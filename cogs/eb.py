import discord
from discord.ext import commands
from discord import ui

class musuemview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value=None

    @discord.ui.button(label="Info", style=discord.ButtonStyle.blurple, emoji="<a:blackbut:1173677079905194014>")
    async def info(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="MUSEUMSOC",description="- led by [icidqve](https://www.instagram.com/icidqve?igsh=MWl0ZTFrNjFramdhZw==)\n- Multi Fandom" ,color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1226151638201536703/1226240519395475556/00947474-35ED-4029-89B6-CE11D90E7F10.jpg?ex=66240c7a&is=6611977a&hm=d0ece9f89da039032a3e2b8ac8f5832bcc9c103db138d612df014401441dd4c1&")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1137730730261237970/83e98bfd3cf4b8fd708a4c7412d52de3.webp?size=1024&format=webp&width=0&height=307")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class lyragrp(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value=None

    @discord.ui.button(label="Info", style=discord.ButtonStyle.blurple, emoji="<:1817bunnylove:1135527331398692975>")
    async def info(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="GRP LYRA",description="- led by [lyrinari](https://www.instagram.com/lyrinari/), [hiraeyq](https://www.instagram.com/hiraeyq/), [.denisaur.](https://www.instagram.com/_.denisaur._/) & [kazuhqra](https://www.instagram.com/kazuhqra/)\n- multi-fandom" ,color=0xfebcbe)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1221580405921284317/1225300494621343776/form_gfx_w_grains.png?ex=6620a102&is=660e2c02&hm=d8b1ada951fd18e3836895d778d0323a1a60ff0ae729ff612cc9fb38751d5eba&")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1134736053803159592/a_479bb36059893c697962d64e636728c8.gif?size=1024&width=0&height=307")
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
        guild_id = 1121841073673736215
        channel_id = 1148042725950767138
        guild = interaction.client.get_guild(guild_id)
        accepts = await self.count_accepted(member.id)
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

        if interaction.user.id == 609515684740988959:
            await self.update_reece_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True)  
        if interaction.user.id == 603077306956644353:
            await self.update_nani_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 1169110493303164930:
            await self.update_adil_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 705866935178362901:
            await self.update_kelly_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 758834972446031912:
            await self.update_luki_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 1111564587024789504:
            await self.update_josh_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 497548184298586133:
            await self.update_kio_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 891348311544590376:
            await self.update_mari_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 751895538646909038:
            await self.update_marie_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 764293346364620810:
            await self.update_riri_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True)
        if interaction.user.id == 887365538232270959:
            await self.update_kai_row(member.id, 1)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True)
        if accepts == 3:
            message_id = interaction.message.id
            message = await interaction.channel.fetch_message(message_id)
            accept_embed = discord.Embed(description=f"> `🌠` __**Welcome to kanzengrp**__"
                "\n- You have been accepted into kanzengrp!"
                "\n - Click the **Join now** button to join our members server"
                "\n - If you have any questions feel free to ping @staff or @lead"
                "\n\nThank you for joining kanzengrp!", color=0x2b2d31)
            accept_embed.set_thumbnail(url=interaction.guild.icon)
            await self.update_accepted_status(member.id)
            button = discord.ui.Button(label="Click to join!", url=f"{link}")
            view = discord.ui.View()
            view.add_item(button)
            await member.send(embed=accept_embed, view=view)
            await message.edit(content="ACCEPTED", view=None)
            embed = discord.Embed(description=f"> `💫` **__{self.member} was accepted__**\nTheir instagram is {self.instagram}", color=0x2b2d31)
            embed.set_thumbnail(url=member.avatar)
            button2 = discord.ui.Button(label=f"Follow {self.instagram}", url=f"https://instagram.com/{self.instagram}/", emoji="🌕")
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
        declines = await self.count_declined(member.id)
        attempts = await self.get_apps(member.id)
        if interaction.user.id == 609515684740988959:
            await self.update_reece_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to decline {self.member}, if you change your mind you can click the decline button", ephemeral=True)  
        if interaction.user.id == 603077306956644353:
            await self.update_nani_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to decline {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 1169110493303164930:
            await self.update_adil_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to decline {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 705866935178362901:
            await self.update_kelly_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to decline {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 758834972446031912:
            await self.update_luki_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to decline {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 1111564587024789504:
            await self.update_josh_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to decline {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 497548184298586133:
            await self.update_kio_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to decline {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 891348311544590376:
            await self.update_mari_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to decline {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 751895538646909038:
            await self.update_marie_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to decline {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if interaction.user.id == 764293346364620810:
            await self.update_riri_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to decline {self.member}, if you change your mind you can click the decline button", ephemeral=True)
        if interaction.user.id == 887365538232270959:
            await self.update_kai_row(member.id, 2)
            await interaction.response.send_message(f"You have voted to accept {self.member}, if you change your mind you can click the decline button", ephemeral=True) 
        if declines == 3:
            message_id = interaction.message.id
            message = await interaction.channel.fetch_message(message_id)
            accept_embed = discord.Embed(description=f"> `🌠` __**Your application has been declned**__"
            f"\n- You **{attempts}** application attempts left", color=0x2b2d31)
            accept_embed.set_thumbnail(url=interaction.guild.icon)
            await member.send(embed=accept_embed)
            await message.edit(content="# DECLINED", view=None)

    async def count_accepted(self, member_id: int) -> int:
        query = '''SELECT reece, nani, adil, kelly, luki, josh, kio, mari, marie, riri FROM apps WHERE member_id = ?'''
        total_accepted = 0
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                rows = await cursor.fetchall()
                if rows:
                    row = rows[0]
                    total_accepted = sum(1 for value in row if value == 1)
            return total_accepted

    async def count_declined(self, member_id: int) -> int:
        query = '''SELECT reece, nani, adil, kelly, luki, josh, kio, mari, marie, riri FROM apps WHERE member_id = ?'''
        total_declined = 0
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id,))
                rows = await cursor.fetchall()
                if rows:
                    row = rows[0]
                    total_declined = sum(1 for value in row if value == 2)
            return total_declined

    async def update_reece_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET reece = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_kai_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET kai = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_nani_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET nani = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_adil_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET adil = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_kelly_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET kelly = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_luki_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET luki = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_josh_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET josh = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_kio_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET kio = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_mari_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET mari = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_marie_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET marie = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

    async def update_riri_row(self, member_id: int, value: int) -> None:
        query = '''UPDATE apps SET riri = ? WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (value, member_id))
                await conn.commit()

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
        user = interaction.user
        await self.add_member(interaction.user.id)
        apps = await self.get_apps(interaction.user.id)
        applied = await self.get_applied(interaction.user.id)
        accepted = await self.get_accepted(interaction.user.id)
        booster_role_id = 1136803676854431745
        has_booster_role = any(role.id == booster_role_id for role in user.roles)

        if accepted == "yes":
            await interaction.response.send_message("You have been accepted! Please check your DMs from Hoshi if you haven't already", ephemeral=True)
            return

        if applied == "true":
            await interaction.response.send_message("You have already applied. Please wait for a response before applying again.", ephemeral=True)
            return

        if apps == 0:
            await interaction.response.send_message("You cannot apply anymore since you have no applications left.", ephemeral=True)
            return

        if has_booster_role:
            await interaction.response.send_modal(apply(bot=self.bot))
        else:
            await interaction.response.send_modal(apply(bot=self.bot))

    @discord.ui.button(label="Check", style=discord.ButtonStyle.grey)
    async def check(self, interaction: discord.Interaction, button: discord.Button):
        apps = await self.get_apps(interaction.user.id)
        await self.add_member(interaction.user.id)
        user = interaction.user
        booster_role_id = 1136803676854431745
        has_booster_role = any(role.id == booster_role_id for role in user.roles)
        if apps == 0:
            attempts = "You have **0** attempts left"
        elif apps:
            attempts = f"You have **{apps}** application attempts left!"
        else:
            attempts = "Please try again... An error occurred"
        if has_booster_role:
            attempts = "You are a booster of the server... You have unlimited attempts!"
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
    pastmember = ui.TextInput(label="Where you a past member?", placeholder="Yes or No", style=discord.TextStyle.short)
    edit = ui.TextInput(label="The link to the edit you're applying with", placeholder="Paste link here", style=discord.TextStyle.short)
    other = ui.TextInput(label="Anything else you want us to know?", placeholder="Anything else?", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(description=f"`☄️` Kanzen Forms\nSent from [**{self.instagram.value}**](https://instagram.com{self.instagram.value})\n\nWere they a past member?\n> {self.pastmember.value}\n\nThe edit they applied with\n> {self.edit.value}\n\nAnything Else?\n> {self.other.value}", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text=f"Sent from {interaction.user.name} | {interaction.user.id}")
        channel=interaction.client.get_channel(1222674203447267399)
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
        embed = discord.Embed(description="<a:Arrow_1:1227576761722732647> Click the `Apply` button to apply for our grp"
        "\n<a:Arrow_1:1227576761722732647> Hoshi will dm you saying if you got accepted or declined"
        "\n<a:Arrow_1:1227576761722732647> You only get **2** attempts or unlimited if you boost"
        "\n<a:Arrow_1:1227576761722732647> The `check` button will show you how many attempts you have"
        "\n<a:Arrow_1:1227576761722732647> Once you have applied twice you can no longer apply"
        "\n<a:Arrow_1:1227576761722732647> Apply with an edit that is no longer than **3 months** old"
        "\n<a:Arrow_1:1227576761722732647> Applications will close on <t:1714431600:D> | <t:1714431600:R> "
        "\n<a:Arrow_1:1227576761722732647>  Make sure you followed the rules on our recruit post", color=0x2b2d31)
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

    @commands.command()
    async def staffinfo(self, ctx):
        embed = discord.Embed(description="> `💫` **__Staff Information__**"
"\n\n<a:Arrow_1:1145603161701224528> To accept a form, you just need to click the **Vote Accept** button"
"\n\n<a:Arrow_1:1145603161701224528> Voting accept will add one vote to a members form, but voting to decline will subtract one vote"
"\n\n<a:Arrow_1:1145603161701224528> A form needs **3** accept votes before being accepted (the form should be updated with the amount of votes)"
"\n\n<a:Arrow_1:1145603161701224528> To clearly see what forms you have voted on or not voted on, feel free to leave a reaction on the form, so you don't get confused"
"\n\n<a:Arrow_1:1145603161701224528> If you want to discuss someone's edits, you can always create a thread on the form (look at the image below to see how to make one if you don't know)"
"\n\n<a:Arrow_1:1145603161701224528> If someone has mentioned that they would like criticism, pls make sure you do (ask someone else for help if you don't know what to put)"
"\n\n<a:Arrow_1:1145603161701224528> If you don't see the **decline** button, it is because the member has one more application left, the decline button will be replaced with a **reapp** button"
"\n\n<a:Arrow_1:1145603161701224528> If the buttons do not work (says interaction failed) please do tell Reece, we can then keep track of votes manually and accept them via commands", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1221859377200496781/image.png?ex=66141c38&is=6601a738&hm=0338ddd0f1acf13e40359e9a5d0fbdbce75f611fe30a3e21f1fd81cf72edfcd9&")
        await ctx.reply(embed=embed)

    @commands.command()
    async def partners(self, ctx):
        aster = discord.ui.View()
        astersite = discord.ui.Button(label="Website", url="https://grpaster.com")
        asterinsta = discord.ui.Button(label="Instagram", url="https://instagram.com/grpaster")
        aster.add_item(astersite)
        aster.add_item(asterinsta)
        await ctx.send("https://discord.gg/aster-hiraya-day-748021504830341330", view=aster)
        hsgrp = discord.ui.View()
        hsgrpinsta = discord.ui.Button(label="Instagram", url="https://instagram.com/heartstoppergrp?igshid=MzRlODBiNWFlZA==")
        hsgrp.add_item(hsgrpinsta)
        await ctx.send("https://discord.gg/XVpKTcJhf8", view=hsgrp)
        lyragrps = lyragrp()
        lyrainsta = discord.ui.Button(label="Instagram", url="https://www.instagram.com/gplyra/")
        lyatiktok = discord.ui.Button(label="TikTok", url="https://www.tiktok.com/@grplyra")
        lyragrps.add_item(lyrainsta)
        lyragrps.add_item(lyatiktok)
        await ctx.send("https://discord.gg/uCPhm6PECW", view=lyragrps)
        musuem = musuemview()
        museuminsta = discord.ui.Button(label="Instagram", url="https://www.instagram.com/museumsoc?igsh=MTFvb2VkcWxyZmVicA==")
        musuem.add_item(museuminsta)
        await ctx.send("https://discord.gg/S6r49qzmdT", view=musuem)
        embed= discord.Embed(description="Want to partner with us? read our partner info in <#1131005271502753812>", color=0x2b2d31)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def bp(self, ctx):
        link = discord.ui.View()
        megalink = discord.ui.Button(label="Click here to get the resources", url="https://mega.nz/folder/B0EXESbB")
        link.add_item(megalink)
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1214944837451780116/1223588936706953286/bc60109af32c0520fc17f8dffbdd75e922b31527r1-736-916v2_hq.jpg?ex=661a66ff&is=6607f1ff&hm=5a4670c879ff1e1bb3a3dd08c85c115de97c1e03a21a9390720a613aa2cc3fd8&")
        embed2 = discord.Embed(description="> `🚀` **__Booster Perks__**"
        "\n\nThank you so much for boosting!"
        "\n\nMore may be added later on "
        "\n\nPlease do not send this to anyone..."
        "\n\nIf the link no longer works pls dm Reece !", color=0x2b2d31)
        await ctx.send("<@&1136803676854431745>",embed=embed)
        await ctx.send(embed=embed2, view=link)
        await ctx.send("Key: `UpSW3UlHZne2ADMwiQoUzA`")

    async def get_voting_counts(self) -> dict:
        query = '''SELECT reece, nani, adil, kelly, luki, josh, kio, mari, marie, riri, kai FROM apps'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall()

        voting_counts = {}
        for row in rows:
            for index, value in enumerate(row):
                member_name = ['reece', 'nani', 'adil', 'kelly', 'luki', 'josh', 'kio', 'mari', 'marie', 'riri', 'kai'][index]
                if isinstance(value, int):
                    accepts = 1 if value == 1 else 0
                    declines = 1 if value == 2 else 0
                else:
                    accepts = 0
                    declines = 0
                voting_counts[member_name] = {'total_votes': accepts + declines, 'accepts': accepts, 'declines': declines}

        return voting_counts

    @commands.command()
    async def staffvotes(self, ctx):
        voting_counts = await self.get_voting_counts()

        if not voting_counts:
            await ctx.send("No votes found.")
            return

        result_message = ""
        for member_name, counts in voting_counts.items():
            result_message += f"**{member_name.capitalize()}**\n"
            result_message += f"Voted - **{counts['total_votes']}** times | **{counts['accepts']}** accepts - **{counts['declines']}** declines\n\n"
        embed = discord.Embed(title="> `🌙` Staff app votes", description=f"{result_message}", color=0x2b2d31)
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Forms(bot))