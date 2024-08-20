import discord
from discord.ext import commands

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_channel_id = 1011212849965715528
        self.starboarded_messages = {}

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        try:
            min_stars = 1
            if (
                str(reaction.emoji) == "⭐"
                and reaction.message.guild.id == 694010548605550675
                and reaction.count >= min_stars
            ):
                starboard_channel_id = 1090249213188784138
                starboard_channel = self.bot.get_channel(starboard_channel_id)
                if not starboard_channel:
                    error_channel = self.bot.get_channel(self.error_channel_id)
                    await error_channel.send(f"Starboard channel (ID: {starboard_channel_id}) not found.")
                    return
                message_id = reaction.message.id
                if message_id not in self.starboarded_messages:
                    stars = reaction.count
                    channel_name = reaction.message.channel.id
                    embed = discord.Embed(color=0x2b2d31)
                    if reaction.message.content:
                        embed.description = reaction.message.content
                    embed.set_author(name=reaction.message.author.display_name, icon_url=reaction.message.author.avatar.url)
                    embed.add_field(name="Original Message", value=f"[Jump!](https://discordapp.com/channels/{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id})")
                    image_url = None
                    if reaction.message.attachments:
                        image_url = reaction.message.attachments[0].url
                    elif reaction.message.content:
                        for word in reaction.message.content.split():
                            if word.lower().endswith((".jpg", ".png", ".gif", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0")):
                                image_url = word
                                break
                    if image_url:
                        embed.set_image(url=image_url)
                    sent_message = await starboard_channel.send(f"⭐ {stars} <#{channel_name}>", embed=embed)
                    self.starboarded_messages[message_id] = (sent_message, channel_name)
                else:
                    stars = reaction.count
                    message, channel_name = self.starboarded_messages[message_id]
                    await message.edit(content=f"⭐ {stars} <#{channel_name}>", embed=message.embeds[0])
        except Exception as e:
            error_channel = self.bot.get_channel(self.error_channel_id)
            await error_channel.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Starboard(bot))