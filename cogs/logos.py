import discord
from discord.ext import commands

class logos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def openapps(self, ctx):
        embed = discord.Embed(
            title='Apply Here!',
            description='Please make sure you read the [Rules](https://discord.com/channels/1122181605591621692/1122195332516810873) and the info below!',
            color=0x2b2d31
        )
        embed.add_field(name='Application Rules', value='<:arrow_00000:1121934367569227837> Make sure you are following [@remqsi](https://www.instagram.com/remqsi/) and the [group account](https://www.instagram.com/uzaigrp/)\n<:arrow_00000:1121934367569227837> Please only send one form!', inline=False)
        embed.add_field(name='Application Info', value='<:arrow_00000:1121934367569227837> Velocity edits are an **auto decline**\n<:arrow_00000:1121934367569227837> You will receive an acceptence message if you are accepted, and a decline message if you get declined.\n<:arrow_00000:1121934367569227837> There is no doing reapps so choose the edit you want to apply with wisely\n<:arrow_00000:1121934367569227837> Make sure you answer all the questions on the form before sending!\n<:arrow_00000:1121934367569227837> Apply with your best edit. We look for creative and smooth edits', inline=False)
        embed.set_image(url='https://cdn.discordapp.com/attachments/1122195332516810874/1122208438345281666/IMG_2232_00000_00000.png')
        embed.set_footer(text='If you need any help, feel free to ping @lead')

        button = discord.ui.Button(
            label='Click to apply!',
            url='https://example.com'
        )

        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(logos(bot))