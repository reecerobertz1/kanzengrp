import asyncio
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
        self.server1_log_channel_id = 1122627075682078720
        self.server2_log_channel_id = 1122994947444973709

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

        log_channel_id = self.get_log_channel_id(ctx.guild.id)
        if log_channel_id is not None:
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                await log_channel.send(f"{ctx.author.mention} used the say command, and they said: {message}")

    def get_log_channel_id(self, guild_id):
        if guild_id == 1121841073673736215:
            return self.server1_log_channel_id
        elif guild_id == 957987670787764224:
            return self.server2_log_channel_id
        else:
            return None


    @commands.command()
    async def dog(self, ctx):
        loading_msg = await ctx.reply("<a:loading:1122893578461520013> Searching for an image")
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        image_url = data['message']

        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url=image_url)

        await asyncio.sleep(1)  # Wait for 3 seconds (you can adjust the duration)
        await loading_msg.delete()  # Delete the loading message
        await ctx.reply(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        try:
            loading_msg = await ctx.reply("<a:loading:1122893578461520013> Searching for an image")
            response = requests.get('https://api.thecatapi.com/v1/images/search')
            response.raise_for_status()
            data = response.json()
            image_url = data[0]['url']

            embed = discord.Embed(color=0x2b2d31)
            embed.set_image(url=image_url)

            await asyncio.sleep(1)  # Wait for 3 seconds (you can adjust the duration)
            await loading_msg.delete()  # Delete the loading message
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

    @commands.command()
    async def trivia(self, ctx):
        """Starts a trivia game with multiple-choice questions."""
        # Define a list of trivia questions and their corresponding answers
        trivia_questions = [
            {
                "question": "What is the capital of France?",
                "options": ["Ⓐ London", "Ⓑ Paris", "Ⓒ Rome", "Ⓓ Berlin"],
                "answer": 1  # Index of the correct answer (starts from 0)
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Ⓐ Mars", "Ⓑ Jupiter", "Ⓒ Saturn", "Ⓓ Venus"],
                "answer": 0
            },
            {
                "question": "What is the chemical symbol for the element oxygen?",
                "options": ["Ⓐ O", "Ⓑ H", "Ⓒ C", "Ⓓ N"],
                "answer": 0
            },
            {
                "question": "What is the bodies largest organ?",
                "options": ["Ⓐ Skin", "Ⓑ Liver", "Ⓒ Kidney", "D) Large Intestine"],
                "answer": 0
            },
            {
                "question": "How many oceans are there on earth?",
                "options": ["Ⓐ 3", "Ⓑ 10", "Ⓒ 7", "Ⓓ 5"],
                "answer": 3
            },
            {
                "question": "How long is an Olympic swimming pool (in meters)?",
                "options": ["Ⓐ 30 meters", "Ⓑ 100 meters", "Ⓒ 50 meters", "Ⓓ 25 meters"],
                "answer": 2
            },
            {
                "question": "How many languages are written from right to left?",
                "options": ["Ⓐ 12", "Ⓑ 5", "Ⓒ 13", "Ⓓ 20"],
                "answer": 0
            },
            {
                "question": "What is the name of the biggest technology company in South Korea?",
                "options": ["Ⓐ Asus", "Ⓑ Samsung", "Ⓒ Apple", "Ⓓ Windows"],
                "answer": 1
            },
            {
                "question": 'What group is often reffered to as "The kings of kpop"?',
                "options": ["Ⓐ BTS", "Ⓑ Shinee", "Ⓒ Big Bang", "Ⓓ EXO"],
                "answer": 2
            },
            {
                "question": 'Which group were the first K-Pop artist to appear on the US Billboard Hot 100?',
                "options": ["Ⓐ BTS", "Ⓑ Blackpink", "Ⓒ PSY", "Ⓓ Wonder Girls"],
                "answer": 3
            },
            {
                "question": 'What is Blackpinks most viewed music video on YouTube?',
                "options": ["Ⓐ Kill This Love", "Ⓑ Lovesick Girls", "Ⓒ DDU-DU-DDU-DU", "Ⓓ Shut Down"],
                "answer": 2
            },
            {
                "question": 'How many sub-units of NCT are there?',
                "options": ["Ⓐ 3", "Ⓑ 5", "Ⓒ 2", "Ⓓ 4"],
                "answer": 3
            },
            {
                "question": 'Which is the last music video to include all 12 original EXO members??',
                "options": ["Ⓐ Call Me Baby", "Ⓑ Overdose", "Ⓒ Growl", "Ⓓ Wolf"],
                "answer": 1
            }
            
        ]

        # Choose a random question from the list
        question = random.choice(trivia_questions)

        # Send the question and options as an embedded message
        embed = discord.Embed(title="Trivia", description=question["question"], color=0x2b2d31)
        for i, option in enumerate(question["options"]):
            embed.add_field(name=f"Option {i+1}", value=option, inline=False)
            embed.set_footer(text='Answer with numbers (1 - 4)')
        question_msg = await ctx.reply(embed=embed)

        # Define a check function to validate answers
        def check_answer(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            # Wait for the user's answer
            user_answer = await self.bot.wait_for('message', timeout=10.0, check=check_answer)

            # Check if the answer is correct
            if user_answer.content.isdigit() and int(user_answer.content) - 1 == question["answer"]:
                await ctx.reply("✅ Correct answer!")
            elif user_answer.content.isdigit():
                await ctx.reply(f"❌ Incorrect answer! The correct answer is {question['options'][question['answer']]}")
            else:
                await ctx.reply("Please provide a valid option number as your answer.")

        except asyncio.TimeoutError:
            await ctx.reply("⌛ Time's up! You took too long to answer.")

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        avatar_url = member.display_avatar.url

        await ctx.reply(f"{avatar_url}")

async def setup(bot):
    await bot.add_cog(funcmds(bot))