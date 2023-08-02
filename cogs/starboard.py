import discord
from discord.ext import commands

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Starboard cog is ready.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Check if the reaction is a star (⭐) emoji
        if str(reaction.emoji) == "⭐" and reaction.message.guild.id == 1121841073673736215 and reaction.count >= min_stars:
            # Set the minimum number of stars required for a message to be starred
            min_stars = 3

            # Check if the reaction count is greater than or equal to the minimum stars required
            if reaction.count >= min_stars:
                # Get the starboard channel by ID
                starboard_channel = self.bot.get_channel(1136384691671416932)

                # Create the embed
                embed = discord.Embed(title="Starboard", description=reaction.message.content, color=0x2b2d31)
                embed.set_author(name=reaction.message.author.display_name, icon_url=reaction.message.author.avatar_url)

                # Add a field for the original message link
                jump_link = f"[jump!](https://discord.com/channels/{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id})"
                embed.add_field(name="Original Message", value=jump_link)

                # Check if the message has an image
                if reaction.message.attachments:
                    # Use the first attachment as the image URL
                    image_url = reaction.message.attachments[0].url
                    embed.set_image(url=image_url)

                # Send the embed to the starboard channel
                await starboard_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Starboard(bot))