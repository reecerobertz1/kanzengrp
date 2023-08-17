import discord
from discord.ext import commands
from dispie import EmbedCreator
from examples.embed_creator.embed_options import options

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def embednew(self, ctx: commands.Context):
        """Embed Generator With Default Embed"""
        view = EmbedCreator(bot=self.bot)
        embed = discord.Embed(title="This is title", description="Use the dropdown menu to edit my sections!", color=0x927faf)
        embed.set_author("Welcome to embed builder.", icon_url="https://cdn.discordapp.com/avatars/849682093575372841/f04c5815341216fdafe736a2564a4d09.png?size=1024")
        embed.set_footer(text="Footer", icon_url="https://cdn.discordapp.com/avatars/849682093575372841/f04c5815341216fdafe736a2564a4d09.png?size=1024")
        await ctx.send(embed=embed, view=view)

print("loaded cogs.embed")

async def setup(bot):
    await bot.add_cog(Embed(bot))