import discord
from discord.ext import commands

class logos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def logo(self, ctx):
        embed = discord.Embed(
            title='<a:Lumi_penguin_fall:1122607666578063531> : Kanzen Logos',
            description='• Please make sure you watermark the logos!\n• Use the watermark on every edit\n• Do not share this link with anyone outside the group!',
            color=0x2b2d31
        )
        embed.set_footer(text='Made us some logos? send them to Reece!')

        button = discord.ui.Button(
            label='Click here for logos!',
            url='https://mega.nz/folder/J40zCTYY#L73pTeQKWpCh15wpuQaIFA'
        )

        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(logos(bot))