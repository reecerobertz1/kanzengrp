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
        embed = view.get_default_embed  # Remove parentheses here
        await ctx.send(embed=embed, view=view)

print("loaded cogs.embed")

async def setup(bot):
    await bot.add_cog(Embed(bot))