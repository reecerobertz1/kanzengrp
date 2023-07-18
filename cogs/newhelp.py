from typing import Any
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import View, Select

class newhelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

class HelpSelect(Select):
    def __init__(self, bot: commands.bot):
        super().__init__(
            placeholder="Choose a category",
            options=[
                discord.SelectOption(
            label=cog_name, description=cog.__doc__
                ) for cog_name, cog in bot.cogs.items if cog.__cog__commands and cog_name not in ['Jishaku']
            ]
        )

        self.bot = bot

    async def callback(self, interaction: discord.Interaction) -> None:
        cog = self.bot.get_cog(self.values[0])
        assert cog

        commands_mixer = []
        for i in cog.walk_commands():
            commands_mixer.append(i)

        for i in cog.walk_commands():
            commands_mixer.append(i)

        embed = discord.Embed(
            title=f'{cog.__cog_name__} Commands',
            description='\n'.join(
            f"**{command}**, `{command.description}`"
            for command in commands_mixer
            )
        )
        await interaction.response.send_message(embed=embed)


        @commands.hybrid_command(name=newhelp, description='Shows list of commands')
        async def newhelp(self, ctx):
            embed = discord.Embed(
                title='Help command',
                description='This is a help command'
            )
            view = View().add_item(HelpSelect(self.bot))
            await ctx.send(embed=embed, view=view)

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(newhelp(bot))