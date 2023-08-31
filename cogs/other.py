import asyncio
import random
import discord
from discord.ext import commands

class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hello_loop = None

    @commands.command()
    async def kanzenrevive(self, ctx):
        if self.hello_loop is None:
            self.hello_loop = HelloLoop(self.bot, ctx.channel)
            self.hello_loop.start()
            await ctx.send('Started pinging chat revive.')

    @commands.command()
    async def aurarevive(self, ctx):
        if self.hello_loop is not None:
            self.hello_loop.cancel()
            self.hello_loop = None
            await ctx.send('Stopped pinging chat revive.')

    @commands.command()
    async def aurarevive(self, ctx):
        if self.pingloop is None:
            self.pingloop = HelloLoop(self.bot, ctx.channel)
            self.pingloop.start()
            await ctx.send('Started pinging chat revive.')

    @commands.command()
    async def auradie(self, ctx):
        if self.pingloop is not None:
            self.pingloop.cancel()
            self.pingloop = None
            await ctx.send('Stopped pinging chat revive.')

class HelloLoop:
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        self.loop = asyncio.get_event_loop()
        self.hello_task = None

    async def send_hello(self):
        target_channel = self.bot.get_channel(1125053619893440653)
        while True:
            revive = [
            "<@&1122927309813461143> Hi wake up! come and chat", "<@&1122927309813461143> wakey wakey!", "<@&1122927309813461143> hello start a conversation", "im bored anyone want to chat or play a game? <@&1122927309813461143>",
            "<@&1122927309813461143>", "<@&1122927309813461143> where is everyone?"
        ]

            ping = random.choice(revive)
            await target_channel.send(ping)
            await asyncio.sleep(86400)

class pingloop:
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        self.loop = asyncio.get_event_loop()
        self.hello_task = None

    async def send_ping(self):
        target_channel = self.bot.get_channel(1122238827973595238)
        while True:
            revive = [
            "<@&1122999575200940083> Hi wake up! come and chat", "<@&1122999575200940083> wakey wakey!", "<@&1122999575200940083> hello start a conversation", "im bored anyone want to chat or play a game? <@&1122999575200940083>",
            "<@&1122999575200940083>", "<@&1122999575200940083> where is everyone?"
        ]

            ping = random.choice(revive)
            await target_channel.send(ping)
            await asyncio.sleep(86400)

    def start(self):
        if self.hello_task is None:
            self.hello_task = self.loop.create_task(self.send_hello())

    def cancel(self):
        if self.hello_task is not None:
            self.hello_task.cancel()
            self.hello_task = None

    @commands.Cog.listener()
    async def on_message(self, message, ctx):
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
        if message.content.lower() == "why is it so dead":
            await message.channel.send("<@&1134876934585712773> where are you")
        if message.content.lower() == "where is everyone":
            await message.channel.send("<@&1134876934585712773> where are you")
        if message.content.lower() == "anyone there?":
            await message.channel.send("<@&1134876934585712773> where are you")
        if message.content.lower() == "hi":
            await message.channel.send(f"{ctx.author.mention} hello!")

async def setup(bot):
    await bot.add_cog(other(bot))