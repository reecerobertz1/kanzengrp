import discord
from discord.ext import commands
from discord import app_commands, ui

class FollowupView(discord.ui.View):
    def __init__(self, bot: commands.Bot, question: str, answer: str, asker: discord.User):
        super().__init__(timeout=None)
        self.bot = bot
        self.question = question
        self.answer = answer
        self.asker = asker

    @discord.ui.button(label="Ask a Follow-Up Question", style=discord.ButtonStyle.secondary)
    async def follow_up_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FollowUpModal(self.bot, self.question, self.answer, self.asker))


class AnswerView(discord.ui.View):
    def __init__(self, bot: commands.Bot, asker: discord.User, question: str):
        super().__init__(timeout=None)
        self.bot = bot
        self.asker = asker
        self.question = question

    @discord.ui.button(label="Answer", style=discord.ButtonStyle.primary)
    async def Answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Answer(self.bot, self.question, self.asker))


class FollowupAnswerView(discord.ui.View):
    def __init__(self, bot: commands.Bot, asker: discord.User, ogquestion: str, oganswer: str, question: str):
        super().__init__(timeout=None)
        self.bot = bot
        self.asker = asker
        self.ogquestion = ogquestion
        self.oganswer = oganswer
        self.question = question

    @discord.ui.button(label="Answer", style=discord.ButtonStyle.primary)
    async def Answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(
            FollowupAnswer(self.bot, self.question, self.asker, self.ogquestion, self.oganswer)
        )


class QnAView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Ask a Question", style=discord.ButtonStyle.primary, custom_id="ask_question")
    async def ask_question(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = QnAModal(self.bot)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="View FAQs", style=discord.ButtonStyle.secondary, custom_id="view_faqs")
    async def view_faqs(self, interaction: discord.Interaction, button: discord.ui.Button):
        faq_embed = discord.Embed(
            title="Frequently Asked Questions",
            description=(
                "・⠀**When will Chromatica recruit again?**\n"
                "-# ⠀— ・⠀We don’t have a fixed schedule for recruiting. We usually open applications when it feels right or when we need new members.\n\n"

                "・⠀**How many members are accepted during recruitment?**\n"
                "-# ⠀— ・⠀There is no set number. It depends on the applicants and what we are looking for at the time.\n\n"

                "・⠀**If accepted, can we use Chromagrp logos?**\n"
                "-# ⠀— ・⠀No, since Chromagrp disbanded, and Chromatica is a rebrand, using Chromagrp logos is not allowed.\n\n"

                "・⠀**Can we receive feedback if our application is declined?**\n"
                "-# ⠀— ・⠀We currently do not provide feedback due to past issues with how it was received.\n"
                "-# ⠀— ・⠀However, you can ask for editing opinions in #・edit﹒help.\n"
                "-# ⠀— ・⠀This may return in the future if we find a better system.\n\n"

                "・⠀**Can we pay or contribute logos to join the group?**\n"
                "-# ⠀— ・⠀No. Chromatica will never allow this, as it would be unfair to other applicants.\n\n"

                "・⠀**Does Chromatica accept TikTok editors?**\n"
                "-# ⠀— ・⠀Yes. We accept editors from both TikTok and Instagram.\n\n"

                "・⠀**What does Chromatica look for in edits?**\n"
                "-# ⠀— ・⠀A common misconception is that we only accept one style or specific software.\n"
                "-# ⠀— ・⠀We look for creative transitions that are smooth and well executed.\n"
                "-# ⠀— ・⠀Your program, style, or fandom does not matter.\n\n"

                "・⠀**If I join Chromatica, am I also part of Chromagrp?**\n"
                "-# ⠀— ・⠀No. Chromagrp disbanded in January 2026 and is no longer active.\n"
                "-# ⠀— ・⠀Any use of Chromagrp logos is likely from leaks or former members ignoring the disbandment."
            )
        )

        await interaction.response.send_message(embed=faq_embed, ephemeral=True)


class QnAModal(discord.ui.Modal, title="Ask a Question"):
    question = discord.ui.TextInput(label="Your Question", style=discord.TextStyle.paragraph)

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        question_channel = self.bot.get_channel(1477653077510066360)

        embed = discord.Embed(title="CHROMATICA Q&A", description=f"**QUESTION**\n{self.question.value}")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"Asked by {interaction.user.display_name} ({interaction.user.id})")

        await question_channel.send(
            embed=embed,
            view=AnswerView(self.bot, asker=interaction.user, question=self.question.value)
        )

        await interaction.response.send_message(
            "Your question has been submitted! A staff member will get back to you as soon as possible.",
            ephemeral=True
        )


class Answer(discord.ui.Modal, title="Answer a Question"):
    answer = discord.ui.TextInput(label="Your Answer", style=discord.TextStyle.paragraph)

    def __init__(self, bot: commands.Bot, question: str, asker: discord.User):
        super().__init__()
        self.bot = bot
        self.question = question
        self.asker = asker

    async def on_submit(self, interaction: discord.Interaction):
        answer_channel = self.bot.get_channel(1465297627976564830)
        asker = self.bot.get_user(self.asker.id)

        embed = discord.Embed(
            title="CHROMATICA Q&A",
            description=f"**QUESTION**\n{self.question}\n\n**ANSWER**\n{self.answer.value}"
        )
        embed.set_thumbnail(url=asker.display_avatar.url)
        embed.set_footer(text=f"Asked by {asker.display_name} / Answered by {interaction.user.display_name}")

        await answer_channel.send(f"{asker.mention}", embed=embed)

        try:
            await asker.send(
                embed=embed,
                view=FollowupView(self.bot, question=self.question, answer=self.answer.value, asker=asker)
            )
        except discord.Forbidden:
            pass

        await interaction.message.edit(view=None)
        await interaction.response.send_message("Your answer has been submitted!", ephemeral=True)


class FollowupAnswer(discord.ui.Modal, title="Answer a Follow-Up Question"):
    answer = discord.ui.TextInput(label="Your Answer", style=discord.TextStyle.paragraph)

    def __init__(self, bot: commands.Bot, question: str, asker: discord.User, ogquestion: str, oganswer: str):
        super().__init__()
        self.bot = bot
        self.question = question
        self.asker = asker
        self.ogquestion = ogquestion
        self.oganswer = oganswer

    async def on_submit(self, interaction: discord.Interaction):
        answer_channel = self.bot.get_channel(1465297627976564830)
        asker = self.bot.get_user(self.asker.id)

        embed = discord.Embed(
            title="CHROMATICA Q&A",
            description=(
                f"**ORIGINAL QUESTION**\n{self.ogquestion}\n\n"
                f"**ORIGINAL ANSWER**\n{self.oganswer}\n\n"
                f"**FOLLOW-UP QUESTION**\n{self.question}\n\n"
                f"**ANSWER**\n{self.answer.value}"
            )
        )
        embed.set_thumbnail(url=asker.display_avatar.url)
        embed.set_footer(text=f"Asked by {asker.display_name} / Answered by {interaction.user.display_name}")

        await answer_channel.send(f"{asker.mention}", embed=embed)
        await asker.send(embed=embed)

        await interaction.message.edit(view=None)
        await interaction.response.send_message("Your answer has been submitted!", ephemeral=True)


class FollowUpModal(discord.ui.Modal, title="Ask a Follow-Up Question"):
    follow_up = discord.ui.TextInput(label="Your Follow-Up Question", style=discord.TextStyle.paragraph)

    def __init__(self, bot: commands.Bot, question: str, answer: str, asker: discord.User):
        super().__init__()
        self.bot = bot
        self.question = question
        self.answer = answer
        self.asker = asker

    async def on_submit(self, interaction: discord.Interaction):
        question_channel = self.bot.get_channel(1477653077510066360)

        embed = discord.Embed(
            title="CHROMATICA Q&A - Follow-Up",
            description=(
                f"**ORIGINAL QUESTION**\n{self.question}\n\n"
                f"**ORIGINAL ANSWER**\n{self.answer}\n\n"
                f"**FOLLOW-UP QUESTION**\n{self.follow_up.value}"
            )
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"Asked by {interaction.user.display_name} ({interaction.user.id})")

        await question_channel.send(
            embed=embed,
            view=FollowupAnswerView(
                self.bot,
                asker=self.asker,
                ogquestion=self.question,
                oganswer=self.answer,
                question=self.follow_up.value
            )
        )

        # ✅ REMOVE FOLLOW-UP BUTTON AFTER USE
        try:
            await interaction.message.edit(view=None)
        except:
            pass

        await interaction.response.send_message(
            "Your follow-up question has been submitted! A staff member will get back to you as soon as possible.",
            ephemeral=True
        )


class QnA(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="cgpqna", description="Open the Q&A menu")
    async def cgpqna(self, ctx):
        banner_embed = discord.Embed()
        banner_embed.set_image(url="https://cdn.discordapp.com/attachments/1477651776139427872/1482750185099493426/Small_Headers_00005.png")

        embed = discord.Embed(
            title="CHROMATICA Q&A",
            description="**INFORMATION**\n・⠀01 : Use the **Ask a Question** button to submit your question.\n・⠀02 : Our answers will be sent into <#1465297627976564830> and your dms.\n・⠀03 : You're able to ask a follow-up question from our answers.\n・⠀04 : No question is dumb, feel free to ask anything!\n・⠀05 : Please **View FAQs** before asking questions.\n・⠀06 : Any negative questions will be ignored.\n\n**INFORMATION**\n・⠀01 : We will try our best to answer as soon as possible.\n・⠀02 : Spamming this feature will result in a timeout.\n\n-# **Note:** Harrassing staff will result in a kick or ban from our server!"
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1477651776139427872/1482129813182615693/Comp_5_00000.png")

        await ctx.send(embeds=[banner_embed, embed], view=QnAView(self.bot), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(QnA(bot))