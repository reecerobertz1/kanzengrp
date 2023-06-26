import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        categories = {
            "> <a:Lumi_penguin_fall:1122607666578063531> : About Hoshi": [
                {"name": "Hoshi is coded in Python 3.11.4", "value": "[Download Python 3.11.4](https://www.python.org/downloads/)", "inline": False},
                {"name": "Hoshi is owned by <@609515684740988959>", "value": "Reece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)", "inline": False},
                {"name": "Hoshi's prefix is `+`", "value": "Hoshi was made for **__Kanzengrp__**", "inline": False},
                {"name": "Page", "value": "[page 1/7]", "inline": False}
            ],
            "> Fun commands": [
                {"name": "+dog", "value": "Sends you a random photo of a dog", "inline": False},
                {"name": "+cat", "value": "Sends you a random photo of a cat", "inline": False},
                {"name": "+jail", "value": "Put someone or yourself in jail", "inline": False},
                {"name": "+memberinfo", "value": "View info for yourself or others", "inline": False},
                {"name": "+kiss", "value": "Mention someone to kiss, or don't mention anyone for Hoshi to kiss you", "inline": False},
                {"name": "+hug", "value": "Mention someone to hug, or don't mention anyone for Hoshi to hug you", "inline": False},
                {"name": "+slap", "value": "Mention someone to slap, or don't mention anyone for Hoshi to slap you", "inline": False},
                {"name": "+roast", "value": "Get a roast from Hoshi", "inline": False},
                {"name": "+compliment", "value": "Get a compliment from Hoshi", "inline": False},
                {"name": "+say", "value": "Make Hoshi say exactly what you say", "inline": False},
                {"name": "+8ball", "value": "Ask Hoshi a question and get an answer", "inline": False},
                {"name": "+ship", "value": "Mention 2 members to see if Hoshi ships them (+ship @mention @mention)", "inline": False},
                {"name": "+trivia", "value": "Hoshi will ask you a question, make sure to answer correctly (answer with numbers 1-4)", "inline": False},
                {"name": "Page", "value": "[page 2/7]", "inline": False}
            ],
            "> Editing commands": [
                {"name": "+transition", "value": "Get a random transition to use in your edit", "inline": False},
                {"name": "+audio", "value": "Get an audio added by a member to use for your edit", "inline": False},
                {"name": "+addaudio", "value": "Add an audio from SoundCloud for others to use", "inline": False},
                {"name": "+effects", "value": "Get a random effect to use in your edit", "inline": False},
                {"name": "Page", "value": "[page 3/7]", "inline": False}
            ],
            "> Other commands": [
                {"name": "+ia", "value": "Send us an inactivity message if you go inactive", "inline": False},
                {"name": "Page", "value": "[page 4/7]", "inline": False}
            ],
            "> Levels commands": [
                {"name": "Command 1", "value": "", "inline": False},
                {"name": "Command 2", "value": "", "inline": False},
                {"name": "Command 3", "value": "", "inline": False},
                {"name": "Page", "value": "[page 5/7]", "inline": False}
            ],
            "> Moderation commands": [
                {"name": "+kick", "value": "Kick a member from the server", "inline": False},
                {"name": "+ban", "value": "Ban a member from the server", "inline": False},
                {"name": "+addrole", "value": "Add a role to a member (+addrole @role @mention)", "inline": False},
                {"name": "+removerole", "value": "Remove a role from a member (+removerole @role @mention)", "inline": False},
                {"name": "+buildembed", "value": "Create an embed", "inline": False},
                {"name": "Page", "value": "[page 6/7]", "inline": False}
            ],
            "> Application commands": [
                {"name": "+apply", "value": "Apply for kanzengrp", "inline": False},
                {"name": "+accept @mention", "value": "Accepts member into kanzen", "inline": False},
                {"name": "+decline @mention", "value": "Declines a member from kanzen", "inline": False},
                {"name": "+resetids", "value": "Resets all IDs from forms", "inline": False},
                {"name": "+viewapplications", "value": "See all applications sent", "inline": False},
                {"name": "Page", "value": "[page 7/7]", "inline": False}
            ]
        }

        embeds = []
        for category, commands in categories.items():
            embed = discord.Embed(title=f"{category}", color=0x2b2d31)
            embed.set_thumbnail(url=ctx.guild.icon)
            for command in commands:
                embed.add_field(name=command["name"], value=command["value"], inline=True)
            embeds.append(embed)

        current_page = 0
        message = await ctx.reply(embed=embeds[current_page])

        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.author and reaction.message == message

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if reaction.emoji == "➡️":
                    current_page = (current_page + 1) % len(embeds)
                elif reaction.emoji == "⬅️":
                    current_page = (current_page - 1) % len(embeds)

                await message.edit(embed=embeds[current_page])
                await message.remove_reaction(reaction, user)
            except TimeoutError:
                break

        await message.clear_reactions()



async def setup(bot):
    await bot.add_cog(Help(bot))