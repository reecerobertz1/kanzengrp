import discord
from discord.ext import commands
from discord import app_commands

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2b2d31

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
                color=self.color
            )
            await ctx.reply(embed=embed)

        if failed_changes:
            failed_mentions = ", ".join(failed_changes)
            await ctx.reply(f"The following members' roles were updated, but they were not found in the database: {failed_mentions}")

        if not successful_changes and not failed_changes:
            await ctx.reply("No members were updated. Ensure you mentioned valid members and have sufficient permissions.")

    @commands.command()
    async def delete(self, ctx, member: discord.Member):
        removed_members = await self.remove_from_database(ctx.guild.id, [member.id])
        if removed_members:
            await ctx.reply(f"Okay! {member.mention} has been removed from {ctx.guild.name}'s database")
        else:
            await ctx.reply(f"{member.mention} was not found in {ctx.guild.name}'s database.")

    @app_commands.command(name="verify", description="Verify someone has completed all giveaway rules")
    async def verify(self, interaction: discord.Interaction, member: discord.Member):
        required_roles = {835549528932220938, 835549528932220938}
        member_roles = {role.id for role in interaction.user.roles}
        if required_roles.isdisjoint(member_roles):
            await interaction.response.send_message("Sorry, this command is only available for staff members!", ephemeral=True)
            return

        view = discord.ui.View()
        galink = discord.ui.Button(label="Access Link", url="https://mega.nz/folder/GcdAibib#-kUoNp91QxF10cX5a5x6qA", emoji="🎁")
        view.add_item(galink)
        embed = discord.Embed(title="Chroma Christmas Giveaway", description="Thank you so much for joining our giveaway!\n\n**Rules:**\nWe ask that you respect all of our contributors by rightfully crediting them. They are providing you with their resources for free through this giveaway; therefore we also ask you to show them common courtesy by not spreading their resources without consent. Failing to do so is plainly disrespectful and unfair towards the people who put a lot of time into making this giveaway happen.\n\n**Information:**\n・Each folder in the mega link is named by the contributor's Instagram username.\n・There are many resources in this link for you to use. Some contributor's have added things for multiple editing programs/apps.\n・Not all of the resources were shown in the giveaway.\n・Some contributor's have added a `READ ME` file, or similar, there they will say what they have added and how to give credit's correctly.\n\nClick the button below to gain access to our giveaway!\nHappy Holiday's 🌈", color=self.color)
        await interaction.response.send_message(f"<:whitecheck:1304222829595721770> Okay! I have sent the mega link to **{member.name}**", ephemeral=True)
        channel = interaction.client.get_channel(1319765047614115871)
        log = discord.Embed(title="Giveaway Logs", description=f"**{interaction.user.mention}** verified **{member.mention}**", color=self.color)
        log.set_thumbnail(url=member.avatar)
        await channel.send(embed=log)
        await member.send(embed=embed, view=view)

    @commands.hybrid_command(name="dm", aliases=["message"], description="Dm a user through hoshi", extras="+dm @member (message) : alias +message")
    async def dm(self, ctx, member: discord.Member, *, message: str):
        await member.send(message)
        await ctx.send(f"i have successfully messaged {member.mention}\n{message}")   

async def setup(bot):
    await bot.add_cog(mod(bot))