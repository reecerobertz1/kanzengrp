from discord.ext import commands
import discord
from discord.ui import View, Select

class HelpSelect(Select):
    def __init__(self, bot: commands.Bot):
        options = [
            discord.SelectOption(label=cog_name, description=cog.__doc__, value=cog_name)
            for cog_name, cog in bot.cogs.items()
            if cog.__cog_commands__ and not getattr(cog, "hidden", False) and cog_name != 'jishaku'
        ]
        super().__init__(placeholder="Select a category!", options=options)
        self.bot = bot

    async def callback(self, interaction: discord.Interaction) -> None:
        cog_name = self.values[0]
        cog = self.bot.get_cog(cog_name)
        assert cog

        commands_mixer = []
        for i in cog.walk_commands():
            if not getattr(i, "hidden", False):
                commands_mixer.append(i)

        embed = discord.Embed(description='\n'.join(f"**{self.bot.command_prefix}{command.name}:**\n<a:Arrow_1:1145603161701224528> {command.description}\n" for command in commands_mixer), color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_author(name=f"{cog.__cog_name__} commands", icon_url=interaction.user.avatar)
        await interaction.response.edit_message(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True

    @commands.command(
        name="help", description="Help command for all of Hoshi's commands"
    )
    async def help(self, ctx):
        embed = discord.Embed(
            description="owner info:\n<a:Arrow_1:1145603161701224528> Hoshi is owned by [Reece](https://instagram.com/remqsi)\n<a:Arrow_1:1145603161701224528> Reece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)\n\ndevelopment info:\n<a:Arrow_1:1145603161701224528> Hoshi is coded in Python 3.11.4\n<a:Arrow_1:1145603161701224528> [Download Python 3.11.4](https://www.python.org/downloads/)\n<a:Arrow_1:1145603161701224528> Developed by [Reece](https://instagram.com/remqsi) with help from [Alex](https://instagram.com/rqinflow)\n\nextra info:\n<a:Arrow_1:1145603161701224528> Hoshi's prefix is `+`\n<a:Arrow_1:1145603161701224528> Hoshi was made for [**__Kanzengrp__**](https://instagram.com/kanzengrp)\n\nbug reports\n<a:Arrow_1:1145603161701224528> Use __+report__ to report bug reports!",
            color=0x2b2d31,
        )
        embed.set_author(name="About Hoshi", icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url=ctx.guild.icon)
        view = View().add_item(HelpSelect(self.bot))
        await ctx.reply(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))