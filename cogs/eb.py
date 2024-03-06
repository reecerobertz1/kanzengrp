import discord
from discord.ext import commands
from discord import app_commands, ui

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

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.apply_id=1214940420946272316
        self.forms_id=1131006328207327294
        self.qna_id=1214940489883717662

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

async def setup(bot):
    await bot.add_cog(Forms(bot))