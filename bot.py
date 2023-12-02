from discord.ext import commands
import discord
import aiohttp
from datetime import datetime
import asqlite
from discord import app_commands

my_guild = discord.Object(id=1121841073673736215)

extensions = {
    "jishaku",
    "cogs.aster",
    "cogs.celebgame",
    "cogs.custom",
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
    "cogs.staffapps",
    "cogs.tof",
    "cogs.ttt",
    "cogs.welcandbye"
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
            await conn.execute('''CREATE TABLE IF NOT EXISTS levels (member_id BIGINT, guild_id BIGINT, xp INTEGER, messages INTEGER, bar_color TEXT, image TEXT, PRIMARY KEY(member_id, guild_id))''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS setup (guild_id BIGINT PRIMARY KEY, activated BOOL, top_20_role_id BIGINT)''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS bank (wallet INTEGER, bank INTEGER, maxbank INTEGER, user INTEGER)''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS inventory (user INTEGER,item TEXT,quantity INTEGER DEFAULT 0,PRIMARY KEY (user, item))''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS profiles (user_id INTEGER PRIMARY KEY, about_me TEXT, instagram_username TEXT, pronouns TEXT, banner_url TEXT, background_url TEXT)''')
            await conn.execute('''CREATE TABLE IF NOT EXISTS user_profiles (user_id INTEGER PRIMARY KEY, discord_id INTEGER, bias_list TEXT)''') 
            await conn.execute('''CREATE TABLE IF NOT EXISTS warning (member_id INTEGER, guild_id INTEGER ,reasons TEXT, warnings INTEGER)''')    
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
