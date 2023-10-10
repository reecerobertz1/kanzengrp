import asyncio
import datetime
import io
import json
import math
import os
import random
import textwrap
from typing import Optional
import typing
import aiohttp
import discord
from discord.ext import commands
from discord import ui, app_commands
import requests
from typing import Optional, Tuple
from PIL import ImageDraw, Image
from io import BytesIO
from easy_pil import Font
from triviastuff.getQuestions import getQuestions
from triviastuff.checkHandler import buttonHandler

WORDS = ["apple", "banana", "orange", "grape", "strawberry", "melon", "kiwi", "cherry", "peach","computer","python","discord","programming","keyboard","gaming","music","puzzle","chocolate","coffee","internet","book","beach","mountain","travel","camera","science","flower","rainbow","butterfly","vampire","zombie","castle","ocean","space","sunset","moonlight","fireworks","candle","diamond","treasure","magic","wizard","unicorn","mermaid","dragon","superhero","mystery","adventure","fantasy","horror","comedy","romance","dinosaur","jungle","robot","pirate","ninja","samurai","karate","guitar","painting","museum","pizza","sushi","ice cream","cupcake","raincoat","umbrella","piano","guitar","violin","bicycle","skateboard","surfing","sailing","kayaking","volleyball","basketball","soccer","football","tennis","swimming","dancing","singing","writing","drawing","cooking","baking","gardening","reading","shopping","sleeping","cycling","hiking","running","yoga","meditation","relaxing","waterfall","adventure","telescope","spaceship","galaxy","sunrise","marshmallow","telescope","puzzle","rainbow","hotdog"]

class confessbutton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.value = None
        self.start_time = datetime.datetime.utcnow()

    @discord.ui.button(label="Click to confess", style=discord.ButtonStyle.red)
    async def confess(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(confessmodal())

class confessmodal(ui.Modal, title='Kanzen Confessions'):
    confession = ui.TextInput(label='Whats your confession', placeholder="Enter confession here...", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = interaction.client.get_channel(1145568957345054751)
        embed = discord.Embed(title="New confession", description=f"{self.confession.value}", color=0x2b2d31)
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Use /confess to send a confession!")
        confessions = await channel.send(embed=embed)
        await interaction.followup.send(f"Your confession has been sent to <#1145568957345054751>", ephemeral=True)
        await confessions.add_reaction("<:breaths:1128463455993741352>")
        await confessions.add_reaction("<:pause:1132212249621184634>")
        await confessions.add_reaction("<:__:1132210032822456411>")
        await confessions.add_reaction("<a:crysad:1132210059233988678>")
        await confessions.add_reaction("<a:wAHhh:1128463952423174164>")

class RockPaperScissorsView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.value = None
        self.ctx = ctx

    @discord.ui.button(label="🪨 Rock", style=discord.ButtonStyle.gray)
    async def Rock(self, interaction: discord.Interaction, button: discord.Button):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        if bot_choice == "rock":
            await interaction.response.edit_message(content="It's a tie! Hoshi chose rock.", view=None)
        elif bot_choice == "paper":
            await interaction.response.edit_message(content="You lose! Hoshi chose paper.", view=None)
        else:
            await interaction.response.edit_message(content="You win! Hoshi chose scissors.", view=None)

    @discord.ui.button(label="📰 Paper", style=discord.ButtonStyle.gray)
    async def Paper(self, interaction: discord.Interaction, button: discord.Button):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        if bot_choice == "paper":
            await interaction.response.edit_message(content="It's a tie! Hoshi chose paper.", view=None)
        elif bot_choice == "scissors":
            await interaction.response.edit_message(content="You lose! Hoshi chose scissors.", view=None)
        else:
            await interaction.response.edit_message(content="You win! Hoshi chose rock.", view=None)

    @discord.ui.button(label="✂ Scissors", style=discord.ButtonStyle.gray)
    async def Scissors(self, interaction: discord.Interaction, button: discord.Button):
        bot_choice = random.choice(["rock", "paper", "scissors"])
        if bot_choice == "scissors":
            await interaction.response.edit_message(content="It's a tie! Hoshi chose scissors.", view=None)
        elif bot_choice == "rock":
            await interaction.response.edit_message(content="You lose! Hoshi chose rock.", view=None)
        else:
            await interaction.response.edit_message(content="You win! Hoshi chose paper.", view=None)


class Fun(commands.Cog):
    """Hoshi's fun commands"""
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
        self.games = {}
        self.occupied = []

    def get_random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r, g, b

    @commands.command(description="Make Hoshi say something")
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

    @commands.command(description="See photos + gifs of dogs")
    async def dog(self, ctx):
        async with ctx.typing():
            response = requests.get('https://dog.ceo/api/breeds/image/random')
            data = response.json()
            image_url = data['message']
            await ctx.reply(image_url)

    @commands.command(description="See photos + gifs of cats")
    async def cat(self, ctx):
        async with ctx.typing():
            try:
                response = requests.get('https://api.thecatapi.com/v1/images/search')
                response.raise_for_status()
                data = response.json()
                image_url = data[0]['url']
                await ctx.reply(image_url)
            except (requests.exceptions.RequestException, KeyError):
                await ctx.reply("Sorry, I couldn't fetch a cute cat at the moment. Please try again later.")

    @commands.command(aliases=['prison', 'lockup'],description="Lock someone up in jail")
    async def jail(self, ctx, member: Optional[discord.Member]):
        async with ctx.typing():
            member = member or ctx.author
            avatar_url = member.avatar.url
            async with aiohttp.ClientSession() as session:
                async with session.get(str(avatar_url)) as response:
                    avatar_image = await response.read()

            jail_image = Image.open("./assets/jail_door.png").convert("RGBA")
            avatar_pil = Image.open(io.BytesIO(avatar_image)).convert("RGBA")
            avatar_pil = avatar_pil.resize((550, 550))
            jail_image = jail_image.resize(avatar_pil.size)
            final_image = Image.alpha_composite(avatar_pil, jail_image)
            final_image.save("jail_avatar.png")
            await ctx.send(file=discord.File("jail_avatar.png"))
            os.remove("jail_avatar.png")

    @commands.command(aliases=['gay'],description="Edits your avatar with the pride flag")
    async def pride(self, ctx, member: Optional[discord.Member]):
        member = member or ctx.author
        avatar_url = member.avatar.url
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar_url)) as response:
                avatar_image = await response.read()

        jail_image = Image.open("./assets/pride.png").convert("RGBA")
        avatar_pil = Image.open(io.BytesIO(avatar_image)).convert("RGBA")
        avatar_pil = avatar_pil.resize((180, 180))
        jail_image = jail_image.resize(avatar_pil.size)
        final_image = Image.alpha_composite(avatar_pil, jail_image)
        final_image.save("pride.png")
        await ctx.send(file=discord.File("pride.png"))
        os.remove("pride.png")

    def kanzen_only():
        def predicate(ctx: commands.Context):
            if ctx.guild.id == 1121841073673736215:
                return True
            else:
                return False
        return commands.check(predicate)

    @commands.command(description="Add your pet to the +pets command")
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

    @commands.command(description="See all of kanzen's pets")
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

    @commands.command(aliases=['pp'],description="See who has the biggest pp")
    async def ppsize(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        pp_size = '=' * random.randint(1, 10)
        message = f'{member.mention} Your pp size is: 8{pp_size}D'
        await ctx.send(message)

    @commands.command(description="Hug someone")
    async def hug(self, ctx, member: typing.Optional[discord.Member]):
        if member is None:
            await ctx.send(f"Hoshi gave {ctx.author.mention} a hug <a:mm_hug_tight:1122621840305684632>")
        else:
            embed = discord.Embed(description=f"{ctx.author.mention} gave {member.mention} a hug!", color=0x2b2d31)
            urls = ['https://cdn.discordapp.com/attachments/804482120671821865/814085524548878346/download_1.gif', "https://cdn.discordapp.com/attachments/804482120671821865/814083420194996224/download.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814086607997108254/tenor.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814087205039243274/tenor_1.gif", "https://cdn.discordapp.com/attachments/804482120671821865/814087528906620968/tenor_2.gif"]
            embed.set_image(url=(random.choice(urls)))
            await ctx.reply(embed=embed)

    @commands.command(description="Kiss someone")
    async def kiss(self, ctx, member: typing.Optional[discord.Member]):
        author = ctx.message.author.mention
        if member is None:
            await ctx.reply(f"Hoshi kissed {author}! <a:pkiss:1122621758978138283>")
        else:
            embed = discord.Embed(description=f"{author} kissed {member.mention}", color=0x2b2d31)
            hugs = ['https://cdn.discordapp.com/attachments/804482120671821865/814095974611681280/37f9f27715e7dec6f2f4b7d63ad1af13.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814096796582019082/39fe167bdab90223bcc890bcb067b761.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814097411525836851/5f5afb51884af7c58e8d46c90261f990.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814097832494759936/tenor_1.gif', 'https://cdn.discordapp.com/attachments/804482120671821865/814098373228625970/tenor_2.gif']
            embed.set_image(url=(random.choice(hugs)))
            await ctx.reply(embed=embed)

    @commands.command(description="Slap a bitch")
    async def slap(self, ctx, member: typing.Optional[discord.Member]):
        author = ctx.message.author.mention
        if member is None:
            await ctx.reply(f"Hoshi slap {author}! HAHAHAHAHAHAHA")
        else:
            embed = discord.Embed(description=f"{author} slapped {member.mention}!", color=0x2b2d31)
            hugs = ['https://cdn.discordapp.com/attachments/804482120671821865/814100958463524884/nK.gif','https://media.tenor.com/XiYuU9h44-AAAAAM/anime-slap-mad.gif','https://media.tenor.com/Ws6Dm1ZW_vMAAAAC/girl-slap.gif','https://media.tenor.com/yJmrNruFNtEAAAAC/slap.gif','https://media.tenor.com/eU5H6GbVjrcAAAAM/slap-jjk.gif','https://media.tenor.com/PeJyQRCSHHkAAAAM/saki-saki-mukai-naoya.gif','https://media.tenor.com/ra17G61QRQQAAAAM/tapa-slap.gif','https://media.tenor.com/kggzZQ1ldoUAAAAC/slapped-anime-slap.gif']
            embed.set_image(url=(random.choice(hugs)))
            await ctx.reply(embed=embed)

    @commands.command(aliases=["birthday"],description="Wish someone a happy birthday")
    async def happybirthday(self, ctx, member: typing.Optional[discord.Member]):
        author = ctx.message.author.mention
        if member is None:
            await ctx.reply(f"Hoshi wishes {author} a happy birthday!")
        else:
            embed = discord.Embed(description=f"{author} wished {member.mention} a happy birthday!", color=0x2b2d31)
            bday = ['https://media.tenor.com/M-34lT1ySIIAAAAd/hb.gif','https://media.tenor.com/CA8wXuq5Ec8AAAAd/happy40th-birthday.gif','https://media.tenor.com/ekHNpcO0QPEAAAAC/happy-birthday.gif','https://media.tenor.com/4DZR7mxre0IAAAAC/birthday-happy-birthday.gif','https://media.tenor.com/21kzclFhTg8AAAAC/happy-birthday-birthday.gif','https://media.tenor.com/9WoGmoTqej4AAAAC/happy-birthday-hbd.gif','https://media.tenor.com/BHTQmBYipVEAAAAC/anyon-birthday.gif','https://media.tenor.com/eCGKnoBDOAQAAAAC/happy-birthday.gif']
            embed.set_image(url=(random.choice(bday)))
            await ctx.reply(embed=embed)

    @commands.command(name='roast',description="Roast someone")
    async def roast_command(self, ctx, *, member: discord.Member = None, roast_text: str = None):
        if member is None:
            member = ctx.author

        if roast_text is None:
            roasts = [f"{member.mention}, you're so dumb, you stare at a glass of orange juice because it says 'concentrate'.",f"{member.mention}, I'm not saying I hate you, but I would unplug your life support to charge my phone.",f"{member.mention}, I was going to make a joke about your life, but I see life already beat me to it.",f"{member.mention}, if I had a face like yours, I'd sue my parents.",f"{member.mention}, I envy people who have never met you.",f"{member.mention}, I'm not insulting you, I'm describing you.",f"{member.mention}, I'm sorry, was I meant to be offended? The only thing offending me is your face.",f"{member.mention}, I don't have the time or crayons to explain this to you.",f"{member.mention}, roses are red, violets are blue, I have 5 fingers, and the middle one is for you.",f"{member.mention}, I'm sorry if I hurt your feelings. But I hope you understand that I just don't care."]
        else:
            roasts = [f"{member.mention} {roast_text}"]

        roast = random.choice(roasts)
        await ctx.reply(roast)

    @commands.command(name='compliment',description="Give someone a compliment")
    async def compliment_command(self, ctx, *, member: discord.Member = None, compliment_text: str = None):
        if member is None:
            member = ctx.author

        if compliment_text is None:
            compliments = [f"{member.mention}, you have a beautiful smile!",f"{member.mention}, your kindness is contagious!",f"{member.mention}, you're incredibly smart and talented!",f"{member.mention}, you make the world a better place just by being in it!",f"{member.mention}, your positive attitude is inspiring!",f"{member.mention}, you have a heart of gold!",f"{member.mention}, your creativity knows no bounds!",f"{member.mention}, you always know how to make people feel special!",f"{member.mention}, you're an amazing friend and companion!",f"{member.mention}, your hard work and dedication are truly admirable!",f"{member.mention}, your generosity knows no limits!",f"{member.mention}, you radiate positivity and joy!",f"{member.mention}, you're a beacon of light in everyone's life!",f"{member.mention}, your sense of humor brightens any room!",f"{member.mention}, you're a true inspiration to others!",f"{member.mention}, your compassion for others is unmatched!",f"{member.mention}, your presence brings happiness to those around you!",f"{member.mention}, you're a true blessing to your friends and family!",f"{member.mention}, your smile can make anyone's day better!",f"{member.mention}, you're the epitome of kindness and grace!",f"{member.mention}, your perseverance in the face of challenges is remarkable!",f"{member.mention}, you have a heart full of love and empathy!",f"{member.mention}, your wisdom and insight are greatly appreciated!",f"{member.mention}, you're a role model for all of us!",f"{member.mention}, your friendship means the world to me!",f"{member.mention}, you're a ray of sunshine on a cloudy day!",f"{member.mention}, you're a source of strength and support for others!"]
        else:
            compliments = [f"{member.mention} {compliment_text}"]

        compliment = random.choice(compliments)
        await ctx.reply(compliment)

    @commands.command(name='8ball',description="Ask 8ball a question")
    async def eight_ball(self, ctx, *, question):
        responses = ["It is certain.","It is decidedly so.","Without a doubt.","Yes - definitely.","You may rely on it.","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes.","Reply hazy, try again.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again.","Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.","Very doubtful."]
        response = random.choice(responses)
        embed = discord.Embed(description=f"question: {question}\nanswer: {response}", color=0x2b2d31)
        embed.set_author(name="8ball", icon_url="https://cdn.discordapp.com/attachments/1121841074512605186/1151109254959333426/png-clipart-magic-8-ball-eight-ball-crazy-eights-ball-game-logo.png")
        embed.set_footer(text=f"8ball for {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.reply(embed=embed)

    @commands.command(description="Ship 2 people together")
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

        ship_message = f"❤️ Compatibility between {user1.mention} and {user2.mention}: **{compatibility}%**\n"
        ship_message += f"💑 Ship Name: **__{ship_name}__**"

        await ctx.send(ship_message)

    @commands.command(description="How gay really are you?")
    async def howgay(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        percentage = random.randint(0, 100)
        await ctx.send(f"{member.mention} is **{percentage}%** gay. 🏳️‍🌈")

    @commands.command(aliases=['pfp', 'icon'],description="Get someone avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        avatar_url = member.display_avatar.url

        await ctx.reply(f"{avatar_url}")

    @commands.command(description="Search for gifs")
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
            gif_url = gif["images"]["original"]["url"]
            await ctx.send(gif_url)

            self.gif_cache.setdefault(ctx.author.id, []).append(gif["id"])
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        content = message.content.strip()
        if len(content) == 1 and content.isalpha():
            await self.guess(message, content.lower())

    def get_hidden_word(self):
        return "".join(letter if letter in self.guesses else "_" for letter in self.current_word)

    @commands.command(description="Play hangman with Hoshi!")
    async def hangman(self, ctx):
        self.current_word = random.choice(self.words).lower()
        self.guesses = set()
        self.attempts = 0
        hidden_word = " ".join("◯" if letter.isalpha() else letter for letter in self.current_word)
        embed = discord.Embed(title="Hangman Game", description=f"Let's play Hangman! The word has {len(self.current_word)} letters.", color=0x2b2d31)
        embed.add_field(name="Hidden Word", value=hidden_word, inline=False)
        embed.add_field(name="Attempts Left", value=self.max_attempts - self.attempts, inline=False)
        embed.set_footer(text='Just type a letter to guess')
        await ctx.reply(embed=embed)

    async def guess(self, message, letter):
        if letter in self.guesses:
            await message.channel.send("You already guessed that letter.")
            return

        self.guesses.add(letter)

        if letter in self.current_word:
            if all(letter in self.guesses for letter in self.current_word):
                await message.channel.send(f"Congratulations! You guessed the word: `{self.current_word}`.")
                self.current_word = ""
                return
            else:
                hidden_word = " ".join(letter if letter in self.guesses else "◯" for letter in self.current_word)
                embed = discord.Embed(title="Hangman Game", color=0x2b2d31)
                embed.add_field(name="Hidden Word", value=hidden_word, inline=False)
                embed.add_field(name="Good guess!", value=f"Letter `{letter}` is in the word.", inline=False)
                embed.add_field(name="Attempts Left", value=self.max_attempts - self.attempts, inline=False)
                embed.set_footer(text='Just type a letter to guess')
                await message.channel.send(embed=embed)
        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                await message.channel.send(f"Sorry, you've reached the maximum number of attempts. The word was: `{self.current_word}`.")
                self.current_word = ""
            else:
                hidden_word = " ".join(letter if letter in self.guesses else "◯" for letter in self.current_word)
                embed = discord.Embed(title="Hangman Game", color=0x2b2d31)
                embed.add_field(name="Hidden Word", value=hidden_word, inline=False)
                embed.add_field(name="Wrong letter!", value=f"Letter `{letter}` is not in the word.", inline=False)
                embed.add_field(name="Attempts Left", value=self.max_attempts - self.attempts, inline=False)
                embed.set_footer(text='Just type a letter to guess')
                await message.channel.send(embed=embed)

    @commands.hybrid_command(name="trivia", description="Play a game of trivia", timeout=3.0)
    async def trivia(self, ctx):
        
        try:
            view = buttonHandler()
            embed, answer = await getQuestions()
            message = await ctx.reply(f"Your current score is: **{view.score}**\nYou have ❤**{view.lives}** lives left.", embed=embed, view = view)
        except asyncio.TimeoutError:
            await message.edit(content=f"You ran out of time! Your score was {view.score}!", view=None)

    @commands.command(aliases=["rps"],description="Play rock, paper scissors with Hoshi")
    async def rockpaperscissors(self, ctx):
        message = await ctx.send("Let's play rock-paper-scissors! Click your choice below.")
        view = RockPaperScissorsView(message)
        await message.edit(view=view)

    def _get_round_avatar(self, avatar: BytesIO) -> Tuple[Image.Image, Image.Image]:
        circle = Image.open('./assets/circle-mask.png').resize((160, 160)).convert('L')
        avatar_image = Image.open(avatar).convert('RGBA')
        avatar_image = avatar_image.resize((160, 160))
        return avatar_image, circle

    @commands.command(description="Tweet as yourself with Hoshi")
    async def tweet(self, ctx, *tweet: str) -> BytesIO:
        tweet_text = " ".join(tweet)
        avatar_url = ctx.author.avatar.url
        async with self.bot.session.get(avatar_url) as response:
            if response.status == 200:
                avatar_data = await response.read()
            else:
                avatar_data = None

        img = Image.open(f'./assets/twitter.png')
        draw = ImageDraw.Draw(img)
        if avatar_data:
            avatar = BytesIO(avatar_data)
            avatar_paste, circle = self._get_round_avatar(avatar)
            img.paste(avatar_paste, (37, 17), circle)
            
        poppins = Font.poppins(size=55)
        poppins_small = Font.poppins(size=45)
        poppins_xsmall = Font.poppins(size=35)
        wrapped_text = textwrap.fill(tweet_text, width=45)
        display_name_parts = ctx.author.display_name.split('|')
        display_name = display_name_parts[0].strip() if display_name_parts else ctx.author.display_name
        draw.text((25, 190), wrapped_text, font=poppins)
        draw.text((215, 29), display_name, font=poppins_small)
        draw.text((215, 75), f"@{ctx.author.name}", font=poppins_xsmall, fill=0x2D2D2D)
        img.save("tweet.png")
        await ctx.reply(file=discord.File("tweet.png"))

    @app_commands.command(name='confess', description='Drop your juiciest secrets!')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def confess(self, interaction: discord.Interaction):
        view = confessbutton()
        await interaction.response.send_message('Your confessions are sent anonymously! Do not be scared to tell us anything', view=view, ephemeral=True)

    @commands.command(description="Unscramble words given to you by Hoshi")
    async def scramble(self, ctx):
        word = random.choice(WORDS)
        scrambled_word = ''.join(random.sample(word, len(word)))
        await ctx.reply(f"Unscramble the word: **{scrambled_word}**")

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        try:
            response = await self.bot.wait_for('message', check=check, timeout=20.0)
            if response.content.lower() == word:
                await ctx.reply(f"Correct! The word is **{word}**.")
            else:
                await ctx.reply(f"Sorry, that's incorrect. The correct word is **{word}**.")
        except asyncio.TimeoutError:
            await ctx.reply(f"Time's up! The correct word is **{word}**.")

async def setup(bot):
    await bot.add_cog(Fun(bot))