from typing import Optional
import discord
from discord.ext import commands
from typing import List, Optional, TypedDict, Union, Tuple

class LevelRow(TypedDict):
    member_id: int
    xp: int
    messages: int
    color: str
    image: str

class start(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.responses = {}
        self.bot = bot

    @discord.ui.button(label="Start Survey", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 1'] = None
        embed = discord.Embed(title="Question 1", description="Do you think we have too many, too few, or a good amount of events?\n-# **Note:** This doesn't include collabs\n\n**A.** too many\n**B.** too few\n**C.** good amount", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=eventsgoodorbad(self.bot, self.responses))

class eventsgoodorbad(discord.ui.View):
    def __init__(self, bot, responses):
        super().__init__(timeout=None)
        self.responses = responses
        self.bot = bot

    @discord.ui.button(label="A")
    async def a(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 1'] = "too many"
        embed = discord.Embed(title="Question 2", description="Are there any holidays we could do events for? (Lunar New Year, etc.)", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=holidayevents(responses=self.responses, bot=self.bot))

    @discord.ui.button(label="B")
    async def b(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 1'] = "too few"
        embed = discord.Embed(title="Question 2", description="Are there any holidays we could do events for? (Lunar New Year, etc.)", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=holidayevents(responses=self.responses, bot=self.bot))

    @discord.ui.button(label="C")
    async def c(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 1'] = "good amount"
        embed = discord.Embed(title="Question 2", description="Are there any holidays we could do events for? (Lunar New Year, etc.)", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=holidayevents(responses=self.responses, bot=self.bot))

class holidayevents(discord.ui.View):
    def __init__(self, bot, responses):
        super().__init__(timeout=None)
        self.responses = responses
        self.bot = bot

    @discord.ui.button(label="Answer")
    async def a(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(holidayeventmodal(responses=self.responses, bot=self.bot))

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.red)
    async def b(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 2'] = "Skipped"
        embed = discord.Embed(title="Question 3", description="Have our staff been helpful in anyway? If yes how?", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=helpfulstaff(responses=self.responses, bot=self.bot))

class helpfulstaff(discord.ui.View):
    def __init__(self, bot, responses):
        super().__init__(timeout=None)
        self.responses = responses
        self.bot = bot

    @discord.ui.button(label="Answer")
    async def a(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(staff(responses=self.responses, bot=self.bot))

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.red)
    async def b(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 3'] = "Skipped"
        embed = discord.Embed(title="Question 4", description="Are there any features you want us to add to hoshi?", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=features(responses=self.responses, bot=self.bot))

class features(discord.ui.View):
    def __init__(self, bot, responses):
        super().__init__(timeout=None)
        self.responses = responses
        self.bot = bot

    @discord.ui.button(label="Answer")
    async def a(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(hoshifeatures(responses=self.responses, bot=self.bot))

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.red)
    async def b(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 4'] = "Skipped"
        embed = discord.Embed(title="Question 5", description="Are our servers easy to navigate? (members + community)\nPlease let us know what you think!", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=servers(responses=self.responses, bot=self.bot))

class servers(discord.ui.View):
    def __init__(self, bot, responses):
        super().__init__(timeout=None)
        self.responses = responses
        self.bot = bot

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def a(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 5'] = "Yes"
        embed = discord.Embed(title="Question 6", description="Have you ever felt uncomfortable, upset or just didn't like what some members are/have done\nIf yes please tell us why\n\n-# **Note: no need to name names if you don't want to**", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=uncomfortable(responses=self.responses, bot=self.bot))

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def b(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(serversno(responses=self.responses, bot=self.bot))

class uncomfortable(discord.ui.View):
    def __init__(self, bot, responses):
        super().__init__(timeout=None)
        self.responses = responses
        self.bot = bot

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def a(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(uncomfort(responses=self.responses, bot=self.bot))

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def b(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 6'] = "No"
        embed = discord.Embed(title="Question 7", description="If you're an old chromie. Do you think the new leads have improved Chroma in anyway?\nIf no, how can we imrpove more?", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=newchromie(responses=self.responses, bot=self.bot))

class newchromie(discord.ui.View):
    def __init__(self, bot, responses):
        super().__init__(timeout=None)
        self.responses = responses
        self.bot = bot

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def a(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 7'] = "Yes"
        embed = discord.Embed(title="Question 8", description="Is there anything else you'd like to tell us that you wasn't able to answer?", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=anythingelse(responses=self.responses, bot=self.bot))

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def b(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(newchromies(responses=self.responses, bot=self.bot))

class anythingelse(discord.ui.View):
    def __init__(self, bot, responses):
        super().__init__(timeout=None)
        self.responses = responses
        self.bot = bot

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def a(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(anything(responses=self.responses, bot=self.bot))
        

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def b(self, interaction: discord.Interaction, button: discord.Button):
        self.responses['Question 8'] = "No"
        embed = discord.Embed(title="End of survey", description="Please click submit below and you will receive **1,000xp**", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=end(responses=self.responses, bot=self.bot))

class end(discord.ui.View):
    def __init__(self, bot, responses):
        super().__init__(timeout=None)
        self.responses = responses
        self.bot = bot
        self.questions = {
            'Question 1': "Do you think we have too many, too few, or a good amount of events?",
            'Question 2': "Are there any holidays we could do events for? (Lunar New Year, etc.)",
            'Question 3': "Have our staff been helpful in anyway? If yes how?",
            'Question 4': "Are there any features you want us to add to hoshi?",
            'Question 5': "Are our servers easy to navigate? (members + community)",
            'Question 6': "Have you ever felt uncomfortable, upset or just didn't like what some members are/have done",
            'Question 7': "If you're an old chromie. Do you think the new leads have improved Chroma in anyway?",
            'Question 8': "Is there anything else you'd like to tell us that you wasn't able to answer?"
        }

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.green)
    async def submit(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(
            title="Survey Complete", 
            description="Thank you so much for completing this survey! We will go over your answers and improve chroma!\nYou have received **1,000 XP**", 
            color=0x2b2d31
        )
        await interaction.response.edit_message(embed=embed, view=None)

        guild = self.bot.get_guild(694010548605550675)
        channel = guild.get_channel(1287148738795536504)

        if channel:
            formatted_responses = "\n".join(
                [f"**{self.questions[question]}**\n・ {answer}" for question, answer in self.responses.items()]
            )

            survey_results_embed = discord.Embed(
                title="Survey Results", 
                description=f"{formatted_responses}", 
                color=0x2b2d31
            )
            await channel.send(embed=survey_results_embed)
            levels = await self.get_member_levels(interaction.user.id)
            await self.add_xp(interaction.user.id, 1000, levels)
        else:
            print("Failed to find the channel")

    async def get_member_levels(self, member_id: int) -> Optional[LevelRow]:
        query = '''SELECT * from chromalevels WHERE member_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, ))
                row = await cursor.fetchone()
                if row:
                    return row
                else:
                    return None

    async def add_xp(self, member_id: int, xp: int, levels: Optional[LevelRow]) -> None:
        if levels:
            current_xp = levels['xp']
            new_xp = current_xp + xp

            query = '''UPDATE chromalevels SET xp = ? WHERE member_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (new_xp, member_id))
                    await conn.commit()
        else:
            await self.add_member(member_id, xp)

    async def add_member(self, member_id: int, xp=5) -> None:
        query = '''INSERT INTO chromalevels (member_id, xp, messages, color) VALUES (?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, xp, 1, '#c45a72'))
                await conn.commit()
            await self.bot.pool.release(conn)

class anything(discord.ui.Modal):
    def __init__(self, bot, responses):
        self.bot = bot
        self.responses = responses
        super().__init__(title="Chroma Survey")

    reason = discord.ui.TextInput(label="Answer here", placeholder="", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        self.responses['Question 8'] = self.children[0].value
        embed = discord.Embed(title="End of survey", description="Please click submit below and you will receive **1,000xp**", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=end(responses=self.responses, bot=self.bot))

class newchromies(discord.ui.Modal):
    def __init__(self, bot, responses):
        self.bot = bot
        self.responses = responses
        super().__init__(title="Chroma Survey")

    reason = discord.ui.TextInput(label="Answer here", placeholder="", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        self.responses['Question 7'] = self.children[0].value
        embed = discord.Embed(title="Question 8", description="Is there anything else you'd like to tell us that you wasn't able to answer?", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=end(responses=self.responses, bot=self.bot))

class uncomfort(discord.ui.Modal):
    def __init__(self, bot, responses):
        self.bot = bot
        self.responses = responses
        super().__init__(title="Chroma Survey")

    reason = discord.ui.TextInput(label="Answer here", placeholder="", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        self.responses['Question 6'] = self.children[0].value
        embed = discord.Embed(title="Question 7", description="If you're an old chromie. Do you think the new leads have improved Chroma in anyway?", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=newchromie(responses=self.responses, bot=self.bot))

class serversno(discord.ui.Modal):
    def __init__(self, bot, responses):
        self.bot = bot
        self.responses = responses
        super().__init__(title="Chroma Survey")

    reason = discord.ui.TextInput(label="Answer here", placeholder="", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        self.responses['Question 5'] = self.children[0].value
        embed = discord.Embed(title="Question 6", description="Have you ever felt uncomfortable, upset or just didn't like what some members are/have done\nIf yes please tell us why\n\n-# **Note: no need to name names if you don't want to**", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=uncomfortable(responses=self.responses, bot=self.bot))

class hoshifeatures(discord.ui.Modal):
    def __init__(self, bot, responses):
        self.bot = bot
        self.responses = responses
        super().__init__(title="Chroma Survey")

    reason = discord.ui.TextInput(label="Answer here", placeholder="", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        self.responses['Question 4'] = self.children[0].value
        embed = discord.Embed(title="Question 5", description="Are our servers easy to navigate? (members + community)", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=servers(responses=self.responses, bot=self.bot))

class staff(discord.ui.Modal):
    def __init__(self, bot, responses):
        self.bot = bot
        self.responses = responses
        super().__init__(title="Chroma Survey")

    reason = discord.ui.TextInput(label="Answer here", placeholder="", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        self.responses['Question 3'] = self.children[0].value
        embed = discord.Embed(title="Question 4", description="Are there any features you want us to add to hoshi?", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=features(responses=self.responses, bot=self.bot))

class holidayeventmodal(discord.ui.Modal):
    def __init__(self, bot, responses):
        self.bot = bot
        self.responses = responses
        super().__init__(title="Chroma Survey")

    reason = discord.ui.TextInput(label="Answer here", placeholder="", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        self.responses['Question 2'] = self.children[0].value
        embed = discord.Embed(title="Question 3", description="Have our staff been helpful in anyway? If yes how?", color=0x2b2d31)
        await interaction.response.edit_message(embed=embed, view=helpfulstaff(responses=self.responses, bot=self.bot))

class survey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def survey(self, ctx):
        member = ctx.author
        if ctx.guild:
            await ctx.message.delete()
        embed = discord.Embed(title="Chromagrp Survey", description="Thank you for wanting to help us improve our group!\nFor completing this survey you will be granted **1,000xp**\n-# **Note:** Some questions about new features are concepts for now. They may not be added in the future", color=0x2b2d31)
        await member.send(embed=embed, view=start(bot=self.bot))

async def setup(bot):
    await bot.add_cog(survey(bot))