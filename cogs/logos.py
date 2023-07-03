import discord
from discord.ext import commands

class logos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def logocommandwithbuttons(self, ctx):
        embed = discord.Embed(
            title='<:brazy_milksip:958479364184490075> : Aura Logos',
            description='<a:greenarrow:1123286634629169203> Please make sure you watermark the logos!\n<a:greenarrow:1123286634629169203> Use the watermark on every edit\n<a:greenarrow:1123286634629169203> Do not share this link with anyone outside the group!',
            color=0x2b2d31
        )
        embed.set_footer(text='Made us some logos? send them to a lead or co lead!')
        embed.set_image(url='https://cdn.discordapp.com/attachments/1003438198862659644/1125109046316380230/TXT-2-2048x1365.jpg')

        button = discord.ui.Button(
            label='Click here for logos!',
            url='https://mega.nz/folder/fNkhXaTZ#HESDVux7S8DrUXYgiexxmg'
        )

        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)
        await ctx.send('#𝗮𝘂𝗿𝗮𝗴𝗿𝗽')

    @commands.command()
    async def daegupartner(self, ctx):
        embed = discord.Embed(
            title='<:members:1119069738493026364> : DAEGUTOWN FORMS',
            description='<a:redarrow:1123372633182982155> editing server\n<a:redarrow:1123372633182982155> amazing logos + custom bot\n<a:redarrow:1123372633182982155> booster pack | booster form',
            color=0x2b2d31
        )

        button = discord.ui.Button(
            label='Click here to join Daegu Forms!',
            url='https://discord.gg/R5d7TXVdcj'
        )
        embed.set_footer(text='Go support our partners!')
        embed.set_thumbnail(url='https://cdn.discordapp.com/icons/901409710572466217/f8973672eb44f06548685f4ff8aa5b26.png?size=1024')
        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def aurapartner(self, ctx):
        embed = discord.Embed(
            title='<:frogyay:1123652434913402950> : Aura Forms',
            description='<a:greenarrow:1123286634629169203> editing server\n<a:greenarrow:1123286634629169203> cute aesthetic logos\n<a:greenarrow:1123286634629169203> custom bot\n<a:greenarrow:1123286634629169203> recruitment happening now!',
            color=0x2b2d31
        )

        button = discord.ui.Button(
            label='Click here to join Aura Forms!',
            url='https://discord.gg/edDCM3JUvM'
        )
        embed.set_footer(text='Go support our partners!')
        embed.set_thumbnail(url='https://cdn.discordapp.com/icons/1123347338841313331/b66ab79181757db75af6661670992a33.png?size=1024')
        view = discord.ui.View()
        view.add_item(button)

        await ctx.send('@everyone', embed=embed, view=view)

    @commands.command()
    async def kanzenpartner(self, ctx):
        embed = discord.Embed(
            title='<a:Lumi_penguin_fall:1122607666578063531> : Kanzen Forms',
            description='<:pr_dash:1123654552843993099> editing group\n<:pr_dash:1123654552843993099> cute logos\n<:pr_dash:1123654552843993099> custom bot',
            color=0x2b2d31
        )
        embed.set_footer(text='Go support our partners!')
        button = discord.ui.Button(
            label='Click here to join Kanzen Forms!',
            url='https://discord.gg/9MqbUTYthE'
        )

        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def answerlol(self, ctx):
        embed = discord.Embed(
            title='New Update!',
            description='New celebs have been added to the `+who2edit` command!\nthere is now members from:\nLesserafim\nItzy\nStray Kids\nTXT\nAespa\nAteez\nSeventeen\nTwice\nP1harmony\nNew Jeans\nEnhypen!\n If you have any other ideas for new commands or other idols/celebs to add to `+who2edit` you can either do `+suggest` or ping Reece!',
            color=0x2b2d31
        )
        embed.set_footer(text="Use the command in Hoshi's channel!")
        await ctx.send('<@&1122999466438438962>', embed=embed)


async def setup(bot):
    await bot.add_cog(logos(bot))