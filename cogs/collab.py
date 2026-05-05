import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import uuid
import traceback

DATA_FILE = "json/collabs.json"
ERROR_CHANNEL_ID = 1477653852768440460

async def report_error(bot: commands.Bot, error: BaseException, source: str):
    channel = bot.get_channel(ERROR_CHANNEL_ID)
    if channel is None:
        try:
            channel = await bot.fetch_channel(ERROR_CHANNEL_ID)
        except Exception:
            return

    traceback_text = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    if len(traceback_text) > 1900:
        traceback_text = traceback_text[-1900:]

    await channel.send(
        f"**Collab Cog Error**\n"
        f"Source: {source}\n"
        f"```py\n{traceback_text}\n```"
    )


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as f:
        content = f.read()
        if not content.strip():
            return {}

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {}


def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class CollabModal(discord.ui.Modal, title="Create Collab"):
    theme = discord.ui.TextInput(label="Theme", placeholder="Edit concept...")
    max_members = discord.ui.TextInput(label="Max Members", placeholder="e.g. 5")

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        try:
            data = load_data()
            try:
                max_members = int(self.max_members.value)
            except ValueError:
                return await interaction.response.send_message(
                    "Max members must be a number.", ephemeral=True
                )

            collab_id = str(uuid.uuid4())

            data[collab_id] = {
                "host": interaction.user.id,
                "members": [interaction.user.id],
                "theme": self.theme.value,
                "max": max_members,
                "locked": False,
            }

            save_data(data)

            embed = discord.Embed(
                title="🎬 New Collab",
                description=f"**Theme:** {self.theme.value}\n\n👥 1/{max_members}",
                color=discord.Color.purple()
            )

            view = CollabView(self.cog, collab_id)
            self.cog.bot.add_view(view)

            await interaction.response.send_message(embed=embed, view=view)
        except Exception as error:
            await report_error(self.cog.bot, error, "CollabModal.on_submit")
            await interaction.response.send_message(
                "An unexpected error occurred. Staff has been notified.",
                ephemeral=True
            )

class CollabView(discord.ui.View):
    def __init__(self, cog, collab_id):
        super().__init__(timeout=None)
        self.cog = cog
        self.collab_id = collab_id

    def get_data(self):
        return load_data()

    def update_embed(self, data):
        collab = data[self.collab_id]
        return discord.Embed(
            title="🎬 Collab",
            description=f"**Theme:** {collab['theme']}\n\n👥 {len(collab['members'])}/{collab['max']}",
            color=discord.Color.purple()
        )

    @discord.ui.button(label="Join", style=discord.ButtonStyle.green, custom_id="collab_join")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            data = self.get_data()
            collab = data.get(self.collab_id)

            if not collab:
                return await interaction.response.send_message("Collab not found.", ephemeral=True)

            if collab["locked"]:
                return await interaction.response.send_message("This collab is locked.", ephemeral=True)

            if interaction.user.id in collab["members"]:
                return await interaction.response.send_message("You're already in.", ephemeral=True)

            if len(collab["members"]) >= collab["max"]:
                return await interaction.response.send_message("Collab is full.", ephemeral=True)

            collab["members"].append(interaction.user.id)
            save_data(data)

            await interaction.response.edit_message(embed=self.update_embed(data), view=self)
        except Exception as error:
            await report_error(self.cog.bot, error, "CollabView.join")
            await interaction.response.send_message(
                "An unexpected error occurred. Staff has been notified.",
                ephemeral=True
            )

    @discord.ui.button(label="Leave", style=discord.ButtonStyle.red, custom_id="collab_leave")
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            data = self.get_data()
            collab = data.get(self.collab_id)

            if not collab:
                return await interaction.response.send_message("Collab not found.", ephemeral=True)

            if interaction.user.id == collab["host"]:
                return await interaction.response.send_message("Host cannot leave.", ephemeral=True)

            if interaction.user.id not in collab["members"]:
                return await interaction.response.send_message("You're not in this collab.", ephemeral=True)

            collab["members"].remove(interaction.user.id)
            save_data(data)

            await interaction.response.edit_message(embed=self.update_embed(data), view=self)
        except Exception as error:
            await report_error(self.cog.bot, error, "CollabView.leave")
            await interaction.response.send_message(
                "An unexpected error occurred. Staff has been notified.",
                ephemeral=True
            )

    @discord.ui.button(label="Lock", style=discord.ButtonStyle.blurple, custom_id="collab_lock")
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            data = self.get_data()
            collab = data.get(self.collab_id)

            if not collab:
                return await interaction.response.send_message("Collab not found.", ephemeral=True)

            if interaction.user.id != collab["host"]:
                return await interaction.response.send_message("Only host can lock.", ephemeral=True)

            collab["locked"] = True
            save_data(data)

            guild = interaction.guild

            category = discord.utils.get(guild.categories, name="Collabs")
            if not category:
                category = await guild.create_category("Collabs")

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False)
            }

            for member_id in collab["members"]:
                member = guild.get_member(member_id)
                if member:
                    overwrites[member] = discord.PermissionOverwrite(view_channel=True)

            safe_name = interaction.user.name.lower().replace(" ", "-")
            channel = await guild.create_text_channel(
                name=f"collab-{safe_name}",
                overwrites=overwrites,
                category=category
            )

            await channel.send(f"🎬 Collab started!\nTheme: {collab['theme']}")

            await interaction.response.edit_message(
                content=f"🔒 Collab locked! Channel created: {channel.mention}",
                embed=None,
                view=None
            )
        except Exception as error:
            await report_error(self.cog.bot, error, "CollabView.lock")
            await interaction.response.send_message(
                "An unexpected error occurred. Staff has been notified.",
                ephemeral=True
            )

class CollabCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        """Re-register persistent views on startup"""
        try:
            data = load_data()
            for collab_id in data.keys():
                self.bot.add_view(CollabView(self, collab_id))
        except Exception as error:
            await report_error(self.bot, error, "CollabCog.cog_load")

    @app_commands.command(name="collab", description="Create a collab")
    async def collab(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CollabModal(self))

async def setup(bot):
    await bot.add_cog(CollabCog(bot))