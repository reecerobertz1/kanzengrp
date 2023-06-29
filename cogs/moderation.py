import asyncio
from datetime import datetime
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

    @commands.command()
    async def uptime(self, ctx):
        current_time = datetime.now()
        uptime = current_time - self.start_time

        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

        await ctx.reply(f"Bot Uptime: {uptime_str}")

        self.deleted_messages = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.deleted_messages[message.channel.id] = message

    @commands.command()
    async def snipe(self, ctx):
        channel = ctx.channel
        deleted_message = self.deleted_messages.get(channel.id)

        if deleted_message is None:
            await ctx.send("There are no recently deleted messages in this channel.")
            return

        author_mention = deleted_message.author.mention
        content = deleted_message.content

        embed = discord.Embed(color=0xff0000)
        embed.set_author(name="Deleted Message")
        embed.add_field(name="Author", value=author_mention, inline=False)
        embed.add_field(name="Content", value=content, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def addrole(self, ctx, role: discord.Role, user: discord.Member):
        await user.add_roles(role)
        await ctx.reply(f'Successfully added {role.mention} to {user.mention}')

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def removerole(self, ctx, role: discord.Role, user: discord.Member):
        await user.remove_roles(role)
        await ctx.reply(f'Successfully removed {role.mention} from {user.mention}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for reason: {reason}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for reason: {reason}')

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds

        await ctx.reply(f"Pong! :ping_pong: Latency: {latency}ms")


    @commands.command()
    async def createrole(self, ctx, role_name, role_color):
        guild = ctx.guild

        # Check if the role already exists
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if existing_role:
            await ctx.send(f"A role with the name '{role_name}' already exists.")
            return

        # Create the role
        try:
            role = await guild.create_role(name=role_name, color=discord.Color(role_color))
            await ctx.send(f"Role '{role_name}' has been created with color #{role.color.value:06x}.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to create roles.")
        except discord.HTTPException:
            await ctx.send("Failed to create the role.")

    @commands.command()
    async def openapps(self, ctx):
        embed = discord.Embed(
            title='Apply Here!',
            description='Please make sure you read the [Rules](https://discord.com/channels/1122181605591621692/1122195332516810873) and the info below!',
            color=0x2b2d31
        )
        embed.add_field(name='Application Rules', value='<:arrow_00000:1121934367569227837> Make sure you are following [@remqsi](https://www.instagram.com/remqsi/) and the [group account](https://www.instagram.com/uzaigrp/)\n<:arrow_00000:1121934367569227837> Please only send one form!', inline=False)
        embed.add_field(name='Application Info', value='<:arrow_00000:1121934367569227837> Velocity edits are an **auto decline**\n<:arrow_00000:1121934367569227837> You will receive an acceptence message if you are accepted, and a decline message if you get declined.\n<:arrow_00000:1121934367569227837> There is no doing reapps so choose the edit you want to apply with wisely\n <:arrow_00000:1121934367569227837> Make sure you answer all the questions on the form before sending!\n<:arrow_00000:1121934367569227837> Apply with your best edit. We look for creative and smooth edits', inline=False)
        embed.set_image(url='https://cdn.discordapp.com/attachments/1122195332516810874/1122208438345281666/IMG_2232_00000_00000.png')
        embed.set_footer(text='If you need any help, feel free to ping @lead')

        button = discord.ButtonStyle.link(label='Click to apply!', url='https://example.com')

        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)
        
    @commands.command()
    async def roles(self, ctx):
        embed = discord.Embed(
            title='✦ Colour Roles',
            description="<:red:1122922281027522670> <@&1122919355273986138>\n<:peach:1122922314430959676> <@&1122920134223335524>\n<:orange:1122922351282098246> <@&1122920245267542106>\n<:yellow:1122922412250513528> <@&1122920319557046413>\n<:lightgreen:1122922505049473248> <@&1122920394735763526>\n<:green:1122922547172888627> <@&1122920478194028646>\n<:teal:1122922731520938056> <@&1122920653876633670>\n<:lightteal:1122922687375876191> <@&1122920539766407178>\n<:lightblue:1122922756657385523> <@&1122920731529973841>\n<:blue:1122922771052245063> <@&1122920821216792617>\n<:purple:1122922810122190949> <@&1122920986086477964>\n<:lavender:1122922908713504908> <@&1122920902858899456>\n<:ezgif52386587f75:1123256905289191484> <@&1122921065744707634>\n<:lightpink:1122922955488383046> <@&1122921134174769304>\n<:white_00000:1122923529994764408> <@&1122921232145338480>\n<:black:1122922973234475019> <@&1122921204630696009>",
            color=0x2b2d31
        )
        embed.set_footer(text='- React with the emojis below to select your roles')
        await ctx.send(embed=embed)

    @commands.command()
    async def roles2(self, ctx):
        embed = discord.Embed(
            title='✦ Pronouns',
            description="<a:pr_lnumber_1:1122926192018870382>  <@&1121852424353755137> \n<a:pr_lnumber_2:1122926359002493048> <@&1122635691487137884> \n<a:pr_lnumber_3:1122926388224200785> <@&1122635724559241317> \n<a:pr_lnumber_4:1122926425918414880> <@&1122635760445706321> \n<a:pr_lnumber_5:1122926454133493800> <@&1122635742229835897> \n<a:pr_lnumber_6:1122926485095850024> <@&1122635791844266064>",
            color=0x2b2d31
        )
        embed.set_footer(text='- React with the emojis below to select your roles')
        await ctx.send(embed=embed)

    @commands.command()
    async def roles3(self, ctx):
        embed = discord.Embed(
            title='✦ Editing Programs',
            description="<:aftereffects:1122925440240193649> <@&1122921620047147131> \n<:alightmotion:1122925541901734022> <@&1122921640288850025> \n<:videostar:1122925486209777704> <@&1122921660320858274>",
            color=0x2b2d31
        )
        embed.set_footer(text='- React with the emojis below to select your roles')
        await ctx.send(embed=embed)

    @commands.command()
    async def roles4(self, ctx):
        embed = discord.Embed(
            title='✦ Game Roles',
            description="<:fortnite_00004:1122978882816069702> <@&1122921698367389756> \n<:MCicon:1122978908124479488> <@&1122979205324480553> \n<:ROBLOXicon:1122978966651805856> <@&1122921713823395851> \n<:Valoranticon:1122979072704782337> <@&1122921729384271963> \n<:gtaV:1122978939539837129> <@&1122921800502878259>",
            color=0x2b2d31
        )
        embed.set_footer(text='- React with the emojis below to select your roles')
        await ctx.send(embed=embed)

    @commands.command()
    async def roles5(self, ctx):
        embed = discord.Embed(
            title='✦ Extra Roles',
            description="<:Lumi_purple_star:1122927969086734456> <@&1122655473368314017> \n<a:pr_lnumber_1:1122926192018870382> <@&1122927309813461143> \n<a:pr_lnumber_2:1122926359002493048> <@&1122928933575335936> \n<a:pr_lnumber_3:1122926388224200785> <@&1122926819553841162> \n<a:pr_lnumber_4:1122926425918414880> <@&1122926767192154142> \n<a:pr_lnumber_5:1122926454133493800> <@&1122926835936809090>",
            color=0x2b2d31
        )
        embed.set_footer(text='- React with the emojis below to select your roles')
        await ctx.send(embed=embed)

    @commands.command()
    async def rules(self, ctx):
        embed = discord.Embed(
            title='<a:3b56330f710c3a978f27c9cc7e099180:1122633149764088030> : __Kanzen rules__',
            description="",
            color=0x2b2d31
        )
        embed.set_footer(text='If you need to go inactive, use the command +ia')
        embed.add_field(name='✦ Group Rules :', value='• always watermark the logos\n• do not share the logos link outside the server!\n• make sure you are following [@remqsi](https://www.instagram.com/remqsi/) + [@kanzengrp](https://www.instagram.com/kanzengrp/)!\n• if you do ever decide to leave the grp, or move accounts. please let reece know!', inline= False)
        embed.add_field(name='✦ Chat Rules :', value='• please be as active as possible!\n• using any slurs / words that can be offensive!\n• please set your nickname as "your name | username"\n• no impersonation as other editors\n• no trash talking other editors and groups!')
        embed.set_image(url='https://serving.photos.photobox.com/0814269535cc11c4fac2f41446e80b4f01b10a9db227f0f8574292f78abe9067e6361440.jpg')
        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        suggestion_channel_id = 1124038649814724638  

        suggestion_channel = self.bot.get_channel(suggestion_channel_id)
        if suggestion_channel:
            embed = discord.Embed(title="New Suggestion", description=suggestion, color=0x2b2d31)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

            suggestion_message = await suggestion_channel.send(f"Suggestion made by {ctx.author.mention}", embed=embed)
            await suggestion_message.add_reaction("✅")
            await suggestion_message.add_reaction("❌")

            confirmation_message = await ctx.send(f"Suggestion has been sent to {suggestion_channel.mention}.")
            await asyncio.sleep(5)
            await ctx.message.delete()
            await confirmation_message.delete()
        else:
            await ctx.send("Failed to find the suggestion channel.")


async def setup(bot):
    await bot.add_cog(Moderation(bot))