import discord
from discord.ext import commands

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.error_channel_id = 1136384691671416932

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        try:
            min_stars = 1  # Adjust this as needed
            if str(reaction.emoji) == "⭐" and reaction.message.guild.id == 1121841073673736215 and reaction.count >= min_stars:
                starboard_channel_id = 1136384691671416932
                starboard_channel = self.bot.get_channel(starboard_channel_id)

                if not starboard_channel:
                    error_channel = self.bot.get_channel(self.error_channel_id)
                    await error_channel.send(f"Starboard channel (ID: {starboard_channel_id}) not found.")
                    return

                embed = discord.Embed(title="Starboard Message")

                if reaction.message.content:
                    embed.description = reaction.message.content

                embed.set_author(name=reaction.message.author.display_name, icon_url=reaction.message.author.avatar_url)
                embed.add_field(name="Original Message", value=f"[Jump!](https://discordapp.com/channels/{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id})")

                if reaction.message.attachments:
                    image_url = reaction.message.attachments[0].url
                    embed.set_image(url=image_url)

                await starboard_channel.send(embed=embed)

        except Exception as e:
            error_channel = self.bot.get_channel(self.error_channel_id)
            await error_channel.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Starboard(bot))