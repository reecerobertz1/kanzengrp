import discord
from discord.ext import commands
from discord import ui

class embedview(discord.ui.View):
    def __init__(self, embed_message):
        super().__init__(timeout=None)
        self.embed_message = embed_message

    @discord.ui.button(label="Author")
    async def q1(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(q1(self.embed_message))

    @discord.ui.button(label="Title")
    async def q2(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(q2(self.embed_message))

    @discord.ui.button(label="Description")
    async def q3(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(q3(self.embed_message))

    @discord.ui.button(label="Thumbnail")
    async def q4(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(q4(self.embed_message))

    @discord.ui.button(label="Image")
    async def q5(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(q5(self.embed_message))

    @discord.ui.button(label="Footer")
    async def q6(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(q6(self.embed_message))

    @discord.ui.button(label="Color")
    async def q7(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(q7(self.embed_message))

    @discord.ui.button(label="Embed", emoji="<:trash:1284281733000204288>", style=discord.ButtonStyle.red)
    async def clear(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description="Embed has been cleared!")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Send", emoji="<:check_white:1284282565645176892>",style=discord.ButtonStyle.green)
    async def q0(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(q0(self.embed_message))

class q0(ui.Modal, title='Channel'):
    def __init__(self, embed_message):
        super().__init__()
        self.embed_message = embed_message
        self.channel_id = ui.TextInput(label='Enter Channel ID', style=discord.TextStyle.short, required=True)
        self.ping = ui.TextInput(label='Enter Text', placeholder="The text that goes above the embed. Can be a role!" ,style=discord.TextStyle.short, required=False)
        self.add_item(self.channel_id)
        self.add_item(self.ping)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if not isinstance(self.embed_message, discord.Embed):
                await interaction.response.send_message("The embed message is not correctly set.", ephemeral=True)
                return

            channel_id = int(self.channel_id.value)
            channel = interaction.guild.get_channel(channel_id)

            if channel is None:
                await interaction.response.send_message("Invalid channel ID or the bot does not have access to the channel.", ephemeral=True)
                return
            if self.ping:
                await channel.send(self.ping.value, embed=self.embed_message)
            else:
                await channel.send(embed=self.embed_message)
            await interaction.message.edit(self.embed_message, view=None)
            await interaction.response.send_message(f"Embed sent to <#{channel_id}>")
        except ValueError:
            await interaction.response.send_message("Invalid channel ID format. Please enter a valid channel ID.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to send embed: {e}", ephemeral=True)

class q1(ui.Modal, title='Set Author'):
    def __init__(self, embed_message):
        super().__init__()
        self.embed_message = embed_message
        self.author_name = ui.TextInput(label='Author Name', style=discord.TextStyle.short, required=False)
        self.author_icon = ui.TextInput(label='Author Icon URL', style=discord.TextStyle.short, required=False)
        self.add_item(self.author_name)
        self.add_item(self.author_icon)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if self.author_name.value:
                self.embed_message.set_author(name=self.author_name.value, icon_url=self.author_icon.value or None)
            else:
                self.embed_message.set_author(name="", icon_url=None)
            
            await interaction.message.edit(embed=self.embed_message)
            await interaction.response.send_message(f"Embed author updated.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to update embed: {e}", ephemeral=True)

class q2(ui.Modal, title='Set Title'):
    def __init__(self, embed_message):
        super().__init__()
        self.embed_message = embed_message
        self.title_input = ui.TextInput(
            label='Title',
            style=discord.TextStyle.short,
            required=False,
            min_length=1,
            max_length=256
        )
        self.add_item(self.title_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if self.title_input.value:
                self.embed_message.title = self.title_input.value
            else:
                self.embed_message.title = ""  # Set to empty string instead of None

            await interaction.message.edit(embed=self.embed_message)
            await interaction.response.send_message(f"Embed title updated.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to update embed: {e}", ephemeral=True)

class q3(ui.Modal, title='Set Description'):
    def __init__(self, embed_message):
        super().__init__()
        self.embed_message = embed_message
        self.description_input = ui.TextInput(
            label='Description',
            style=discord.TextStyle.paragraph,
            required=False
        )
        self.add_item(self.description_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if self.description_input.value:
                self.embed_message.description = self.description_input.value
            else:
                self.embed_message.description = None

            await interaction.message.edit(embed=self.embed_message)
            await interaction.response.send_message(f"Embed description updated.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to update embed: {e}", ephemeral=True)

class q4(ui.Modal, title='Set Thumbnail'):
    def __init__(self, embed_message):
        super().__init__()
        self.embed_message = embed_message
        self.Thumbnail_input = ui.TextInput(
            label='Thumbnail URL',
            style=discord.TextStyle.short,
            required=False
        )
        self.add_item(self.Thumbnail_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if self.Thumbnail_input.value:
                self.embed_message.set_thumbnail(url=self.Thumbnail_input.value)
            else:
                self.embed_message.set_thumbnail(url=None)

            await interaction.message.edit(embed=self.embed_message)
            await interaction.response.send_message(f"Embed thumbnail updated.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to update embed: {e}", ephemeral=True)

class q5(ui.Modal, title='Set Image'):
    def __init__(self, embed_message):
        super().__init__()
        self.embed_message = embed_message
        self.Image_input = ui.TextInput(
            label='Image URL',
            style=discord.TextStyle.short,
            required=False
        )
        self.add_item(self.Image_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if self.Image_input.value:
                self.embed_message.set_image(url=self.Image_input.value)
            else:
                self.embed_message.set_image(url=None)

            await interaction.message.edit(embed=self.embed_message)
            await interaction.response.send_message(f"Embed image updated.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to update embed: {e}", ephemeral=True)

class q6(ui.Modal, title='Set Footer'):
    def __init__(self, embed_message):
        super().__init__()
        self.embed_message = embed_message
        self.Footer_input = ui.TextInput(label='Footer', style=discord.TextStyle.short, required=False, min_length=1, max_length=256)
        self.Footer_Icon_input = ui.TextInput(label='Footer', style=discord.TextStyle.short, required=False)
        self.add_item(self.Footer_input)
        self.add_item(self.Footer_Icon_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if self.Footer_input.value:
                self.embed_message.set_footer(icon_url=self.Footer_Icon_input.value, text=self.Footer_input.value)
            else:
                self.embed_message.set_footer(text=None)

            await interaction.message.edit(embed=self.embed_message)
            await interaction.response.send_message(f"Embed footer updated.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to update embed: {e}", ephemeral=True)

class q7(ui.Modal, title='Set Color'):
    def __init__(self, embed_message):
        super().__init__()
        self.embed_message = embed_message
        self.Color_input = ui.TextInput(
            label='Color (hex code)',
            style=discord.TextStyle.short,
            required=False,
            min_length=7,
            max_length=7
        )
        self.add_item(self.Color_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            if self.Color_input.value:
                color = int(self.Color_input.value.lstrip('#'), 16)
                self.embed_message.color = color
            else:
                self.embed_message.color = None

            await interaction.message.edit(embed=self.embed_message)
            await interaction.response.send_message(f"Embed color updated.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to update embed: {e}", ephemeral=True)


class welcnbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def embed(self, ctx):
        try:
            embed = discord.Embed(description="Create an embed by using the buttons below!\n\n__Information:__\n• Imput the text you want to have in your embeds in the modals!\n• Leave the modal empty to clear the section\n• `Set color` uses hex codes (default: #2b2d31)\n• The embeds need at least 1 thing, you can't clear everything!\n• Get the ID of the channel you want to send it in\n• Image and thumbnails use Image links!\n-# Need any help? Ping <@609515684740988959>", color=0x2b2d31)
            embed.set_author(name="Hoshi Embed Maker", icon_url=ctx.guild.icon.url)
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            view = embedview(embed)
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            print(f"Error in embed command: {e}")

async def setup(bot):
    await bot.add_cog(welcnbye(bot))