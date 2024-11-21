import discord
from discord.ext import commands
from discord import app_commands

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def remove_from_database(self, guild_id: int, member_ids: list[int]):
        removed_members = []
        async with self.bot.pool.acquire() as conn:
            for member_id in member_ids:
                result = await conn.execute(
                    '''DELETE FROM levelling WHERE guild_id = ? AND member_id = ?''',
                    (guild_id, member_id)
                )
                await conn.commit()
                if result:
                    removed_members.append(member_id)
        return removed_members

    @app_commands.command(name="kick", description="Kick a member from your server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"I have kicked {member.name} from the server!\nReason: **{reason}**", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from your server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"I have banned {member.name} from the server!\nReason: **{reason}**", ephemeral=True)

    @app_commands.command(name="dm", description="Send a dm to a member through Hoshi")
    async def dm(self, interaction: discord.Interaction, member: discord.Member, *, message: str):
        await member.send(f"{message}\n\nSent by **{interaction.user.name}**")
        await interaction.response.send_message(f"Your message has been sent to **{member.name}**\n\nYour message was {message}")

    @app_commands.command(name="addrole", description="Add a role to a member")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def addrole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await interaction.response.send_message(f"Gave {member.name} the role {role}", ephemeral=True)

    @app_commands.command(name="removerole", description="Remove a role from a member")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def removerole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await interaction.response.send_message(f"Removed {role} from {member.name}", ephemeral=True)

    @commands.command()
    async def demote(self, ctx, members: commands.Greedy[discord.Member]):
        if not members:
            await ctx.reply("You must mention at least one member to demote.")
            return

        role_to_remove = ctx.guild.get_role(1134797882420117544)
        role_to_add = ctx.guild.get_role(1134797836135964723)

        if not role_to_remove or not role_to_add:
            await ctx.reply("One or both roles could not be found. Please check the role IDs.")
            return

        successful_changes = []
        failed_changes = []
        guild_id = ctx.guild.id
        member_ids = [member.id for member in members]
        removed_from_db = await self.remove_from_database(guild_id, member_ids)

        for member in members:
            try:
                if role_to_remove in member.roles:
                    await member.remove_roles(role_to_remove, reason="Demotion command executed")
                if role_to_add not in member.roles:
                    await member.add_roles(role_to_add, reason="Demotion command executed")

                if member.id in removed_from_db:
                    successful_changes.append(member.mention)
                else:
                    failed_changes.append(member.mention)

            except discord.Forbidden:
                await ctx.reply(f"Could not update roles for {member.mention}. Insufficient permissions.")
            except discord.HTTPException:
                await ctx.reply(f"An error occurred while updating roles for {member.mention}.")

        if successful_changes:
            member_mentions = "\n".join(f"{i}. {mention}" for i, mention in enumerate(successful_changes, start=1))
            embed = discord.Embed(
                title="Members Demoted",
                description=(
                    f"{member_mentions}\n\n"
                    f"-# The `{role_to_remove.name}` role has been removed, the `{role_to_add.name}` role has been added, "
                    f"and they have been removed from the database!"
                ),
                color=0x2b2d31
            )
            await ctx.reply(embed=embed)

        if failed_changes:
            failed_mentions = ", ".join(failed_changes)
            await ctx.reply(f"The following members' roles were updated, but they were not found in the database: {failed_mentions}")

        if not successful_changes and not failed_changes:
            await ctx.reply("No members were updated. Ensure you mentioned valid members and have sufficient permissions.")

    @commands.command()
    async def delete(self, ctx, member: discord.Member):
        await self.remove_from_database(ctx.guild.id, member.id)
        await ctx.reply(f"Okay! {member.mention} has been removed from {ctx.guild.name}'s database")

async def setup(bot):
    await bot.add_cog(mod(bot))