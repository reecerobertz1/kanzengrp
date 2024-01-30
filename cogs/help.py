from discord.ext import commands
import discord
from discord.ui import View, Select

class HelpSelect(Select):
    def __init__(self, bot: commands.Bot):
        options = [
            discord.SelectOption(label=cog_name, description=cog.__doc__, value=cog_name, emoji=str(cog.emoji))
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

        embed = discord.Embed(description='\n'.join(f"**{self.bot.command_prefix}{command.name}:**\n<:1166196254141861979:1188190233267818566>  {command.description}\n<:1166196258499727480:1188190249768210582> {command.extras}" for command in commands_mixer), color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_author(name=f"{cog.__cog_name__} commands", icon_url=interaction.user.avatar)
        await interaction.response.edit_message(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.emoji = "<:tata:1121909389280944169>"

    @commands.command(
        name="help", description="Help command for all of Hoshi's commands"
    )
    async def help(self, ctx):
        embed = discord.Embed(
            description="owner info:\n<:CF12:1188186414387568691> Hoshi is owned by [Reece](https://instagram.com/remqsi)\n<:CF12:1188186414387568691> Reece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)\n\ndevelopment info:\n<:CF12:1188186414387568691> Hoshi is coded in Python 3.11.4\n<:CF12:1188186414387568691> Developed by [Reece](https://instagram.com/remqsi), [Alex](https://instagram.com/rqinflow) and [Josh](https://instagram.com/xiaosaeq)\n\nextra info:\n<:CF12:1188186414387568691> Hoshi's prefix is `+`\n<:CF12:1188186414387568691> Hoshi was made for [Kanzengrp](https://instagram.com/kanzengrp)\n<:CF12:1188186414387568691>  Use __+report__ to report bugs",
            color=0x2b2d31,
        )
        embed.set_author(name=f"requsted by {ctx.author.name}", icon_url=ctx.author.avatar)
        embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url=ctx.guild.icon)
        view = View().add_item(HelpSelect(self.bot))
        donatebutton = discord.ui.Button(label=f"Donate to support hoshi development", url=f"https://www.paypal.me/lovinasbutera", emoji="<:payapl:1201895220065865798>")
        view.add_item(donatebutton)
        await ctx.reply(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))