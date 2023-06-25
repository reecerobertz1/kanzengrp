import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        categories = {
        f"> <a:Lumi_penguin_fall:1122607666578063531> About Lisa": [f'﹒Lisa is coded in [Python 3.11.4](https://www.python.org/downloads/)\n﹒Lisa is owned by <@609515684740988959>.\n﹒Lisas prefix is `+`\n﹒Reece coded Lisa in [Visual Studio Code](https://code.visualstudio.com/).\n﹒Lisa was made for **__Kanzengrp__**', 'Page [1/7]'],
        "> Fun commands": [f"**+dog** : sends you a random photo of a dog", f"**+cat** : sends you a random photo of a cat\n**+jail** : put someone or yourself in jail\n**+memberinfo** : you can see info for yourself or others\n**+kiss** : mention someone to kiss, or dont mention anyone for aroma to kiss you\n**+hug** : mention someone to hug, or dont mention anyone for aroma to hug you\n**+slap** : mention someone to slap, or dont mention anyone for aroma to slap you\n**+roast** : get a roast from aroma\n**+compliment** : get a compliment from aroma\n**+say** : make aroma say exactly what you say\n**+8ball** : ask aroma a question, and get an answer", 'Page [2/7]'],
        "> Editing commands": [f"**+transition** : get a random transition to use in your edit", f"**+audio** : get an audio added by a member to use for your edit", f"**+addaudio** : you can add an audio from soundcloud for others to use", f"**+effects** : get a random effect to use in your edit", 'Page [3/7]'],
        "> Other commands": [f"**+ia** : send us an inactivity message if you go inactive", 'Page [4/7]'],
        "> Levels commands": [f"Command 1", "Command 2", "Command 3", 'Page [5/7]'],
        "> Custom commands": [f"**+listcmds**: shows you all of the custom commands added here", f"**+addcmd** : allows you to add a command (+addcmd hello hi)", 'Page [6/7]'],
        "> Moderation commands": [f"**+kick** : kicks a member from the server", f"**+ban** : bans a member from the server", f"**+addrole** : add a role to a member (+addrole @role @mention)", f"**+removerole** : removes a role from a member (+reoverole @role @mention)", f"**+buildembed** : make an embed",  'Page [7/7]']
        }

        embeds = []
        for category, commands in categories.items():
            embed = discord.Embed(title=f"{category}", description="\n".join(commands), color=0x2b2d31)
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