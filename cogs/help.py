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
        # Create the dropdown menu with different categories
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

        # Create the initial "About Hoshi" embed with fields
        about_hoshi_embed = discord.Embed(title="About Hoshi",description="owner info:\n<a:bounceyarrow:1132507393050296331> Hoshi is owned by [reece](https://instagram.com/remqsi)\n<a:bounceyarrow:1132507393050296331> Reece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)\n\ncoding info:\n<a:bounceyarrow:1132507393050296331> Hoshi is coded in Python 3.11.4\n<a:bounceyarrow:1132507393050296331> [Download Python 3.11.4](https://www.python.org/downloads/)\n<a:bounceyarrow:1132507393050296331> Developed by [reece](https://instagram.com/remqsi) with help from [alex](https://instagram.com/rqinflow)\n\nextra info:\n<a:bounceyarrow:1132507393050296331> Hoshi's prefix is `+`\n<a:bounceyarrow:1132507393050296331> Hoshi was made for [**__Kanzengrp__**](https://instagram.com/kanzengrp)" ,color=0x2b2d31)
        about_hoshi_embed.set_thumbnail(url=ctx.guild.icon)

        # Create a view to handle the interaction
        view = discord.ui.View()
        view.add_item(dropdown)

        # Send the initial "About Hoshi" embed with the dropdown menu
        message = await ctx.send(embed=about_hoshi_embed, view=view)

        # Function to handle the dropdown selection
        async def dropdown_callback(interaction: discord.Interaction):
            selected_category = interaction.data["values"][0]
            if selected_category == categories[0]:
                embed = discord.Embed(title="> Fun commands", color=0x2b2d31)
                embed.add_field(name="+dog", value="<:reply:1125269313432059904> Sends you a random photo of a dog", inline=False) # ✅
                embed.add_field(name="+cat", value="<:reply:1125269313432059904> Sends you a random photo of a cat", inline=False) # ✅
                embed.add_field(name="+jail", value="<:reply:1125269313432059904> Put someone or yourself in jail", inline=False) # ✅
                embed.add_field(name="+pride", value="<:reply:1125269313432059904> Puts the pride flag on someones avatar", inline=False) # ✅
                embed.add_field(name="+memberinfo", value="<:reply:1125269313432059904> View info for yourself or others", inline=False) # ✅
                embed.add_field(name="+kiss", value="<:reply:1125269313432059904> Mention someone to kiss, or don't mention anyone for Hoshi to kiss you", inline=False)# ✅
                embed.add_field(name="+hug", value="<:reply:1125269313432059904> Mention someone to hug, or don't mention anyone for Hoshi to hug you", inline=False)# ✅
                embed.add_field(name="+slap", value="<:reply:1125269313432059904> Mention someone to slap, or don't mention anyone for Hoshi to slap you", inline=False)# ✅
                embed.add_field(name="+roast", value="<:reply:1125269313432059904> Get a roast from Hoshi", inline=False)# ✅
                embed.add_field(name="+compliment", value="<:reply:1125269313432059904> Get a compliment from Hoshi", inline=False)# ✅
                embed.add_field(name="+say", value="<:reply:1125269313432059904> Make Hoshi say exactly what you say", inline=False)# ✅
                embed.add_field(name="+8ball", value="<:reply:1125269313432059904> Ask Hoshi a question and get an answer", inline=False)# ✅
                embed.add_field(name="+ship", value="<:reply:1125269313432059904> Mention 2 members to see if Hoshi ships them (+ship @mention @mention)", inline=False)# ✅
                embed.add_field(name="+avatar", value="<:reply:1125269313432059904> Get a photo of your avatar or someone elses", inline=False)# ✅
                embed.add_field(name="+giphy", value="<:reply:1125269313432059904> Search for a gif with giphy", inline=False)# ✅
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[1]:
                embed = discord.Embed(title="> Editing commands", color=0x2b2d31)
                embed.add_field(name="+transition", value="<:reply:1125269313432059904> Get a random transition to use in your edit", inline=False)# ✅
                embed.add_field(name="+audio", value="<:reply:1125269313432059904> Get an audio added by a member to use for your edit", inline=False)# ✅
                embed.add_field(name="+addaudio", value="<:reply:1125269313432059904> Add an audio from SoundCloud for others to use", inline=False)# ✅
                embed.add_field(name="+addedit", value="<:reply:1125269313432059904> Add your own edit to Hoshi (must be a streamable link)", inline=False)# ✅
                embed.add_field(name="+edits", value="<:reply:1125269313432059904> Watch edits added from members of, Aura, Kanzen and Daegu", inline=False)# ✅
                embed.add_field(name="+effects", value="<:reply:1125269313432059904> Get a random effect to use in your edit", inline=False)# ✅
                embed.add_field(name="+colorscheme", value="<:reply:1125269313432059904> Get a random color scheme to use in your edit", inline=False)# ✅
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[2]:
                embed = discord.Embed(title="> Other commands", color=0x2b2d31)
                embed.add_field(name="+ia", value="<:reply:1125269313432059904> Send us an inactivity message if you go inactive", inline=False)# ✅
                embed.add_field(name="/ia", value="<:reply:1125269313432059904> Send us an inactivity message if you go inactive (kanzengrp only)", inline=False)# ✅
                embed.add_field(name="+suggest", value="<:reply:1125269313432059904> Suggest what we can do in the group (+suggest [suggestion])", inline=False)# ✅
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[3]:
                embed = discord.Embed(title="> Minigames", color=0x2b2d31)
                embed.add_field(name="+scramble", value="<:reply:1125269313432059904> Unscramble the word Hoshi gives you in 20 seconds", inline=False)# ✅
                embed.add_field(name="+trivia", value="<:reply:1125269313432059904> Hoshi will ask you a question, make sure to answer correctly (answer with numbers 1-4)", inline=False)# ✅
                embed.add_field(name="+tictactoe", value="<:reply:1125269313432059904> Play a game of tictactoe with the person you mention", inline=False)# ✅
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[4]:
                embed = discord.Embed(title="> Kanzen only commands", color=0x2b2d31)
                embed.add_field(name="+newcmd", value="<:reply:1125269313432059904> Make your own command! `+newcmd (command name) (hoshi's responce)`", inline=False)
                embed.add_field(name="+listcmds", value="<:reply:1125269313432059904> See all the commands other zennies have added", inline=False)
                embed.add_field(name="+removecmd", value="<:reply:1125269313432059904> Made a mistake in your command? do `+removecmd (+commandname)`", inline=False)
                embed.add_field(name="+daily", value="<:reply:1125269313432059904> Get anywhere from 100xp - 300xp everyday! (server boosters only wait 12 hours)", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[5]:
                embed = discord.Embed(title="> Levels commands", color=0x2b2d31)
                embed.add_field(name="+rank", value="<:reply:1125269313432059904> See your rank, or someone elses", inline=False)
                embed.add_field(name="+levels", value="<:reply:1125269313432059904> See the level leaderboard for the server", inline=False)
                embed.add_field(name="+rankcolor", value="<:reply:1125269313432059904> Set your rank color with a hex code", inline=False)
                embed.add_field(name="+xp add", value="<:reply:1125269313432059904> Add xp to a member (admin only command)", inline=False)
                embed.add_field(name="+xp remove", value="<:reply:1125269313432059904> Remove xp from a member (admin only command)", inline=False)
                embed.add_field(name="+reset add", value="<:reply:1125269313432059904> Resets xp for everyone (admin only)", inline=False)
                embed.add_field(name="+levelling on", value="<:reply:1125269313432059904> Enables the levelling system for the server (admin only)", inline=False)
                embed.add_field(name="+levelling off", value="<:reply:1125269313432059904> Disables the levelling system for the server (admin only)", inline=False)
                embed.add_field(name="+levelling setrole", value="<:reply:1125269313432059904> Set the top 20 active role", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[6]:
                embed = discord.Embed(title="> Moderation commands", color=0x2b2d31)
                embed.add_field(name="/kick", value="<:reply:1125269313432059904> Kick a member from the server", inline=False)
                embed.add_field(name="/ban", value="<:reply:1125269313432059904> Ban a member from the server", inline=False)
                embed.add_field(name="/addrole", value="<:reply:1125269313432059904> Add a role to a member (+addrole @role @mention)", inline=False)
                embed.add_field(name="/removerole", value="<:reply:1125269313432059904> Remove a role from a member (+removerole @role @mention)", inline=False)
                embed.add_field(name="+buildembed", value="<:reply:1125269313432059904> Create an embed", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[7]:
                embed = discord.Embed(title="> Application commands", color=0x2b2d31)
                embed.add_field(name="/apply", value="<:reply:1125269313432059904> Apply for kanzengrp", inline=False)
                embed.add_field(name="/app", value="<:reply:1125269313432059904> Apply for auragrp", inline=False)
                embed.add_field(name="+accept @mention", value="<:reply:1125269313432059904> Accepts member into kanzen", inline=False)
                embed.add_field(name="+decline @mention", value="<:reply:1125269313432059904> Declines a member from kanzen", inline=False)
                embed.add_field(name="+qna", value="<:reply:1125269313432059904> Ask the lead a question", inline=False)
                embed.add_field(name="+answer", value="<:reply:1125269313432059904> Answer a question sent", inline=False)
                embed.set_thumbnail(url=ctx.guild.icon)
            elif selected_category == categories[8]:
                embed = discord.Embed(title="> Community commands", color=0x2b2d31)
                embed.add_field(name="+giveaway", value="<:reply:1125269313432059904> Start a giveaway", inline=False)# ✅
                embed.set_thumbnail(url=ctx.guild.icon)
            else:
                embed = discord.Embed(title="Invalid category", description="Please select a valid category from the dropdown menu.")

            await interaction.response.edit_message(embed=embed)

        # Assign the callback function to the dropdown
        dropdown.callback = dropdown_callback

    @commands.command()
    async def helpjail(self, ctx):
        embed = discord.Embed(title='+jail <member>', description='Put someone or yourself in jail!', color=0x2b2d31)
        embed.add_field(name='aliases', value='prison, lockup', inline=False)
        embed.add_field(name='arguments', value='`member`\n<:reply:1125269313432059904> mention someone to put in jail\nor dont mention someone to put yourself in jail', inline=False)
        embed.add_field(name='example', value='+jail <@609515684740988959>', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helppride(self, ctx):
        embed = discord.Embed(title='+pride <member>', description='Puts the pride flag over your or the mentioned users avatar', color=0x2b2d31)
        embed.add_field(name='aliases', value='gay, pridemonth', inline=False)
        embed.add_field(name='arguments', value='`member`\n<:reply:1125269313432059904> mention someone for hoshi to put the pride flag on their avatar\nor dont mention someone so hoshi puts the pride flag on your avatar', inline=False)
        embed.add_field(name='example', value='+pride <@609515684740988959>', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpmemberinfo(self, ctx):
        embed = discord.Embed(title='+memberinfo <member>', description='See info of yourself or other members', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`member`\n<:reply:1125269313432059904> mention someone to see their info\nor dont mention someone to see your own info', inline=False)
        embed.add_field(name='example', value='+memberinfo <@609515684740988959>', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpkiss(self, ctx):
        embed = discord.Embed(title='+kiss <member>', description='Kiss members, or get Hoshi to kiss you', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`member`\n<:reply:1125269313432059904> mention someone to kiss\nor dont mention someone to have Hoshi kiss you', inline=False)
        embed.add_field(name='example', value='+kiss <@609515684740988959>', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helphug(self, ctx):
        embed = discord.Embed(title='+hug <member>', description='Hug members, or get Hoshi to hug you', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`member`\n<:reply:1125269313432059904> mention someone to hug\nor dont mention someone to have Hoshi hug you', inline=False)
        embed.add_field(name='example', value='+hug <@609515684740988959>', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpslap(self, ctx):
        embed = discord.Embed(title='+slap <member>', description='slap members, or get Hoshi to slap you', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`member`\n<:reply:1125269313432059904> mention someone to slap\nor dont mention someone to have Hoshi slap you', inline=False)
        embed.add_field(name='example', value='+slap <@609515684740988959>', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helproast(self, ctx):
        embed = discord.Embed(title='+roast', description='Hoshi roasts you', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='none', inline=False)
        embed.add_field(name='example', value='+roast', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpcompliment(self, ctx):
        embed = discord.Embed(title='+compliment', description='Hoshi compliments you', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='none', inline=False)
        embed.add_field(name='example', value='+compliment', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpsay(self, ctx):
        embed = discord.Embed(title='+say <message>', description='Hoshi will repeat whatever you say', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`message`\n<:reply:1125269313432059904> the text you want hoshi to say', inline=False)
        embed.add_field(name='example', value='+say hello', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def help8ball(self, ctx):
        embed = discord.Embed(title='+8ball <question>', description='Hoshi will tell you if something is likely or not likely to happen', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`question`\n<:reply:1125269313432059904> the question you want hoshi to answer', inline=False)
        embed.add_field(name='example', value='+8ball will i get rich?', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpship(self, ctx):
        embed = discord.Embed(title='+ship <mention> <mention>', description='Hoshi will tell you you and your mentioned are a good match', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`mention`\n<:reply:1125269313432059904> mention yourself first\n`mention`\n<:reply:1125269313432059904> the person you want to be shipped with', inline=False)
        embed.add_field(name='example', value='+ship <@609515684740988959> <@718144988688679043>', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helptictactoe(self, ctx):
        embed = discord.Embed(title='+tictactoe <mention> ', description='Play a game of tictactoe with the person you have mentioned', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`mention`\n<:reply:1125269313432059904> The person you want to play with', inline=False)
        embed.add_field(name='example', value='+tictactoe <@718144988688679043>', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helptrivia(self, ctx):
        embed = discord.Embed(title='+trivia', description='Play trivia with hoshi (answer questions with numbers : 1 - 4)', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='none', inline=False)
        embed.add_field(name='example', value='+trivia', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpavatar(self, ctx):
        embed = discord.Embed(title='+avatar <mention>', description='Hoshi will get your avatar, or the person you mentioned avatar', color=0x2b2d31)
        embed.add_field(name='aliases', value='pfp, icon', inline=False)
        embed.add_field(name='arguments', value='`mention`\n<:reply:1125269313432059904> hoshi will get this persons avatar instead', inline=False)
        embed.add_field(name='example', value='+avatar <@609515684740988959>', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpgiphy(self, ctx):
        embed = discord.Embed(title='+giphy <search>', description='Hoshi will search for a gif of what you searched', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`search`\n<:reply:1125269313432059904> the subject you want to search', inline=False)
        embed.add_field(name='example', value='+search blackpink', inline=False)
        await ctx.reply(embed=embed)

    # EDITING HELP COMMANDS

    @commands.command()
    async def helptransition(self, ctx):
        embed = discord.Embed(title='+transition', description='Hoshi will give you a random transition', color=0x2b2d31)
        embed.add_field(name='aliases', value='+transitions', inline=False)
        embed.add_field(name='arguments', value='none', inline=False)
        embed.add_field(name='example', value='+transition', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpeffects(self, ctx):
        embed = discord.Embed(title='+transition', description='Hoshi will give you a random effect', color=0x2b2d31)
        embed.add_field(name='aliases', value='+effect', inline=False)
        embed.add_field(name='arguments', value='none', inline=False)
        embed.add_field(name='example', value='+effect', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpaudio(self, ctx):
        embed = discord.Embed(title='+audio', description='Hoshi will give you a random audio added by members', color=0x2b2d31)
        embed.add_field(name='aliases', value='+audios', inline=False)
        embed.add_field(name='arguments', value='none', inline=False)
        embed.add_field(name='example', value='+audio', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpaddaudio(self, ctx):
        embed = discord.Embed(title='+addaudio <soundcloud link>', description='You can add audios to the `+audio` command', color=0x2b2d31)
        embed.add_field(name='aliases', value='+audios', inline=False)
        embed.add_field(name='arguments', value='`soundcloud link`\n<:reply:1125269313432059904> the audios link (has to be from soundcloud)', inline=False)
        embed.add_field(name='example', value='+addaudio https://soundcloud.com/remqsi', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpedits(self, ctx):
        embed = discord.Embed(title='+edits', description='Hoshi sends a random edit added by a member', color=0x2b2d31)
        embed.add_field(name='aliases', value='+edit', inline=False)
        embed.add_field(name='arguments', value='none', inline=False)
        embed.add_field(name='example', value='+edits', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def helpaddedit(self, ctx):
        embed = discord.Embed(title='+addedit <streamable link>', description='You can add your edits to the `+edits` command', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`streamable link`\n<:reply:1125269313432059904> the audios link (has to be from streamable)', inline=False)
        embed.add_field(name='example', value='+addedit https://streamable.com/6l2840', inline=False)
        await ctx.reply(embed=embed)    

    @commands.command()
    async def helpcolorscheme(self, ctx):
        embed = discord.Embed(title='+colorscheme', description='Hoshi sends a random color scheme', color=0x2b2d31)
        embed.add_field(name='aliases', value='cs', inline=False)
        embed.add_field(name='arguments', value='none', inline=False)
        embed.add_field(name='example', value='+colorscheme', inline=False)
        await ctx.reply(embed=embed)    

    @commands.command()
    async def helpia(self, ctx):
        embed = discord.Embed(title='+ia / /ia <reason>', description='Send an inactivity message to the leads of the group(s)', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`reason`\n<:reply:1125269313432059904> the reason youre going inactive', inline=False)
        embed.add_field(name='example', value='+ia school', inline=False)
        await ctx.reply(embed=embed)   

    @commands.command()
    async def helpsuggest(self, ctx):
        embed = discord.Embed(title='+suggest <suggestion>', description='Send a suggestion to the suggestions channel for others to vote on', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`suggestion`\n<:reply:1125269313432059904> the thing you would like to suggest', inline=False)
        embed.add_field(name='example', value='+suggest group collab', inline=False)
        await ctx.reply(embed=embed)  

    @commands.command()
    async def helptrivia(self, ctx):
        embed = discord.Embed(title='+trivia', description='Play a game of trivia', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='none', inline=False)
        embed.add_field(name='example', value='+trivia', inline=False)
        await ctx.reply(embed=embed)  

    @commands.command()
    async def helpscramble(self, ctx):
        embed = discord.Embed(title='+scramble', description='Play a game of word scramble', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='none', inline=False)
        embed.add_field(name='example', value='+scramble', inline=False)
        await ctx.reply(embed=embed)  

    @commands.command()
    async def helpgiveaway(self, ctx):
        embed = discord.Embed(title='+giveaway <time> <prize> <host|optional>', description='Create a giveaway', color=0x2b2d31)
        embed.add_field(name='aliases', value='none', inline=False)
        embed.add_field(name='arguments', value='`time`\n<:reply:1125269313432059904> the length of time the giveaway lasts for\n`prize`\n<:reply:1125269313432059904> the prize for the giveaway\n`host`\n<:reply:1125269313432059904> the host of the giveaway (optional)', inline=False)
        embed.add_field(name='example', value='+giveaway 12 overlays @remqsi', inline=False)
        await ctx.reply(embed=embed)  

async def setup(bot):
    await bot.add_cog(Help(bot))