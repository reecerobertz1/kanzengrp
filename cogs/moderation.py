from datetime import datetime
import discord
from discord.ext import commands
from interactions import SlashContext

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

async def setup(bot):
    await bot.add_cog(Moderation(bot))