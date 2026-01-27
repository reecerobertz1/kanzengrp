import datetime
import discord
from discord.ext import commands

class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild.id != 1462079847433244799:
            return
        if before.author.bot or before.content == after.content:
            return
        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        editor = None
        try:
            async for entry in before.guild.audit_logs(action=discord.AuditLogAction.message_edit, limit=1):
                if entry.target.id == before.author.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                    editor = entry.user
                    break
        except:
            pass

        embed = discord.Embed(
            title="Message Edited",
            color=0xffa500,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Author", value=f"{before.author.mention} ({before.author.id})", inline=True)
        embed.add_field(name="Channel", value=before.channel.mention, inline=True)
        if editor and editor != before.author:
            embed.add_field(name="Edited by", value=f"{editor.mention} ({editor.id})", inline=True)
        embed.add_field(name="Before", value=before.content[:1024] if before.content else "None", inline=False)
        embed.add_field(name="After", value=after.content[:1024] if after.content else "None", inline=False)
        embed.set_footer(text=f"Message ID: {before.id} | Author ID: {before.author.id}")
        embed.set_thumbnail(url=before.author.display_avatar.url)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild.id != 1462079847433244799:
            return
        if message.author.bot:
            return
        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        deleter = None
        try:
            async for entry in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
                if entry.target.id == message.author.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                    deleter = entry.user
                    break
        except:
            pass

        embed = discord.Embed(
            title="Message Deleted",
            color=0xff0000,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Author", value=f"{message.author.mention} ({message.author.id})", inline=True)
        embed.add_field(name="Channel", value=message.channel.mention, inline=True)
        if deleter:
            embed.add_field(name="Deleted by", value=f"{deleter.mention} ({deleter.id})", inline=True)
        embed.add_field(name="Content", value=message.content[:1024] if message.content else "None", inline=False)
        embed.set_footer(text=f"Message ID: {message.id}")
        embed.set_thumbnail(url=message.author.display_avatar.url)
        await log_channel.send(embed=embed)

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
                async for entry in before.guild.audit_logs(action=discord.AuditLogAction.member_update, limit=1):
                    if entry.target.id == before.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
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
            embed.set_footer(text=f"User ID: {before.id}")
            embed.set_thumbnail(url=before.display_avatar.url)
            await log_channel.send(embed=embed)

        if before.roles != after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]
            changer = None
            reason = None
            try:
                async for entry in before.guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=1):
                    if entry.target.id == before.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                        changer = entry.user
                        reason = entry.reason
                        break
            except:
                pass

            if added_roles or removed_roles:
                embed = discord.Embed(
                    title="Member Roles Updated",
                    color=0x0000ff,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.add_field(name="Member", value=f"{before.mention} ({before.id})", inline=True)
                if changer:
                    embed.add_field(name="Updated by", value=f"{changer.mention} ({changer.id})", inline=True)
                if added_roles:
                    embed.add_field(name="Added Roles", value=", ".join([role.mention for role in added_roles]), inline=False)
                if removed_roles:
                    embed.add_field(name="Removed Roles", value=", ".join([role.mention for role in removed_roles]), inline=False)
                if reason:
                    embed.add_field(name="Reason", value=reason, inline=False)
                embed.set_footer(text=f"User ID: {before.id}")
                embed.set_thumbnail(url=before.display_avatar.url)
                await log_channel.send(embed=embed)

        if before.communication_disabled_until != after.communication_disabled_until:
            embed = discord.Embed(
                title="Member Timeout Updated",
                color=0xffd700,
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name="Member", value=f"{before.mention} ({before.id})", inline=True)
            
            # Get who did it from audit log
            timeout_user = None
            reason = None
            try:
                async for entry in before.guild.audit_logs(action=discord.AuditLogAction.member_update, limit=1):
                    if entry.target.id == before.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                        timeout_user = entry.user
                        reason = entry.reason
                        break
            except:
                pass
            
            if timeout_user:
                embed.add_field(name="Updated by", value=f"{timeout_user.mention} ({timeout_user.id})", inline=True)
            
            if after.communication_disabled_until:
                embed.add_field(name="Timeout Until", value=f"<t:{int(after.communication_disabled_until.timestamp())}:F>", inline=True)
                embed.add_field(name="Duration", value=f"<t:{int(after.communication_disabled_until.timestamp())}:R>", inline=True)
            else:
                embed.add_field(name="Status", value="Timeout Removed", inline=True)
            
            if reason:
                embed.add_field(name="Reason", value=reason, inline=False)
            
            embed.set_footer(text=f"User ID: {before.id}")
            embed.set_thumbnail(url=before.display_avatar.url)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.guild.id != 1462079847433244799:
            return
        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        changes = []
        if before.name != after.name:
            changes.append(f"Name: {before.name} → {after.name}")
        if before.topic != after.topic:
            changes.append(f"Topic: {before.topic or 'None'} → {after.topic or 'None'}")
        if before.position != after.position:
            changes.append(f"Position: {before.position} → {after.position}")
        if before.category != after.category:
            changes.append(f"Category: {before.category.name if before.category else 'None'} → {after.category.name if after.category else 'None'}")

        if before.overwrites != after.overwrites:
            permission_changes = []

            for target, overwrite in after.overwrites.items():
                if target not in before.overwrites:
                    target_name = target.name if hasattr(target, 'name') else str(target)
                    target_type = "Role" if isinstance(target, discord.Role) else "User"
                    allow_perms = [perm[0] for perm in overwrite if perm[1] is True]
                    deny_perms = [perm[0] for perm in overwrite if perm[1] is False]
                    allow_str = f"Allow: {', '.join(allow_perms)}" if allow_perms else ""
                    deny_str = f"Deny: {', '.join(deny_perms)}" if deny_perms else ""
                    perm_details = " | ".join([s for s in [allow_str, deny_str] if s])
                    permission_changes.append(f"**Added {target_type} Override:** {target_name}\n{perm_details}")

            for target, overwrite in before.overwrites.items():
                if target not in after.overwrites:
                    target_name = target.name if hasattr(target, 'name') else str(target)
                    target_type = "Role" if isinstance(target, discord.Role) else "User"
                    allow_perms = [perm[0] for perm in overwrite if perm[1] is True]
                    deny_perms = [perm[0] for perm in overwrite if perm[1] is False]
                    allow_str = f"Allow: {', '.join(allow_perms)}" if allow_perms else ""
                    deny_str = f"Deny: {', '.join(deny_perms)}" if deny_perms else ""
                    perm_details = " | ".join([s for s in [allow_str, deny_str] if s])
                    permission_changes.append(f"**Removed {target_type} Override:** {target_name}\n{perm_details}")

            for target, after_overwrite in after.overwrites.items():
                if target in before.overwrites:
                    before_overwrite = before.overwrites[target]
                    if before_overwrite != after_overwrite:
                        target_name = target.name if hasattr(target, 'name') else str(target)
                        target_type = "Role" if isinstance(target, discord.Role) else "User"

                        before_allow = [perm[0] for perm in before_overwrite if perm[1] is True]
                        before_deny = [perm[0] for perm in before_overwrite if perm[1] is False]

                        after_allow = [perm[0] for perm in after_overwrite if perm[1] is True]
                        after_deny = [perm[0] for perm in after_overwrite if perm[1] is False]

                        added_allow = [p for p in after_allow if p not in before_allow]
                        removed_allow = [p for p in before_allow if p not in after_allow]
                        added_deny = [p for p in after_deny if p not in before_deny]
                        removed_deny = [p for p in before_deny if p not in after_deny]
                        
                        change_details = []
                        if added_allow:
                            change_details.append(f"+Allow: {', '.join(added_allow)}")
                        if removed_allow:
                            change_details.append(f"-Allow: {', '.join(removed_allow)}")
                        if added_deny:
                            change_details.append(f"+Deny: {', '.join(added_deny)}")
                        if removed_deny:
                            change_details.append(f"-Deny: {', '.join(removed_deny)}")
                        
                        if change_details:
                            permission_changes.append(f"**Modified {target_type} Override:** {target_name}\n{chr(10).join(change_details)}")
            
            if permission_changes:
                changes.append("**Permission Changes:**\n" + "\n\n".join(permission_changes))
        if not changes:
            return

        updater = None
        try:
            async for entry in before.guild.audit_logs(action=discord.AuditLogAction.channel_update, limit=1):
                if entry.target.id == before.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                    updater = entry.user
                    break
        except:
            pass

        embed = discord.Embed(
            title="Channel Updated",
            color=0xffff00,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Channel", value=f"{before.mention} ({before.id})", inline=True)
        if updater:
            embed.add_field(name="Updated by", value=f"{updater.mention} ({updater.id})", inline=True)
        embed.add_field(name="Changes", value="\n".join(changes), inline=False)
        embed.set_footer(text=f"Channel ID: {before.id}")
        embed.set_thumbnail(url=before.guild.icon.url if before.guild.icon else discord.Embed.Empty)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.guild.id != 1462079847433244799:
            return
        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        creator = None
        try:
            async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create, limit=1):
                if entry.target.id == channel.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                    creator = entry.user
                    break
        except:
            pass

        channel_type = "Category" if isinstance(channel, discord.CategoryChannel) else "Channel"
        embed = discord.Embed(
            title=f"{channel_type} Created",
            color=0x00ff00,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name=channel_type, value=f"{channel.name} ({channel.id})", inline=True)
        if creator:
            embed.add_field(name="Created by", value=f"{creator.mention} ({creator.id})", inline=True)
        embed.add_field(name="Type", value=channel_type, inline=True)
        if hasattr(channel, 'position'):
            embed.add_field(name="Position", value=channel.position, inline=True)
        if hasattr(channel, 'category') and channel.category:
            embed.add_field(name="Category", value=channel.category.name, inline=True)
        embed.set_footer(text=f"{channel_type} ID: {channel.id}")
        embed.set_thumbnail(url=channel.guild.icon.url if channel.guild.icon else discord.Embed.Empty)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if channel.guild.id != 1462079847433244799:
            return
        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        deleter = None
        try:
            async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1):
                if entry.target.id == channel.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                    deleter = entry.user
                    break
        except:
            pass

        channel_type = "Category" if isinstance(channel, discord.CategoryChannel) else "Channel"
        embed = discord.Embed(
            title=f"{channel_type} Deleted",
            color=0xff0000,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name=channel_type, value=f"{channel.name} ({channel.id})", inline=True)
        if deleter:
            embed.add_field(name="Deleted by", value=f"{deleter.mention} ({deleter.id})", inline=True)
        embed.add_field(name="Type", value=channel_type, inline=True)
        if hasattr(channel, 'position'):
            embed.add_field(name="Position", value=channel.position, inline=True)
        embed.set_footer(text=f"{channel_type} ID: {channel.id}")
        embed.set_thumbnail(url=channel.guild.icon.url if channel.guild.icon else discord.Embed.Empty)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if before.id != 1462079847433244799:
            return
        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        changes = []
        updater = None

        if before.icon != after.icon:
            try:
                async for entry in before.audit_logs(action=discord.AuditLogAction.guild_update, limit=1):
                    if (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                        updater = entry.user
                        break
            except:
                pass

            embed = discord.Embed(
                title="Server Icon Updated",
                color=0x3498db,
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name="Server", value=f"{before.name} ({before.id})", inline=True)
            if updater:
                embed.add_field(name="Updated by", value=f"{updater.mention} ({updater.id})", inline=True)
            embed.add_field(name="Old Icon", value="None" if not before.icon else f"[View Old Icon]({before.icon.url})", inline=True)
            embed.add_field(name="New Icon", value="None" if not after.icon else f"[View New Icon]({after.icon.url})", inline=True)
            embed.set_footer(text=f"Server ID: {before.id}")
            if after.icon:
                embed.set_thumbnail(url=after.icon.url)
            else:
                embed.set_thumbnail(url=before.guild.icon.url if before.guild.icon else discord.Embed.Empty)
            await log_channel.send(embed=embed)
            return

        if before.banner != after.banner:
            if not updater:
                try:
                    async for entry in before.audit_logs(action=discord.AuditLogAction.guild_update, limit=1):
                        if (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                            updater = entry.user
                            break
                except:
                    pass

            embed = discord.Embed(
                title="Server Banner Updated",
                color=0xe67e22,
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name="Server", value=f"{before.name} ({before.id})", inline=True)
            if updater:
                embed.add_field(name="Updated by", value=f"{updater.mention} ({updater.id})", inline=True)
            embed.add_field(name="Old Banner", value="None" if not before.banner else f"[View Old Banner]({before.banner.url})", inline=True)
            embed.add_field(name="New Banner", value="None" if not after.banner else f"[View New Banner]({after.banner.url})", inline=True)
            embed.set_footer(text=f"Server ID: {before.id}")
            if after.banner:
                embed.set_image(url=after.banner.url)
            embed.set_thumbnail(url=before.guild.icon.url if before.guild.icon else discord.Embed.Empty)
            await log_channel.send(embed=embed)
            return 

        if before.name != after.name:
            changes.append(f"Name: {before.name} → {after.name}")
        if before.description != after.description:
            changes.append(f"Description: {before.description or 'None'} → {after.description or 'None'}")
        if before.verification_level != after.verification_level:
            changes.append(f"Verification Level: {before.verification_level.name} → {after.verification_level.name}")
        if before.explicit_content_filter != after.explicit_content_filter:
            changes.append(f"Explicit Content Filter: {before.explicit_content_filter.name} → {after.explicit_content_filter.name}")
        if before.default_notifications != after.default_notifications:
            changes.append(f"Default Notifications: {before.default_notifications.name} → {after.default_notifications.name}")
        if before.afk_timeout != after.afk_timeout:
            changes.append(f"AFK Timeout: {before.afk_timeout // 60} minutes → {after.afk_timeout // 60} minutes")
        if before.afk_channel != after.afk_channel:
            changes.append(f"AFK Channel: {before.afk_channel.name if before.afk_channel else 'None'} → {after.afk_channel.name if after.afk_channel else 'None'}")
        if before.system_channel != after.system_channel:
            changes.append(f"System Channel: {before.system_channel.name if before.system_channel else 'None'} → {after.system_channel.name if after.system_channel else 'None'}")
        if before.system_channel_flags != after.system_channel_flags:
            changes.append(f"System Channel Flags: {before.system_channel_flags.value} → {after.system_channel_flags.value}")

        if not changes:
            return

        if not updater:
            try:
                async for entry in before.audit_logs(action=discord.AuditLogAction.guild_update, limit=1):
                    if (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                        updater = entry.user
                        break
            except:
                pass

        embed = discord.Embed(
            title="Server Settings Updated",
            color=0x9b59b6,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Server", value=f"{before.name} ({before.id})", inline=True)
        if updater:
            embed.add_field(name="Updated by", value=f"{updater.mention} ({updater.id})", inline=True)
        embed.add_field(name="Changes", value="\n".join(changes), inline=False)
        embed.set_footer(text=f"Server ID: {before.id}")
        embed.set_thumbnail(url=before.guild.icon.url if before.guild.icon else discord.Embed.Empty)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if guild.id != 1462079847433244799:
            return
        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        reason = None
        banner = None
        try:
            async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=1):
                if entry.target.id == user.id:
                    banner = entry.user
                    reason = entry.reason
                    break
        except:
            pass

        embed = discord.Embed(
            title="Member Banned",
            color=0x8b0000,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="User", value=f"{user} ({user.id})", inline=True)
        if banner:
            embed.add_field(name="Banned by", value=f"{banner.mention} ({banner.id})", inline=True)
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"User ID: {user.id}")
        embed.set_thumbnail(url=user.display_avatar.url)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if guild.id != 1462079847433244799:
            return
        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        reason = None
        unbanner = None
        try:
            async for entry in guild.audit_logs(action=discord.AuditLogAction.unban, limit=1):
                if entry.target.id == user.id:
                    unbanner = entry.user
                    reason = entry.reason
                    break
        except:
            pass

        embed = discord.Embed(
            title="Member Unbanned",
            color=0x006400,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="User", value=f"{user} ({user.id})", inline=True)
        if unbanner:
            embed.add_field(name="Unbanned by", value=f"{unbanner.mention} ({unbanner.id})", inline=True)
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"User ID: {user.id}")
        embed.set_thumbnail(url=user.display_avatar.url)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != 1462079847433244799:
            return
        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return
        
        kicker = None
        reason = None
        try:
            async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick, limit=1):
                if entry.target.id == member.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
                    kicker = entry.user
                    reason = entry.reason
                    break
        except:
            pass

        if kicker:
            embed = discord.Embed(
                title="Member Kicked",
                color=0xff4500,
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(name="User", value=f"{member} ({member.id})", inline=True)
            embed.add_field(name="Kicked by", value=f"{kicker.mention} ({kicker.id})", inline=True)
            if reason:
                embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"User ID: {member.id}")
            embed.set_thumbnail(url=member.display_avatar.url)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        if invite.guild.id != 1462079847433244799:
            return
        log_channel = self.bot.get_channel(1462240814318227477)
        if not log_channel:
            return

        embed = discord.Embed(
            title="Invite Created",
            color=0x800080,
            timestamp=datetime.datetime.utcnow()
        )
        if invite.inviter:
            embed.add_field(name="Created by", value=f"{invite.inviter.mention} ({invite.inviter.id})", inline=True)
        embed.add_field(name="Channel", value=invite.channel.mention, inline=True)
        embed.add_field(name="Invite Code", value=invite.code, inline=True)
        embed.add_field(name="Max Uses", value="Unlimited" if invite.max_uses == 0 else str(invite.max_uses), inline=True)
        embed.add_field(name="Expires", value=f"<t:{int(invite.expires_at.timestamp())}:R>" if invite.expires_at else "Never", inline=True)
        embed.set_footer(text=f"Invite Code: {invite.code}")
        embed.set_thumbnail(url=invite.guild.icon.url if invite.guild.icon else discord.Embed.Empty)
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
            async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_create, limit=1):
                if entry.target.id == role.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
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
        embed.add_field(name="Permissions", value=len([p for p in role.permissions if p[1]]), inline=True)
        embed.add_field(name="Position", value=role.position, inline=True)
        embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
        embed.add_field(name="Hoisted", value=role.hoist, inline=True)
        embed.set_footer(text=f"Role ID: {role.id}")
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
            changes.append(f"Color: #{before.color.value:06x} → #{after.color.value:06x}")
        if before.permissions != after.permissions:
            added_perms = []
            removed_perms = []
            
            for perm_name, has_perm in after.permissions:
                if has_perm and not getattr(before.permissions, perm_name, False):
                    added_perms.append(perm_name)
            
            for perm_name, has_perm in before.permissions:
                if has_perm and not getattr(after.permissions, perm_name, False):
                    removed_perms.append(perm_name)
            
            if added_perms or removed_perms:
                perm_changes = []
                if added_perms:
                    perm_changes.append(f"**Added Permissions:** {', '.join(added_perms)}")
                if removed_perms:
                    perm_changes.append(f"**Removed Permissions:** {', '.join(removed_perms)}")
                changes.append("\n".join(perm_changes))
        if before.hoist != after.hoist:
            changes.append(f"Hoisted: {before.hoist} → {after.hoist}")
        if before.mentionable != after.mentionable:
            changes.append(f"Mentionable: {before.mentionable} → {after.mentionable}")
        if before.position != after.position:
            changes.append(f"Position: {before.position} → {after.position}")

        if not changes:
            return

        updater = None
        try:
            async for entry in before.guild.audit_logs(action=discord.AuditLogAction.role_update, limit=1):
                if entry.target.id == before.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
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
        embed.set_footer(text=f"Role ID: {before.id}")
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
            async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_delete, limit=1):
                if entry.target.id == role.id and (datetime.datetime.utcnow() - entry.created_at).total_seconds() < 10:
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
        embed.add_field(name="Permissions", value=len([p for p in role.permissions if p[1]]), inline=True)
        embed.add_field(name="Position", value=role.position, inline=True)
        embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
        embed.add_field(name="Hoisted", value=role.hoist, inline=True)
        embed.set_footer(text=f"Role ID: {role.id}")
        embed.set_thumbnail(url=role.guild.icon.url if role.guild.icon else discord.Embed.Empty)
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(logging(bot))