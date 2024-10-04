import discord
from discord.ext import commands
from discord import app_commands

class StaffApps(discord.ui.Modal, title="Chroma Staff Application - Helper"):
	user = discord.ui.TextInput(label="What's your username?", placeholder="Put your Instagram @ here...", style=discord.TextStyle.short)
	why = discord.ui.TextInput(label="Why should we pick you?", placeholder="Put your reasoning here...", style=discord.TextStyle.paragraph)
	experience = discord.ui.TextInput(label="What kind of previous experience do you have?", placeholder="List your previous experience here...", style=discord.TextStyle.paragraph)
	events = discord.ui.TextInput(label="What would you contribute with?", placeholder="E.g. Events you wanna host and why, things you wanna improve in Chroma etc...", style=discord.TextStyle.paragraph)
	other = discord.ui.TextInput(label="Anything else you want us to know?", placeholder="Extra information goes here...", style=discord.TextStyle.paragraph, required=False)

	async def on_submit(self, interaction: discord.Interaction):
		await interaction.response.defer()
		for response in [self.why.value, self.experience.value, self.events.value, self.other.value]:
			if response is not None:
				if len(response) > 1024:
					return await interaction.followup.send("Your form reply exceeds our limits, try shortening your responses!", ephemeral=True)
		embed = discord.Embed(title="General Staff Application 🌈", description="", color=0x2B2D31)
		embed.add_field(name="Instagram Username", value=self.user.value, inline=False)
		embed.add_field(name="Why should we pick you?", value=self.why.value)
		embed.add_field(name="What kind of previous experience do you have?", value=self.experience.value, inline=False)
		embed.add_field(name="What kind of activities and/or events would you initiate in Chroma?", value=self.events.value, inline=False)
		if self.other.value:
			embed.add_field(name="Anything else you want us to know?", value=self.other.value, inline=False)
		embed.set_thumbnail(url=interaction.user.avatar)
		embed.set_footer(text=f"Sent from {interaction.user.name}")
		await interaction.client.get_channel(1098242178947481741).send(f"{interaction.user.mention}", embed=embed)
		await interaction.followup.send(f"<:check:1291748345194348594>**{interaction.user.name}**, I have sent your application!\n-# <:reply:1290714885792989238> If you think you have made a mistake, or wish to remove your application. Please ping a lead!", ephemeral=True)

class staffapps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @app_commands.command(description="Apply to be a part of the Chroma staff")
    @app_commands.guilds(discord.Object(id=694010548605550675))
    async def staffapps(self, interaction: discord.Interaction):
        await interaction.response.send_modal(StaffApps())

async def setup(bot):
    await bot.add_cog(staffapps(bot))