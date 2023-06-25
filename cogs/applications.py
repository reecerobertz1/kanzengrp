import json
import random
import discord
from discord.ext import commands




class apps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.accept_role_id = 1122191098006224906
        self.decline_role_id = 1122191119430733835
        self.server_id = 1121841073673736215

    @commands.command()
    async def openapps(self, ctx):
        embed = discord.Embed(
            title='Apply Here!',
            description='Please make sure you read the [Rules](https://discord.com/channels/1122181605591621692/1122195332516810873) and the info below!',
            color=0x2b2d31
        )
        embed.add_field(name='Application Rules', value='• Make sure you are following [@remqsi](https://www.instagram.com/remqsi/) and the [group account](https://www.instagram.com/uzaigrp/)\n• Please only send one form!', inline=False)
        embed.add_field(name='Application Info', value='• Velocity edits are an **auto decline**\n• You will receive an acceptance message if you are accepted, and a decline message if you get declined.\n• There is no redoing applications, so choose the edit you want to apply with wisely.\n• Make sure you answer all the questions on the form before sending!\n• Apply with your best edit. We look for creative and smooth edits', inline=False)
        embed.set_image(url='https://cdn.discordapp.com/attachments/1122195332516810874/1122208438345281666/IMG_2232_00000_00000.png')
        embed.set_footer(text='If you need any help, feel free to ping @lead')

        button = discord.ui.Button(
            label='Click to apply!',
            url='https://example.com'
        )

        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.guild_only()
    async def accept(self, ctx: commands.Context, member: discord.Member):
        if ctx.guild.id != self.server_id:
            await ctx.reply("This command can only be used in the specified server.")
            return

        accept_role = ctx.guild.get_role(self.accept_role_id)
        decline_role = ctx.guild.get_role(self.decline_role_id)
        server = self.bot.get_guild(self.server_id)

        if not accept_role or not decline_role:
            await ctx.reply("Server roles not found.")
            return

        try:
            invite = await server.text_channels[0].create_invite()
        except discord.Forbidden:
            await ctx.reply("I couldn't create an invite. Please try again later.")
            return

        accept_message = f"Hey, you have been accepted! You can join the server here: {invite.url}"

        try:
            await member.send(accept_message)
            await ctx.send("The acceptance message has been sent.")
        except discord.Forbidden:
            await ctx.reply("I couldn't send the acceptance message. Please try again later.")

        await member.add_roles(accept_role)
        await member.remove_roles(decline_role)

    @commands.command()
    @commands.is_owner()  # Restrict command to server owner
    async def decline(self, ctx, member: discord.Member):
        message = "Hey, unfortunately, you have been declined from the group. We will have more recruitment opportunities in the future!"
        await member.send(message)
        await ctx.reply("Decline message sent.")



async def setup(bot):
    await bot.add_cog(apps(bot))