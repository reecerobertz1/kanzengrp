import discord
from discord.ext import commands

class buildembed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def buildembed(self, ctx):
        def check_author(m):
            return m.author == ctx.author

        async def ask_question(question):
            message = await ctx.send(question)
            response = await self.bot.wait_for('message', check=check_author)
            await message.delete()
            await response.delete()
            return response.content

        async def ask_confirmation():
            message = await ctx.send("Are you finished with this embed?\nReact with ✅ to send the embed, or ❌ to continue editing.")
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            reaction, _ = await self.bot.wait_for('reaction_add', check=lambda r, u: u == ctx.author and str(r.emoji) in ["✅", "❌"])
            await message.clear_reactions()
            return str(reaction.emoji)

        title = await ask_question("What should the title be? (Type 'X' to skip)")
        description = await ask_question("What should the description be? (Type 'X' to skip)")
        thumbnail_url = await ask_question("Enter the thumbnail URL (Type 'X' to skip)")
        image_url = await ask_question("Enter the image URL (Type 'X' to skip)")
        footer = await ask_question("What should the footer be? (Type 'X' to skip)")
        color_input = await ask_question("What should the color be? (Type 'X' to skip or enter a hexadecimal color code)")

        if color_input.lower() == 'x':
            color = None
        else:
            try:
                color = int(color_input, 16)
            except ValueError:
                await ctx.send("Invalid color code. Using default color.")
                color = None

        embed = discord.Embed(title=title, description=description, color=color)
        if thumbnail_url.lower() != 'x':
            embed.set_thumbnail(url=thumbnail_url)
        if image_url.lower() != 'x':
            embed.set_image(url=image_url)
        if footer.lower() != 'x':
            embed.set_footer(text=footer)

        message = await ctx.send(embed=embed)
        await ctx.message.delete()

        confirmation = await ask_confirmation()
        if confirmation == "❌":
            await ctx.invoke(self.buildembed)



async def setup(bot):
    await bot.add_cog(buildembed(bot))