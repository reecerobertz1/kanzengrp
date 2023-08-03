import discord
from discord.ext import commands

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_channel_id = 1136384691671416932
        self.starboarded_messages = {}

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        try:
            min_stars = 1
            if (
                str(reaction.emoji) == "⭐"
                and reaction.message.guild.id == 1121841073673736215
                and reaction.count >= min_stars
            ):
                starboard_channel_id = 1136384691671416932
                starboard_channel = self.bot.get_channel(starboard_channel_id)

                if not starboard_channel:
                    error_channel = self.bot.get_channel(self.error_channel_id)
                    await error_channel.send(f"Starboard channel (ID: {starboard_channel_id}) not found.")
                    return

                message_id = reaction.message.id

                if message_id not in self.starboarded_messages:
                    # Send a new message to the starboard
                    stars = reaction.count
                    channel_name = reaction.message.channel.id
                    embed = discord.Embed(color=0x2b2d31)

                    if reaction.message.content:
                        embed.description = reaction.message.content

                    embed.set_author(name=reaction.message.author.display_name, icon_url=reaction.message.author.avatar.url)
                    embed.add_field(name="Original Message", value=f"[Jump!](https://discordapp.com/channels/{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id})")

                    if reaction.message.attachments:
                        image_url = reaction.message.attachments[0].url
                        embed.set_image(url=image_url)

                    sent_message = await starboard_channel.send(f"⭐ {stars} <#{channel_name}>", embed=embed)
                    self.starboarded_messages[message_id] = (sent_message, channel_name)
                else:
                    # Edit the existing message on the starboard
                    stars = reaction.count
                    message, channel_name = self.starboarded_messages[message_id]
                    await message.edit(content=f"⭐ {stars} <#{channel_name}>", embed=message.embeds[0])

        except Exception as e:
            error_channel = self.bot.get_channel(self.error_channel_id)
            await error_channel.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Starboard(bot))