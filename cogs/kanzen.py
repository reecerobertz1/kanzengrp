import discord
from discord.ext import commands
from discord import ui

class infoview(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.value = None
        self.bot = bot

    @discord.ui.button(label="Logos")
    async def klogos(self, interaction: discord.Interaction, button: discord.ui.Button):
        logos = discord.Embed(title="<a:bun:1098764398962671677> Chroma Logos!", description="˃ Please make sure you watermark the logos!\n˃ Use the watermark on every edit\n˃ Do not share this link with anyone outside the group!", color=0x2b2d31)
        logos.set_footer(text="Made us some logos? send them to Reece or Alisha!")
        logos.set_image(url=interaction.guild.banner)
        await interaction.user.send("key: `chUZuZ7Eu0mqLOM5rxRsQw`\nhttps://mega.nz/folder/xOk1SApA", embed=logos)
        channel = interaction.client.get_channel(1069358104740900985)
        log = discord.Embed(title="Logo button has been used!", description=f"`{interaction.user.display_name}` has used the logos button", color=0x2b2d31)
        log.set_footer(text=f"id: {interaction.user.id}", icon_url=interaction.user.display_avatar)
        await channel.send(embed=log)
        await interaction.response.send_message(f'I have sent you the logos! Check your DMs', ephemeral=True)

    @discord.ui.button(label="Inactive")
    async def inactive(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(ia(bot=self.bot))

    @discord.ui.button(label="Report member")
    async def report(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(reportmember())

class reportmember(ui.Modal, title='Report'):
    reported = ui.TextInput(label='Who are you reporting?', placeholder="Enter instagram + discord user", style=discord.TextStyle.short)
    why  = ui.TextInput(label='Why are you reporting them?', placeholder="Tell us here", style=discord.TextStyle.long)
    dm = ui.TextInput(label="Can we dm you for me info?", placeholder="yes or no", style=discord.TextStyle.short, required=False)
    user = ui.TextInput(label="Instagram / discord username", placeholder="Leave blank to stay anonymous", style=discord.TextStyle.short, required=False)
    async def on_submit(self, interaction: discord.Interaction):
        if self.user.value:
            description=f"reported member:\n{self.reported.value}\n\nwhy was they reported:\n{self.why.value}\n\nwho reported:\n{interaction.user.mention}\n\nyou can dm them for more information\n-# please react to this report message once the issue has been resolved!"
        else:
            description=f"reported member:\n{self.reported.value}\n\nwhy was they reported?\n{self.why.value}"
        embed = discord.Embed(description=description, color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        channel = interaction.client.get_channel(1274063410463641642)
        await channel.send("<@&739513680860938290>", embed=embed)
        await interaction.response.send_message(f'Your report has been sent!\nThank you for helping us make Chroma a better place!', ephemeral=True)

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
        embed.add_field(name="Group Rules", value="• Must be following [remqsi](https://instagra,.com/remqsi), [wqndqs](https://instagra,.com/wqndqs) + [chromagrp](https://instagra,.com/chromagrp)."
                                            "\n• Always use our hashtag #𝗰𝗵𝗿𝗼𝗺𝗮𝗴𝗿𝗽."
                                            "\n• Watermark logos if the background is mostly plain."
                                            "\n• Never share the logos with anyone outside of Chroma."
                                            "\n-# **Note:** Leaking our logos will get you banned.", inline=False)
        embed.add_field(name="Chat Rules", value="• Make sure you have your age roles from <id:customize>!"
                            "\n• No NSFW content or sexual discussions."
                            "\n• No offensive jokes that can make others uncomfortable."
                            '\n• Please stay as active as possible.'
                            '\n• Set your nickname as "name | username".'
                            "\n• No impersonating other editors."
                            "\n• Be friendly and respect everyone."
                            "\n• If you move accounts or leave, please dm [chromagrp](https://instagram.com/chromagrp)."
                            "\n• No trash talking of other groups or editors."
                            "\n• Respect the server and use channels correctly."
                            "\n-# **Note:** Breaking any of the rules will lead to a warning / kick or ban!", inline=False)
        embed2 = discord.Embed(title="Reporting Members", description="• If you see someone breaking our rules, report them below.\n• You can stay anonymous by leaving your username blank.\n• Click the `Report Member` button to report a chroma member.\n-# We may DM you for more information if we need more.", color=0x2b2d31)
        view=infoview(bot=self.bot)
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2, view=view)

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