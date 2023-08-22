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
            "fun",
            "editing",
            "other",
            "minigames",
            "kanzen only",
            "levels",
            "moderation",
            "applications",
            "community"
        ]
        dropdown = discord.ui.Select(placeholder="Select a category", options=[discord.SelectOption(label=category) for category in categories])

        about_hoshi_embed = discord.Embed(title="About Hoshi",description="owner info:\n<a:bounceyarrow:1128155233437106187> Hoshi is owned by [reece](https://instagram.com/remqsi)\n<a:bounceyarrow:1128155233437106187> Reece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)\n\ncoding info:\n<a:bounceyarrow:1128155233437106187> Hoshi is coded in Python 3.11.4\n<a:bounceyarrow:1128155233437106187> [Download Python 3.11.4](https://www.python.org/downloads/)\n<a:bounceyarrow:1128155233437106187> Developed by [reece](https://instagram.com/remqsi) with help from [alex](https://instagram.com/rqinflow)\n\nextra info:\n<a:bounceyarrow:1128155233437106187> Hoshi's prefix is `+`\n<a:bounceyarrow:1128155233437106187> Hoshi was made for [**__Kanzengrp__**](https://instagram.com/kanzengrp)" ,color=0x2b2d31)
        about_hoshi_embed.set_thumbnail(url=ctx.guild.icon)

        view = discord.ui.View()
        view.add_item(dropdown)

        message = await ctx.send(embed=about_hoshi_embed, view=view)

        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            if selected_category == categories[0]:
                embed = discord.Embed(title="fun commands", color=0x2b2d31)
                embed.add_field(name="+dog", value="<a:bounceyarrow:1128155233437106187> Sends you a random photo of a dog", inline=False) 
                embed.add_field(name="+cat", value="<a:bounceyarrow:1128155233437106187> Sends you a random photo of a cat", inline=False) 
                embed.add_field(name="+jail", value="<a:bounceyarrow:1128155233437106187> Put someone or yourself in jail", inline=False) 
                embed.add_field(name="+memberinfo", value="<a:bounceyarrow:1128155233437106187> View info for yourself or others", inline=False) 
                embed.add_field(name="+kiss", value="<a:bounceyarrow:1128155233437106187> Mention someone to kiss, or don't mention anyone for Hoshi to kiss you", inline=False)
                embed.add_field(name="+hug", value="<a:bounceyarrow:1128155233437106187> Mention someone to hug, or don't mention anyone for Hoshi to hug you", inline=False)
                embed.add_field(name="+slap", value="<a:bounceyarrow:1128155233437106187> Mention someone to slap, or don't mention anyone for Hoshi to slap you", inline=False)
                embed.add_field(name="+roast", value="<a:bounceyarrow:1128155233437106187> Get a roast from Hoshi", inline=False)
                embed.add_field(name="+compliment", value="<a:bounceyarrow:1128155233437106187> Get a compliment from Hoshi", inline=False)
                embed.add_field(name="+say", value="<a:bounceyarrow:1128155233437106187> Make Hoshi say exactly what you say", inline=False)
                embed.add_field(name="+8ball", value="<a:bounceyarrow:1128155233437106187> Ask Hoshi a question and get an answer", inline=False)
                embed.add_field(name="+ship", value="<a:bounceyarrow:1128155233437106187> Mention 2 members to see if Hoshi ships them (+ship @mention @mention)", inline=False)
                embed.add_field(name="+avatar", value="<a:bounceyarrow:1128155233437106187> Get a photo of your avatar or someone elses", inline=False)
                embed.add_field(name="+giphy", value="<a:bounceyarrow:1128155233437106187> Search for a gif with giphy", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[1]:
                embed = discord.Embed(title="editing commands", color=0x2b2d31)
                embed.add_field(name="+transition", value="<a:bounceyarrow:1128155233437106187> Get a random transition to use in your edit", inline=False)
                embed.add_field(name="+audio soft", value="<a:bounceyarrow:1128155233437106187> Get a soft audio added by a member to use for your edit", inline=False)
                embed.add_field(name="+addsoft", value="<a:bounceyarrow:1128155233437106187> Add a soft audio from SoundCloud for others to use", inline=False)
                embed.add_field(name="+audio hot", value="<a:bounceyarrow:1128155233437106187> Get a hot audio added by a member to use for your edit", inline=False)
                embed.add_field(name="+addhot", value="<a:bounceyarrow:1128155233437106187> Add a hot audio from SoundCloud for others to use", inline=False)
                embed.add_field(name="+addedit", value="<a:bounceyarrow:1128155233437106187> Add your own edit to Hoshi (must be a streamable link)", inline=False)
                embed.add_field(name="+edits", value="<a:bounceyarrow:1128155233437106187> Watch edits added from members of, Aura, Kanzen and Daegu", inline=False)
                embed.add_field(name="+effects", value="<a:bounceyarrow:1128155233437106187> Get a random effect to use in your edit", inline=False)
                embed.add_field(name="+colorscheme", value="<a:bounceyarrow:1128155233437106187> Get a random color scheme to use in your edit", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[2]:
                embed = discord.Embed(title="other commands", color=0x2b2d31)
                embed.add_field(name="+ia", value="<a:bounceyarrow:1128155233437106187> Send us an inactivity message if you go inactive", inline=False)
                embed.add_field(name="</ia:1130538786854539336>", value="<a:bounceyarrow:1128155233437106187> Send us an inactivity message if you go inactive (kanzengrp only)", inline=False)
                embed.add_field(name="+suggest", value="<a:bounceyarrow:1128155233437106187> Suggest what we can do in the group (+suggest [suggestion])", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[3]:
                embed = discord.Embed(title="minigames", color=0x2b2d31)
                embed.add_field(name="+scramble", value="<a:bounceyarrow:1128155233437106187> Unscramble the word Hoshi gives you in 20 seconds", inline=False)
                embed.add_field(name="+trivia", value="<a:bounceyarrow:1128155233437106187> Hoshi will ask you a question, make sure to answer correctly (answer with numbers 1-4)", inline=False)
                embed.add_field(name="+tictactoe", value="<a:bounceyarrow:1128155233437106187> Play a game of tictactoe with the person you mention", inline=False)
                embed.add_field(name="+hangman", value="<a:bounceyarrow:1128155233437106187> Play a game of hangman with Hoshi!", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[4]:
                embed = discord.Embed(title="kanzen only commands", color=0x2b2d31)
                embed.add_field(name="+cmd new", value="<a:bounceyarrow:1128155233437106187> Make your own command! `+cmd new (command name) (hoshi's responce)`", inline=False)
                embed.add_field(name="+cmd list", value="<a:bounceyarrow:1128155233437106187> See all the commands other zennies have added", inline=False)
                embed.add_field(name="+cmd remove", value="<a:bounceyarrow:1128155233437106187> Made a mistake in your command? do `+cmd remove (+commandname)`", inline=False)
                embed.add_field(name="+daily", value="<a:bounceyarrow:1128155233437106187> Get anywhere from 100xp - 300xp everyday! (server boosters only wait 12 hours)", inline=False)
                embed.add_field(name="+pets", value="<a:bounceyarrow:1128155233437106187> See other zennies pets!", inline=False)
                embed.add_field(name="+addpet", value="<a:bounceyarrow:1128155233437106187> Attach an image of your pet and add a name when doing this command", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[5]:
                embed = discord.Embed(title="levels commands", color=0x2b2d31)
                embed.add_field(name="+rank", value="<a:bounceyarrow:1128155233437106187> See your rank, or someone elses", inline=False)
                embed.add_field(name="+levels", value="<a:bounceyarrow:1128155233437106187> See the level leaderboard for the server", inline=False)
                embed.add_field(name="+rankcolor", value="<a:bounceyarrow:1128155233437106187> Set your rank color with a hex code", inline=False)
                embed.add_field(name="+xp add", value="<a:bounceyarrow:1128155233437106187> Add xp to a member (admin only command)", inline=False)
                embed.add_field(name="+xp remove", value="<a:bounceyarrow:1128155233437106187> Remove xp from a member (admin only command)", inline=False)
                embed.add_field(name="+xp reset", value="<a:bounceyarrow:1128155233437106187> Resets xp for everyone (admin only)", inline=False)
                embed.add_field(name="+levelling on", value="<a:bounceyarrow:1128155233437106187> Enables the levelling system for the server (admin only)", inline=False)
                embed.add_field(name="+levelling off", value="<a:bounceyarrow:1128155233437106187> Disables the levelling system for the server (admin only)", inline=False)
                embed.add_field(name="+levelling setrole", value="<a:bounceyarrow:1128155233437106187> Set the top 20 active role", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[6]:
                embed = discord.Embed(title="moderation commands", color=0x2b2d31)
                embed.add_field(name="</kick:1131780353477054484>", value="<a:bounceyarrow:1128155233437106187> Kick a member from the server", inline=False)
                embed.add_field(name="</ban:1131780353477054485>", value="<a:bounceyarrow:1128155233437106187> Ban a member from the server", inline=False)
                embed.add_field(name="</addrole:1131784754698666035>", value="<a:bounceyarrow:1128155233437106187> Add a role to a member (+addrole @role @mention)", inline=False)
                embed.add_field(name="</removerole:1131784754698666036>", value="<a:bounceyarrow:1128155233437106187> Remove a role from a member (+removerole @role @mention)", inline=False)
                embed.add_field(name="+buildembed", value="<a:bounceyarrow:1128155233437106187> Create an embed", inline=False)
                embed.add_field(name="+warn", value="<a:bounceyarrow:1128155233437106187> Give a warning to a member in [editors block](https://discord.gg/yuqXebz8vr)", inline=False)
                embed.add_field(name="+steal", value="<a:bounceyarrow:1128155233437106187> Steal an emoji from any server", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[7]:
                embed = discord.Embed(title="application commands", color=0x2b2d31)
                embed.add_field(name="+daegu openapps", value="<a:bounceyarrow:1128155233437106187> Opens applications for daegutowngrp", inline=False)
                embed.add_field(name="+daegu closeapps", value="<a:bounceyarrow:1128155233437106187> Closes applications for daegutowngrp", inline=False)
                embed.add_field(name="+aura openapp", value="<a:bounceyarrow:1128155233437106187> Opens applications for auragrps", inline=False)
                embed.add_field(name="+aura closeapp", value="<a:bounceyarrow:1128155233437106187> Closes applications for auragrps", inline=False)
                embed.add_field(name="+kanzen appsopen", value="<a:bounceyarrow:1128155233437106187> Opens applications for kanzengrp", inline=False)
                embed.add_field(name="+kanzen appsclose", value="<a:bounceyarrow:1128155233437106187> Closes applications for kanzengrp", inline=False)
                embed.add_field(name="+accept", value="<a:bounceyarrow:1128155233437106187> Accepts member into kanzen", inline=False)
                embed.add_field(name="+decline", value="<a:bounceyarrow:1128155233437106187> Declines a member from kanzen", inline=False)
                embed.add_field(name="+answer", value="<a:bounceyarrow:1128155233437106187> Answer a question sent", inline=False)
                embed.add_field(name="+answerpriv", value="<a:bounceyarrow:1128155233437106187> Answer a question sent in DMs", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[8]:
                embed = discord.Embed(title="community commands", color=0x2b2d31)
                embed.add_field(name="+giveaway", value="<a:bounceyarrow:1128155233437106187> Start a giveaway", inline=False)
                embed.add_field(name="+enter banner", value="<a:bounceyarrow:1128155233437106187> Enter in Editors block banner contest", inline=False)
                embed.add_field(name="+enter icon", value="<a:bounceyarrow:1128155233437106187> Enter in Editors block icon contest", inline=False)
                embed.add_field(name="+contest close", value="<a:bounceyarrow:1128155233437106187> Closes the banner / icon contest", inline=False)
                embed.add_field(name="+contest open", value="<a:bounceyarrow:1128155233437106187> Opens the banner / icon contest", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")

            await interaction.response.edit_message(embed=embed)
        dropdown.callback = dropdown_callback

async def setup(bot):
    await bot.add_cog(Help(bot))