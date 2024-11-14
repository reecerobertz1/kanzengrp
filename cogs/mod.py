import discord
from discord.ext import commands
from discord import app_commands

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @app_commands.command(name="dm", description="Send a dm to a member through mizuki")
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

async def setup(bot):
    await bot.add_cog(mod(bot))