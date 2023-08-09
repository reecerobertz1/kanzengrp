
from discord.ext import commands
import discord
import aiohttp
from datetime import datetime
import asqlite
from discord import app_commands

my_guild = discord.Object(id=1121841073673736215)

# the extensions/cogs i want to load
extensions = {
    "jishaku",
    "cogs.addedits",
    "cogs.buildembed",
    "cogs.editing",
    "cogs.fun",
    "cogs.help",
    "cogs.inactivity",
    "cogs.memberinfo",
    "cogs.moderation",
    "cogs.welcandbye",
    "cogs.logos",
    "cogs.status",
    "cogs.levels",
    "cogs.other",
    "cogs.audios",
    "cogs.custom",
    "cogs.scramble",
    "cogs.ttt",
    "cogs.starboard",
    "cogs.roles",
    "cogs.kgrp"
}

# bot subclass
class LalisaBot(commands.Bot):

    # assigning attributes to the bot
    # access these through bot.session, bot.launch_time
    session: aiohttp.ClientSession
    launch_time: datetime
    pool: asqlite.Pool

    # initalising the subclass
    # clarifying the intents
    # and then in super().__init__() set a prefix and add the intents
    def __init__(self):
        intents = discord.Intents(
            guilds=True,
            members=True,
            emojis=True,
            messages=True,
            reactions=True,
            message_content=True,
            presences=True
        )
        super().__init__(
            command_prefix='+',
            intents=intents,
            help_command=None
        )

        # makes it so that the cog commands are case insensitive
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()

    # startup stuff
async def setup_hook(self):
    print(f"Logged in as {self.user}")

    # defining the attributes
    self.launch_time = datetime.utcnow()
    self.session = aiohttp.ClientSession()
    self.pool = await asqlite.create_pool('databases/levels.db')

    # sqlite database setup (moved after the attribute assignments)
    async with self.pool.acquire() as conn:
        await conn.execute('''CREATE TABLE IF NOT EXISTS levels (member_id BIGINT, guild_id BIGINT, xp INTEGER, messages INTEGER, bar_color TEXT, PRIMARY KEY(member_id, guild_id))''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS setup (guild_id BIGINT PRIMARY KEY, activated BOOL, top_20_role_id BIGINT)''')
        await conn.commit()

    # Check if the CommandTree instance already exists
    if not hasattr(self, "tree"):
        # Create a new CommandTree instance
        self.tree = app_commands.CommandTree(self)
        await self.tree.sync(guild=my_guild)
        self.tree.copy_global_to(guild=my_guild)

    # loads cogs/extensions
    for ext in extensions:
        await self.load_extension(ext)

    # i have to have this here for when the bot closes
    async def close(self):
        # Your other cleanup code...
        if self.pool is not None:
            await self.pool.close()
        await self.session.close()
        await super().close()

# old stuff
""" import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='+', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('Loaded cogs:')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{cog_name}')
                print(cog_name)
            except Exception as e:
                print(f'Error loading {cog_name}: {str(e)}') """