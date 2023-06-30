import discord
from discord.ext import commands

class logos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def logocommandwithbuttons(self, ctx):
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
        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def aurapartner(self, ctx):
        embed = discord.Embed(
            title='<:frogyay:1123652434913402950> : Aura Forms',
            description='<a:greenarrow:1123286634629169203> editing server\n<a:greenarrow:1123286634629169203> cute aesthetic logos\n<a:greenarrow:1123286634629169203> custom bot',
            color=0x2b2d31
        )

        button = discord.ui.Button(
            label='Click here to join Aura Forms!',
            url='https://discord.gg/edDCM3JUvM'
        )
        embed.set_footer(text='Go support our partners!')
        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

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
    async def daegulogos(self, ctx):
        embed = discord.Embed(
            title='> <:members:1119069738493026364> : Daegutown Logos',
            description='<a:redarrow:1063328187599302716> Watermark the logos!\n<a:redarrow:1063328187599302716> Always use the group hashtag\n<a:redarrow:1063328187599302716> Send your edit [here](https://discord.com/channels/896619762354892821/1106539453440331826) for xp!\nInfo about xp is pinned in that channel',
            color=0x2b2d31
        )
        embed.set_footer(text='Go support our partners!')
        button = discord.ui.Button(
            label='Click here for the logos!',
            url='https://mega.nz/folder/4QZWTBjR#ZmyJUH2HHj8lFrwkY1BrPw'
        )

        view = discord.ui.View()
        view.add_item(button)
        await ctx.send('#𝗗𝗔𝗘𝗚𝗨𝗧𝗢𝗪𝗡')
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(logos(bot))