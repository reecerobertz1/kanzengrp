import io
import os
import random
from typing import Optional
import typing
import aiohttp
import discord
from discord.ext import commands
import requests
from PIL import Image

class funcmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1122627075682078720  # Replace with your desired log channel ID

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

        log_channel = self.bot.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(f"{ctx.author.mention} used the say command, and they said: {message}")


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
    async def ppsize(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        pp_size = '=' * random.randint(1, 10)  # Randomly generate "=" characters
        message = f'{member.mention} Your pp size is: 8{pp_size}D'
        await ctx.send(message)

    @commands.command()
    async def hug(self, ctx, member: typing.Optional[discord.Member]):
        if member is None:
            await ctx.send(f"Hoshi gave {ctx.author.mention} a hug <a:mm_hug_tight:1122621840305684632>")
        else:
            embed = discord.Embed(description=f"{ctx.author.mention} gave {member.mention} a hug!", color=0x2b2d31)
            urls = ['https://cdn.discordapp.com/attachments/804482120671821865/814085524548878346/download_1.gif', "https://cdn.discordapp.com/attachments/804482120671821865/814083420194996224/download.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814086607997108254/tenor.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814087205039243274/tenor_1.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814087528906620968/tenor_2.gif"]
            embed.set_image(url=(random.choice(urls)))
            await ctx.reply(embed=embed)

    @commands.command()
    async def kiss(self, ctx, member: typing.Optional[discord.Member]):
        author = ctx.message.author.mention
        if member is None:
            await ctx.reply(f"Hoshi kissed {author}! <a:pkiss:1122621758978138283>")
        else:
            embed = discord.Embed(description=f"{author} kissed {member.mention}", color=0x2b2d31)
            hugs = ['https://cdn.discordapp.com/attachments/804482120671821865/814095974611681280/37f9f27715e7dec6f2f4b7d63ad1af13.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814096796582019082/39fe167bdab90223bcc890bcb067b761.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814097411525836851/5f5afb51884af7c58e8d46c90261f990.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814097832494759936/tenor_1.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814098373228625970/tenor_2.gif']
            embed.set_image(url=(random.choice(hugs)))
            await ctx.reply(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: typing.Optional[discord.Member]):
        author = ctx.message.author.mention
        if member is None:
            await ctx.reply(f"Hoshi slapped {author}! HAHAHAHAHAHAHA")
        else:
            embed = discord.Embed(description=f'{author} slapped {member.mention}!', color=0x2b2d31)
            embed.set_image(url='https://cdn.discordapp.com/attachments/804482120671821865/814100958463524884/nK.gif')
            await ctx.reply(embed=embed)

    @commands.command()
    async def fuck(self, ctx, member: typing.Optional[discord.Member]):
        author = ctx.message.author.mention
        if member is None:
            await ctx.reply(f"Hoshi fuck {author}! UGH OMFG")
        else:
            embed = discord.Embed(description=f'{author} fucked {member.mention}!', color=0x2b2d31)
            embed.set_image(url='https://myteenwebcam.com/fapp/gifs/df33afb45614b12e96ef2aedf5a56225.gif')
            await ctx.reply(embed=embed)

    @commands.command(name='roast')
    async def roast_command(self, ctx, *, member: discord.Member = None):
        # If no member is mentioned, default to the author of the command
        if member is None:
            member = ctx.author

        # List of roasts
        roasts = [
            "you're so dumb, you stare at a glass of orange juice because it says 'concentrate'.",
            "I'm not saying I hate you, but I would unplug your life support to charge my phone.",
            "I was going to make a joke about your life, but I see life already beat me to it.",
            "if I had a face like yours, I'd sue my parents.",
            "I envy people who have never met you.",
            "I'm not insulting you, I'm describing you.",
            "I'm sorry, was I meant to be offended? The only thing offending me is your face.",
            "I don't have the time or crayons to explain this to you.",
            "roses are red, violets are blue, I have 5 fingers, and the middle one is for you.",
            "I'm sorry if I hurt your feelings. But I hope you understand that I just don't care."
        ]

        roast = random.choice(roasts)
        await ctx.reply(roast)

    @commands.command(name='compliment')
    async def compliment_command(self, ctx, *, member: discord.Member = None):
        # If no member is mentioned, default to the author of the command
        if member is None:
            member = ctx.author

        # List of compliments
        compliments = [
            "you have a beautiful smile!",
            "your kindness is contagious!",
            "you're incredibly smart and talented!",
            "you make the world a better place just by being in it!",
            "your positive attitude is inspiring!",
            "you have a heart of gold!",
            "your creativity knows no bounds!",
            "you always know how to make people feel special!",
            "you're an amazing friend and companion!",
            "your hard work and dedication are truly admirable!"
        ]

        compliment = random.choice(compliments)
        await ctx.reply(compliment)


    @commands.command(name='8ball')
    async def eight_ball(self, ctx, *, question):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]

        response = random.choice(responses)
        await ctx.reply(f"Question: {question}\nAnswer: {response}")

    @commands.command()
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member):
        """Calculates the compatibility between two users."""
        # Calculate compatibility score (random number between 0 and 100)
        compatibility = random.randint(0, 100)

        # Determine ship name based on compatibility score
        if compatibility < 20:
            ship_name = "Incompatible Duo"
        elif compatibility < 40:
            ship_name = "Awkward Pair"
        elif compatibility < 60:
            ship_name = "Potential Couple"
        elif compatibility < 80:
            ship_name = "Perfect Match"
        else:
            ship_name = "Soulmates"

        # Construct the ship message
        ship_message = f"❤️ Compatibility between {user1.mention} and {user2.mention}: {compatibility}%\n"
        ship_message += f"💑 Ship Name: {ship_name}"

        await ctx.send(ship_message)

async def setup(bot):
    await bot.add_cog(funcmds(bot))