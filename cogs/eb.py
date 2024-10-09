import asyncio
import re
import discord
from discord.ext import commands
from discord import ui

class reviewbuttons(discord.ui.View):
    def __init__ (self, member, user, edit, program, more, bot):
        super().__init__(timeout=None)
        self.value = None
        self.member = member
        self.user = user
        self.edit = edit
        self.program = program
        self.more = more
        self.bot = bot

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.Button):
        member = self.member
        embed = discord.Embed(title="Chroma Recruit", color=0xc01d25)
        embed.add_field(name=f"Instagram Username", value=f"[{self.user}](https://instagram.com/{self.user})", inline=False)
        embed.add_field(name=f"Edit Link", value=self.edit, inline=False)
        embed.add_field(name=f"Program", value=self.program, inline=False)
        embed.set_footer(text=f"Sent from {member.name} | Status: Declined")
        embed.set_thumbnail(url=member.avatar)
        attempts = await self.get_attempts(member.id)
        await self.remove_attempt(member.id)
        if self.more:
            embed.add_field(name=f"Anything Else", value=self.more, inline=False)
        if attempts == 1:
            description = f"Unfortunately, your application has been declined from [chromagrp](https://instagram.com/chromagrp)\nYou have **{attempts-1}** attempts and you cannot reapply.\nPlease do not be discouraged, we will have more recruits in the future!"
        else:
            description=f"Unfortunately, your application has been declined from [chromagrp](https://instagram.com/chromagrp)\nYou have **{attempts-1}** more attempt to reapply remaining. Use it well + Good luck !!"
        dmembed = discord.Embed(description=description)
        await member.send(embed=dmembed)
        await self.update_applied(member.id)
        await interaction.response.edit_message(embed=embed, view=None)

    async def update_applied(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = '''UPDATE recruit SET applied = 0 WHERE member_id = ?'''
                await cursor.execute(query, (member_id,))
                await conn.commit()

    async def remove_attempt(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = '''UPDATE recruit SET attempts = attempts - 1 WHERE member_id = ? AND attempts > 0'''
                await cursor.execute(query, (member_id,))
                await conn.commit()

    async def get_attempts(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT attempts FROM recruit WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return 0

class applybutton(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Apply")
    async def ask(self, interaction: discord.Interaction, button: discord.Button):
        attempts = await self.get_attempts(interaction.user.id)
        accepted = await self.get_accepted(interaction.user.id)
        applied = await self.get_applied(interaction.user.id)
        if attempts == 0:
            await interaction.response.send_message("You have no more attempts to reapply!", ephemeral=True)
        elif accepted == 1:
            await interaction.response.send_message("You have been accepted already!\nPlease check your dms from <@849682093575372841> to join our members server", ephemeral=True)
        elif applied == 1:
            await interaction.response.send_message("Seems like you have already applied. Please wait for a response from us before trying again!\nIf you made a mistake on your form, Please let a lead know", ephemeral=True)
        else:
            await interaction.response.send_modal(recruit(bot=self.bot))

    async def get_applied(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT applied FROM recruit WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return -1

    async def get_attempts(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT attempts FROM recruit WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return -1

    async def get_accepted(self, member_id: int) -> int:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT accepted FROM recruit WHERE member_id = ?", (member_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                return -1

class arrows(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="<")
    async def asked(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed (title="Commonly asked question", description="1. **When do you guys usually review applications?**\n We review when we can! but multiple staff have to review your app before you get a response. So please be patient with us!\n\n2. **How long is the recruit / scout for?**\n The recruits / scouts typically last about 2 weeks - a month\n\n3. **How many members are you accepting?**\n As many as we can! there is not a number to how many members we accept\n\n4. **When will the next recruit be?**\n We never know the answer to this question... Recruits happen whenever we see fit\n\n5. **How old can an edit be before its too old to apply with?**\n We prefer to see newer edits. We usually ask you to apply when an edit that isn't older than 3 months. But we do sometimes look at more of your edits on your account", color=0x2b2d31)
        embed.set_footer(text="Page 1/2")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label=">")
    async def asked2(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="Commonly asked question", description="6. **Do we get a decline / reapp message?**\n For past recruits the answer would have been no... but we will hopefully have decline / reapp messages implemented soon\n\n7. **How do we know if we got accepted, declined or reapped?**\n You will receive a private DM from our bot Hoshi. He will let you know when you get a response from us!\n\n8. **Will we receive criticism for our edits?**\n No, due to the amount of applications we receive, giving criticism for them all would be an extremely difficult thing to do. And all our staff members do have different opinions so it wouldn't really be specific feedback either!\n\n9. **Do you accept all styles?**\n Yes! all styles are accepted in chroma. All we look for are creative and smooth transitions\n\n10. **When we reapply, do we need to do the rules again?**\n No, there isn't a point in re doing rules. You can reapply without re doing them!", color=0x2b2d31)
        embed.set_footer(text="Page 2/2")
        await interaction.response.edit_message(embed=embed)

class qnabutton(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Ask", style=discord.ButtonStyle.blurple)
    async def ask(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(qna())

    @discord.ui.button(label="Commonly Asked")
    async def asked(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed (title="Commonly asked question", description="1. **When do you guys usually review applications?**\n We review when we can! but multiple staff have to review your app before you get a response. So please be patient with us!\n\n2. **How long is the recruit / scout for?**\n The recruits / scouts typically last about 2 weeks - a month\n\n3. **How many members are you accepting?**\n As many as we can! there is not a number to how many members we accept\n\n4. **When will the next recruit be?**\n We never know the answer to this question... Recruits happen whenever we see fit\n\n5. **How old can an edit be before its too old to apply with?**\n We prefer to see newer edits. We usually ask you to apply when an edit that isn't older than 3 months. But we do sometimes look at more of your edits on your account", color=0x2b2d31)
        embed.set_footer(text="Page 1/2")
        await interaction.response.send_message(embed=embed, view=arrows(), ephemeral=True)

class qna(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Chroma Q&A")

    reason = discord.ui.TextInput(label="What is your question?", placeholder="Ask us here!", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Chroma Q&A", color=0x2b2d31)
        embed.add_field(name=f"User ID", value=interaction.user.id, inline=False)
        embed.add_field(name="Question", value=self.reason.value, inline=False)
        msg = await interaction.client.get_channel(862615059355271188).send(embed=embed)
        await interaction.response.send_message('Thanks! I have sent your question!', ephemeral=True)

class recruit(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="Chroma application")
        self.bot = bot

    user = discord.ui.TextInput(label="What is your instagram user?", placeholder="Enter username here...", style=discord.TextStyle.short)
    edit = discord.ui.TextInput(label="The edit you're applying with", placeholder="Insta or Streamable link here...", style=discord.TextStyle.short)
    program = discord.ui.TextInput(label="What program/app do you use?", placeholder="After effects, videostar etc", style=discord.TextStyle.short)
    more = discord.ui.TextInput(label="Anything else you'd like to mention?", style=discord.TextStyle.long, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Chroma Recruit",description="-# Please react when sent to <#1067235666917859348>!!" ,color=0x2b2d31)
        embed.add_field(name="Discord ID", value=interaction.user.id, inline=False)
        embed.add_field(name=f"Instagram Username", value=self.user.value, inline=False)
        embed.add_field(name=f"Edit Link", value=self.edit.value, inline=False)
        embed.add_field(name=f"Program", value=self.program.value, inline=False)
        embed.set_thumbnail(url=interaction.user.avatar)
        embed.set_footer(text=f"Sent from {interaction.user.name} | Status: Pending")
        view = reviewbuttons(member=interaction.user, user=self.user.value, edit=self.edit.value, program=self.program.value, more=self.more.value, bot=self.bot)
        user = discord.ui.Button(label=f"View {self.user.value}'s account", url=f"https://instagram.com/{self.user.value}")
        await self.add_member(member_id=interaction.user.id)
        view.add_item(user)
        if self.more.value:
            embed.add_field(name=f"Anything Else", value=self.more.value, inline=False)
        msg = await interaction.client.get_channel(835497793703247903).send(embed=embed, view=view)
        await self.update_applied(interaction.user.id)
        await interaction.response.send_message('Thanks! I have sent your application!', ephemeral=True)

    async def update_applied(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = '''UPDATE recruit SET applied = 1 WHERE member_id = ?'''
                await cursor.execute(query, (member_id,))
                await conn.commit()

    async def add_member(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT 1 FROM recruit WHERE member_id = ?", (member_id,))
                existing_member = await cursor.fetchone()
                if existing_member is not None:
                    return
                
                query = '''INSERT INTO recruit(member_id, attempts, reviewed, accepted) VALUES (?, ?, ?, ?)'''
                await cursor.execute(query, (member_id, 2, 0, 0))
                await conn.commit()

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    def is_staff():
        async def predicate(ctx):
            role_id = 835549528932220938
            role = ctx.guild.get_role(role_id)
            return role in ctx.author.roles
        return commands.check(predicate)

    @commands.command()
    async def partners(self, ctx):
        lyraembed = discord.Embed(title="༝ __GRP LYRA__ ! ⋆",description="• led by [lyrinari](https://www.instagram.com/lyrinari/), [hiraeyq](https://www.instagram.com/hiraeyq/), [.denisaur.](https://www.instagram.com/_.denisaur._/) & [kazuhqra](https://www.instagram.com/kazuhqra/)\n• co-led by [luno1rs](https://instagram.com/luno1rs/) & [remqsi](https://www.instagram.com/remqsi/)" ,color=0xfebcbe)
        lyraembed.set_image(url="https://cdn.discordapp.com/attachments/1221580405921284317/1225300494621343776/form_gfx_w_grains.png?ex=6620a102&is=660e2c02&hm=d8b1ada951fd18e3836895d778d0323a1a60ff0ae729ff612cc9fb38751d5eba&")
        lyraembed.set_thumbnail(url="https://cdn.discordapp.com/icons/1134736053803159592/a_479bb36059893c697962d64e636728c8.gif?size=1024&width=0&height=307")
        lyragrps = discord.ui.View()
        joinlyra = discord.ui.Button(label="Join", url="https://discord.gg/uCPhm6PECW", emoji="<:1817bunnylove:1135527331398692975")
        lyrainsta = discord.ui.Button(label="Instagram", url="https://www.instagram.com/gplyra/")
        lyatiktok = discord.ui.Button(label="TikTok", url="https://www.tiktok.com/@grplyra")
        lyragrps.add_item(joinlyra)
        lyragrps.add_item(lyrainsta)
        lyragrps.add_item(lyatiktok)
        await ctx.send(embed=lyraembed, view=lyragrps)

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def qna(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Question and Answer", description="Please read the information below before using our Q&A!\n\n**General Information**\n・Use the `ask` button below to send us your question.\n・Once your question has been answered, our response will be sent into <#862617899356651531>>\n・No question is dumb, so feel free to ask any questions you have!\n・You can ask about our recruits or chroma as a whole.\n・Our staff and leads will be answering your questions!\n・Use the `commonly asked` button or look through <#862617899356651531> to check if the question you have has been answered already.\n\n**Please be patient**\n・We will try our best to get back to you as soon as possible.\n・If you spam our qna we will not respond!\n・Do not abuse this feature, and do not harass out staff.\n-# **Note:** If you harass our staff we will kick or ban you from our server!", color=0x2b2d31)
        await ctx.send(embed=embed, view=qnabutton())

    @commands.command()
    async def answer(self, ctx, answer: str):
        if ctx.message.reference is not None:
            try:
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                embed = msg.embeds[0]
                user_id_field = next((field for field in embed.fields if field.name == 'User ID'), None)
                question = next((field for field in embed.fields if field.name == 'Question'), None)
                answer_channel = self.bot.get_channel(862617899356651531)
                if not question or not user_id_field:
                    await ctx.send("Invalid embed format. Please make sure the embed contains fields 'Group(s) they want to be in:' and 'User ID'.")
                    return
                
                question = question.value.lower()
                question = [question.strip() for question in re.split(r'[,\s]+', question)]
                if user_id_field:
                    user_id = user_id_field.value.strip()
                    user = await ctx.guild.fetch_member(int(user_id))
                    if user:
                        embed = discord.Embed(title="Q&A", color=0x2b2d31, description=f"**Question:**\n{' '.join(question)}\n**Answer:**\n{answer}")
                        embed.set_footer(text=f"asked by {user.display_name} | answered by {ctx.author.display_name}")
                        await answer_channel.send(f"<@{user_id}>", embed=embed)
                        embed = msg.embeds[0]
                        embed.add_field(name="Status", value="Answered ✅")
                        await ctx.message.add_reaction("✅")
                        await msg.edit(embed=embed)
                else:
                    await ctx.send("Failed to find the User ID field in the embed.")
            except Exception as e:
                print(f"Failed to process the command: {e}")
        else:
            await ctx.send("Please reply to the question you want to answer.")

    @commands.command()
    async def recruit(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1055168099252437094/1284963438040317972/forms_00000.png?ex=66e88af5&is=66e73975&hm=2c1c96c3ac04970b242182ae64f310cb06b09bc491e3080ec3ac5ba5e8ee9c15&")
        embed2 = discord.Embed(title="Halloween Recruit", description="Welcome to [chromagrp's](https://instagram.com/chromagrp) Halloween recruit! Please\nread the information below!\n\n**INFORMATION**\n• Make sure you have followed all  recruit rules\n• Click the **Apply** button and fill out the form\n• Hoshi will DM you with our response\n・you will get a response if you're declined!\n• You only have 2 attempts to apply\n\n-# **Note:** please be patient with us! you will get a\n-# response soon!\n-# Ask any questions in <#862624723057508372>", color=0x2b2d31)
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2, view=applybutton(bot=self.bot))

    async def update_accepted(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = '''UPDATE recruit SET accepted = 1 WHERE member_id = ?'''
                await cursor.execute(query, (member_id,))
                await conn.commit()

    @commands.command()
    @is_staff()
    async def accept(self, ctx):
        """Accept a member"""
        if ctx.message.reference is not None:
            try:
                channel_id = 694010549532360726
                channel = self.bot.get_channel(channel_id)
                msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                user_id_str = msg.embeds[0].fields[0].value
                username = msg.embeds[0].fields[1].value
                user_id = int(user_id_str)
                member = ctx.guild.get_member(user_id)
                if not member:
                    return await ctx.send(f"Member with ID {user_id} not found in the guild.")
                
                print(f"member id: {user_id} member: {member} username: {username}")
                embed = msg.embeds[0]
                embed.set_footer(text=f"Sent from {member.name} | Status: Accepted")
                embed.color=0x6db870
                await ctx.message.add_reaction("✅")
                await msg.edit(embed=embed, view=None)

                member_embed = discord.Embed(
                    title="Welcome to chroma!",
                    description="Read the rules before joining the Chroma discord!",
                    color=0x2b2d31
                )
                member_embed.add_field(
                    name="\u200b",
                    value=(
                        '**Group Rules**\n'
                        '• Must be following [remqsi](https://instagra,.com/remqsi), '
                        '[wqndqs](https://instagra,.com/wqndqs) + [chromagrp](https://instagra,.com/chromagrp).\n'
                        '• Always use our hashtag #𝗰𝗵𝗿𝗼𝗺𝗮𝗴𝗿𝗽\n'
                        '• Watermark logos if the background is mostly plain\n'
                        '• Never share the logos with anyone outside of Chroma\n\n'
                        '**Chat Rules**\n'
                        '• No NSFW content or sexual discussions\n'
                        '• No offensive jokes that can make others uncomfortable\n'
                        '• Please stay as active as possible\n'
                        '• Set your nickname as "name | username"\n'
                        '• No impersonating other editors\n'
                        '• Be friendly and respect everyone\n'
                        '• If you move accounts or leave, please DM chromagrp\n'
                        '• No trash talking of other groups or editors\n'
                        '• Respect the server and use channels correctly'
                    )
                )
                member_embed.set_thumbnail(url="https://cdn.discordapp.com/icons/694010548605550675/a_80f4bc45ba19971839fb3643ab1042ac.gif?size=1024&width=0&height=307")

                invite = await channel.create_invite(max_age=86400, max_uses=1, unique=True)
                invite_url = str(invite)

                view = discord.ui.View()
                invite_button = discord.ui.Button(label="Click to join", url=invite_url)
                view.add_item(invite_button)
                await self.update_accepted(member.id)
                await member.send(embed=member_embed, view=view)

                roleid = 836244165637046283
                role = ctx.guild.get_role(roleid)
                await member.add_roles(role)

                msgchannel = self.bot.get_channel(835837557036023819)
                sendch = self.bot.get_channel(836677673681944627)
                embed2 = discord.Embed(description=f"**you accepted {member.mention}!**", color=0x2b2d31)
                view = discord.ui.View()
                user = discord.ui.Button(label=f"follow {username}", url=f"https://instagram.com/{username}")
                view.add_item(user)
                await msgchannel.send(embed=embed2, view=view)
            
            except discord.errors.Forbidden:
                embed = discord.Embed(
                    title="Error",
                    description="```py\nForbidden\nI can't DM this user.```",
                    color=0xe63241
                )
                await ctx.reply(embed=embed)
        else:
            await ctx.send("No message reference found.")

    @commands.command(alias="wipe")
    @commands.is_owner()
    async def clearapps(self, ctx):
        """Wipe the recruit table"""
        await ctx.send("Are you sure you want to wipe the recruit table? Say `yes` to confirm.")

        def check(m) -> bool:
            return m.content == "yes" and m.author == ctx.author and m.channel == ctx.channel

        try:
            await self.bot.wait_for("message", check=check, timeout=10)

        except asyncio.TimeoutError:
            await ctx.send("Wipe cancelled!")

        else:
            await self.clear_database()
            await ctx.send("The database has been cleared.")

    async def clear_database(self):
        query = '''DELETE FROM recruit'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                await conn.commit()

    @commands.command()
    async def addattempt(self, ctx, member: discord.Member):
        await self.add_attempt(member.id)
        await ctx.reply(f"I have added 1 attempt for {member.mention}")

    async def add_attempt(self, member_id: int) -> None:
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = '''UPDATE recruit SET attempts = attempts + 1 WHERE member_id = ? AND attempts > 0'''
                await cursor.execute(query, (member_id,))
                await conn.commit()

async def setup(bot):
    await bot.add_cog(Forms(bot))