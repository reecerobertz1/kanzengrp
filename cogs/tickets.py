import discord
from discord.ext import commands
from bot import LalisaBot
import asyncio
import io

class CloseTicket(discord.ui.View):
    def __init__(self, log_channel_id: int):
        super().__init__(timeout=None)
        self.log_channel_id = log_channel_id

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.grey)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        log_channel = interaction.guild.get_channel(self.log_channel_id)
        messages = []
        async for message in interaction.channel.history(limit=None, oldest_first=True):
            messages.append(f"{message.created_at} - {message.author}: {message.content}")

        transcript = "\n".join(messages) or "No messages."
        transcript_io = io.StringIO(transcript)
        transcript_file = discord.File(fp=transcript_io, filename=f"{interaction.channel.name}.txt")

        if log_channel:
            await log_channel.send(
                f"📄 Ticket closed by {interaction.user.mention} in {interaction.channel.name}",
                file=transcript_file
            )

        await interaction.channel.send(
            f"{interaction.user.mention} has closed this ticket. Deleting in 5 seconds..."
        )
        await interaction.response.defer()
        await asyncio.sleep(5)
        try:
            await interaction.channel.delete()
        except discord.Forbidden:
            await interaction.channel.send("I don't have permission to delete this channel!")

class Tickets(discord.ui.View):
    def __init__(self, log_channel_id: int):
        super().__init__(timeout=None)
        self.log_channel_id = log_channel_id

    @discord.ui.button(label="Commonly Asked", style=discord.ButtonStyle.grey)
    async def common(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Commonly Asked Questions")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.grey)
    async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        category_id = 1396664226545668200
        category = discord.utils.get(guild.categories, id=category_id)

        if category is None:
            await interaction.response.send_message("Ticket category not found.", ephemeral=True)
            return

        channel_name = f"ticket-{interaction.user.name}".lower().replace(" ", "-")

        existing_channel = discord.utils.get(category.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(
                f"You already have an open ticket: {existing_channel.mention}",
                ephemeral=True
            )
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        staff_role = discord.utils.get(guild.roles, id=1220492654455033936)
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                manage_channels=True
            )

        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            reason="New ticket created"
        )

        staff_embed = discord.Embed(
            title="🎫 Ticket Opened",
            description=(
                f"**Opened by:** {interaction.user.mention}\n"
                f"**User ID:** `{interaction.user.id}`\n\n"
                "Thank you for creating a ticket! A staff member will be with you shortly.\n"
                "When your issue is resolved, click **Close Ticket** below.\n\n"
                f"-# Ticket opened | {discord.utils.format_dt(discord.utils.utcnow(), style='F')}"
            ),
            color=0x505147
        )

        await channel.send(
            "<@609515684740988959>",
            embed=staff_embed,
            view=CloseTicket(self.log_channel_id)
        )

        await channel.send(
            f"Hey {interaction.user.mention}, thank you for opening a ticket! A staff member will be with you shortly.\nWhile you wait, let us know why you opened up this ticket!"
        )

        await interaction.response.send_message(
            f"Your ticket has been created: {channel.mention}",
            ephemeral=True
        )


class tickets(commands.Cog):
    def __init__(self, bot: LalisaBot):
        self.bot = bot

    @commands.command()
    async def tickets(self, ctx):
        embed = discord.Embed(
            description="### ᯓ Aster Tickets༝ ⁺\nIf you have any questions or concerns, please feel free to create a ticket below, our leads and staff are always happy to assist you."
                        "\nBefore you open a ticket, kindly make sure you’ve read through the Commonly Asked questions!"
                        "\n\nOnce you create a ticket"
                        "\n﹒A private channel will be created just for you and our leads and staff."
                        "\n﹒Our team will respond to you as soon as possible!"
                        "\n﹒Please be patient and avoid creating multiple tickets for the same issue."
                        "\n﹒Ask us anything — there are no bad questions (as long as they’re appropriate)."
                        "\n\nThank you for being a part of our community!",
            color=0x505147
        )
        log_channel_id = 1396669400651792485
        await ctx.send(embed=embed, view=Tickets(log_channel_id))


async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(tickets(bot))