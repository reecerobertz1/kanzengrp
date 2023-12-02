import asyncio
import random
import discord
from discord.ext import commands

class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hello_loop = None
        self.hidden = True
        self.emoji = "<:shooky:1121909564799987722>"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.lower() == "reece":
            await message.channel.send("<@609515684740988959> is the sexiest")
        if message.content.lower() == "tae":
            await message.channel.send("<@718144988688679043> is mommy")
        if message.content.lower() == "nani":
            await message.channel.send("i woke up in a new 🔥bugatti🔥")
        if message.content.lower() == "spotify ads":
            await message.channel.send("follow 0470pm for free spotify premium")
        if message.content.lower() == "jess":
            await message.channel.send("https://media0.giphy.com/media/DWPCBPJPBLRsSG0LI2/giphy.gif?cid=ad7b17ba5hahdaf6h1wgccgl9loldyoowq0u3d0c68fisadd&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        if message.content.lower() == "kira":
            await message.channel.send("OMG JIMIN<:chimmy:1128727915664785409>:heartpulse::face_with_peeking_eye::heart_eyes::face_holding_back_tears::pleading_face::sob::weary::tired_face::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::pray_tone1::pinching_hand:<:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> :face_holding_back_tears::face_holding_back_tears::face_holding_back_tears:")
        if message.content.lower() == "kelly":
            await message.channel.send("Jungkook is so jungkook and no one will ever jungkook like jungkook <:boobs:1142888878999613520>")
        if message.content.lower() == "savvi":
            await message.channel.send("SAVVI IS THE FUCKING BEST NO ONE ELSE CAN BEAT HER")
        if "MessageType.premium_guild" in str(message.type):
                embed = discord.Embed(title=f"Thank you for boosting! {message.author.display_name}!", description="<a:Arrow_1:1145603161701224528> dm staff or lead for your custom role\n<a:Arrow_1:1145603161701224528> go into [#booster-perks](https://discord.com/channels/1121841073673736215/1164318431462563951) to claim the perks\n<a:Arrow_1:1145603161701224528> we really appreciate your support!", color=0x2b2d31)
                embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar)
                embed.set_footer(text=f"We are up to {message.guild.premium_subscription_count} boosts!")
                if message.guild.id == 1121841073673736215:
                    await message.channel.send(f"{message.author.mention}", embed=embed)
                else:
                    pass

async def setup(bot):
    await bot.add_cog(other(bot))