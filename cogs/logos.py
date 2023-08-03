from typing import Any
import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import View, Select
import asyncio

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
            description='<a:bounceyarrow:1126865547255091343> editing group\n<a:bounceyarrow:1126865547255091343> cute logos\n<a:bounceyarrow:1126865547255091343> custom bot\n<a:bounceyarrow:1126865547255091343> group activities',
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

        await ctx.send(embed=embed, view=view)

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
    async def kda(self, ctx):
        embed = discord.Embed(
            title='<a:bearhugz:1131122693085868172> : Welcome to the server!',
            color=0x2b2d31
        )
        embed.set_image(url='https://cdn.discordapp.com/attachments/1131006428631539773/1131124927685214268/blackpink-jisoo-jennie-rose-lisa-k-pop-singers-red-2048x1536-4679.jpg')
        embed.set_footer(text='Thank you for joining!')
        embed.add_field(name='Group Leads', value="<a:bounceyarrow:1126865547255091343> **kanzengrp** - <@609515684740988959>\n<a:bounceyarrow:1126865547255091343> **daegutowngrp** - <@609515684740988959> + <@541538705106534423>\n<a:bounceyarrow:1126865547255091343> **auragrps** - <@609515684740988959> + <@718144988688679043> + <@603077306956644353>", inline=False)
        button = discord.ui.Button(label='Follow kanzengrp', url='https://www.instagram.com/kanzengrp/')
        button2 = discord.ui.Button(label='Follow daegutowngrp',url='https://www.instagram.com/daegutowngrp/')
        button3 = discord.ui.Button(label='Follow auragrps',url='https://www.instagram.com/auragrps/')

        view = discord.ui.View()
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)

        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def newupdatehoshiupdates(self, ctx):
        servers = [{'server_id': 1121841073673736215,'channel_id': 1122655402899800234,'ping_role': '<@&1122655473368314017>'},{    'server_id': 957987670787764224,    'channel_id': 1122242141037547531,    'ping_role': '<@&1122999466438438962>'},{    'server_id': 896619762354892821,    'channel_id': 1063639288178286663,    'ping_role': '<@&939923109413290005>'}]

        embed = discord.Embed(
            title='New update!',
            color=0x2b2d31
        )
        embed.set_footer(text="Go and use these commands in Hoshi's channel!")
        embed.add_field(name='Change to audio command', value='instead of doing the usual `+addaudio` to add an audio and `+audio` to get an audio, you can now do `+addsoft` `+softaudio` to add and get soft audios and `+addhot` `+hotaudios` to add and get hot audios!\nthe old commands have been removed and do not work anymore!\nif you have any other ideas for commands and games to add to hoshi, you can do `+suggest (type suggestion here)` to suggest or go to the suggestions channel if youre in daegu!', inline=False)

        for server_data in servers:
            server = self.bot.get_guild(server_data['server_id'])
            channel = server.get_channel(server_data['channel_id'])
            await channel.send(server_data['ping_role'], embed=embed)

    @commands.command()
    async def lol(self, ctx):
        embed = discord.Embed(title="Welcome to Editors Block!", description="Thank you for joining Editors Block! This is a community server made for all types of editors.\nFeel free to ping @owners or @staff if you need any help.\n\nAlso, we will do group recruits for the groups Kanzen, Aura, and Daegu!", color=0x2b2d31)
        embed.set_footer(text="Follow the groups below!", icon_url='https://cdn.discordapp.com/icons/1131003330810871979/128ca9e19d2f0aa0e41c99310673dfac.png?size=1024')

        button = discord.ui.Button(label="Kanzen", url="https://www.instagram.com/kanzengrp/", emoji="<:kanzen:1136701626799886366>")
        button2 = discord.ui.Button(label="Aura", url="https://www.instagram.com/auragrps/", emoji="<:aura:1136701593018978415>")
        button3 = discord.ui.Button(label="Daegu", url="https://www.instagram.com/daegutowngrp/", emoji="<:daegu:1136701608026185879>")

        view = discord.ui.View()
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)

        await ctx.send(embed=embed, view=view)

        embed2 = discord.Embed(title="Owner Info", description="Editors Block is owned by @remqsi, @yoongiaeps, and @taedxck", color=0x2b2d31)
        embed2.set_author(name="Hoshi#3105", icon_url='https://cdn.discordapp.com/avatars/849682093575372841/f04c5815341216fdafe736a2564a4d09.png?size=1024')

        button_rules = discord.ui.Button(label="Server Rules", style=discord.ButtonStyle.primary, custom_id="server_rules")
        button_roles = discord.ui.Button(label="Role Info", style=discord.ButtonStyle.primary, custom_id="role_info")

        view2 = discord.ui.View()
        view2.add_item(button_rules)
        view2.add_item(button_roles)

        await ctx.send(embed=embed2, view=view2)

        def check(interaction):
            return interaction.user == ctx.author and interaction.message.embeds[0].title == "Owner Info"

        try:
            interaction = await self.bot.wait_for('button_click', check=check)
        except Exception:
            return

        if interaction.custom_id == "server_rules":
            embed_rules = discord.Embed(title="Server Rules", description="Here are the server rules:\n1. No spamming.\n2. Be respectful to others.\n3. No NSFW content.\n4. No advertising.\n5. Follow Discord's Terms of Service and Community Guidelines.")
            await interaction.send(embed=embed_rules)
        elif interaction.custom_id == "role_info":
            embed_roles = discord.Embed(title="Role Info", description="Here's some information about the roles in the server:\n- Owner: The owners of the server.\n- Staff: The staff members who help moderate the server.\n- Members: Regular members of the server.")
            await interaction.send(embed=embed_roles)
        

async def setup(bot):
    await bot.add_cog(logos(bot))