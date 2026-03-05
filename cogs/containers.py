import discord
from discord import ui
from discord.ext import commands

class MenuLayout(ui.LayoutView):
    def __init__(self):
        super().__init__()

        container = ui.Container(ui.TextDisplay("This is a text display"))
        container.add_item(ui.Separator())

        yas = ui.Section(ui.TextDisplay("This is a section"), accessory=ui.Button(label="Click me!"))

        self.add_item(container)
        container.add_item(yas)

class container_test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def container(self, ctx):
        layout = MenuLayout()
        await ctx.send(view=layout)

async def setup(bot):
    await bot.add_cog(container_test(bot))