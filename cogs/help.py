import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        categories = {
            "> <a:Lumi_penguin_fall:1122607666578063531> : About Hoshi": [
                {"name": "The Coding", "value": "Hoshi is coded in Python 3.11.4\n[Download Python 3.11.4](https://www.python.org/downloads/)", "inline": False},
                {"name": "Owner", "value": "Hoshi is owned by Reeceroberts\nReece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)", "inline": False},
                {"name": "Extra Information", "value": "Hoshi's prefix is `+`\nHoshi was made for **__Kanzengrp__**", "inline": False},
                {"name": "", "value": "`[page 1/8]`", "inline": True}
            ],
            "> Fun commands": [
                {"name": "+dog", "value": "<:reply:1125269313432059904> Sends you a random photo of a dog", "inline": False},
                {"name": "+cat", "value": "<:reply:1125269313432059904> Sends you a random photo of a cat", "inline": False},
                {"name": "+jail", "value": "<:reply:1125269313432059904> Put someone or yourself in jail", "inline": False},
                {"name": "+memberinfo", "value": "<:reply:1125269313432059904> View info for yourself or others", "inline": False},
                {"name": "+kiss", "value": "<:reply:1125269313432059904> Mention someone to kiss, or don't mention anyone for Hoshi to kiss you", "inline": False},
                {"name": "+hug", "value": "<:reply:1125269313432059904> Mention someone to hug, or don't mention anyone for Hoshi to hug you", "inline": False},
                {"name": "+slap", "value": "<:reply:1125269313432059904> Mention someone to slap, or don't mention anyone for Hoshi to slap you", "inline": False},
                {"name": "+roast", "value": "<:reply:1125269313432059904> Get a roast from Hoshi", "inline": False},
                {"name": "+compliment", "value": "<:reply:1125269313432059904> Get a compliment from Hoshi", "inline": False},
                {"name": "+say", "value": "<:reply:1125269313432059904> Make Hoshi say exactly what you say", "inline": False},
                {"name": "+8ball", "value": "<:reply:1125269313432059904> Ask Hoshi a question and get an answer", "inline": False},
                {"name": "+ship", "value": "<:reply:1125269313432059904> Mention 2 members to see if Hoshi ships them (+ship @mention @mention)", "inline": False},
                {"name": "+trivia", "value": "<:reply:1125269313432059904> Hoshi will ask you a question, make sure to answer correctly (answer with numbers 1-4)", "inline": False},
                {"name": "+avatar", "value": "<:reply:1125269313432059904> Get a photo of your avatar or someone elses", "inline": False},
                {"name": "", "value": "`[page 2/8]`", "inline": True}
            ],
            "> Editing commands": [
                {"name": "+transition", "value": "<:reply:1125269313432059904> Get a random transition to use in your edit", "inline": False},
                {"name": "+audio", "value": "<:reply:1125269313432059904> Get an audio added by a member to use for your edit", "inline": False},
                {"name": "+addaudio", "value": "<:reply:1125269313432059904> Add an audio from SoundCloud for others to use", "inline": False},
                {"name": "+addedit", "value": "<:reply:1125269313432059904> Add your own edit to Hoshi (must be a streamable link)", "inline": False},
                {"name": "+edits", "value": "<:reply:1125269313432059904> Watch edits added from members of, Aura, Kanzen and Daegu", "inline": False},
                {"name": "+effects", "value": "<:reply:1125269313432059904> Get a random effect to use in your edit", "inline": False},
                {"name": "+colorscheme", "value": "<:reply:1125269313432059904> Get a random color scheme to use in your edit", "inline": False},
                {"name": "", "value": "`[page 3/8]`", "inline": True}
            ],
            "> Other commands": [
                {"name": "+ia", "value": "<:reply:1125269313432059904> Send us an inactivity message if you go inactive", "inline": False},
                {"name": "", "value": "`[page 4/8]`", "inline": True}
            ],
            "> Kanzen only commands": [
                {"name": "+newcmd", "value": "<:reply:1125269313432059904> Make your own command! `+newcmd (command name) (hoshi's responce)`", "inline": False},
                {"name": "+listcmds", "value": "<:reply:1125269313432059904> See all the commands other zennies have added", "inline": False},
                {"name": "+removecmd", "value": "<:reply:1125269313432059904> Made a mistake in your command? do `+removecmd (+commandname)", "inline": False},
                {"name": "", "value": "`[page 5/8]`", "inline": True}
            ],
            "> Levels commands": [
                {"name": "+rank", "value": "<:reply:1125269313432059904> See your rank, or someone elses", "inline": False},
                {"name": "+levels", "value": "<:reply:1125269313432059904> See the level leaderboard for the server", "inline": False},
                {"name": "+rankcolor", "value": "<:reply:1125269313432059904> Set your rank color with a hex code", "inline": False},
                {"name": "+xp add", "value": "<:reply:1125269313432059904> Add xp to a member (admin only command)", "inline": False},
                {"name": "+xp remove", "value": "<:reply:1125269313432059904> Remove xp from a member (admin only command)", "inline": False},
                {"name": "+reset add", "value": "<:reply:1125269313432059904> Resets xp for everyone (admin only)", "inline": False},
                {"name": "+levelling on", "value": "<:reply:1125269313432059904> Enables the levelling system for the server (admin only)", "inline": False},
                {"name": "+levelling off", "value": "<:reply:1125269313432059904> Disables the levelling system for the server (admin only)", "inline": False},
                {"name": "+levelling setrole", "value": "<:reply:1125269313432059904> Set the top 20 active role", "inline": False},
                {"name": "", "value": "`[page 6/8]`", "inline": True}
            ],
            "> Moderation commands": [
                {"name": "+kick", "value": "<:reply:1125269313432059904> Kick a member from the server", "inline": False},
                {"name": "+ban", "value": "<:reply:1125269313432059904> Ban a member from the server", "inline": False},
                {"name": "+addrole", "value": "<:reply:1125269313432059904> Add a role to a member (+addrole @role @mention)", "inline": False},
                {"name": "+removerole", "value": "<:reply:1125269313432059904> Remove a role from a member (+removerole @role @mention)", "inline": False},
                {"name": "+buildembed", "value": "<:reply:1125269313432059904> Create an embed", "inline": False},
                {"name": "+suggest", "value": "<:reply:1125269313432059904> Suggest what we can do in the group (+suggest [suggestion])", "inline": False},
                {"name": "+uptime", "value": "<:reply:1125269313432059904> See how long the bot has been online for", "inline": False},
                {"name": "+ping", "value": "<:reply:1125269313432059904> See the bots ping", "inline": False},
                {"name": "", "value": "`[page 7/8]`", "inline": True}
            ],
            "> Application commands": [
                {"name": "+app", "value": "<:reply:1125269313432059904> Apply for kanzengrp", "inline": False},
                {"name": "+accept @mention", "value": "<:reply:1125269313432059904> Accepts member into kanzen", "inline": False},
                {"name": "+decline @mention", "value": "<:reply:1125269313432059904> Declines a member from kanzen", "inline": False},
                {"name": "+resetapps", "value": "<:reply:1125269313432059904> Resets all IDs from forms", "inline": False},
                {"name": "+viewapps", "value": "<:reply:1125269313432059904> See all applications sent", "inline": False},
                {"name": "+qna", "value": "<:reply:1125269313432059904> Ask the lead a question", "inline": False},
                {"name": "+answer", "value": "<:reply:1125269313432059904> Answer a question sent", "inline": False},
                {"name": "", "value": "`[page 8/8]`", "inline": True}
            ]
        }

        embeds = []
        for category, commands in categories.items():
            embed = discord.Embed(title=f"{category}", color=0x2b2d31)
            embed.set_thumbnail(url=ctx.guild.icon)
            for command in commands:
                embed.add_field(name=command["name"], value=command["value"], inline=False)
                embed.set_footer(text='Do +help (command) to see how to use the command!')
            embeds.append(embed)

        current_page = 0
        message = await ctx.reply(embed=embeds[current_page])

        await message.add_reaction("◀")
        await message.add_reaction("▶")

        def check(reaction, user):
            return user == ctx.author and reaction.message == message

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if reaction.emoji == "▶":
                    current_page = (current_page + 1) % len(embeds)
                elif reaction.emoji == "◀":
                    current_page = (current_page - 1) % len(embeds)

                await message.edit(embed=embeds[current_page])
                await message.remove_reaction(reaction, user)
            except TimeoutError:
                break

        await message.clear_reactions()

    @commands.command()
    async def helpjail(self, ctx):
        embed = discord.Embed(title='+jail <member>', description='Put someone or yourself in jail!', color=0x2b2d31)
        embed.add_field(name='aliases', value='prison, lockup', inline=False)
        embed.add_field(name='arguments', value='`member`\n<:reply:1125269313432059904> mention someone to put in jail\nor dont mention someone to put yourself in jail', inline=False)
        embed.add_field(name='example', value='+jail <@609515684740988959>', inline=False)
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

async def setup(bot):
    await bot.add_cog(Help(bot))