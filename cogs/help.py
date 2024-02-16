from discord.ext import commands
import discord
from discord.ui import View, Select
from discord import app_commands

class animalsell(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=30.0)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="<")
    async def turkey(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=f"<:shooky:1121909564799987722> Economy Commands", description=f"**+balance**\n<:1166196258499727480:1188190249768210582> Check your bank and wallet balance\n**+donate**\n<:1166196258499727480:1188190249768210582> Donate to ~~the poor~~ other members\n**+beg**\n<:1166196258499727480:1188190249768210582> Beg celebs for coins\n**+search**\n<:1166196258499727480:1188190249768210582> Search locations for coins\n**+crime**\n<:1166196258499727480:1188190249768210582> Commit a crime for coins\n**+wealth**\n<:1166196258499727480:1188190249768210582> See the richest kanzen members\n**+rob**\n<:1166196258499727480:1188190249768210582> Steal coins from other members\n**+shop**\n<:1166196258499727480:1188190249768210582> Check the shop and buy items\n**+sell**\n<:1166196258499727480:1188190249768210582> Sell your useless/unwanted items\n**+inventory**\n<:1166196258499727480:1188190249768210582> See what items you have", color=0x2b2d31)
        embed.set_footer(text="• Page 1/2", icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label=">")
    async def rabbit(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title=f"<:shooky:1121909564799987722> Economy Commands", description=f"**+jobs**\n<:1166196258499727480:1188190249768210582> See what jobs are avaliable\n**+work**\n<:1166196258499727480:1188190249768210582> Work a shift and earn coins\n**+gamble**\n<:1166196258499727480:1188190249768210582> Gamble your life savings\n**+hunt**\n<:1166196258499727480:1188190249768210582> Go hunting for animals and sell them for profit\n**+fish**\n<:1166196258499727480:1188190249768210582> Go fishing for fish and sell them for profit\n**+mine**\n<:1166196258499727480:1188190249768210582> Go mining for min and sell them for profit\n**+lotto**\n<:1166196258499727480:1188190249768210582> Use a lottery ticket and see if it is a winner", color=0x2b2d31)
        embed.set_footer(text="• Page 2/2", icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await interaction.response.edit_message(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True

    @app_commands.command(name="help", description="Help with Hoshi commands")
    async def help(self, interaction: discord.Interaction):
        categories = [
            "Levels",
            "Moderation",
            "Miscellaneous",
            "Fun commands",
            "Editing Commands",
            "Economy Commands"
        ]
        descriptions = [
            "Commands for the levelling system",
            "Moderation commands to help you with your server",
            "Miscellaneous commands",
            "Fun commands for you to play with",
            "Commands to help you with editing",
            "Commands for the economy system"
        ]
        emojis = [
            "<:cooky:1121909627156705280>",
            "<:rj:1121909526300479658>",
            "<:tata:1121909389280944169>",
            "<:chimmy2:1148234652448981072>",
            "<:mang:1121909428866793582>",
            "<:shooky:1121909564799987722>"
        ]
        animal_sell_view = animalsell(bot=self.bot)
        dropdown = discord.ui.Select(
            placeholder="Select a category",
            options=[discord.SelectOption(label=category, description=description, emoji=emoji) for category, description, emoji in zip(categories, descriptions, emojis)]
        )

        welc = discord.Embed(title=f"HOME PAGE", description=f"owner info:\n> Hoshi is owned by [@remqsi](https://instagram.com/remqsi)\n> Reece coded Hoshi [Visual Studio Code](https://code.visualstudio.com/)\n\ndevelopment info:\n> Hoshi is coded in Python 3.11.4\n> Developed by [Reece](https://instagram.com/remqsi) \n> [Alex](https://instagram.com/rqinflow) + [Josh](https://instagram.com/xiaosaeq) helped with development\n\nextra info:\n> Hoshi was made for [@kanzengrp](https://instagram.com/kanzengrp)\n> Do </report:1207661290831618048> to report bugs \n> Do </request:1207660914824708106> to suggest commands", color=0x2b2d31, url="https://instagram.com/kanzengrp/")
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
                embed = discord.Embed(title=f"<:cooky:1121909627156705280> Level Commands", description=f"</rank:1204816939382345790>\n<:1166196258499727480:1188190249768210582> Check your current rank\n</leaderboard:1204816939382345793>\n<:1166196258499727480:1188190249768210582> Check the servers leaderboard\n</add:1204816939382345791>\n<:1166196258499727480:1188190249768210582> Add xp to a member\n</remove:1204816939382345792>\n<:1166196258499727480:1188190249768210582> Remove xp from a member\n</reset:1204816939382345795>\n<:1166196258499727480:1188190249768210582> Reset everyone's levels for a server\n</rankbg:1205566036280082434>\n<:1166196258499727480:1188190249768210582> Change your rank cards background\n</rankcolor:1205565156155990136>\n<:1166196258499727480:1188190249768210582> Change your rank cards colour", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[1]:
                embed = discord.Embed(title=f"<:rj:1121909526300479658> Moderation Commands", description=f"</kick:1205908002087899210>\n<:1166196258499727480:1188190249768210582> Kick a member from the server\n</ban:1205908002087899211>\n<:1166196258499727480:1188190249768210582> Ban a member from the server\n</dm:1205908002087899212>\n<:1166196258499727480:1188190249768210582> Dm a member through {self.bot.user.name}\n</staffrep:1205908002629091338>\n<:1166196258499727480:1188190249768210582> Add staff rep", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[2]:
                embed = discord.Embed(title=f"<:tata:1121909389280944169> Miscellaneous Commands", description=f"</about:1206986179933773856>\n<:1166196258499727480:1188190249768210582> Gives information about Hoshi\n</serverinfo:1207298297266708481>\n<:1166196258499727480:1188190249768210582> Gives information about the server\n</afk:1194514645004849284>\n<:1166196258499727480:1188190249768210582> Go afk and set a reason", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[3]:
                embed = discord.Embed(title=f"<:chimmy2:1148234652448981072> Fun Commands", description=f"</howgay:1207323370878664707>\n<:1166196258499727480:1188190249768210582> How gay really are you?\n</jail:1207311199054725131>\n<:1166196258499727480:1188190249768210582> Put someone or yourself in jail\n</slap:1207323370878664704>\n<:1166196258499727480:1188190249768210582> Slap someone because they deserve it\n</kiss:1207323370878664705>\n<:1166196258499727480:1188190249768210582> Give someone a kiss\n</hug:1207323370878664706>\n<:1166196258499727480:1188190249768210582> Give someone a hug\n</8ball:1207314876716814399>\n<:1166196258499727480:1188190249768210582> Ask 8ball a question\n</ppsize:1207314876716814398>\n<:1166196258499727480:1188190249768210582> Who has the biggest pp?\n</ship:1207314876716814396>\n<:1166196258499727480:1188190249768210582> Ship to members together\n</tictactoe:1208096663311360041>\n<:1166196258499727480:1188190249768210582> Play a game of TicTacToe with a member\n</fight:1208096663311360040>\n<:1166196258499727480:1188190249768210582> Fight a member and beat them up", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[4]:
                embed = discord.Embed(title=f"<:mang:1121909428866793582> Editing Commands", description=f"</addcollab:1208106805159399464>\n<:1166196258499727480:1188190249768210582> Add collab audios to Hoshi\n</addsoft:1208106804676923392>\n<:1166196258499727480:1188190249768210582> Add soft audios to Hoshi\n</addhot:1208106804676923394>\n<:1166196258499727480:1188190249768210582> Add hot audios to Hoshi\n</addedit:1208106804123541527>\n<:1166196258499727480:1188190249768210582> Add your edits to Hoshi\n</collab:1208106806241660929>\n<:1166196258499727480:1188190249768210582> Get collab audios added by zennies\n</soft:1208106805159399465>\n<:1166196258499727480:1188190249768210582> Get soft audios added by zennies\n</hot:1208106806241660928>\n<:1166196258499727480:1188190249768210582> Get hot audios added by zennies\n</edits:1208106804123541528>\n<:1166196258499727480:1188190249768210582> Watch edits added by other zennies\n</whotoedit:1208106804123541524>\n<:1166196258499727480:1188190249768210582> Don't know who to edit? use this command\n</colorpalette:1208106804123541526>\n<:1166196258499727480:1188190249768210582> Get a randomly generated color palette from Hoshi", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[5]:
                for item in animal_sell_view.children:
                    view.add_item(item)
                embed = discord.Embed(title=f"<:shooky:1121909564799987722> Economy Commands", description=f"**+balance**\n<:1166196258499727480:1188190249768210582> Check your bank and wallet balance\n**+donate**\n<:1166196258499727480:1188190249768210582> Donate to ~~the poor~~ other members\n**+beg**\n<:1166196258499727480:1188190249768210582> Beg celebs for coins\n**+search**\n<:1166196258499727480:1188190249768210582> Search locations for coins\n**+crime**\n<:1166196258499727480:1188190249768210582> Commit a crime for coins\n**+wealth**\n<:1166196258499727480:1188190249768210582> See the richest kanzen members\n**+rob**\n<:1166196258499727480:1188190249768210582> Steal coins from other members\n**+shop**\n<:1166196258499727480:1188190249768210582> Check the shop and buy items\n**+sell**\n<:1166196258499727480:1188190249768210582> Sell your useless/unwanted items\n**+inventory**\n<:1166196258499727480:1188190249768210582> See what items you have", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Page 1/2", icon_url=self.bot.user.display_avatar.url)
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")

            await interaction.response.edit_message(embed=embed, view=view)

        dropdown.callback = dropdown_callback

async def setup(bot):
    await bot.add_cog(Help(bot))