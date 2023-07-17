import discord
from discord.ext import commands
from discord import app_commands
import traceback
from typing import Optional
from io import BytesIO

# Modals

class Recruit(discord.ui.Modal, title="Chroma Recruit"):
	instagram = discord.ui.TextInput(label="Instagram Username", placeholder="Put username here...")
	edit_link = discord.ui.TextInput(label="Link to edit (Instagram/Streamble Only)", placeholder="Put a link to an edit here...")
	program = discord.ui.TextInput(label="Editing Program", placeholder="Put the editing program you use here...")
	other = discord.ui.TextInput(label="Anything else you want us to know?", placeholder="Put other information here...", required=False)

	async def on_submit(self, interaction: discord.Interaction):
		await interaction.response.defer()
		embed = discord.Embed(title="idk what im doing help me", description="", color=0x303136)
		embed.add_field(name="Discord ID", value=interaction.user.id, inline=False)
		embed.add_field(name="Instagram Username", value=self.instagram.value, inline=False)
		embed.add_field(name="Account Link", value=f"https://instagram.com/{self.instagram.value}")
		embed.add_field(name="Edit Link", value=self.edit_link.value, inline=False)
		embed.add_field(name="Editing Program", value=self.program.value, inline=False)
		embed.set_thumbnail(url="https://rqinflow.com/static/chroma-pfp-animation.gif")
		if self.other.value:
			embed.add_field(name="Anything else", value=self.other.value, inline=False)
		async with interaction.client.db.cursor() as cursor:
			try:
				await cursor.execute('''INSERT INTO applications (user_id, instagram, accepted) VALUES (?, ?, ?)''', (interaction.user.id, self.instagram.value, 0))
				await interaction.client.db.commit()
			except Exception as e:
				if str(e) == "UNIQUE constraint failed: applications.instagram":
					return await interaction.followup.send(f"An entry for **{self.instagram.value}** has already been registered. If this wasn't you, please notify a staff member and they will help you out!", ephemeral=True)
				else:
					print(str(e))
					return await interaction.followup.send("Something went wrong!", ephemeral=True)
			msg = await interaction.client.get_channel(835497793703247903).send(embed=embed)
			await cursor.execute('''UPDATE applications SET msg_id = ? WHERE user_id = ?''', (msg.id, interaction.user.id))
			await interaction.client.db.commit()
		await interaction.followup.send(f'Thanks for joining the recruit!', ephemeral=True)

	async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
		await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
		traceback.print_tb(error.__traceback__)
		
class Slash(commands.Cog):
	"""All of cloudy's slash commands"""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot: commands.Bot = bot
		super().__init__()

	@app_commands.command(description="Join the Chroma Recruit")
	async def apply(self, interaction: discord.Interaction):
		async with interaction.client.db.cursor() as cursor:
			await cursor.execute('''SELECT * FROM applications WHERE user_id = ?''', (interaction.user.id,))
			row = await cursor.fetchone()
			if row:
				return await interaction.response.send_message('You have already applied!', ephemeral=True)
		await interaction.response.send_modal(Recruit())
		

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Slash(bot))