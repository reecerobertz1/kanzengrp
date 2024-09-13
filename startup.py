import asyncio
import discord
from bot import LalisaBot
import logging
import logging.handlers
from config import token
from discord import ui

bot = LalisaBot()

class EditEmbedView(ui.View):
    def __init__(self, embed_message: discord.Message):
        super().__init__()
        self.embed_message = embed_message

    @ui.button(label="Edit Title", style=discord.ButtonStyle.primary)
    async def edit_title(self, interaction: discord.Interaction, button: ui.Button):
        modal = TitleModal(self.embed_message)
        await interaction.response.send_modal(modal)

    @ui.button(label="Edit Author", style=discord.ButtonStyle.primary)
    async def edit_author(self, interaction: discord.Interaction, button: ui.Button):
        modal = AuthorModal(self.embed_message)
        await interaction.response.send_modal(modal)

    @ui.button(label="Edit Description", style=discord.ButtonStyle.primary)
    async def edit_description(self, interaction: discord.Interaction, button: ui.Button):
        modal = DescriptionModal(self.embed_message)
        await interaction.response.send_modal(modal)

    @ui.button(label="Edit Color", style=discord.ButtonStyle.primary)
    async def edit_color(self, interaction: discord.Interaction, button: ui.Button):
        modal = ColorModal(self.embed_message)
        await interaction.response.send_modal(modal)

    @ui.button(label="Edit Footer", style=discord.ButtonStyle.primary)
    async def edit_footer(self, interaction: discord.Interaction, button: ui.Button):
        modal = FooterModal(self.embed_message)
        await interaction.response.send_modal(modal)

    @ui.button(label="Edit Image", style=discord.ButtonStyle.primary)
    async def edit_image(self, interaction: discord.Interaction, button: ui.Button):
        modal = ImageModal(self.embed_message)
        await interaction.response.send_modal(modal)

    @ui.button(label="Edit Thumbnail", style=discord.ButtonStyle.primary)
    async def edit_thumbnail(self, interaction: discord.Interaction, button: ui.Button):
        modal = ThumbnailModal(self.embed_message)
        await interaction.response.send_modal(modal)

class TitleModal(ui.Modal, title="Edit Title"):
    def __init__(self, embed_message: discord.Message):
        super().__init__()
        self.embed_message = embed_message
        self.title_input = ui.TextInput(label="New Title", required=False)
        self.add_item(self.title_input)

    async def on_submit(self, interaction: discord.Interaction):
        embed = self.embed_message.embeds[0]
        embed.title = self.title_input.value or None
        await self.embed_message.edit(embed=embed)
        await interaction.response.send_message("Title updated!", ephemeral=True)

class AuthorModal(ui.Modal, title="Edit Author"):
    def __init__(self, embed_message: discord.Message):
        super().__init__()
        self.embed_message = embed_message
        self.author_name = ui.TextInput(label="Author Name", required=False)
        self.author_icon = ui.TextInput(label="Author Icon URL", required=False)
        self.add_item(self.author_name)
        self.add_item(self.author_icon)

    async def on_submit(self, interaction: discord.Interaction):
        embed = self.embed_message.embeds[0]
        embed.set_author(name=self.author_name.value or None, icon_url=self.author_icon.value or None)
        await self.embed_message.edit(embed=embed)
        await interaction.response.send_message("Author updated!", ephemeral=True)

class DescriptionModal(ui.Modal, title="Edit Description"):
    def __init__(self, embed_message: discord.Message):
        super().__init__()
        self.embed_message = embed_message
        self.description_input = ui.TextInput(label="New Description", style=discord.TextStyle.long, required=False)
        self.add_item(self.description_input)

    async def on_submit(self, interaction: discord.Interaction):
        embed = self.embed_message.embeds[0]
        embed.description = self.description_input.value or None
        await self.embed_message.edit(embed=embed)
        await interaction.response.send_message("Description updated!", ephemeral=True)

class ColorModal(ui.Modal, title="Edit Color"):
    def __init__(self, embed_message: discord.Message):
        super().__init__()
        self.embed_message = embed_message
        self.color_input = ui.TextInput(label="New Color (Hex)", placeholder="#FFFFFF", required=False)
        self.add_item(self.color_input)

    async def on_submit(self, interaction: discord.Interaction):
        embed = self.embed_message.embeds[0]
        if self.color_input.value:
            try:
                color_value = int(self.color_input.value.lstrip('#'), 16)
                embed.color = discord.Color(color_value)
            except ValueError:
                await interaction.response.send_message("Invalid color format!", ephemeral=True)
                return
        else:
            embed.color = discord.Color.default()
        await self.embed_message.edit(embed=embed)
        await interaction.response.send_message("Color updated!", ephemeral=True)

class FooterModal(ui.Modal, title="Edit Footer"):
    def __init__(self, embed_message: discord.Message):
        super().__init__()
        self.embed_message = embed_message
        self.footer_text = ui.TextInput(label="Footer Text", required=False)
        self.footer_icon = ui.TextInput(label="Footer Icon URL", required=False)
        self.add_item(self.footer_text)
        self.add_item(self.footer_icon)

    async def on_submit(self, interaction: discord.Interaction):
        embed = self.embed_message.embeds[0]
        embed.set_footer(text=self.footer_text.value or None, icon_url=self.footer_icon.value or None)
        await self.embed_message.edit(embed=embed)
        await interaction.response.send_message("Footer updated!", ephemeral=True)

class ImageModal(ui.Modal, title="Edit Image"):
    def __init__(self, embed_message: discord.Message):
        super().__init__()
        self.embed_message = embed_message
        self.image_url = ui.TextInput(label="Image URL", required=False)
        self.add_item(self.image_url)

    async def on_submit(self, interaction: discord.Interaction):
        embed = self.embed_message.embeds[0]
        embed.set_image(url=self.image_url.value or None)
        await self.embed_message.edit(embed=embed)
        await interaction.response.send_message("Image updated!", ephemeral=True)

class ThumbnailModal(ui.Modal, title="Edit Thumbnail"):
    def __init__(self, embed_message: discord.Message):
        super().__init__()
        self.embed_message = embed_message
        self.thumbnail_url = ui.TextInput(label="Thumbnail URL", required=False)
        self.add_item(self.thumbnail_url)

    async def on_submit(self, interaction: discord.Interaction):
        embed = self.embed_message.embeds[0]
        embed.set_thumbnail(url=self.thumbnail_url.value or None)
        await self.embed_message.edit(embed=embed)
        await interaction.response.send_message("Thumbnail updated!", ephemeral=True)

@bot.tree.context_menu(name="Edit Embed")
async def edit_embed(interaction: discord.Interaction, message: discord.Message):
    embed = discord.Embed(title="Edit Embed", description="Select a section to edit", color=0x2b2d31)
    view = EditEmbedView(message)  # Pass the message with the embed to the view
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=3,  # Rotate through 3 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # starts the bot
    async with bot:
        await bot.start(token)

asyncio.run(main())