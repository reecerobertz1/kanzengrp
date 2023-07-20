import discord
from discord.ext import commands

class buildembed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def createembed(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None):
        """makes a custom embed
        
        Parameters
        -----------
        channel: discord.TextChannel, optional
            the channel to send the embed in
        """

        if channel == None:
            channel = ctx.channel

        await ctx.message.delete()
        first = await ctx.send("What title do you want your embed to have?")

        title1 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        title = title1.content
        await title1.delete()
        await first.delete()
        second = await ctx.send('Okay! What do you want your description to be?')

        desc1 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        desc = desc1.content
        await desc1.delete()
        await second.delete()

        col = await ctx.send('What color do you want your embed to be? (in hex; eg., 2B2D31)')
        color = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        await col.delete()
        await color.delete()

        third = await ctx.send('Are you finished with your embed? Say ``yes`` if you are and ``no`` if you arent!')
        answer1 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if 'yes' in answer1.content:
            await answer1.delete()
            await third.delete()
            embed0 = discord.Embed(title=f'{title}', description=f'{desc}', colour=int(color.content, 16))
            await channel.send(embed=embed0)
        else:
            four = await ctx.send('OK! What do you want the name of the first field to be!')

            name0 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            name1 = name0.content
            await name0.delete()
            await four.delete()
            five = await ctx.send('Cool! What do you want your value to be?')

            value0 = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            value1 = value0.content
            await value0.delete()
            await five.delete()
            embed = discord.Embed(title=f'{title}', description=f'{desc}', colour=0x60e5fc)
            embed.add_field(name=f'{name1}', value=f'{value1}')
            await channel.send(embed=embed)



async def setup(bot):
    await bot.add_cog(buildembed(bot))