import datetime
import random
import discord
from discord.ext import commands

class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def randomembed1(self, ctx):
        embed = discord.Embed(
            title='> Apply To Kanzen',
            color=0x2b2d31)
        embed.set_image(url='https://cdn.discordapp.com/attachments/1122181606254330008/1126868683462017024/theme_00000.png')
        embed.add_field(name='how to apply', value="<a:Lumi_arrow_R:1126865547255091343> Do the command `+app` and answer the questions Hoshi asks!\n<a:Lumi_arrow_R:1126865547255091343> Your messages will be deleted, but don't worry, Hoshi is just saving your answers to send over!\n<a:Lumi_arrow_R:1126865547255091343> Hoshi will DM you if you have been accepted or declined.\n<a:Lumi_arrow_R:1126865547255091343> If you have been accepted, Hoshi will give you a link to the members server", inline=False)
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

    @commands.command()
    async def daily(self, ctx):
        user = ctx.author
        current_time = datetime.datetime.utcnow()

        # Check user's roles for wait time
        wait_time = datetime.timedelta(hours=24)  # Default wait time for non-boosters
        if any(role.name.lower() == "Kanzen Booster" for role in user.roles):
            wait_time = datetime.timedelta(hours=12)  # Wait time for server boosters

        # Check if user has bypass permission
        if ctx.author.guild_permissions.manage_guild:
            wait_time = datetime.timedelta(seconds=0)  # No wait time for admins

        # Check if user has previously claimed daily XP
        last_claimed = self.get_last_claimed(user)
        if last_claimed:
            next_claim = last_claimed + wait_time
            if current_time < next_claim:
                remaining_time = next_claim - current_time
                return await ctx.send(f"{user.mention}, you need to wait {remaining_time} before claiming daily XP again!")

        xp = random.randint(100, 300)

        # Send a message in the current channel
        await ctx.send(f"{user.mention}, you received {xp} XP for your daily activity!")

        # Send a message in the specified channel with user and XP information
        channel_id = 1125999933149949982  # Change to your desired channel ID
        channel = self.bot.get_channel(channel_id)

        if channel:
            await channel.send(f"{user.name}#{user.discriminator} ({user.id}) earned {xp} XP for their daily activity!")

        # Save the current time as the last claimed time
        self.save_last_claimed(user, current_time)

    def get_last_claimed(self, user):
        # Retrieve the last claimed time from storage (not implemented in the code)
        return None  # Replace with your code to retrieve the last claimed time

    def save_last_claimed(self, user, current_time):
        # Save the last claimed time to storage (not implemented in the code)
        pass  # Replace with your code to save the last claimed time

async def setup(bot):
    await bot.add_cog(other(bot))