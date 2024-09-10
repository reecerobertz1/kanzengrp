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
            "Lyra levels",
            "Chroma levels",
            "Moderation",
            "Miscellaneous",
            "Fun commands",
            "Editing Commands"
        ]
        descriptions = [
            "Commands for Lyra's levelling system",
            "Commands for Chroma's levelling system",
            "Moderation commands to help you with your server",
            "Miscellaneous commands",
            "Fun commands for you to play with",
            "Commands to help you with editing"
        ]
        emojis = [
            "<:cooky:1121909627156705280>",
            "<:rj:1121909526300479658>",
            "<:tata:1121909389280944169>",
            "<:chimmy2:1148234652448981072>",
            "<:shooky:1282841998373421139>",
            "<:mang:1121909428866793582>"
        ]
        dropdown = discord.ui.Select(
            placeholder="Select a category",
            options=[discord.SelectOption(label=category, description=description, emoji=emoji) for category, description, emoji in zip(categories, descriptions, emojis)]
        )

        welc = discord.Embed(title=f"HOME PAGE", description=f"**Categories:**\n\n<:cooky:1121909627156705280> **Lyra levels**\n<:Empty:1244752102807441540>・See the commands for gplyra's levels\n\n<:rj:1112498372511805501> **Chroma levels**\n<:Empty:1244752102807441540>・See the commands for chromagrp's levels\n\n<:tata:1282842043579760680> **Moderation**\n<:Empty:1244752102807441540>・See Hoshi's moderation commands\n\n<:chimmy:1282842084763762770> **Miscellaneous**\n<:Empty:1244752102807441540>・Misc commands for anyone to use\n\n<:shooky:1282841998373421139> **Fun commands**\n<:Empty:1244752102807441540>・Some fun commands to use with friends\n\n<:mang:1282842064781971546> **Editing commands**\n<:Empty:1244752102807441540>・Commands to help you with editing", color=0x2b2d31, url="https://instagram.com/chromagrp/")
        welc.set_thumbnail(url=self.bot.user.display_avatar.url)
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
                embed = discord.Embed(title=f"<:cooky:1121909627156705280> Lyra level Commands", description=f"</rank:1204816939382345790>\n<:Empty:1244752102807441540>・ Check your current rank\n</leaderboard:1204816939382345793>\n<:Empty:1244752102807441540>・ Check the servers leaderboard\n</add:1204816939382345791>\n<:Empty:1244752102807441540>・ Add xp to a member\n</remove:1204816939382345792>\n<:Empty:1244752102807441540>・ Remove xp from a member\n</reset:1204816939382345795>\n<:Empty:1244752102807441540>・ Reset everyone's levels for a server\n</rankbg:1205566036280082434>\n<:Empty:1244752102807441540>・ Change your rank cards background\n</rankcolor:1205565156155990136>\n<:Empty:1244752102807441540>・ Change your rank cards colour", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[1]:
                embed = discord.Embed(title=f"<:rj:1112498372511805501> Chroma level Commands", description=f"**+rank**\n<:Empty:1244752102807441540>・ Check your current rank\n**+leaderboard**\n<:Empty:1244752102807441540>・ Check the servers leaderboard\n**+add**\n<:Empty:1244752102807441540>・ Add xp to a member\n**+multiadd**\n<:Empty:1244752102807441540>・ Add xp to multiple members\n**+remove**\n<:Empty:1244752102807441540>・ Remove xp from a member\n**+reset**\n<:Empty:1244752102807441540>・ Reset everyone's levels for a server\n**+rankbg**\n<:Empty:1244752102807441540>・ Change your rank cards background\n**+rankcolor**\n<:Empty:1244752102807441540>・ Change your rank cards colour", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[2]:
                embed = discord.Embed(title=f"<:rj:1121909526300479658> Moderation Commands", description=f"</kick:1205908002087899210>\n<:Empty:1244752102807441540>・ Kick a member from the server\n</ban:1205908002087899211>\n<:Empty:1244752102807441540>・ Ban a member from the server\n</dm:1205908002087899212>\n<:Empty:1244752102807441540>・ Dm a member through {self.bot.user.name}\n</staffrep:1205908002629091338>\n<:Empty:1244752102807441540>・ Add staff rep", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[3]:
                embed = discord.Embed(title=f"<:tata:1121909389280944169> Miscellaneous Commands", description=f"</about:1206986179933773856>\n<:Empty:1244752102807441540>・ Gives information about Hoshi\n</serverinfo:1207298297266708481>\n<:Empty:1244752102807441540>・ Gives information about the server\n</afk:1194514645004849284>\n<:Empty:1244752102807441540>・ Go afk and set a reason", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[4]:
                embed = discord.Embed(title=f"<:chimmy2:1148234652448981072> Fun Commands", description=f"</howgay:1207323370878664707>\n<:Empty:1244752102807441540>・ How gay really are you?\n</jail:1207311199054725131>\n<:Empty:1244752102807441540>・ Put someone or yourself in jail\n</slap:1207323370878664704>\n<:Empty:1244752102807441540>・ Slap someone because they deserve it\n</kiss:1207323370878664705>\n<:Empty:1244752102807441540>・ Give someone a kiss\n</hug:1207323370878664706>\n<:Empty:1244752102807441540>・ Give someone a hug\n</8ball:1207314876716814399>\n<:Empty:1244752102807441540>・ Ask 8ball a question\n</ppsize:1207314876716814398>\n<:Empty:1244752102807441540>・ Who has the biggest pp?\n</ship:1207314876716814396>\n<:Empty:1244752102807441540>・ Ship to members together\n</tictactoe:1208096663311360041>\n<:Empty:1244752102807441540>・ Play a game of TicTacToe with a member\n</fight:1208096663311360040>\n<:Empty:1244752102807441540>・ Fight a member and beat them up\n**+countryvia**\n<:Empty:1244752102807441540>・ Play a game of country trivia, enter the amount of rounds (+countryvia 15)", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            elif selected_category == categories[5]:
                embed = discord.Embed(title=f"<:mang:1121909428866793582> Editing Commands", description=f"**+addcollab**\n<:Empty:1244752102807441540>・ Add collab audios to Hoshi\n**+addsoft**\n<:Empty:1244752102807441540>・ Add soft audios to Hoshi\n**+addhot**\n<:Empty:1244752102807441540>・ Add hot audios to Hoshi\n**+audio collab**\n<:Empty:1244752102807441540>・ Get collab audios added by members\n**+audio soft**\n<:Empty:1244752102807441540>・ Get soft audios added by members\n**+audio hot**\n<:Empty:1244752102807441540>・ Get hot audios added by members\n**+whotoedit**\n<:Empty:1244752102807441540>・ Don't know who to edit? use this command\n**+colorpalette**\n<:Empty:1244752102807441540>・ Get a randomly generated color palette from Hoshi", color=0x2b2d31)
                embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                embed.set_footer(text="• Use the dropdown menu to select a category", icon_url=self.bot.user.display_avatar.url)
            else:
                embed = discord.Embed(description="Sorry. There seems to be an issue with this category...")

            await interaction.response.edit_message(embed=embed, view=view)

        dropdown.callback = dropdown_callback

async def setup(bot):
    await bot.add_cog(Help(bot))