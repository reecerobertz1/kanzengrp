import discord
from discord.ext import commands

class logos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def logo(self, ctx):
        embed = discord.Embed(
            title='<:brazy_milksip:958479364184490075> : Aura Logos',
            description='<a:greenarrow:1123286634629169203> Please make sure you watermark the logos!\n<a:greenarrow:1123286634629169203> Use the watermark on every edit\n<a:greenarrow:1123286634629169203> Do not share this link with anyone outside the group!',
            color=0x2b2d31
        )
        embed.set_footer(text='If you need any help, feel free to ping @lead')

        button = discord.ui.Button(
            label='Click here for logos!',
            url='https://example.com'
        )

        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(logos(bot))