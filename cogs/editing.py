from io import BytesIO
import json
import random
import discord
from discord.ext import commands
from colorthief import ColorThief
from discord import app_commands
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from matplotlib import colors
import discord
import io
from discord.ui import Button, View

class PaletteOptionsView(View):
    def __init__(self, bot, image):
        super().__init__()
        self.bot = bot
        self.image = image
        self.num_colors = None

    @discord.ui.button(label="4 colors", style=discord.ButtonStyle.primary, custom_id="4")
    async def four_colors(self, interaction: discord.Interaction, button: Button):
        self.num_colors = 4
        await self.generate_palette(interaction)

    @discord.ui.button(label="5 colors", style=discord.ButtonStyle.primary, custom_id="5")
    async def five_colors(self, interaction: discord.Interaction, button: Button):
        self.num_colors = 5
        await self.generate_palette(interaction)

    @discord.ui.button(label="6 colors", style=discord.ButtonStyle.primary, custom_id="6")
    async def six_colors(self, interaction: discord.Interaction, button: Button):
        self.num_colors = 6
        await self.generate_palette(interaction)

    @discord.ui.button(label="7 colors", style=discord.ButtonStyle.primary, custom_id="7")
    async def seven_colors(self, interaction: discord.Interaction, button: Button):
        self.num_colors = 7
        await self.generate_palette(interaction)

    @discord.ui.button(label="8 colors", style=discord.ButtonStyle.primary, custom_id="8")
    async def eight_colors(self, interaction: discord.Interaction, button: Button):
        self.num_colors = 8
        await self.generate_palette(interaction)

    async def generate_palette(self, interaction: discord.Interaction):
        image_bytes = await self.image.read()
        resized_image = self.bot.get_cog("editing").resize_image(image_bytes, max_size=750)
        centroids = self.bot.get_cog("editing").kmeans_cluster_colors(resized_image, n_clusters=self.num_colors)
        output_path = self.bot.get_cog("editing").get_palette(centroids)
        await interaction.response.send_message(file=discord.File(output_path))

class editing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.num_colors = 5

    def calculate_brightness(self, color):
        return (0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]) / 255

    @app_commands.command(name="colorpalette", description="Get a random color palette from Hoshi")
    async def colourpalette(self, interaction: discord.Interaction):
        with open('./json/hexcodes.json', 'r') as file:
            color_groups = json.load(file)

        group = random.choice(color_groups)
        padding = 5
        square_size = 100
        max_columns = len(group)
        image_width = max_columns * (square_size + padding) - padding
        image_height = square_size
        image = Image.new('RGB', (image_width, image_height), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("./fonts/zhcn.ttf")
        font1 = ImageFont.truetype("./fonts/zhcn.ttf")

        x = 0

        for color_hex in group:
            color = tuple(int(color_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
            draw.rectangle([x, 0, x + square_size, square_size], fill=color)

            hex_code = color_hex.upper()
            text_width, text_height = draw.textsize(hex_code, font=font1)
            text_x = x + (square_size - text_width) // 2
            text_y = square_size - text_height

            brightness = self.calculate_brightness(color)
            text_color = "#272727" if brightness > 0.5 else "#ffffff"
            
            draw.text((text_x, text_y), hex_code, fill=text_color, font=font1)
            x += square_size + padding

        image.save("color_palette.png")
        await interaction.response.send_message(file=discord.File("color_palette.png"))

    @app_commands.command(name="transition", description="Get a random transition from Hoshi")
    async def random_transition(self, interaction: discord.Interaction):
        with open('./json/transitions.json', 'r') as file:
            data = json.load(file)
            transitions = data["transitions"]
            chosen_transition = random.choice(transitions)
            await interaction.response.send_message(f"Your random transition is: **{chosen_transition}**")

    def resize_image(self, image_bytes, max_size=750):
        img = Image.open(io.BytesIO(image_bytes))
        input_width, input_height = img.size
        if input_width <= max_size and input_height <= max_size:
            return img.copy()

        scale_factor = max_size / max(input_width, input_height)
        new_width = int(input_width * scale_factor)
        new_height = int(input_height * scale_factor)
        resized = img.resize((new_width, new_height))
        return resized

    def extract_colors(self, input_image):
        img = input_image.convert("RGB")
        pixels = np.array(img)
        colors = pixels.reshape(-1, 3)
        return colors

    def kmeans_cluster_colors(self, input_image, n_clusters=5):
        colors_path = self.extract_colors(input_image)
        scaler = StandardScaler()
        scaled_colors = scaler.fit_transform(colors_path)
        kmeans = KMeans(n_clusters=n_clusters, n_init="auto")
        kmeans.fit(scaled_colors)
        centroids = kmeans.cluster_centers_
        rgb_colors = scaler.inverse_transform(centroids).astype(int)
        rgb_colors = rgb_colors[:, :3]
        hex_colors = [colors.rgb2hex(c / 255) for c in rgb_colors]
        return hex_colors

    def get_palette(self, hex_colors, output_path="palette.png"):
        square_size = 100
        font_size = 15
        padding = 0
        bar_height = 28
        radius = 18
        bar_margin_x = 10
        bar_margin_bottom = 8

        num_colors = len(hex_colors)
        width = num_colors * (square_size + padding) - padding
        height = square_size
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./fonts/Bold.otf", font_size)

        for i, hex_color in enumerate(hex_colors):
            x0 = i * (square_size + padding)
            x1 = x0 + square_size
            draw.rectangle([x0, 0, x1, square_size], fill=hex_color)

        bar_y1 = height - bar_margin_bottom
        bar_y0 = bar_y1 - bar_height
        bar_x0 = bar_margin_x
        bar_x1 = width - bar_margin_x

        blur_area = img.crop((bar_x0, bar_y0, bar_x1, bar_y1))
        blurred = blur_area.filter(ImageFilter.GaussianBlur(20))
        brightened = ImageEnhance.Brightness(blurred).enhance(1.5)

        mask = Image.new("L", (bar_x1 - bar_x0, bar_height), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, bar_x1 - bar_x0, bar_height), radius=radius, fill=255)

        img.paste(brightened, (bar_x0, bar_y0), mask)

        text_mask = Image.new("L", (width, height), 0)
        text_draw = ImageDraw.Draw(text_mask)

        for i, hex_color in enumerate(hex_colors):
            x0 = i * (square_size + padding)
            text = hex_color.upper()
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = x0 + (square_size - text_width) // 2
            text_y = bar_y0 + (bar_height - text_height) // 2 - 3

            if bar_x0 <= text_x <= bar_x1 - text_width:
                text_draw.text((text_x, text_y), text, fill=255, font=font)

        darkened_img = img.copy()
        enhancer = ImageEnhance.Brightness(darkened_img)
        darkened_img = enhancer.enhance(0.3)

        img.paste(darkened_img, (0, 0), text_mask)

        img.save(output_path)
        return output_path

    @app_commands.command(name="palette", description="Upload an image to generate a color palette.")
    async def palette(self, interaction: discord.Interaction, image: discord.Attachment):
        view = PaletteOptionsView(self.bot, image)
        await interaction.response.send_message("Pick the number of colors:", view=view)

async def setup(bot):
    await bot.add_cog(editing(bot))