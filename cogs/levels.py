import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import random

class levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.add_experience(message.author, 5)

    async def add_experience(self, member, xp):
        # Add the given amount of XP to the member's total
        # You can customize this logic to suit your needs
        # Example: Store XP in a database or file
        # For now, we'll use a simple dictionary as an in-memory storage
        guild_id = member.guild.id
        user_id = member.id

        if guild_id not in self.bot.xp_data:
            self.bot.xp_data[guild_id] = {}
        if user_id not in self.bot.xp_data[guild_id]:
            self.bot.xp_data[guild_id][user_id] = 0

        self.bot.xp_data[guild_id][user_id] += xp

        # Check if the member has leveled up
        level = self.get_level(self.bot.xp_data[guild_id][user_id])
        if level > 1:
            await self.check_level_up(member, level)

    def get_level(self, xp):
        # Calculate the level based on the XP
        # You can customize this logic to suit your needs
        return xp // 100  # Assuming 100 XP per level

    async def check_level_up(self, member, level):
        # Perform actions when a member levels up
        # You can customize this to your liking
        # Example: Assign roles, send messages, etc.
        await member.send(f"Congratulations! You leveled up to level {level}!")

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        guild_id = ctx.guild.id
        user_id = member.id

        xp = self.bot.xp_data.get(guild_id, {}).get(user_id, 0)
        level = self.get_level(xp)

        # You can customize the rank card design to your liking
        # Here's a basic example
        rank_card = discord.File("rank_card.png", filename="rank_card.png")
        embed = discord.Embed(title="Rank Card", color=discord.Color.blue())
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Level", value=str(level))
        embed.add_field(name="XP", value=str(xp))

        await ctx.send(file=rank_card, embed=embed)

    @commands.command()
    @commands.is_owner()
    async def addxp(self, ctx, member: discord.Member, xp: int):
        await self.add_experience(member, xp)
        await ctx.send(f"{xp} XP added to {member.display_name}.")

    @commands.command()
    @commands.is_owner()
    async def removexp(self, ctx, member: discord.Member, xp: int):
        guild_id = ctx.guild.id
        user_id = member.id

        if guild_id in self.bot.xp_data and user_id in self.bot.xp_data[guild_id]:
            self.bot.xp_data[guild_id][user_id] = max(0, self.bot.xp_data[guild_id][user_id] - xp)
            await ctx.send(f"{xp} XP removed from {member.display_name}.")
        else:
            await ctx.send(f"{member.display_name} has no XP data.")

    @commands.command()
    async def leaderboard(self, ctx, page: int = 1):
        guild_id = ctx.guild.id

        if guild_id in self.bot.xp_data:
            xp_data = self.bot.xp_data[guild_id]
            sorted_xp_data = sorted(xp_data.items(), key=lambda x: x[1], reverse=True)

            items_per_page = 10
            start_index = (page - 1) * items_per_page
            end_index = start_index + items_per_page

            leaderboard = []
            for index, (user_id, xp) in enumerate(sorted_xp_data[start_index:end_index], start=start_index):
                member = ctx.guild.get_member(user_id)
                if member:
                    leaderboard.append(f"{index + 1}. {member.display_name}: {xp} XP")

            if leaderboard:
                embed = discord.Embed(title=f"Leaderboard (Page {page})", description="\n".join(leaderboard), color=discord.Color.gold())
                await ctx.send(embed=embed)
            else:
                await ctx.send("No leaderboard data available.")
        else:
            await ctx.send("No leaderboard data available.")


async def setup(bot):
    await bot.add_cog(levels(bot))