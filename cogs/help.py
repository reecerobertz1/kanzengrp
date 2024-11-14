from discord.ext import commands
import discord
from discord.ui import View, Select
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True

    @app_commands.command(name="help", description="Help with Hoshi commands")
    async def help(self, interaction: discord.Interaction):
        categories = [
            "Levels",
            "Moderation",
            "Fun"
        ]
        descriptions = [
            "Commands for the levelling system",
            "Moderation commands to help you with your server",
            "Fun commands for you to use"
        ]
        dropdown = discord.ui.Select(
            placeholder="Select a category",
            options=[discord.SelectOption(label=category, description=description) for category, description in zip(categories, descriptions)]
        )

        welc = discord.Embed(title=f"{self.bot.user.name}'s commands", description="Hoshi Info:\n> Hoshi was made by [remqsi](https://instagram.com/remqsi/)\n> Hoshi is coded in [Visual Studio Code](https://code.visualstudio.com/)\n> Hoshi is coded in Python 3.11.4\n\nExtra Info:\n> Hoshi is made for all types of editing grps\n> Join [Hoshi's server](https://instagram.com/remqsi/) for more help\n> Do /report to report any bugs you find!", color=0x2b2d31)
        welc.set_thumbnail(url=self.bot.user.display_avatar.url)
        welc.set_author(name=f"requsted by {interaction.user.name}", icon_url=interaction.user.avatar)
        welc.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
        view = discord.ui.View()
        view.add_item(dropdown)
        message = await interaction.response.send_message(embed=welc, view=view)

        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            for item in view.children:
                if not isinstance(item, discord.ui.Select):
                    view.remove_item(item)

            if selected_category == categories[0]:
                embed = discord.Embed(title="Level Commands", description=f"**/rank**\n<:1166196258499727480:1188190249768210582> Check your current rank\n**/leaderboard**\n<:1166196258499727480:1188190249768210582> Check the servers leaderboard\n**/add**\n<:1166196258499727480:1188190249768210582> Add xp to a member\n**/remove**\n<:1166196258499727480:1188190249768210582> Remove xp from a member\n**/reset**\n<:1166196258499727480:1188190249768210582>Reset everyone's levels for a server", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[1]:
                embed = discord.Embed(title="Moderation Commands", description=f"</kick:1202616237537103962>\n<:1166196258499727480:1188190249768210582> Kick a member from the server\n</ban:1202618584908439572>\n<:1166196258499727480:1188190249768210582> Ban a member from the server\n</dm:1202619823155191869>\n<:1166196258499727480:1188190249768210582> Dm a member through Hoshi\n</addrole:1202626668548722751>\n<:1166196258499727480:1188190249768210582> Add a role to a member\n</removerole:1202626668548722752>\n<:1166196258499727480:1188190249768210582> Remove a role from a member", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[2]:
                embed = discord.Embed(title="Fun Commands", description=f"</hug:1202707363530940487>\n<:1166196258499727480:1188190249768210582> Hug a member\n</kiss:1202707363530940486>\n<:1166196258499727480:1188190249768210582> Kiss a member\n</slap:1202702254268743681>\n<:1166196258499727480:1188190249768210582> Slap a member\n</jail:1203759833493540925>\n<:1166196258499727480:1188190249768210582> Put someone in jail", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")

            await interaction.response.edit_message(embed=embed, view=view)

        dropdown.callback = dropdown_callback

async def setup(bot):
    await bot.add_cog(Help(bot))