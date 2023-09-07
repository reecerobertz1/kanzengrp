import asyncio
import io
import json
import math
import os
import random
from typing import Optional
import typing
import aiohttp
import discord
from discord.ext import commands
import requests
from PIL import Image, ImageDraw, ImageFont
from triviastuff.getQuestions import getQuestions
from triviastuff.checkHandler import buttonHandler

class RockPaperScissorsView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.value = None
        self.ctx = ctx

    async def on_timeout(self):
        try:
            message = await self.ctx.channel.fetch_message(self.ctx.id)
            await message.edit(content="Rock-paper-scissors game timed out.", view=None)
        except Exception as e:
            print(f"An error occurred while editing the message: {e}")

    @discord.ui.button(label="Rock", style=discord.ButtonStyle.gray)
    async def Rock(self, interaction: discord.Interaction, button: discord.Button):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        if bot_choice == "rock":
            await interaction.response.edit_message(content="It's a tie! Hoshi chose rock.", view=None)
        elif bot_choice == "paper":
            await interaction.response.edit_message(content="You lose! Hoshi chose paper.", view=None)
        else:
            await interaction.response.edit_message(content="You win! Hoshi chose scissors.", view=None)

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.gray)
    async def Paper(self, interaction: discord.Interaction, button: discord.Button):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        if bot_choice == "paper":
            await interaction.response.edit_message(content="It's a tie! Hoshi chose paper.", view=None)
        elif bot_choice == "scissors":
            await interaction.response.edit_message(content="You lose! Hoshi chose scissors.", view=None)
        else:
            await interaction.response.edit_message(content="You win! Hoshi chose rock.", view=None)

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.gray)
    async def Scissors(self, interaction: discord.Interaction, button: discord.Button):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        if bot_choice == "scissors":
            await interaction.response.edit_message(content="It's a tie! Hoshi chose scissors.", view=None)
        elif bot_choice == "rock":
            await interaction.response.edit_message(content="You lose! Hoshi chose rock.", view=None)
        else:
            await interaction.response.edit_message(content="You win! Hoshi chose paper.", view=None)


class funcmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gif_cache = {}
        self.server1_log_channel_id = 1122627075682078720
        self.server2_log_channel_id = 1122994947444973709
        self.server3_log_channel_id = 1134857444250632343
        self.editorsblock_log_channel_id = 1134857444250632343
        self.words = ["banana", "noodle", "giraffe", "chicken", "penguin","hamburger", "koala", "panda", "pizza", "unicorn","elephant", "kangaroo", "hippopotamus", "dolphin", "flamingo","chameleon", "jellyfish", "butterfly", "octopus", "toucan","giraffe", "hedgehog", "narwhal", "sloth", "lemur","raccoon", "zebra", "otter", "meerkat", "lemur","tortoise", "koala", "armadillo", "penguin", "seahorse","giraffe", "panda", "kangaroo", "elephant", "chameleon","flamingo", "hippopotamus", "jellyfish", "butterfly", "dolphin","koala", "otter", "toucan", "raccoon", "sloth","penguin", "tortoise", "meerkat", "narwhal", "armadillo","lemur", "chicken", "butterfly", "unicorn", "panda","pizza", "koala", "hamburger", "elephant", "toucan","giraffe", "chameleon", "dolphin", "seahorse", "otter","raccoon", "tortoise", "meerkat", "penguin", "sloth","koala", "unicorn", "narwhal", "jellyfish", "flamingo","lemur", "panda", "koala", "penguin", "unicorn","chicken", "hamburger", "pizza", "toucan", "sloth","giraffe", "dolphin", "armadillo", "seahorse", "butterfly","raccoon", "elephant", "meerkat", "flamingo", "jellyfish","paris", "london", "tokyo", "newyork", "sydney","berlin", "amsterdam", "moscow", "rome", "madrid","bts", "blackpink", "twice", "exo", "redvelvet","nct", "got7", "seventeen", "itzy", "straykids","usa", "canada", "australia", "japan", "france","germany", "italy", "spain", "china", "brazil","india", "russia", "mexico", "southkorea", "uk","thailand", "egypt", "greece", "argentina", "turkey","norway", "sweden", "finland", "denmark", "netherlands"]
        self.max_attempts = 6
        self.current_word = ""
        self.guesses = set()
        self.attempts = 0

    def get_random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r, g, b

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(1)
            await ctx.send(message)
            embed = discord.Embed(title="Say command log", description=f"{ctx.author.name} has used the say command\nthey said: `{message}`", color=0x2b2d31)
            embed.set_footer(text=f"id: {ctx.author.id}", icon_url=ctx.author.avatar)
            log_channel_id = self.get_log_channel_id(ctx.guild.id)
            if log_channel_id is not None:
                log_channel = self.bot.get_channel(log_channel_id)
                if log_channel:
                    await log_channel.send(embed=embed)

    def get_log_channel_id(self, guild_id):
        if guild_id == 1121841073673736215:
            return self.server1_log_channel_id
        elif guild_id == 957987670787764224:
            return self.server2_log_channel_id
        elif guild_id == 1131003330810871979:
            return self.server3_log_channel_id
        elif guild_id == 1131003330810871979:
            return self.editorsblock_log_channel_id
        else:
            return None

    @commands.command()
    async def dog(self, ctx):
        async with ctx.typing():
            response = requests.get('https://dog.ceo/api/breeds/image/random')
            data = response.json()
            image_url = data['message']
            embed = discord.Embed(color=discord.Color.from_rgb(*self.get_random_color()))
            embed.set_image(url=image_url)
            await ctx.reply(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        async with ctx.typing():
            try:
                response = requests.get('https://api.thecatapi.com/v1/images/search')
                response.raise_for_status()
                data = response.json()
                image_url = data[0]['url']
                embed = discord.Embed(color=discord.Color.from_rgb(*self.get_random_color()))
                embed.set_image(url=image_url)
                await ctx.reply(embed=embed)
            except (requests.exceptions.RequestException, KeyError):
                await ctx.reply("Sorry, I couldn't fetch a cute cat at the moment. Please try again later.")

    @commands.command(aliases=['prison', 'lockup'])
    async def jail(self, ctx, member: Optional[discord.Member]):
        async with ctx.typing():
            member = member or ctx.author
            avatar_url = member.avatar.url
            async with aiohttp.ClientSession() as session:
                async with session.get(str(avatar_url)) as response:
                    avatar_image = await response.read()

            jail_image = Image.open("jail_door.png").convert("RGBA")
            avatar_pil = Image.open(io.BytesIO(avatar_image)).convert("RGBA")
            avatar_pil = avatar_pil.resize((550, 550))
            jail_image = jail_image.resize(avatar_pil.size)
            final_image = Image.alpha_composite(avatar_pil, jail_image)
            final_image.save("jail_avatar.png")
            await ctx.send(file=discord.File("jail_avatar.png"))
            os.remove("jail_avatar.png")

    @commands.command(aliases=['gay'])
    async def pride(self, ctx, member: Optional[discord.Member]):
        member = member or ctx.author
        avatar_url = member.avatar.url
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar_url)) as response:
                avatar_image = await response.read()

        jail_image = Image.open("pride.png").convert("RGBA")
        avatar_pil = Image.open(io.BytesIO(avatar_image)).convert("RGBA")
        avatar_pil = avatar_pil.resize((180, 180))
        jail_image = jail_image.resize(avatar_pil.size)
        final_image = Image.alpha_composite(avatar_pil, jail_image)
        final_image.save("pride.png")
        await ctx.send(file=discord.File("pride.png"))
        os.remove("pride.png")

    @commands.command()
    async def dog(self, ctx):
        loading_msg = await ctx.reply("<a:loading:1122893578461520013> Searching for an image")
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        data = response.json()
        image_url = data['message']

        embed = discord.Embed(color=discord.Color.from_rgb(*self.get_random_color()))
        embed.set_image(url=image_url)

        await asyncio.sleep(1)
        await loading_msg.delete()
        await ctx.reply(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        try:
            loading_msg = await ctx.reply("<a:loading:1122893578461520013> Searching for an image")
            response = requests.get('https://api.thecatapi.com/v1/images/search')
            response.raise_for_status()
            data = response.json()
            image_url = data[0]['url']

            embed = discord.Embed(color=discord.Color.from_rgb(*self.get_random_color()))
            embed.set_image(url=image_url)

            await asyncio.sleep(1)
            await loading_msg.delete()
            await ctx.reply(embed=embed)
        except (requests.exceptions.RequestException, KeyError):
            await ctx.reply("Sorry, I couldn't fetch a cute cat at the moment. Please try again later.")

    def kanzen_only():
        def predicate(ctx: commands.Context):
            if ctx.guild.id == 1121841073673736215:
                return True
            else:
                return False
        return commands.check(predicate)

    @commands.command()
    @kanzen_only()
    async def addpet(self, ctx, pet_name):
        """Adds a pet to the pet data"""
        if not ctx.message.attachments:
            await ctx.send("Please attach an image of your pet.")
            return
        
        pet_image = ctx.message.attachments[0].url
        
        try:
            with open("pets.json", "r") as file:
                pet_data = json.load(file)
        except FileNotFoundError:
            pet_data = {}

        if str(ctx.author.id) not in pet_data:
            pet_data[str(ctx.author.id)] = []

        pet_data[str(ctx.author.id)].append({"name": pet_name, "image": pet_image, "owner_id": str(ctx.author.id)})

        with open("pets.json", "w") as file:
            json.dump(pet_data, file, indent=4)

        await ctx.send("Pet added successfully!")

    @commands.command()
    @kanzen_only()
    async def pets(self, ctx):
        try:
            with open("pets.json", "r") as file:
                pet_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            pet_data = {}

        if pet_data:
            random_user_id = random.choice(list(pet_data.keys()))
            pets = pet_data[random_user_id]
            random_pet = random.choice(pets)

            try:
                user = await self.bot.fetch_user(int(random_user_id))
            except discord.NotFound:
                await ctx.send("Oops! An error occurred while fetching user information.")
                return
            
            pet_name = random_pet["name"]
            pet_image = random_pet["image"]

            embed = discord.Embed(title=f"{user.display_name}'s Pet: {pet_name}", description=f"This is {pet_name}! <@{user.id}>'s pet", color=0x2b2d31)
            embed.set_image(url=pet_image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("No pets have been added yet.")


    @commands.command(aliases=['pp'])
    async def ppsize(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        pp_size = '=' * random.randint(1, 10)
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
            await ctx.reply(f"Hoshi slap {author}! HAHAHAHAHAHAHA")
        else:
            embed = discord.Embed(description=f"{author} slapped {member.mention}!", color=0x2b2d31)
            hugs = ['https://cdn.discordapp.com/attachments/804482120671821865/814100958463524884/nK.gif',
                    'https://media.tenor.com/XiYuU9h44-AAAAAM/anime-slap-mad.gif',
                    'https://media.tenor.com/Ws6Dm1ZW_vMAAAAC/girl-slap.gif',
                    'https://media.tenor.com/yJmrNruFNtEAAAAC/slap.gif',
                    'https://media.tenor.com/eU5H6GbVjrcAAAAM/slap-jjk.gif',
                    'https://media.tenor.com/PeJyQRCSHHkAAAAM/saki-saki-mukai-naoya.gif',
                    'https://media.tenor.com/ra17G61QRQQAAAAM/tapa-slap.gif',
                    'https://media.tenor.com/kggzZQ1ldoUAAAAC/slapped-anime-slap.gif']
            embed.set_image(url=(random.choice(hugs)))
            await ctx.reply(embed=embed)

    @commands.command(aliases=["birthday"])
    async def happybirthday(self, ctx, member: typing.Optional[discord.Member]):
        author = ctx.message.author.mention
        if member is None:
            await ctx.reply(f"Hoshi wishes {author} a happy birthday!")
        else:
            embed = discord.Embed(description=f"{author} wished {member.mention} a happy birthday!", color=0x2b2d31)
            bday = ['https://media.tenor.com/M-34lT1ySIIAAAAd/hb.gif',
                    'https://media.tenor.com/CA8wXuq5Ec8AAAAd/happy40th-birthday.gif',
                    'https://media.tenor.com/ekHNpcO0QPEAAAAC/happy-birthday.gif',
                    'https://media.tenor.com/4DZR7mxre0IAAAAC/birthday-happy-birthday.gif',
                    'https://media.tenor.com/21kzclFhTg8AAAAC/happy-birthday-birthday.gif',
                    'https://media.tenor.com/9WoGmoTqej4AAAAC/happy-birthday-hbd.gif',
                    'https://media.tenor.com/BHTQmBYipVEAAAAC/anyon-birthday.gif',
                    'https://media.tenor.com/eCGKnoBDOAQAAAAC/happy-birthday.gif']
            embed.set_image(url=(random.choice(bday)))
            await ctx.reply(embed=embed)

    @commands.command(name='roast')
    async def roast_command(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

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
        if member is None:
            member = ctx.author

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
        compatibility = random.randint(0, 100)

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

        ship_message = f"❤️ Compatibility between {user1.mention} and {user2.mention}: {compatibility}%\n"
        ship_message += f"💑 Ship Name: {ship_name}"

        await ctx.send(ship_message)

    @commands.command()
    async def howgay(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        percentage = random.randint(0, 100)
        await ctx.send(f"{member.mention} is {percentage}% gay. 🏳️‍🌈")

    @commands.command(aliases=['pfp', 'icon'])
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        avatar_url = member.display_avatar.url

        await ctx.reply(f"{avatar_url}")

    @commands.command()
    async def giphy(self, ctx, *, search):
        api_key = "PF48beXJTbUkvh35ThoQ4t1qhyjleLwD"
        url = f"https://api.giphy.com/v1/gifs/search"
        params = {
            "api_key": api_key,
            "q": search,
            "limit": 10,  
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
            gifs = data["data"]
            
            if not gifs:
                await ctx.send("No GIFs found for the given search query.")
                return
            
            gifs = [gif for gif in gifs if gif["id"] not in self.gif_cache.get(ctx.author.id, [])]
            
            if not gifs:
                self.gif_cache[ctx.author.id] = []
                gifs = data["data"]
            
            gif = random.choice(gifs)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            
            gif_embed = discord.Embed(color=discord.Color.from_rgb(r, g, b))
            gif_embed.set_image(url=gif["images"]["original"]["url"])
            await ctx.send(embed=gif_embed)
            
            self.gif_cache.setdefault(ctx.author.id, []).append(gif["id"])
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    def get_hidden_word(self):
        return "".join(letter if letter in self.guesses else "_" for letter in self.current_word)

    @commands.command()
    async def hangman(self, ctx):
        self.current_word = random.choice(self.words).lower()
        self.guesses = set()
        self.attempts = 0
        hidden_word = " ".join("◯" if letter.isalpha() else letter for letter in self.current_word)
        embed = discord.Embed(title="Hangman Game", description=f"Let's play Hangman! The word has {len(self.current_word)} letters.", color=0x2b2d31)
        embed.add_field(name="Hidden Word", value=hidden_word, inline=False)
        embed.add_field(name="Attempts Left", value=self.max_attempts - self.attempts, inline=False)
        embed.set_footer(text='do +guess <letter> to guess the letters')
        await ctx.reply(embed=embed)

    @commands.command()
    async def guess(self, ctx, letter: str):
        if not letter.isalpha() or len(letter) != 1:
            await ctx.reply("Please enter a valid single letter.")
            return

        letter = letter.lower()

        if letter in self.guesses:
            await ctx.reply("You already guessed that letter.")
            return

        self.guesses.add(letter)

        if letter in self.current_word:
            if all(letter in self.guesses for letter in self.current_word):
                await ctx.reply(f"Congratulations! You guessed the word: `{self.current_word}`.")
                self.current_word = ""
                return
            else:
                hidden_word = " ".join(letter if letter in self.guesses else "◯" for letter in self.current_word)
                embed = discord.Embed(title="Hangman Game", color=0x2b2d31)
                embed.add_field(name="Hidden Word", value=hidden_word, inline=False)
                embed.add_field(name="Good guess!", value=f"Letter `{letter}` is in the word.", inline=False)
                embed.add_field(name="Attempts Left", value=self.max_attempts - self.attempts, inline=False)
                embed.set_footer(text='do +guess <letter> to guess the letters')
                await ctx.reply(embed=embed)
        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                await ctx.reply(f"Sorry, you've reached the maximum number of attempts. The word was: `{self.current_word}`.")
                self.current_word = ""
            else:
                hidden_word = " ".join(letter if letter in self.guesses else "◯" for letter in self.current_word)
                embed = discord.Embed(title="Hangman Game", color=0x2b2d31)
                embed.add_field(name="Hidden Word", value=hidden_word, inline=False)
                embed.add_field(name="Wrong letter!", value=f"Letter `{letter}` is not in the word.", inline=False)
                embed.add_field(name="Attempts Left", value=self.max_attempts - self.attempts, inline=False)
                embed.set_footer(text='do +guess <letter> to guess the letters')
                await ctx.reply(embed=embed)

    @commands.hybrid_command(name="trivia", description="Starts a quiz", timeout=3.0)
    async def trivia(self, ctx):
        
        try:
            view = buttonHandler()
            embed, answer = await getQuestions()
            message = await ctx.reply(f"Your current score is: **{view.score}**\nYou have ❤**{view.lives}** lives left.", embed=embed, view = view)
        except asyncio.TimeoutError:
            await message.edit(content=f"You ran out of time! Your score was {view.score}!", view=None)

async def setup(bot):
    await bot.add_cog(funcmds(bot))