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


    @app_commands.command()
    async def ianewtest(self, interation: discord.Integration):
        await interation.responce.send_modal(ia())

async def setup(bot):
    await bot.add_cog(modals(bot))