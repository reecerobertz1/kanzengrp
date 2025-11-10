import random
from typing import Optional
import discord
from discord.ext import commands
from discord import ui
from discord import app_commands
from io import BytesIO
import datetime

class verify(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Verify")
    async def verify(self, interaction: discord.Interaction, button: discord.Button):
        letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
        numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        code = "".join([
            random.choice(letters), random.choice(letters), str(random.choice(numbers)),
            random.choice(letters), random.choice(letters), str(random.choice(numbers)),
            random.choice(letters), random.choice(letters), str(random.choice(numbers))
        ])

        await interaction.response.send_message(f"Please type this code below:\n`{code}`", ephemeral=True)

        def check(msg: discord.Message):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            msg = await interaction.client.wait_for("message", check=check, timeout=60)

            if msg.content.strip().upper() == code:
                role = interaction.guild.get_role(1437208382514663486)
                if role:
                    await interaction.user.add_roles(role)
                    await interaction.followup.send("✅ Verification successful! You have been given the role.", ephemeral=True)
                    await msg.delete()
                else:
                    await interaction.followup.send("❌ The 'Verified' role was not found. Please contact an admin.", ephemeral=True)
                    await msg.delete()
            else:
                await interaction.followup.send("❌ Incorrect code! Please try again by clicking the verify button again.", ephemeral=True)
                await msg.delete()

        except TimeoutError:
            await interaction.followup.send("⌛ You took too long to respond. Please try again.", ephemeral=True)

    @discord.ui.button(label="Help")
    async def help(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed (description="## Verification Help\n<:bullet_point_blue:1340661702378786879>Click the `Verify` button below\n<:bullet_point_blue:1340661702378786879>Hoshi will randomly generate a code for you to use\n<:bullet_point_blue:1340661702378786879>Send the same code within 60 seconds into chat to complete verification\n<:bullet_point_blue:1340661702378786879>If the bot does not reply after you have sent the code, or doesn't give you <@&1341753597368733736>. Please contact a staff member!", color=0xA4C4E6)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Apply(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot
        if not hasattr(self.bot, "savior_cooldowns"):
            self.bot.savior_cooldowns = {}

    @discord.ui.button(label="Apply")
    async def yes(self, interaction: discord.Interaction, button: discord.Button):
            now = datetime.datetime.utcnow()
            last = self.bot.savior_cooldowns.get(interaction.user.id)
            if last is not None:
                elapsed = now - last
                if elapsed < datetime.timedelta(hours=24):
                    remaining = datetime.timedelta(hours=24) - elapsed
                    total_seconds = int(remaining.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    await interaction.response.send_message(
                        f"You can only apply once every 24 hours. Please wait {hours}h {minutes}m before applying again.",
                        ephemeral=True,
                    )
                    return

            self.bot.savior_cooldowns[interaction.user.id] = now
            await interaction.response.send_modal(AppModal(bot=self.bot))

class AppModal(discord.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(title="Savior Applications")

    instagram = discord.ui.TextInput(label="Instagram Username", placeholder="Put username here...")
    edit = discord.ui.TextInput(label="Link one edit", placeholder="Edit url here...", style=discord.TextStyle.short)
    program = discord.ui.TextInput(label="What editing program do you use?", placeholder="", style=discord.TextStyle.short)
    more = discord.ui.TextInput(label="Anything else we should know?", placeholder="", style=discord.TextStyle.long)
    

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Savior Apps", description=f"・From: [@{self.instagram.value}](https://instagram.com/{self.instagram.value} )\n\n・edit:\n{self.edit.value}\n\n・program:\n{self.program.value}\n\n・more:\n{self.more.value}", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.user.display_avatar)
        now = datetime.datetime.now()
        timestamp = now.strftime("%d/%m/%Y %I:%M %p")
        embed.set_footer(text=f"User ID: {interaction.user.id} • {timestamp}")
        msg = await interaction.client.get_channel(1436127348901810196).send(embed=embed)
        await interaction.response.send_message(f'Thank you for applying to Savior\nPlease wait for a response for us!', ephemeral=True)

class Savior(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = None

    @commands.command()
    async def saviorapps(self, ctx: commands.Context):
        view = Apply(bot=self.bot)
        embed = discord.Embed(title="Savior applications", description="Welcome to [saviorogs](https://www.instagram.com/saviorogs/) recruitment!\nPlease read all the information below before applying.\n\n**INFORMATION**\n• You can only apply once per **24 hours**.\n• We will ping you in #channel with your review.\n⠀— ・You will get **Accept** or **Re-app** from us.\n• Remakes and velocities are auto declined.\n• Edits older than **6 month** are auto declined.")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1401326232431231006/77c2c07a25904f931b7e669defe86e55.webp?size=1024")
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def verifyy(self, ctx):
        embed = discord.Embed(description="## Verification Required\n• To access the server, you need to pass the verification first.\n• Click `Verify` to begin the verification process.", color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1395051044773298236/1411030763255890104/verify_banner_00000.png?ex=68b32c4d&is=68b1dacd&hm=d67ca1aa5dacc39f6361224173bed89bb1563e282a86416ffef2275dd2895659&")
        await ctx.send(embed=embed, view=verify())

async def setup(bot):
    await bot.add_cog(Savior(bot))