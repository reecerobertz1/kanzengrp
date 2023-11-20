from discord.ext import commands
from discord import app_commands
import discord
import asqlite

class secretsanta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = None
        self.pairings = {}

    async def setup_database(self):
        self.pool = await asqlite.create_pool('databases/levels.db')
        async with self.pool.acquire() as conn:
            await conn.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                discord_id INTEGER,
                bias_list TEXT
            )''')

    @app_commands.command(name='join', description='Set your bias list')
    async def join(self, interaction: discord.Interaction, bias_list: str):
        async with self.pool.acquire() as conn:
            user_id = interaction.user.id
            await conn.execute('INSERT OR REPLACE INTO user_profiles (user_id, discord_id, bias_list) VALUES (?, ?, ?)', (user_id, user_id, bias_list))
            await conn.commit()
        await interaction.response.send_message('Your bias list has been updated!', ephemeral=True)

    @app_commands.command(name='listusers', description='List all users and their bias lists')
    async def list_users(self, interaction: discord.Interaction):
        async with self.pool.acquire() as conn:
            cursor = await conn.execute('SELECT discord_id, bias_list FROM user_profiles')
            all_users = await cursor.fetchall()

        user_list = "\n".join([f"<@{user[0]}> - {user[1]}" for user in all_users])
        await interaction.response.send_message(f"{user_list}")

async def setup(bot):
    await bot.add_cog(secretsanta(bot))