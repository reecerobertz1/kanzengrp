import asyncio
import re
import discord
from discord.ext import commands
from discord import ui
import random

class verify(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.red)
    async def verify(self, interaction: discord.Interaction, button: discord.Button):
        letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
        numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        code = "".join([
            random.choice(letters), random.choice(letters), str(random.choice(numbers)),
            random.choice(letters), random.choice(letters), str(random.choice(numbers)),
            random.choice(letters), random.choice(letters), str(random.choice(numbers))
        ])

        await interaction.response.send_message(f"Please type this code below:\n`{code}`", ephemeral=True)

        def check(msg: discord.Message):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await interaction.client.wait_for("message", check=check, timeout=60)

            if msg.content.strip().upper() == code:
                role = interaction.guild.get_role(1341753597368733736)
                if role:
                    await interaction.user.add_roles(role)
                    await interaction.followup.send("✅ Verification successful! You have been given the role.", ephemeral=True)
                    await msg.delete()
                else:
                    await interaction.followup.send("❌ The 'Verified' role was not found. Please contact an admin.", ephemeral=True)
                    await msg.delete()
            else:
                await interaction.followup.send("❌ Incorrect code! Please try again by clicking the verify button again.", ephemeral=True)
                await msg.delete()

        except TimeoutError:
            await interaction.followup.send("⌛ You took too long to respond. Please try again.", ephemeral=True)

    @discord.ui.button(label="Help")
    async def help(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed (description="## Verification Help\n<:bullet_point_blue:1340661702378786879>Click the `Verify` button below\n<:bullet_point_blue:1340661702378786879>Hoshi will randomly generate a code for you to use\n<:bullet_point_blue:1340661702378786879>Send the same code within 60 seconds into chat to complete verification\n<:bullet_point_blue:1340661702378786879>If the bot does not reply after you have sent the code, or doesn't give you <@&1341753597368733736>. Please contact a staff member!", color=0xA4C4E6)
        await interaction.response.send_message(embed=embed, ephemeral=True)

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

class Community(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def qna(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Chroma Q&A", description="**INFORMATION**\n・Use the **Ask** button below to send us your question.\n・Our response will be sent into <#862617899356651531>\n・No question is dumb, so feel free to ask any questions you have!\n・Use the **Commonly Asked** button to check if your question has an answer already.", color=0x2b2d31)
        embed.add_field(name="EXTRA", value="・We will try our best to get back to you as soon as possible.\n・If you spam our qna we will not respond!\n・Do not abuse this feature, and do not harass out staff.\n⠀— ・**Note:** If you harass our staff we will kick or ban you from our server!")
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
    async def verifyy(self, ctx):
        embed = discord.Embed(description="## Verification Required\n<:redpoint:1348433483844030484>To access the server, you need to pass the verification first.\n<:redpoint:1348433483844030484>Click `Verify` to begin the verification process.", color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1055168099252437094/1348432753070444544/Comp_7_00000.png?ex=67cf715d&is=67ce1fdd&hm=62675a13b52993107da1b725afbd3919ec187b2c5f7713fedfee6fe8e8b08464&")
        await ctx.send(embed=embed, view=verify())

async def setup(bot):
    await bot.add_cog(Community(bot))