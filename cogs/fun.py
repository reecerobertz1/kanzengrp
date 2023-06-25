import io
import os
from typing import Optional
import aiohttp
import discord
from discord.ext import commands
import requests
from PIL import Image

class funcmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




    @commands.command()
    async def dog(self, ctx):
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        image_url = data['message']

        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url=image_url)

        await ctx.reply(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        try:
            response = requests.get('https://api.thecatapi.com/v1/images/search')
            response.raise_for_status()
            data = response.json()
            image_url = data[0]['url']

            embed = discord.Embed(color=0x2b2d31)
            embed.set_image(url=image_url)

            await ctx.reply(embed=embed)
        except (requests.exceptions.RequestException, KeyError):
            await ctx.reply("Sorry, I couldn't fetch a cute cat at the moment. Please try again later.")


    @commands.command()
    async def jail(self, ctx, member: Optional[discord.Member]):
        # Get the user's avatar URL
        member = member or ctx.author
        avatar_url = member.avatar.url

        # Open the avatar image
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar_url)) as response:
                avatar_image = await response.read()

        # Open the jail cell door image
        jail_image = Image.open("jail_door.png").convert("RGBA")

        # Open the avatar image using PIL
        avatar_pil = Image.open(io.BytesIO(avatar_image)).convert("RGBA")
        avatar_pil = avatar_pil.resize((128, 128))

        # Resize the jail cell door image to match the avatar size
        jail_image = jail_image.resize(avatar_pil.size)

        # Composite the images
        final_image = Image.alpha_composite(avatar_pil, jail_image)

        # Save the final image
        final_image.save("jail_avatar.png")

        # Send the modified avatar image
        await ctx.send(file=discord.File("jail_avatar.png"))

        # Delete the temporary files
        os.remove("jail_avatar.png")

        
    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(funcmds(bot))