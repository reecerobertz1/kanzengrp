import datetime
import discord
from discord.ext import commands

class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild.id != 1462079847433244799:
            return
        if before.bot:
            return

        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        if before.nick != after.nick:
            changer = None
            try:
                async for entry in before.guild.audit_logs(
                    action=discord.AuditLogAction.member_update, limit=1
                ):
                    if entry.target.id == before.id:
                        changer = entry.user
                        break
            except:
                pass

            embed = discord.Embed(
                title="Nickname Updated",
                color=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name="Member", value=f"{before.mention} ({before.id})", inline=True)
            embed.add_field(name="Before", value=before.nick or before.name, inline=True)
            embed.add_field(name="After", value=after.nick or after.name, inline=True)
            if changer:
                embed.add_field(name="Changed by", value=f"{changer.mention} ({changer.id})", inline=True)
            embed.set_thumbnail(url=before.display_avatar.url)
            await log_channel.send(embed=embed)

        if before.roles != after.roles:
            added_roles = [r for r in after.roles if r not in before.roles]
            removed_roles = [r for r in before.roles if r not in after.roles]

            if not added_roles and not removed_roles:
                return

            changer = None
            reason = None
            try:
                async for entry in before.guild.audit_logs(
                    action=discord.AuditLogAction.member_role_update, limit=1
                ):
                    if entry.target.id == before.id:
                        changer = entry.user
                        reason = entry.reason
                        break
            except:
                pass

            embed = discord.Embed(
                title="Member Roles Updated",
                color=0x0000ff,
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name="Member", value=f"{before.mention} ({before.id})", inline=True)

            if changer:
                embed.add_field(name="Updated by", value=f"{changer.mention} ({changer.id})", inline=True)

            if added_roles:
                embed.add_field(
                    name="Added Roles",
                    value=", ".join(r.mention for r in added_roles),
                    inline=False
                )

            if removed_roles:
                embed.add_field(
                    name="Removed Roles",
                    value=", ".join(r.mention for r in removed_roles),
                    inline=False
                )

            if reason:
                embed.add_field(name="Reason", value=reason, inline=False)

            embed.set_thumbnail(url=before.display_avatar.url)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if role.guild.id != 1462079847433244799:
            return

        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        creator = None
        try:
            async for entry in role.guild.audit_logs(
                action=discord.AuditLogAction.role_create, limit=1
            ):
                if entry.target.id == role.id:
                    creator = entry.user
                    break
        except:
            pass

        embed = discord.Embed(
            title="Role Created",
            color=0x00ff00,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Role", value=f"{role.mention} ({role.id})", inline=True)
        if creator:
            embed.add_field(name="Created by", value=f"{creator.mention} ({creator.id})", inline=True)
        embed.add_field(name="Color", value=f"#{role.color.value:06x}", inline=True)
        embed.add_field(
            name="Permissions",
            value=len([p for p in role.permissions if p[1]]),
            inline=True
        )
        embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
        embed.add_field(name="Hoisted", value=role.hoist, inline=True)
        embed.set_thumbnail(url=role.guild.icon.url if role.guild.icon else discord.Embed.Empty)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if before.guild.id != 1462079847433244799:
            return

        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        changes = []

        if before.name != after.name:
            changes.append(f"Name: {before.name} → {after.name}")

        if before.color != after.color:
            changes.append(
                f"Color: #{before.color.value:06x} → #{after.color.value:06x}"
            )

        if before.permissions != after.permissions:
            added = []
            removed = []

            for perm, value in after.permissions:
                if value and not getattr(before.permissions, perm):
                    added.append(perm)

            for perm, value in before.permissions:
                if value and not getattr(after.permissions, perm):
                    removed.append(perm)

            if added:
                changes.append(f"Added Permissions: {', '.join(added)}")
            if removed:
                changes.append(f"Removed Permissions: {', '.join(removed)}")

        if before.hoist != after.hoist:
            changes.append(f"Hoisted: {before.hoist} → {after.hoist}")

        if before.mentionable != after.mentionable:
            changes.append(f"Mentionable: {before.mentionable} → {after.mentionable}")

        if not changes:
            return

        updater = None
        try:
            async for entry in before.guild.audit_logs(
                action=discord.AuditLogAction.role_update, limit=1
            ):
                if entry.target.id == before.id:
                    updater = entry.user
                    break
        except:
            pass

        embed = discord.Embed(
            title="Role Updated",
            color=0xffa500,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Role", value=f"{before.mention} ({before.id})", inline=True)
        if updater:
            embed.add_field(name="Updated by", value=f"{updater.mention} ({updater.id})", inline=True)
        embed.add_field(name="Changes", value="\n".join(changes), inline=False)
        embed.set_thumbnail(url=before.guild.icon.url if before.guild.icon else discord.Embed.Empty)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if role.guild.id != 1462079847433244799:
            return

        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        deleter = None
        try:
            async for entry in role.guild.audit_logs(
                action=discord.AuditLogAction.role_delete, limit=1
            ):
                if entry.target.id == role.id:
                    deleter = entry.user
                    break
        except:
            pass

        embed = discord.Embed(
            title="Role Deleted",
            color=0xff0000,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Role", value=f"{role.name} ({role.id})", inline=True)
        if deleter:
            embed.add_field(name="Deleted by", value=f"{deleter.mention} ({deleter.id})", inline=True)
        embed.add_field(name="Color", value=f"#{role.color.value:06x}", inline=True)
        embed.add_field(
            name="Permissions",
            value=len([p for p in role.permissions if p[1]]),
            inline=True
        )
        embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
        embed.add_field(name="Hoisted", value=role.hoist, inline=True)
        embed.set_thumbnail(url=role.guild.icon.url if role.guild.icon else discord.Embed.Empty)
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(logging(bot))