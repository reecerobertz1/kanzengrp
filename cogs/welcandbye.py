import discord
from discord.ext import commands

class welcandleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1121921106706710567  # Replace with your desired channel ID

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            mention = member.mention
            await channel.send(f"{mention}")

            embed = discord.Embed(
                title=f"Welcome to Kanzen {member.name}!",
                description=f"Welcome {mention} to the kanzen!\n"
                            f"﹒Please read the [Rules](https://discord.com/channels/1121841073673736215/1121913361169391666)\n"
                            f"﹒Go get your [Roles](https://discord.com/channels/1121841073673736215/1121922077071507476)\n"
                            f"﹒The logos are [here](https://discord.com/channels/1121841073673736215/1121922101708857344)",
                color=0x2b2d31
            )
            embed.set_footer(text='Have fun! Thank you for joining <3')

            # Fetch the member's avatar URL
            avatar_url = member.avatar_url_as(static_format='png')

            # Create a discord.File object with the avatar URL
            avatar_file = await avatar_url.read()
            file = discord.File(avatar_file, filename="avatar.png")

            # Set the thumbnail using the discord.File object
            embed.set_thumbnail(url="attachment://avatar.png")

            # Send the embed and file separately
            await channel.send(embed=embed)
            await channel.send(file=file)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            mention = member.mention
            await channel.send(f"{mention}")

            embed = discord.Embed(
                title="Goodbye!",
                description=f"Goodbye {mention}! We'll miss you!",
                color=0x2b2d31
            )
            embed.set_footer(text='Hope to see you again soon <3')

            # Fetch the member's avatar URL
            avatar_url = member.avatar_url_as(static_format='png')

            # Create a discord.File object with the avatar URL
            avatar_file = await avatar_url.read()
            file = discord.File(avatar_file, filename="avatar.png")

            # Set the thumbnail using the discord.File object
            embed.set_thumbnail(url="attachment://avatar.png")

            # Send the embed and file separately
            await channel.send(embed=embed)
            await channel.send(file=file)

async def setup(bot):
    await bot.add_cog(welcandleave(bot))