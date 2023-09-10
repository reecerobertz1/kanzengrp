from typing import Any
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import View, Select

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        categories = [
            "home page",
            "fun",
            "editing",
            "minigames",
            "kanzen only",
            "levels",
            "moderation",
            "applications",
            "community"
        ]
        emojis = [
            ":bt21:1149411052489027674",
            ":tata:1121909389280944169",
            ":shooky:1121909564799987722",
            ":rj:1121909526300479658",
            ":mang:1121909428866793582",
            ":koya:1121909483698925618",
            ":chimmy2:1148234652448981072",
            ":cooky:1121909627156705280",
            ":van:1148235344437846107"
        ]
        descriptions = [
            "Home page for the help command",
            "Includes commands you can use for fun!",
            "Editing commands that can help you edit",
            "Play some minigames with Hoshi",
            "Kanzengrp exclusive commands",
            "Commands for Hoshi levels",
            "Moderation commands for admins and staff",
            "Commands for our applications",
            "Community commands for Editors Block"
        ]
        dropdown = discord.ui.Select(
        placeholder="Select a category",
        options=[discord.SelectOption(label=category, emoji=emoji, description=description) for category, emoji, description in zip(categories, emojis, descriptions)]
        )

        about_hoshi_embed = discord.Embed(description="owner info:\n<a:Arrow_1:1145603161701224528> Hoshi is owned by [Reece](https://instagram.com/remqsi)\n<a:Arrow_1:1145603161701224528> Reece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)\n\ndevelopment info:\n<a:Arrow_1:1145603161701224528> Hoshi is coded in Python 3.11.4\n<a:Arrow_1:1145603161701224528> [Download Python 3.11.4](https://www.python.org/downloads/)\n<a:Arrow_1:1145603161701224528> Developed by [Reece](https://instagram.com/remqsi) with help from [Alex](https://instagram.com/rqinflow)\n\nextra info:\n<a:Arrow_1:1145603161701224528> Hoshi's prefix is `+`\n<a:Arrow_1:1145603161701224528> Hoshi was made for [**__Kanzengrp__**](https://instagram.com/kanzengrp)\n\nbug reports\n<a:Arrow_1:1145603161701224528> Use __+report__ to report bug reports!" ,color=0x2b2d31)
        about_hoshi_embed.set_thumbnail(url=ctx.guild.icon)
        about_hoshi_embed.set_author(name="About Hoshi", icon_url=self.bot.user.display_avatar.url)
        about_hoshi_embed.set_footer(text="Home Page", icon_url=ctx.author.avatar)

        view = discord.ui.View()
        view.add_item(dropdown)

        message = await ctx.send(embed=about_hoshi_embed, view=view)

        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            if selected_category == categories[0]:
                embed = discord.Embed(description="owner info:\n<a:Arrow_1:1145603161701224528> Hoshi is owned by [Reece](https://instagram.com/remqsi)\n<a:Arrow_1:1145603161701224528> Reece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)\n\ndevelopment info:\n<a:Arrow_1:1145603161701224528> Hoshi is coded in Python 3.11.4\n<a:Arrow_1:1145603161701224528> [Download Python 3.11.4](https://www.python.org/downloads/)\n<a:Arrow_1:1145603161701224528> Developed by [Reece](https://instagram.com/remqsi) with help from [Alex](https://instagram.com/rqinflow)\n\nextra info:\n<a:Arrow_1:1145603161701224528> Hoshi's prefix is `+`\n<a:Arrow_1:1145603161701224528> Hoshi was made for [**__Kanzengrp__**](https://instagram.com/kanzengrp)\n\nbug reports\n<a:Arrow_1:1145603161701224528> Use __+report__ to report bug reports!" ,color=0x2b2d31)
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_author(name="About Hoshi", icon_url=self.bot.user.display_avatar.url)
                embed.set_footer(text="Home Page", icon_url=ctx.author.avatar)
            elif selected_category == categories[1]:
                embed = discord.Embed(color=0x2b2d31)
                embed.set_author(name="fun commands", icon_url=self.bot.user.display_avatar.url)
                embed.add_field(name="+memberinfo", value="<a:Arrow_1:1145603161701224528> Shows member info", inline=False) 
                embed.add_field(name="+dog", value="<a:Arrow_1:1145603161701224528> Sends you a random photo of a dog", inline=False) 
                embed.add_field(name="+cat", value="<a:Arrow_1:1145603161701224528> Sends you a random photo of a cat", inline=False) 
                embed.add_field(name="+jail", value="<a:Arrow_1:1145603161701224528> Put someone or yourself in jail", inline=False) 
                embed.add_field(name="+kiss", value="<a:Arrow_1:1145603161701224528> Mention someone to kiss", inline=False)
                embed.add_field(name="+hug", value="<a:Arrow_1:1145603161701224528> Mention someone to hug", inline=False)
                embed.add_field(name="+slap", value="<a:Arrow_1:1145603161701224528> Mention someone to slap", inline=False)
                embed.add_field(name="+roast", value="<a:Arrow_1:1145603161701224528> Get a roast from Hoshi", inline=False)
                embed.add_field(name="+compliment", value="<a:Arrow_1:1145603161701224528> Get a compliment from Hoshi", inline=False)
                embed.add_field(name="+say", value="<a:Arrow_1:1145603161701224528> Make Hoshi say exactly what you say", inline=False)
                embed.add_field(name="+8ball", value="<a:Arrow_1:1145603161701224528> Ask Hoshi a question and get an answer", inline=False)
                embed.add_field(name="+ship", value="<a:Arrow_1:1145603161701224528> Mention 2 members to see if Hoshi ships them", inline=False)
                embed.add_field(name="+avatar", value="<a:Arrow_1:1145603161701224528> Get a photo of your avatar or someone elses", inline=False)
                embed.add_field(name="+giphy", value="<a:Arrow_1:1145603161701224528> Search for a gif with giphy", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="page 1/8", icon_url=ctx.author.avatar)
            elif selected_category == categories[2]:
                embed = discord.Embed(color=0x2b2d31)
                embed.set_author(name="editing commands", icon_url=self.bot.user.display_avatar.url)
                embed.add_field(name="+transition", value="<a:Arrow_1:1145603161701224528> Get a random transition to use in your edit", inline=False)
                embed.add_field(name="+audio soft", value="<a:Arrow_1:1145603161701224528> Get a soft audio added by a member to use for your edit", inline=False)
                embed.add_field(name="+addsoft", value="<a:Arrow_1:1145603161701224528> Add a soft audio from SoundCloud for others to use", inline=False)
                embed.add_field(name="+audio hot", value="<a:Arrow_1:1145603161701224528> Get a hot audio added by a member to use for your edit", inline=False)
                embed.add_field(name="+addhot", value="<a:Arrow_1:1145603161701224528> Add a hot audio from SoundCloud for others to use", inline=False)
                embed.add_field(name="+addedit", value="<a:Arrow_1:1145603161701224528> Add your own edit to Hoshi (must be a streamable link)", inline=False)
                embed.add_field(name="+edits", value="<a:Arrow_1:1145603161701224528> Watch edits added from members of Aura and Kanzen", inline=False)
                embed.add_field(name="+effects ae", value="<a:Arrow_1:1145603161701224528> Get a random effect for After Effects to use in your edit", inline=False)
                embed.add_field(name="+effects vs", value="<a:Arrow_1:1145603161701224528> Get a random effect for Videostar to use in your edit", inline=False)
                embed.add_field(name="+colorscheme", value="<a:Arrow_1:1145603161701224528> Get a random color scheme to use in your edit", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="page 2/8", icon_url=ctx.author.avatar)
            elif selected_category == categories[3]:
                embed = discord.Embed(color=0x2b2d31)
                embed.set_author(name="minigames", icon_url=self.bot.user.display_avatar.url)
                embed.add_field(name="+scramble", value="<a:Arrow_1:1145603161701224528> Unscramble the word Hoshi gives you in 20 seconds", inline=False)
                embed.add_field(name="+trivia", value="<a:Arrow_1:1145603161701224528> Hoshi will ask you a question, make sure to answer correctly", inline=False)
                embed.add_field(name="+tictactoe", value="<a:Arrow_1:1145603161701224528> Play a game of tictactoe with the person you mention", inline=False)
                embed.add_field(name="+hangman", value="<a:Arrow_1:1145603161701224528> Play a game of hangman with Hoshi!", inline=False)
                embed.add_field(name="+trueorfalse", value="<a:Arrow_1:1145603161701224528> Play a game of True or False", inline=False)
                embed.add_field(name="+guesstheceleb", value="<a:Arrow_1:1145603161701224528> Play a game of Game the celeb/idol", inline=False)
                embed.add_field(name="+rps", value="<a:Arrow_1:1145603161701224528> Play a game of Rock Paper Scissors with Hoshi", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="page 3/8", icon_url=ctx.author.avatar)
            elif selected_category == categories[4]:
                embed = discord.Embed(color=0x2b2d31)
                embed.set_author(name="kanzen only commands", icon_url=self.bot.user.display_avatar.url)
                embed.add_field(name="+cmd new", value="<a:Arrow_1:1145603161701224528> Make your own command!", inline=False)
                embed.add_field(name="+cmd list", value="<a:Arrow_1:1145603161701224528> See all the commands other zennies have added", inline=False)
                embed.add_field(name="+cmd remove", value="<a:Arrow_1:1145603161701224528> Made a mistake in your command? do", inline=False)
                embed.add_field(name="+daily", value="<a:Arrow_1:1145603161701224528> Get anywhere from 100xp - 300xp everyday!", inline=False)
                embed.add_field(name="+pets", value="<a:Arrow_1:1145603161701224528> See other zennies pets!", inline=False)
                embed.add_field(name="+addpet", value="<a:Arrow_1:1145603161701224528> Attach an image of your pet and add a name when doing this command", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="page 4/8", icon_url=ctx.author.avatar)
            elif selected_category == categories[5]:
                embed = discord.Embed(color=0x2b2d31)
                embed.set_author(name="level commands", icon_url=self.bot.user.display_avatar.url)
                embed.add_field(name="+rank", value="<a:Arrow_1:1145603161701224528> See your rank, or someone elses", inline=False)
                embed.add_field(name="+levels", value="<a:Arrow_1:1145603161701224528> See the level leaderboard for the server", inline=False)
                embed.add_field(name="+rankcolor", value="<a:Arrow_1:1145603161701224528> Set your rank color with a hex code", inline=False)
                embed.add_field(name="+rankbg", value="<a:Arrow_1:1145603161701224528> Attach an image to set your rank background", inline=False)
                embed.add_field(name="+xp add", value="<a:Arrow_1:1145603161701224528> Add xp to a member", inline=False)
                embed.add_field(name="+xp remove", value="<a:Arrow_1:1145603161701224528> Remove xp from a member", inline=False)
                embed.add_field(name="+xp reset", value="<a:Arrow_1:1145603161701224528> Resets xp for everyone", inline=False)
                embed.add_field(name="+levelling on", value="<a:Arrow_1:1145603161701224528> Enables the levelling system for the server", inline=False)
                embed.add_field(name="+levelling off", value="<a:Arrow_1:1145603161701224528> Disables the levelling system for the server", inline=False)
                embed.add_field(name="+levelling setrole", value="<a:Arrow_1:1145603161701224528> Set the top 20 active role", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="page 5/8", icon_url=ctx.author.avatar)
            elif selected_category == categories[6]:
                embed = discord.Embed(color=0x2b2d31)
                embed.set_author(name="moderation commands", icon_url=self.bot.user.display_avatar.url)
                embed.add_field(name="</kick:1131780353477054484>", value="<a:Arrow_1:1145603161701224528> Kick a member from the server", inline=False)
                embed.add_field(name="</ban:1131780353477054485>", value="<a:Arrow_1:1145603161701224528> Ban a member from the server", inline=False)
                embed.add_field(name="</addrole:1131784754698666035>", value="<a:Arrow_1:1145603161701224528> Add a role to a member", inline=False)
                embed.add_field(name="</removerole:1131784754698666036>", value="<a:Arrow_1:1145603161701224528> Remove a role from a member", inline=False)
                embed.add_field(name="+buildembed", value="<a:Arrow_1:1145603161701224528> Create an embed", inline=False)
                embed.add_field(name="+warn", value="<a:Arrow_1:1145603161701224528> Give a warning to a member in [editors block](https://discord.gg/yuqXebz8vr)", inline=False)
                embed.add_field(name="+steal", value="<a:Arrow_1:1145603161701224528> Steal an emoji from any server", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="page 6/8", icon_url=ctx.author.avatar)
            elif selected_category == categories[7]:
                embed = discord.Embed(color=0x2b2d31)
                embed.set_author(name="application commands", icon_url=self.bot.user.display_avatar.url)
                embed.add_field(name="+daegu openapps", value="<a:Arrow_1:1145603161701224528> Opens applications for daegutowngrp", inline=False)
                embed.add_field(name="+daegu closeapps", value="<a:Arrow_1:1145603161701224528> Closes applications for daegutowngrp", inline=False)
                embed.add_field(name="+aura openapp", value="<a:Arrow_1:1145603161701224528> Opens applications for auragrps", inline=False)
                embed.add_field(name="+aura closeapp", value="<a:Arrow_1:1145603161701224528> Closes applications for auragrps", inline=False)
                embed.add_field(name="+kanzen appsopen", value="<a:Arrow_1:1145603161701224528> Opens applications for kanzengrp", inline=False)
                embed.add_field(name="+kanzen appsclose", value="<a:Arrow_1:1145603161701224528> Closes applications for kanzengrp", inline=False)
                embed.add_field(name="+accept", value="<a:Arrow_1:1145603161701224528> Accepts member into kanzen", inline=False)
                embed.add_field(name="+decline", value="<a:Arrow_1:1145603161701224528> Declines a member from kanzen", inline=False)
                embed.add_field(name="+answer", value="<a:Arrow_1:1145603161701224528> Answer a question sent", inline=False)
                embed.add_field(name="+answerpriv", value="<a:Arrow_1:1145603161701224528> Answer a question sent in DMs", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="page 7/8", icon_url=ctx.author.avatar)
            elif selected_category == categories[8]:
                embed = discord.Embed(color=0x2b2d31)
                embed.set_author(name="community commands", icon_url=self.bot.user.display_avatar.url)
                embed.add_field(name="+giveaway", value="<a:Arrow_1:1145603161701224528> Start a giveaway", inline=False)
                embed.add_field(name="+enter banner", value="<a:Arrow_1:1145603161701224528> Enter in Editors block banner contest", inline=False)
                embed.add_field(name="+enter icon", value="<a:Arrow_1:1145603161701224528> Enter in Editors block icon contest", inline=False)
                embed.add_field(name="+contest close", value="<a:Arrow_1:1145603161701224528> Closes the banner / icon contest", inline=False)
                embed.add_field(name="+contest open", value="<a:Arrow_1:1145603161701224528> Opens the banner / icon contest", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
                embed.set_footer(text="page 8/8", icon_url=ctx.author.avatar)
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")

            await interaction.response.edit_message(embed=embed)
        dropdown.callback = dropdown_callback

async def setup(bot):
    await bot.add_cog(Help(bot))