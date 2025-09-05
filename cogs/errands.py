import discord
from discord.ext import commands
from discord import app_commands
import random
from datetime import timedelta
from typing import Optional, TypedDict


class LevelRow(TypedDict):
    guild_id: int
    member_id: int
    xp: int
    messages: int
    color: str
    color2: str
    image: str


class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_min = 100
        self.xp_max = 200

        self.task_defs = {
            "messages": {
                "desc": "Send 5 messages in <#694010549532360726> or <#1279622704084811776>",
                "channels": [1248039148888129647, 1248039148888129647],
                "count_needed": 5,
                "type": "message"
            },
            "pets": {
                "desc": "Post a picture of your pet in <#1370469965135872140>",
                "channel": 1248039148888129647,
                "needs_attachment": False,
                "type": "message"
            },
            "qotd": {
                "desc": "Answer the question of the day in <#1352448775943229582>",
                "channel": 1248039148888129647,
                "type": "message"
            },
            "jail": {
                "desc": "Use the command </jail:1203759833493540925> to put a member in jail",
                "command_name": "jail",
                "type": "command"
            },
            "palette": {
                "desc": "Use the command </palette:1327717613815599117> to create a new colour palette",
                "command_name": "palette",
                "type": "command"
            },
            "8ball": {
                "desc": "Use the command </8ball:1304250227494096959> and ask hoshi a question",
                "command_name": "8ball",
                "type": "command"
            },
        }

        # {user_id: {"tasks": {task_key: {"progress": int, "done": bool}}, "xp_reward": int, "message": discord.Message}}
        self.user_errands = {}

    async def get_daily_errands(self, user_id, num_tasks=3):
        """Get or create errands for a user."""
        if user_id in self.user_errands:  # don't overwrite existing tasks
            return list(self.user_errands[user_id]["tasks"].keys()), self.user_errands[user_id]["xp_reward"]

        selected_keys = random.sample(list(self.task_defs.keys()), k=num_tasks)
        xp_reward = random.randint(self.xp_min, self.xp_max)
        self.user_errands[user_id] = {
            "tasks": {k: {"progress": 0, "done": False} for k in selected_keys},
            "xp_reward": xp_reward,
            "message": None
        }
        return selected_keys, xp_reward

    def build_errands_embed(self, user_id):
        errands = self.user_errands[user_id]["tasks"]
        lines = []
        for key, info in errands.items():
            task = self.task_defs[key]
            if info["done"]:
                lines.append(f"☑️ {task['desc']}")
            else:
                if key == "messages":
                    lines.append(f"⬜ {task['desc']} ({info['progress']}/{task['count_needed']})")
                else:
                    lines.append(f"⬜ {task['desc']}")
        embed = discord.Embed(description="### **Daily errands**\n" + "\n".join(lines))
        return embed

    async def update_progress(self, user_id, channel, actor=None):
        if user_id not in self.user_errands:
            return

        errands = self.user_errands[user_id]
        if errands["message"]:
            embed = self.build_errands_embed(user_id)
            try:
                await errands["message"].edit(embed=embed)
            except discord.NotFound:
                errands["message"] = None

        done_all = all(info["done"] for info in errands["tasks"].values())
        if done_all and actor:
            guild_id = actor.guild.id
            xp = errands["xp_reward"]

            # fetch existing levels row if available
            levels = await self.fetch_levels(user_id, guild_id)

            await self.add_xp(user_id, guild_id, xp, levels)
            await channel.send(
                f"🎉 Thank you {actor.mention} for doing your errands! "
                f"Here's **{xp} XP**!"
            )
            self.user_errands.pop(user_id, None)

    @commands.hybrid_command(name="errands", description="Complete daily errands to earn xp")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def errands(self, ctx):
        user_id = ctx.author.id
        tasks, xp_reward = await self.get_daily_errands(user_id)

        embed = self.build_errands_embed(user_id)

        try:
            dm = await ctx.author.create_dm()
            msg = await dm.send(embed=embed)
            self.user_errands[user_id]["message"] = msg
            await ctx.reply("📩 I've sent your errands to your DMs!", ephemeral=True)
        except discord.Forbidden:
            await ctx.reply("❌ I couldn't DM you your errands. Please enable DMs!", ephemeral=True)

    @errands.error
    async def errands_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            retry = timedelta(seconds=round(error.retry_after))
            hours, remainder = divmod(retry.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left = f"{hours}h {minutes}m {seconds}s"

            if ctx.interaction:
                await ctx.interaction.response.send_message(
                    f"You have already completed all errands today! Try again in `{time_left}`.",
                    ephemeral=True
                )
            else:
                await ctx.reply(f"You have already completed all errands today! Try again in `{time_left}`.")
        else:
            raise error

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        user_id = message.author.id
        if user_id not in self.user_errands:
            return

        errands = self.user_errands[user_id]["tasks"]

        for task_key, info in errands.items():
            if info["done"]:
                continue
            task = self.task_defs[task_key]

            if task["type"] != "message":
                continue

            if task_key == "messages" and message.channel.id in task["channels"]:
                info["progress"] += 1
                if info["progress"] >= task["count_needed"]:
                    info["done"] = True

            elif task_key == "pets" and message.channel.id == task["channel"]:
                if message.attachments:
                    info["done"] = True

            elif task_key == "qotd" and message.channel.id == task["channel"]:
                info["done"] = True

        await self.update_progress(user_id, message.channel, message.author)

    async def fetch_levels(self, member_id: int, guild_id: int) -> Optional[LevelRow]:
        """Fetch the user's levelling row if it exists."""
        query = '''SELECT member_id, guild_id, xp, messages, color, color2, image
                   FROM levelling WHERE member_id = ? AND guild_id = ?'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id))
                row = await cursor.fetchone()
            await self.bot.pool.release(conn)
        if row:
            return LevelRow(
                member_id=row[0],
                guild_id=row[1],
                xp=row[2],
                messages=row[3],
                color=row[4],
                color2=row[5],
                image=row[6],
            )
        return None

    async def add_member(self, member_id: int, guild_id: int, xp=25) -> None:
        query = '''INSERT INTO levelling (member_id, guild_id, xp, messages, color, color2, image)
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (member_id, guild_id, xp, 1, "#100429", "#ECE2E2", ""))
                await conn.commit()
            await self.bot.pool.release(conn)

    async def add_xp(self, member_id: int, guild_id: int, xp: int, levels: Optional[LevelRow]) -> None:
        if levels:
            query = '''UPDATE levelling SET xp = ? WHERE member_id = ? AND guild_id = ?'''
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, (levels['xp'] + xp, member_id, guild_id))
                    await conn.commit()
                await self.bot.pool.release(conn)
        else:
            await self.add_member(member_id, guild_id, xp)


async def setup(bot):
    await bot.add_cog(Forms(bot))