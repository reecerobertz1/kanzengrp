
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
    "cogs.kgrp",
    "cogs.music",
    "cogs.confessions"
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
            presences=True,
            voice_states = True
        )
        super().__init__(
            command_prefix='+',
            intents=intents,
            help_command=None,
            status=discord.Status.online,
            activity=discord.Game("Hoshi ♡"),
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
            await conn.execute('''CREATE TABLE IF NOT EXISTS levels (member_id BIGINT, guild_id BIGINT, xp INTEGER, messages INTEGER, bar_color TEXT, image TEXT, PRIMARY KEY(member_id, guild_id))''')
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