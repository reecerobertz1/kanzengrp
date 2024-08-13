import discord
from discord.ext import commands

class infoview(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Logos")
    async def klogos(self, interaction: discord.Interaction, button: discord.ui.Button):
        logos = discord.Embed(title="<a:bun:1098764398962671677> CHroma Logos!", description="˃ Please make sure you watermark the logos!\n˃ Use the watermark on every edit\n˃ Do not share this link with anyone outside the group!", color=0x2b2d31)
        logos.set_footer(text="Made us some logos? send them to Reece or Alisha!")
        logos.set_image(url=interaction.guild.banner)
        await interaction.user.send("key: `9evZccDJkjjN7k64fAlAKw`\nhttps://mega.nz/folder/j8NniaoJ", embed=logos)
        channel = interaction.client.get_channel(1069358104740900985)
        log = discord.Embed(title="Logo button has been used!", description=f"`{interaction.user.display_name}` has used the logos button", color=0x2b2d31)
        log.set_footer(text=f"id: {interaction.user.id}", icon_url=interaction.user.display_avatar)
        await channel.send(embed=log)
        await interaction.response.send_message(f'I have sent you the logos! Check your DMs', ephemeral=True)

    @discord.ui.button(label="inactive")
    async def inactive(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(ia(bot=self.bot))

class ia(discord.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(title="Inactive Message")

    instagram = discord.ui.TextInput(label="Instagram Username", placeholder="Put username here...")
    reason = discord.ui.TextInput(label="Why will you be inactive?", placeholder="Put a reason here", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Inactivity", description=f"Sent from: [@{self.instagram.value}](https://instagram.com/{self.instagram.value} )\nReason: {self.reason.value}", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.user.display_avatar)
        embed.set_footer(text=f"User ID: {interaction.user.id}")
        msg = await interaction.client.get_channel(849707778380922910).send(f"{interaction.user.mention}", embed=embed)
        await interaction.response.send_message('Thanks! I have sent your message!', ephemeral=True)

class kanzen(commands.Cog, name="kanzen", description="Includes the commands associated with [Chroma group](https://www.instagram.com/chromagrp) and its members!"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.has_permissions(manage_guild=True)
    async def info1(self, ctx):
        embed = discord.Embed(title="Weclome to Chroma", color=0x2b2d31)
        embed.add_field(name="Group Rules", value="• Must be following [remqsi](https://instagra,.com/remqsi), [wqndqs](https://instagram.com/wqndqs) + [chromagrp](https://instagram.com/chromagrp)"
                                            "\n• Always use our hashtag #𝗰𝗵𝗿𝗼𝗺𝗮𝗴𝗿𝗽"
                                            "\n• Watermark logos if the background is mostly plain"
                                            "\n• Never share the logos with anyone outside of Chroma", inline=False)
        embed.add_field(name="Chat Rules", value="• No NSFW content or sexual discussions"
                            "\n• No offensive jokes that can make others uncomfortable"
                            "\n• Please stay as active as possible"
                            '\n• Set your nickname as "name | username"'
                            "\n• No impersonating other editors"
                            "\n• Be friendly and respect everyone"
                            "\n• If you move accounts or leave, please dm [chromagrp](https://instagram.com/chromagrp)"
                            "\n• No trash talking of other groups or editors"
                            "\n• Respect the server and use channels correctly", inline=False)
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed, view=infoview(bot=self.bot))

    @commands.command(hidden=True)
    @commands.has_permissions(manage_guild=True)
    async def ccrules(self, ctx):
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1226134627664789526/1254162072351277066/welc_banner_00000_00000.png?ex=66787cf3&is=66772b73&hm=cb44b5ff9979c2cb672fc9a6f473e32e23727cd12a17644cb8db1f577e45ee87&")
        embed2 = discord.Embed(description="__Server Rules__:"
        "\n• English chat only"
        "\n• Follow Discord's TOS and [guidelines](https://discord.com/guidelines)"
        "\n• No NSFW content or sexual discussions"
        "\n• Be nice and respectful to everyone"
        "\n• No impersonating editors, Chroma staff, etc"
        "\n• Use channels for their intended purpose"
        "\n• No spamming pings; you will be warned"
        "\n• No trash talking others"
        "\n• No unnecessary pings to Chroma staff"
        "\n• No spamming or flooding channels with messages", color=0x2b2d31)
        await ctx.send(embed=embed)
        socials = discord.ui.View()
        insta = discord.ui.Button(label="instagram", url="https://www.instagram.com/chromagrp/")
        remqsi = discord.ui.Button(label="remqsi", url="https://www.instagram.com/remqsi/")
        wqndqs = discord.ui.Button(label="wqndqs", url="https://www.instagram.com/wqndqs/")
        socials.add_item(insta)
        socials.add_item(remqsi)
        socials.add_item(wqndqs)
        await ctx.send(embed=embed2, view=socials)

async def setup(bot):
    await bot.add_cog(kanzen(bot))