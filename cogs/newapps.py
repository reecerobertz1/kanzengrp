import discord
from discord.ext import commands
from discord import ui
from discord import app_commands

class modals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


class ia(ui.Modal, title='Inactivity Message'):
    instagram = ui.TextInput(label='What is your instagram username?', placeholder='Enter your instagram username here...', style=discord.TextStyle.short)
    iareason = ui.TextInput(label='What is your inactivity reason?', placeholder='Enter your reason here...', style=discord.TextStyle.long)

    async def on_submit(interation: discord.Interaction):
        await interation.responce.send_message('boobs')


class Slash(commands.Cog):
	"""All of cloudy's slash commands"""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot: commands.Bot = bot
		super().__init__()

	@app_commands.command(description="im sorry alex im testing this- its not working i wanna die- i am deleteting this i promise AAAH")
	async def apply(self, interaction: discord.Interaction):
		async with interaction.client.db.cursor() as cursor:
			await cursor.execute('''SELECT * FROM applications WHERE user_id = ?''', (interaction.user.id,))
			row = await cursor.fetchone()
			if row:
				return await interaction.response.send_message('You have already applied!', ephemeral=True)
		await interaction.response.send_modal(ia())

async def setup(bot):
    await bot.add_cog(modals(bot))