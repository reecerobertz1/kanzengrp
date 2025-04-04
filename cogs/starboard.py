import discord
from discord.ext import commands
import re

class Starboard(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._message_cache: dict[int, discord.Message] = {}
        self.spoiler_regex = re.compile(r'\|\|(.+?)\|\|')
        self.starboard_channel_id = 1357465696635846656
        self.chroma_guild_id = 694010548605550675

    def find_spoiler_urls(self, text: str, url: str) -> bool:
        spoilers = self.spoiler_regex.findall(text)
        return any(url in spoiler for spoiler in spoilers)

    def starboard_embed(self, message: discord.Message, author: discord.Member) -> discord.Embed:
        embed = discord.Embed(
            description=message.content,
            color=0x2B2D31
        )
        embed.set_author(name=author.name, icon_url=author.display_avatar.url)
        embed.add_field(name="Original message", value=f"[Jump!]({message.jump_url})", inline=False)

        if message.reference and message.reference.resolved:
            embed.add_field(
                name="Replying to",
                value=f"[{message.reference.resolved.author}]({message.reference.resolved.jump_url})",
                inline=False
            )

        for attachment in message.attachments:
            if (attachment.content_type and "image" in attachment.content_type) and not attachment.is_spoiler():
                embed.set_image(url=attachment.url)
                break

        if not embed.image and message.embeds:
            for data in message.embeds:
                if data.url and not self.find_spoiler_urls(message.content, data.url) and data.type == "image":
                    embed.set_image(url=data.url)
                    break

        embed.set_footer(text=f"ID: {message.id}")
        embed.timestamp = message.created_at
        return embed

    async def get_message(self, channel: discord.abc.Messageable, message_id: int) -> discord.Message | None:
        try:
            return self._message_cache[message_id]
        except KeyError:
            try:
                msg = await channel.fetch_message(message_id)
                self._message_cache[message_id] = msg
                return msg
            except discord.HTTPException:
                return None

    async def handle_star(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) != "⭐" or payload.guild_id != self.chroma_guild_id:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel_or_thread(payload.channel_id) if guild else None
        if not isinstance(channel, (discord.Thread, discord.TextChannel)):
            return
        
        message = await self.get_message(channel, payload.message_id)
        if not message or message.author.bot:
            return
        
        starboard_channel = guild.get_channel(self.starboard_channel_id)
        embed = self.starboard_embed(message, message.author)
        await starboard_channel.send(content=f"⭐ Starred message in <#{channel.id}>", embed=embed)

    async def handle_star(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) != "⭐" or payload.guild_id != self.chroma_guild_id:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel_or_thread(payload.channel_id) if guild else None
        if not isinstance(channel, (discord.Thread, discord.TextChannel)):
            return
        
        message = await self.get_message(channel, payload.message_id)
        if not message or message.author.bot:
            return

        star_reaction = discord.utils.get(message.reactions, emoji="⭐")
        if not star_reaction or star_reaction.count < 1:
            return

        starboard_channel = guild.get_channel(self.starboard_channel_id)
        embed = self.starboard_embed(message, message.author)
        await starboard_channel.send(content=f"⭐ Starred message in <#{channel.id}>", embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        await self.handle_star(payload)

async def setup(bot):
    await bot.add_cog(Starboard(bot))
