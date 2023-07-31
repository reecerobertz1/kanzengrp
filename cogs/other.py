import datetime
import random
import discord
from discord.ext import commands

class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}
        self.allowed_server_id = 1121841073673736215  # Change to your desired server ID

    """ @commands.command()
    async def daily(self, ctx):
        if ctx.guild.id != self.allowed_server_id:
            return  # Exit the command if not in the allowed server

        user = ctx.author
        current_time = datetime.datetime.utcnow()

        # Check if user is on cooldown
        if user.id in self.cooldowns:
            remaining_time = self.cooldowns[user.id] - current_time
            if remaining_time.total_seconds() > 0:
                hours = remaining_time.seconds // 3600
                minutes = (remaining_time.seconds % 3600) // 60
                return await ctx.reply(f"You need to wait {hours} hours {minutes} minutes before claiming daily XP again!")

        # Calculate XP and cooldown based on user's roles
        xp = random.randint(100, 300)
        cooldown = datetime.timedelta(hours=24)  # Default cooldown for non-boosters

        if any(role.name.lower() == "Kanzen Booster" for role in user.roles):
            cooldown = datetime.timedelta(hours=12)  # Cooldown for server boosters

        # Check if user has bypass permission
        if ctx.author.guild_permissions.manage_guild:
            cooldown = datetime.timedelta(seconds=0)  # No cooldown for admins

        # Send a message in the current channel
        await ctx.reply(f"You claimed your daily xp! you got **{xp}xp**")

        # Send a message in the specified channel with user and XP information
        channel_id = 1125999933149949982  # Change to your desired channel ID
        channel = self.bot.get_channel(channel_id)

        if channel:
            await channel.send(f"{user.mention} earned {xp} XP for their daily xp!")

        # Set the cooldown for the user
        self.cooldowns[user.id] = current_time + cooldown """

    @commands.command()
    async def randomembed1(self, ctx):
        embed = discord.Embed(
            title='> Apply To Kanzen',
            color=0x2b2d31)
        embed.set_image(url='https://cdn.discordapp.com/attachments/1122181606254330008/1126868683462017024/theme_00000.png')
        embed.add_field(name='How To Apply', value="<a:Lumi_arrow_R:1126865547255091343> Do the command `/apply` and fill out the form that appears on screen!\n<a:Lumi_arrow_R:1126865547255091343> Hoshi will DM you if you have been accepted or declined.\n<a:Lumi_arrow_R:1126865547255091343> If you have been accepted, Hoshi will give you a link to the members server", inline=False)
        embed.add_field(name='Recruit Info', value="<a:Lumi_arrow_R:1126865547255091343> Velocity edits are an auto decline!\n<a:Lumi_arrow_R:1126865547255091343> Follow the rules on [@kanzengrp's](https://www.instagram.com/kanzengrp/) recent post!\n<a:Lumi_arrow_R:1126865547255091343> Only accept Instagram editors\n<a:Lumi_arrow_R:1126865547255091343> Please be patient when it comes to forms!", inline=False)
        embed.set_footer(text='If you have any question, do +qna')
        await ctx.send(embed=embed)

    @commands.command()
    async def randomembed2(self, ctx):
        embed = discord.Embed(
            title='> Kanzen Q&A',
            color=0x2b2d31)
        embed.set_image(url='https://cdn.discordapp.com/attachments/1122181606254330008/1127005297270071417/jisoo_and_rose_photo_00000.png')
        embed.add_field(name='how to apply', value="<a:bounceyarrow:1126865547255091343> use the command `+qna` to ask the lead a question.\n<a:bounceyarrow:1126865547255091343> your question will be sent to a separate channel and when the lead answers, the answer will be sent to <#1123696762985656451>.\n<a:bounceyarrow:1126865547255091343> you will also be pinged when your question has been answered.\n<a:bounceyarrow:1126865547255091343> please do not abuse this command and spam! you will be kicked from the server, and banned if you continue", inline=False)
        embed.set_footer(text='If you have any question, do +qna')
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots to avoid potential loops
        if message.author.bot:
            return

        # Check if the message content matches the trigger phrase exactly
        if message.content.lower() == "reece":
            # Send the reply message
            await message.channel.send("<@609515684740988959> is the sexiest")

        if message.content.lower() == "tae":
            # Send the reply message
            await message.channel.send("<@718144988688679043> is mommy")

        if message.content.lower() == "nani":
            await message.channel.send("i woke up in a new 🔥bugatti🔥")

        if message.content.lower() == "spotify ads":
            await message.channel.send("follow 0470pm for free spotify premium")

        if message.content.lower() == "jess":
            await message.channel.send("https://media0.giphy.com/media/DWPCBPJPBLRsSG0LI2/giphy.gif?cid=ad7b17ba5hahdaf6h1wgccgl9loldyoowq0u3d0c68fisadd&ep=v1_gifs_search&rid=giphy.gif&ct=g")

        if message.content.lower() == "kira":
            await message.channel.send("OMG JIMIN<:chimmy:1128727915664785409>:heartpulse::face_with_peeking_eye::heart_eyes::face_holding_back_tears::pleading_face::sob::weary::tired_face::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::pray_tone1::pinching_hand:<:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> :face_holding_back_tears::face_holding_back_tears::face_holding_back_tears:")

async def setup(bot):
    await bot.add_cog(other(bot))