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

    @commands.command()
    async def embed2(self, ctx: commands.Context):
        """Embed Generator With Default Embed And Author Check So Only The Invoker Can Use The Editor"""
        # Creates a instance of EmbedCreator class
        view = EmbedCreator(bot=self.bot)
        async def check(interaction: discord.Interaction):
                if interaction.user.id == ctx.author.id:
                    return True
                else:
                    await interaction.response.send_message(f"Only {ctx.author} can use this interaction!", ephemeral=True)
                    return False
        view.interaction_check = check
        await ctx.send(embed=view.get_default_embed, view=view)


    @commands.command()
    async def embed3(self, ctx: commands.Context):
        """Embed Generator With Default Embed And Customized Options
        You can view it in the embed_options.py file also you can customize everything in the embed creator (excepts message responses.)
        """
        # Creates a instance of EmbedCreator class
        view = EmbedCreator(bot=self.bot, **options)
        await ctx.send(embed=view.get_default_embed, view=view)

print("loaded cogs.embed")

async def setup(bot):
    await bot.add_cog(Embed(bot))