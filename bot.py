from discord.ext import commands
import discord
import aiohttp
from datetime import datetime
import asqlite
from discord import app_commands

my_guild = discord.Object(id=1121841073673736215)

extensions = {
    "jishaku",
    "cogs.asstral",
    "cogs.chromies",
    "cogs.community",
    "cogs.editing",
    "cogs.fun",
    "cogs.levels",
    "cogs.mod",
    "cogs.other",
    "cogs.profiles",
    "cogs.settings",
    "cogs.welc"
}

class LalisaBot(commands.Bot):
    session: aiohttp.ClientSession
    launch_time: datetime
    pool: asqlite.Pool
    embed_color: 0x2b2d31

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
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()

    async def setup_hook(self):
        print(f"Logged in as {self.user}")

        self.launch_time = datetime.utcnow()
        self.session = aiohttp.ClientSession()
        self.pool = await asqlite.create_pool('databases/levels.db')

        async with self.pool.acquire() as conn:
            await conn.execute('''CREATE TABLE IF NOT EXISTS levelling (guild_id BIGINT, member_id BIGINT, xp INTEGER, messages INTEGER, color TEXT, image TEXT, decor TEXT, format INTEGER, PRIMARY KEY(guild_id, member_id))''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS levels (guild_id BIGINT, member_id INTEGER, xp INTEGER, messages INTEGER, bar_color TEXT, PRIMARY KEY (guild_id, member_id))''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS decors (member_id BIGINT, unlocked INTEGER, selected INTEGER, currency INTEGER, PRIMARY KEY(member_id))''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS settings (guild_id BIGINT, chatxp INTEGER, voicexp INTEGER, dailyxp TEXT, top20 INTEGER, reprole INTEGER, channels TEXT, voicechannels TEXT, levels INTEGER, PRIMARY KEY(guild_id))''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS chromies (guild_id INTEGER, member_id INTEGER, inactive INTEGER, iamsgs INTEGER, PRIMARY KEY (guild_id, member_id))''')
            await conn.commit()

        if not hasattr(self, "tree"):
            self.tree = app_commands.CommandTree(self)
            await self.tree.sync(guild=my_guild)
            self.tree.copy_global_to(guild=my_guild)

        for ext in extensions:
            await self.load_extension(ext)

    async def close(self):
        if self.pool is not None:
            await self.pool.close()
        await self.session.close()
        await super().close()
