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
        embed.add_field(name='how to apply', value="<a:Lumi_arrow_R:1126865547255091343> Do the command `+app` and answer the questions Hoshi asks!\n<a:Lumi_arrow_R:1126865547255091343> Your messages will be deleted, but don't worry, Hoshi is just saving your answers to send over!\n<a:Lumi_arrow_R:1126865547255091343> Hoshi will DM you if you have been accepted or declined. If you have been accepted, join the server hoshi gives you because thats the members server", inline=False)
        embed.add_field(name='Recruit Info', value="<a:Lumi_arrow_R:1126865547255091343> Velocity edits are an auto decline!\n<a:Lumi_arrow_R:1126865547255091343> Follow the rules on [@kanzengrp's](https://www.instagram.com/kanzengrp/) recent post!\n<a:Lumi_arrow_R:1126865547255091343> Only accept Instagram editors\n<a:Lumi_arrow_R:1126865547255091343> Please be patient when it comes to forms! The lead isn't active 24/7", inline=False)
        embed.set_footer(text='If you have any question, do +qna')
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(other(bot))