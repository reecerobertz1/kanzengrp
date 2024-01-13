import asyncio
import random
import discord
from discord.ext import commands
from typing import TypedDict
import datetime
import humanize
from discord import ui

class banappeal(discord.ui.View):
    def __init__ (self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Appeal Ban", style=discord.ButtonStyle.green)
    async def appeal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(appeal(bot=self.bot))

class approveordecline(discord.ui.View):
    def __init__ (self, bot, one, two, three):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot
        self.guild_id = 1121841073673736215
        self.one = one
        self.two = two
        self.three = three

    async def create_invite(self, guild_id):
        try:
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                raise ValueError("Invalid server ID")

            invite = await guild.text_channels[0].create_invite(max_uses=1, unique=True)
            return invite.url
        except Exception as e:
            print(f"Failed to create invite: {e}")
            return None

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def Approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message_id = interaction.message.id
        msg = await interaction.channel.fetch_message(message_id)
        if msg.embeds:
            embed = msg.embeds[0]
            user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)
            if user_id_field:
                user_id = user_id_field.value.strip()
                try:
                    user = await self.bot.fetch_user(int(user_id))
                except discord.errors.NotFound:
                    await interaction.followup.send("Failed to find the user associated with the appeal. The user might not exist or has left Discord.", ephemeral=True)
                    return
                if user:
                    invite_url = await self.create_invite(self.guild_id)
                    embed.add_field(name="Status", value=":white_check_mark: Approve")
                    await msg.edit(embed=embed, view=None)
                    resolvedembed = discord.Embed(title="Your ban appeal has been approved!", description=f"Please do not continue the behaviour you did before being banned, your appeal will not be approved again...\n[click here to rejoin kanzen]({invite_url})", color=0x42FF00)
                    resolvedembed.set_thumbnail(url=self.bot.user.display_avatar.url)
                    await user.send(embed=resolvedembed)
                    await interaction.followup.send("The ban appeal has been approved, and a message with a new server link has been sent to the user.", ephemeral=True)
                else:
                    await interaction.followup.send("Failed to find the user associated with the appeal.", ephemeral=True)
            else:
                await interaction.followup.send("Invalid embed format. Please make sure the embed contains a field with the name 'Discord ID:'.", ephemeral=True)
        else:
            await interaction.followup.send("No embeds found in the original message.", ephemeral=True)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def Decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message_id = interaction.message.id
        msg = await interaction.channel.fetch_message(message_id)
        if msg.embeds:
            embed = msg.embeds[0]
            user_id_field = next((field for field in embed.fields if field.name == 'Discord ID:'), None)
            if user_id_field:
                user_id = user_id_field.value.strip()
                try:
                    user = await self.bot.fetch_user(int(user_id))
                except discord.errors.NotFound:
                    await interaction.followup.send("Failed to find the user associated with the appeal. The user might not exist or has left Discord.", ephemeral=True)
                    return
                if user:
                    invite_url = await self.create_invite(self.guild_id)
                    embed.add_field(name="Status", value=":x: Declined")
                    await msg.edit(embed=embed, view=None)
                    resolvedembed = discord.Embed(title="Your ban appeal has been declined!", description=f"Your ban appeal has been declined, this means you will no longer be able to join kanzen ever again so good job!", color=0x42FF00)
                    resolvedembed.set_thumbnail(url=self.bot.user.display_avatar.url)
                    await user.send(embed=resolvedembed)
                    await interaction.followup.send("The ban appeal has been declined, and a message has been sent to the user.", ephemeral=True)
                else:
                    await interaction.followup.send("Failed to find the user associated with the appeal.", ephemeral=True)
            else:
                await interaction.followup.send("Invalid embed format. Please make sure the embed contains a field with the name 'Discord ID:'.", ephemeral=True)
        else:
            await interaction.followup.send("No embeds found in the original message.", ephemeral=True)


class AFK(TypedDict):
    user_id: int
    reason: str
    time: datetime.datetime

class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.emoji = "<:tata:1121909389280944169>"

    async def check_afk(self, userid: int) -> AFK:
        query = "SELECT reason, time, user_id FROM afk WHERE user_id = $1"
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                async with connection.cursor() as cursor:
                    await cursor.execute(query, userid)
                    result = await cursor.fetchall()
        return result[0] if result else None

    async def remove_afk(self, userid: int) -> None:
        query = "DELETE FROM afk WHERE user_id = $1"
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                async with connection.cursor() as cursor:
                    await cursor.execute(query, userid)

    async def add_warning(self, member_id, guild_id, reason, change):
        async with self.bot.pool.acquire() as conn:
            await conn.execute("INSERT INTO warning (member_id, guild_id, reasons, warnings) VALUES ($1, $2, $3, $4)", member_id, guild_id, reason, change)
            await conn.commit()

    async def update_warns(self, member_id, guild_id, reason, change=1):
        async with self.bot.pool.acquire() as conn:
            existing_warnings = await conn.fetchone('SELECT warnings FROM warning WHERE member_id = $1 AND guild_id = $2', member_id, guild_id)
            if existing_warnings:
                current_warnings = existing_warnings['warnings']
                updated_warnings = current_warnings + change
                await conn.execute('UPDATE warning SET reasons = $1, warnings = $2 WHERE member_id = $3 AND guild_id = $4',
                                reason, updated_warnings, member_id, guild_id)
            else:
                updated_warnings = change
                await self.add_warning(member_id, guild_id, reason, updated_warnings)
            await conn.commit()
            return updated_warnings

    async def get_warnings(self, member_id):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT warnings FROM warning WHERE member_id = $1", member_id)
                row = await cursor.fetchone()
                return row['warnings'] if row else 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.lower() == "reece":
            await message.channel.send("<@609515684740988959> is the sexiest")
        if message.content.lower() == "tae":
            await message.channel.send("<@718144988688679043> is mommy")
        if message.content.lower() == "nani":
            await message.channel.send("i woke up in a new 🔥bugatti🔥")
        if message.content.lower() == "spotify ads":
            await message.channel.send("follow 0470pm for free spotify premium")
        if message.content.lower() == "jess":
            await message.channel.send("https://media0.giphy.com/media/DWPCBPJPBLRsSG0LI2/giphy.gif?cid=ad7b17ba5hahdaf6h1wgccgl9loldyoowq0u3d0c68fisadd&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        if message.content.lower() == "kira":
            await message.channel.send("OMG JIMIN<:chimmy:1128727915664785409>:heartpulse::face_with_peeking_eye::heart_eyes::face_holding_back_tears::pleading_face::sob::weary::tired_face::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::heartpulse::pray_tone1::pinching_hand:<:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> <:chimmy:1128727915664785409> :face_holding_back_tears::face_holding_back_tears::face_holding_back_tears:")
        if message.content.lower() == "kelly":
            await message.channel.send("Jungkook is so jungkook and no one will ever jungkook like jungkook <:boobs:1142888878999613520>")
        blocked_words = ["nigga", "n i g g a", "niga", "n i g a", "n1ga", "n 1 g a", "n1gger", "nigger", "n1ger", "n i g e r", "n i g a", "n 1 g a", "n 1 g e r", "retard", "r e t a r d", "r3tard", "r 3 t a r d", "batty boy", "bender", "ching chong", "chink", "chinkie", "chinky", "cotton picker", "cracker", "cripple", "curry muncher", "dyke", "eskimo", "fag", "faggot", "gimp", "golliwogg", "kkk", "nazi","nigglet", "fagg0t", "niglet", "osama bin laden", "paki", "retarted", "shemale", "sissy", "tranie", "trannie", "tranny", "trany", "yellow people"]
        lower_content = message.content.lower()
        if any(word in lower_content for word in blocked_words):
            await message.delete()
            member_id = message.author.id
            count = await self.get_warnings(member_id)
            for blocked_word in blocked_words:
                lower_content = lower_content.replace(blocked_word, f"**__{blocked_word}__**")

            description = lower_content
            warningembed = discord.Embed(title="Word Blocked", description=description, color=0xD11717)
            warningembed.set_footer(text=f"sent from {message.author.display_name} | {message.author.id}", icon_url=message.author.display_avatar)
            warningembed.set_thumbnail(url=message.author.display_avatar)
            member = message.author
            memberembed = discord.Embed(title="You have received a warning", description=f"<:CF12:1188186414387568691> You have gotten this warning for saying:\n**{description}**\n\n<:CF12:1188186414387568691> You now have **{count}** warnings. If you get to **3** warnings you will instantly be banned from our group", color=0x2b2d31, url="https://instagram.com/kanzengrp/")
            memberembed.set_thumbnail(url=message.guild.icon)
            memberembed.add_field(name="Your full sentence was:", value=description)
            await message.author.send(embed=memberembed)
            warning = message.guild.get_channel(1178952898273628200)
            member_id = message.author.id
            reason = blocked_word
            guild_id = message.guild.id
            await self.update_warns(member_id, guild_id, reason, change=1)
            count = await self.get_warnings(member_id)
            if count == 3:
                member = message.author
                await member.ban(reason="Reached 3 warnings")
                banembed = discord.Embed(title="You have been banned from Kanzengrp", description=f"You have been banned from Kanzengrp for getting **3 warnings**\nYou received your last warning for saying {', '.join(['**'+word+'**' for word in blocked_words])}. If you would like to appeal your ban, click the button below but it may not be accepted.", color=0x2b2d31, url="https://instagram.com/kanzengrp/")
                banembed.set_thumbnail(url=message.guild.icon)
                view = banappeal(bot=self.bot)
                await member.send(embed=banembed, view=view)
                await warning.send(f"# Member **{member.display_name}** has been banned due to reaching 3 warnings.")
            else:
                await warning.send(embed=warningembed)
        if "MessageType.premium_guild" in str(message.type):
            embed = discord.Embed(title=f"Thank you for boosting! {message.author.display_name}!", description="<a:Arrow_1:1145603161701224528> dm staff or lead for your custom role\n<a:Arrow_1:1145603161701224528> go into [#booster-perks](https://discord.com/channels/1121841073673736215/1164318431462563951) to claim the perks\n<a:Arrow_1:1145603161701224528> we really appreciate your support!", color=0x2b2d31)
            embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar)
            embed.set_footer(text=f"We are up to {message.guild.premium_subscription_count} boosts!")
            if message.guild.id == 1121841073673736215:
                await message.channel.send(f"{message.author.mention}", embed=embed)
            else:
                pass
        afk = await self.check_afk(message.author.id)
        if afk is not None:
            await self.remove_afk(message.author.id)
            await message.reply(f"Hey, <@!{afk['user_id']}> welcome back! You were AFK for **{afk['reason']}**")
        if len(message.mentions) > 0:
            for mention in message.mentions:
                afk_mention = await self.check_afk(mention.id)
                if afk_mention is not None:
                    await message.reply(f"**{mention.name}** went AFK **{afk_mention['reason']}**")

class appeal(ui.Modal, title='Ban Appeal'):
    def __init__(self, bot, **kwargs):
        super().__init__(**kwargs)
        self.bot = bot
        self.value = None

    one = ui.TextInput(label='whats your instagram username?', placeholder="enter your instagram username", style=discord.TextStyle.long)
    two = ui.TextInput(label='why did you get banned?', placeholder="tell us why you was banned...", style=discord.TextStyle.long)
    three = ui.TextInput(label='why should we approve your appeal?', placeholder="tell us why here...", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title='Ban Appeal',description=f"**what's their instagram:**\n{self.one.value}\n\n**why did they get banned:**\n{self.two.value}\n\n**why should we approve their appeal?:**\n{self.three.value}" ,color=0x2b2d31)
        embed.set_footer(text=f"sent from: {interaction.user.name}", icon_url=interaction.user.avatar)
        embed.set_thumbnail(url=interaction.user.display_avatar)
        embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
        channel = interaction.client.get_channel(1195668564057804830)
        view = approveordecline(self.bot, self.one.value, self.two.value, self.three.value)
        await channel.send(embed=embed, view=view)
        await interaction.followup.send(f'Your appeal has been sent. We will let you know if it was approved or not', ephemeral=True)

async def setup(bot):
    await bot.add_cog(other(bot))