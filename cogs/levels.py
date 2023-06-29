import json
import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import random

class levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_level(self, xp):
        return int((xp // 100) ** 0.5)

    def save_data(self):
        with open("xp_data.json", "w") as file:
            json.dump(self.xp_data, file)

    def load_data(self):
        try:
            with open("xp_data.json", "r") as file:
                self.xp_data = json.load(file)
        except FileNotFoundError:
            self.xp_data = {}

    def update_xp(self, guild_id, user_id, xp):
        if guild_id not in self.xp_data:
            self.xp_data[guild_id] = {}
        self.xp_data[guild_id][user_id] = self.xp_data[guild_id].get(user_id, 0) + xp
        self.save_data()

    @commands.Cog.listener()
    async def on_ready(self):
        self.load_data()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_id = message.guild.id
        user_id = message.author.id
        xp = 10  # Modify this to change the XP gained per message

        self.update_xp(guild_id, user_id, xp)

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        guild_id = ctx.guild.id
        user_id = member.id

        xp = self.xp_data.get(guild_id, {}).get(user_id, 0)
        level = self.get_level(xp)

        rank_card = discord.File("rank_card.png", filename="rank_card.png")
        embed = discord.Embed(title="Rank Card", color=discord.Color.blue())
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Level", value=str(level))
        embed.add_field(name="XP", value=str(xp))

        await ctx.send(file=rank_card, embed=embed)

    @commands.command()
    async def leaderboard(self, ctx, page: int = 1):
        guild_id = ctx.guild.id
        xp_data = self.xp_data.get(guild_id, {})

        sorted_users = sorted(xp_data, key=xp_data.get, reverse=True)
        start_index = (page - 1) * 10
        end_index = start_index + 10
        leaderboard = ""

        for index, user_id in enumerate(sorted_users[start_index:end_index], start=start_index):
            member = ctx.guild.get_member(user_id)
            if member:
                leaderboard += f"{index + 1}. {member.display_name} - Level {self.get_level(xp_data[user_id])}\n"

        embed = discord.Embed(title="Leaderboard", description=leaderboard, color=discord.Color.blue())
        embed.set_footer(text=f"Page {page}/{((len(sorted_users) - 1) // 10) + 1}")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def addxp(self, ctx, member: discord.Member, xp: int):
        guild_id = ctx.guild.id
        user_id = member.id

        self.update_xp(guild_id, user_id, xp)
        await ctx.send(f"Added {xp} XP to {member.display_name}.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def removexp(self, ctx, member: discord.Member, xp: int):
        guild_id = ctx.guild.id
        user_id = member.id

        self.update_xp(guild_id, user_id, -xp)
        await ctx.send(f"Removed {xp} XP from {member.display_name}.")


async def setup(bot):
    await bot.add_cog(levels(bot))