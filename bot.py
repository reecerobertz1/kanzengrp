from discord.ext import commands
import discord
import aiohttp
from datetime import datetime
import asqlite
from discord import app_commands

my_guild = discord.Object(id=1121841073673736215)

extensions = {
    "jishaku",
    "cogs.eb",
    "cogs.economy",
    "cogs.editing",
    "cogs.fun",
    "cogs.games",
    "cogs.help",
    "cogs.kanzen",
    "cogs.levels",
    "cogs.misc",
    "cogs.moderation",
    "cogs.other",
    "cogs.welcandbye",
    "cogs.countryvia",
    "cogs.chromalevels",
    "cogs.starboard",
    "cogs.be"
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
            await conn.execute('''CREATE TABLE IF NOT EXISTS levels (member_id BIGINT, xp INTEGER, messages INTEGER, image TEXT, color TEXT, stardust INTEGER, memberlvl INTEGER, mora INTEGER, decor TEXT, roles TEXT, PRIMARY KEY(member_id))''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS chromalevels (member_id BIGINT, xp INTEGER, messages INTEGER, image TEXT, color TEXT, PRIMARY KEY(member_id))''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS setup (guild_id BIGINT PRIMARY KEY, activated BOOL, top_20_role_id BIGINT, bronze_role_id BIGINT, silver_role_id BIGINT, gold_role_id BIGINT, diamond_role_id BIGINT, plat_role_id BIGINT, elite_role_id BIGINT)''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS warning (member_id INTEGER, guild_id INTEGER ,reasons TEXT, warnings INTEGER)''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS staffrep(member_id INTEGER, helped INTEGER, count INTEGER, guild_id INTEGER)''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS apps (guild_id INTEGER, member_id INTEGER, apps INTEGER DEFAULT 2, accepted TEXT, applied TEXT, reece INTEGER, nani INTEGER, adil INTEGER, kelly INTEGER, luki INTEGER, josh INTEGER, kio INTEGER, mari INTEGER, marie INTEGER, riri INTEGER)''')
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
