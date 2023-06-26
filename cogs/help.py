import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        categories = {
            "> <:Lumi_penguin_fall:1122607666578063531> About Hoshi": [
                "• Hoshi is coded in [Python 3.11.4](https://www.python.org/downloads/)",
                "• Hoshi is owned by <@609515684740988959>",
                "• Hoshi's prefix is `+`",
                "• Reece coded Hoshi in [Visual Studio Code](https://code.visualstudio.com/)",
                "• Hoshi was made for **__Kanzengrp__**"
            ],
            "> Fun commands": [
                "+dog: Sends you a random photo of a dog",
                "+cat: Sends you a random photo of a cat",
                "+jail: Put someone or yourself in jail",
                "+memberinfo: View info for yourself or others",
                "+kiss: Mention someone to kiss, or don't mention anyone for Hoshi to kiss you",
                "+hug: Mention someone to hug, or don't mention anyone for Hoshi to hug you",
                "+slap: Mention someone to slap, or don't mention anyone for Hoshi to slap you",
                "+roast: Get a roast from Hoshi",
                "+compliment: Get a compliment from Hoshi",
                "+say: Make Hoshi say exactly what you say",
                "+8ball: Ask Hoshi a question and get an answer",
                "+ship: Mention 2 members to see if Hoshi ships them (+ship @mention @mention)",
                "+trivia: Hoshi will ask you a question, make sure to answer correctly (answer with numbers 1-4)"
            ],
            "> Editing commands": [
                "+transition: Get a random transition to use in your edit",
                "+audio: Get an audio added by a member to use for your edit",
                "+addaudio: Add an audio from SoundCloud for others to use",
                "+effects: Get a random effect to use in your edit"
            ],
            "> Other commands": [
                "+ia: Send us an inactivity message if you go inactive"
            ],
            "> Levels commands": [
                "Command 1",
                "Command 2",
                "Command 3"
            ],
            "> Custom commands": [
                "+listcmds: Show all of the custom commands added here",
                "+addcmd: Add a command (+addcmd hello hi)"
            ],
            "> Moderation commands": [
                "+kick: Kick a member from the server",
                "+ban: Ban a member from the server",
                "+addrole: Add a role to a member (+addrole @role @mention)",
                "+removerole: Remove a role from a member (+removerole @role @mention)",
                "+buildembed: Create an embed"
            ]
        }

        embeds = []
        for category, commands in categories.items():
            embed = discord.Embed(title=f"{category}", color=0x2b2d31)
            embed.set_thumbnail(url=ctx.guild.icon)
            embed.description = "\n".join(commands)
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