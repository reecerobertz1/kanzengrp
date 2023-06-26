import discord
from discord.ext import commands


class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.starboard_channel_id = 1122932049293094953

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        starboard_channel = self.bot.get_channel(self.starboard_channel_id)

        if payload.channel_id == self.starboard_channel_id:
            return  # Ignore reactions added in the starboard channel

        if starboard_channel is None:
            return  # Starboard channel not found

        if payload.emoji.name != '⭐':
            return  # Ignore reactions that are not ⭐

        message_channel = self.bot.get_channel(payload.channel_id)
        message = await message_channel.fetch_message(payload.message_id)

        # Check if the reacted message is from the bot itself
        if message.author == self.bot.user:
            return

        # Check if the reacted message is already in the starboard
        async for star_message in starboard_channel.history():
            if star_message.reference and star_message.reference.message_id == message.id:
                return

        # Check if the reacted message has enough stars (1 star in this case)
        if payload.member is not None and payload.count >= 1:
            embed = discord.Embed(color=0x2b2d31)
            embed.add_field(name="Author", value=message.author.mention, inline=False)
            embed.add_field(name="Content", value=message.content, inline=False)

            await starboard_channel.send(f"{message.author.mention} ⭐ Your message in {message.channel.mention} has been starred:", embed=embed)

    @commands.command()
    async def star(self, ctx, message_id: int):
        starboard_channel = self.bot.get_channel(self.starboard_channel_id)

        if starboard_channel is None:
            await ctx.send("Starboard channel not found.")
            return

        try:
            message = await ctx.fetch_message(message_id)
        except discord.NotFound:
            await ctx.send("Message not found.")
            return

        # Check if the reacted message is already in the starboard
        async for star_message in starboard_channel.history():
            if star_message.reference and star_message.reference.message_id == message.id:
                await ctx.send("The message is already in the starboard.")
                return

        embed = discord.Embed(color=0xffac33)
        embed.add_field(name="Author", value=message.author.mention, inline=False)
        embed.add_field(name="Content", value=message.content, inline=False)

        await starboard_channel.send(f"{message.author.mention} ⭐ Your message in {message.channel.mention} has been starred:", embed=embed)


async def setup(bot):
    await bot.add_cog(starboard(bot))