import discord
from discord.ext import commands

class logos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def logocommandwithbuttons(self, ctx):
        embed = discord.Embed(
            title='<a:kanzenflower:1128154723262943282> : Kanzen Logos',
            description='<a:bounceyarrow:1128155233437106187> Please make sure you watermark the logos!\n<a:bounceyarrow:1128155233437106187> Use the watermark on every edit\n<a:bounceyarrow:1128155233437106187> Do not share this link with anyone outside the group!',
            color=0x2b2d31
        )
        embed.set_footer(text='Made us some logos? send them to Reece!')
        embed.set_image(url='https://cdn.discordapp.com/attachments/1121841074512605186/1128394231115948072/theme_3_00000.png')

        button = discord.ui.Button(
            label='Click here for logos!',
            url='https://mega.nz/folder/J40zCTYY#L73pTeQKWpCh15wpuQaIFA'
        )

        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)
        await ctx.send('#𝗞𝗮𝗻𝘇𝗲𝗻𝗴𝗿𝗽')

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
            description='<a:greenarrow:1123286634629169203> editing server\n<a:greenarrow:1123286634629169203> cute aesthetic logos\n<a:greenarrow:1123286634629169203> custom bot',
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

        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def kanzenpartner(self, ctx):
        embed = discord.Embed(
            title='<a:Lumi_penguin_fall:1122607666578063531> : Kanzen Forms',
            description='<a:bounceyarrow:1126865547255091343> editing group\n<a:bounceyarrow:1126865547255091343> cute logos\n<a:bounceyarrow:1126865547255091343> custom bot\n<a:bounceyarrow:1126865547255091343> recruit happening now!',
            color=0x2b2d31
        )
        embed.set_footer(text='Go support our partners!')
        embed.set_thumbnail(url='https://cdn.discordapp.com/icons/1121841073673736215/ea48ddf8734b328c38e38accbce6bc25.png?size=1024')
        button = discord.ui.Button(
            label='Click here to join Kanzen Forms!',
            url='https://discord.gg/9MqbUTYthE'
        )

        view = discord.ui.View()
        view.add_item(button)

        await ctx.send('@everyone', embed=embed, view=view)

    @commands.command()
    async def kanzenformsrules(self, ctx):
        embed = discord.Embed(
            title='<a:Lumi_penguin_fall:1122607666578063531> : Kanzen Rules',
            color=0x2b2d31
        )
        embed.set_image(url='https://cdn.discordapp.com/attachments/1122181606254330008/1127011636457250997/jisoo_and_rose_photo_00000.png')
        embed.set_footer(text='If you need help, do +qna')
        embed.add_field(name='Server Rules', value="<a:bounceyarrow:1126865547255091343> Be respectful of everyone\n<a:bounceyarrow:1126865547255091343> No trash talk of other groups or editors\n<a:bounceyarrow:1126865547255091343> No impersonation of other edits (you will be banned)\n<a:bounceyarrow:1126865547255091343> Use channels for their intended purpose\n<a:bounceyarrow:1126865547255091343> No spamming the lead for things! be patient", inline=False)
        embed.add_field(name='Application Rules', value="<a:bounceyarrow:1126865547255091343> Be patient with forms, you will get an answer at some point\n<a:bounceyarrow:1126865547255091343> Apply with Instagram or Streamable links only!\n<a:bounceyarrow:1126865547255091343> Follow Discord's [terms](https://discord.com/terms) and [guidelines](https://discord.com/guidelines)")
        button = discord.ui.Button(
            label='Follow kanzengrp',
            url='https://www.instagram.com/kanzengrp/'
        )
        button2 = discord.ui.Button(
            label='Follow remqsi',
            url='https://www.instagram.com/remqsi/'
        )

        view = discord.ui.View()
        view.add_item(button)
        view.add_item(button2)

        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def newupdatehoshiupdates(self, ctx):
        embed = discord.Embed(
            title='New update!',
            color=0x2b2d31
        )
        embed.set_footer(text="Go and use these commands in Hoshi's channel!")
        embed.add_field(name='Create Custom Commands', value='Create your own command with Hoshi with the `+newcmd` command!\nYou can create as many commands as you would like.\n\n**Example:**\n`+newcmd (command) (responce)`\nThe command name is what you would say `+hello` the responce is what Hoshi will say `Hi`\nAny inappropriate commands will be removed!\nYou can also do `+listcmds` to see all the commands added\nOr if you have made a mistake with your command, do `+removecmd` and then remove it\nIf you get stuck and confused, ask other zennies or <@609515684740988959> for help!\n\n**Disclaimer**\nThis command and the custom commands can only be used in Kanzens server!', inline=False)
        await ctx.send('<@&1122655473368314017>', embed=embed)


async def setup(bot):
    await bot.add_cog(logos(bot))