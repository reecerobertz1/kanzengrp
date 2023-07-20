from typing import Optional
import discord
from discord.ext import commands

class buildembed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['be', 'embed'])
    @commands.has_permissions(manage_guild=True)
    async def buildembed(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None):
        """makes a custom embed
        
        Parameters
        -----------
        channel: discord.TextChannel, optional
            the channel to send the embed in
        """

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()

        async def ask_question(question):
            message = await ctx.send(question)
            response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            await message.delete()
            await response.delete()
            return response.content

        title = await ask_question("What title do you want your embed to have?")
        description = await ask_question("Okay! What do you want your description to be?")
        color_input = await ask_question("What color do you want your embed to be? (in hex; e.g., 2B2D31)")

        if color_input.lower() == 'x':
            color = 0x60e5fc
        else:
            try:
                color = int(color_input, 16)
            except ValueError:
                await ctx.send("Invalid color code. Using default color.")
                color = 0x60e5fc

        embed = discord.Embed(title=title, description=description, colour=color)

        thumbnail_url = await ask_question("Enter the thumbnail URL (Type `X` to skip)")
        if thumbnail_url.lower() != 'x':
            embed.set_thumbnail(url=thumbnail_url)

        image_url = await ask_question("Enter the image URL (Type `X` to skip)")
        if image_url.lower() != 'x':
            embed.set_image(url=image_url)

        fields_completed = False
        while not fields_completed:
            field_name = await ask_question("What do you want the name of the field to be? (Type `X` to finish adding fields)")
            if field_name.lower() == 'x':
                fields_completed = True
            else:
                field_value = await ask_question("What do you want the value of the field to be?")
                inline_input = await ask_question("Do you want this field to be inline? (yes/no)")
                if inline_input.lower() == 'yes':
                    inline = True
                else:
                    inline = False
                embed.add_field(name=field_name, value=field_value, inline=inline)

        message = await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(buildembed(bot))