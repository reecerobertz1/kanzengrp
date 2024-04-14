import json
from typing import Any
import discord
from discord.ext import commands
from discord import app_commands
from discord.interactions import Interaction
from discord.ui import View, Select
from typing import List, Optional
from discord import ui

class staffappsbutton(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Apply here")
    async def inactive(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(staffapps())

class staffguide(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Applications")
    async def staffguide(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(description="> `🌌` **__Application help__**"
"\nFirst please make sure you join our public server, as this is where we do all our recruits, click the button at the bottom to join Kanzen Public"

"\n\n- A member will send an application in <#1222674203447267399>"
"\n- Their application will have 2 buttons **accept** and **decline**"
"\n- You can use these buttons to vote whether a member should be accepted or declined"
"\n- Each member needs **4** accepts/declines before getting a response"
"\n- A member is able to DM you for criticism if they got declined, so be prepared"

"\n\n> `💫` **__What we do/don't look for__**"
"\n- Our main things we look for in edits is **smooth** and **creative** edits"
"\n- We sometimes do accept velocity edits, but it is very very rare"
"\n- Please do be very strict when it comes to accepting"
"\n- If a member doesn't have a consistent edit style, it does not matter, if they're good... they're good"
"\n- If a member has used an edit **over 3 months old** decline it and let them know to use a more recent edit", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class infobuttons(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Logos")
    async def klogos(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = kanzenlogos()
        logos = discord.Embed(title="<a:kanzenflower:1128154723262943282> Kanzen Logos!", description="<a:Arrow_1:1145603161701224528> Please make sure you watermark the logos!\n<a:Arrow_1:1145603161701224528> Use the watermark on every edit\n<a:Arrow_1:1145603161701224528> Do not share this link with anyone outside the group!", color=0x2b2d31)
        logos.set_footer(text="Made us some logos? send them to Reece!")
        logos.set_image(url="https://cdn.discordapp.com/attachments/849724031723634688/1145605654539669565/new_banner_00000.png")
        await interaction.user.send(embed=logos, view=view)
        channel = interaction.client.get_channel(1122627075682078720)
        log = discord.Embed(title="Logo button has been used!", description=f"`{interaction.user.display_name}` has used the logos button", color=0x2b2d31)
        log.set_footer(text=f"id: {interaction.user.id}", icon_url=interaction.user.display_avatar)
        await channel.send(embed=log)
        await interaction.response.send_message(f'I have sent you the logos! Check your DMs', ephemeral=True)

    @discord.ui.button(label="Booster Perks")
    async def bp(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("https://cdn.discordapp.com/attachments/1198665603897118720/1225863428967764091/image.png?ex=6622ad48&is=66103848&hm=273b466a3de5ff272322d458ef9dc6f6da5e3ac53435b8d1121aa431309fe86a&", ephemeral=True)

    @discord.ui.button(label="Inactivity")
    async def inactive(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(ia())

class kanzenlogos(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Get logos!")
    async def logos(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Here are the logos!\n[click here](<https://mega.nz/folder/ZtVyULzT#MRTZmGasmhFQHipvBKH00g>)")
        await interaction.followup.send("#𝗞𝗮𝗻𝘇𝗲𝗻𝗴𝗿𝗽")

class daegulogos(discord.ui.View):
    def __init__ (self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Get logos!")
    async def logos(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_message("Here are the logos!\n[click here](<https://mega.nz/folder/4QZWTBjR#ZmyJUH2HHj8lFrwkY1BrPw>)")

class ia(ui.Modal, title='Inactivity Message'):
    instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
    reason = ui.TextInput(label='Inactivity Reason', placeholder="", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(description=f"Instagram - [{self.instagram.value}](https://instagram.com/{self.instagram.value})\nDiscord - {interaction.user.display_name}\nReason - {self.reason.value}", color=0x2b2d31)
        embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        channel = interaction.client.get_channel(1220525020682522777)
        await channel.send(embed=embed)
        await interaction.response.send_message(f'Your inactive message has been sent successfully', ephemeral=True)

class feedback(ui.Modal, title='Kanzen Feedback'):
    rate = ui.TextInput(label='Scale of 1-10, how would you rate Kanzen', placeholder="Enter your rating here", style=discord.TextStyle.short)
    improve = ui.TextInput(label='How can we improve', placeholder="Bullet point ideas here...", style=discord.TextStyle.long)
    likes = ui.TextInput(label='What do you like about our group?', placeholder="List your likes here...", style=discord.TextStyle.long)
    dislikes = ui.TextInput(label='What do you dislike about our group?', placeholder="List your dislikes here...", style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title='Feedback', description=f"what do they rate kanzen 1 - 10:\n{self.rate.value}\n\nhow can we improve:\n{self.improve.value}\n\nwhat do they like:\n{self.likes.value}\n\nwhat do they dislike:\n{self.dislikes.value}", color=0x2b2d31)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text=f"Sent from {interaction.user.name}", icon_url=interaction.user.display_avatar)
        channel = interaction.client.get_channel(1187434136395325469)
        await channel.send(embed=embed)
        await interaction.followup.send(f"Thank you {interaction.user.display_name} your feedback has been sent!", ephemeral=True)

class staffapps(ui.Modal, title='Staff apps'):
    role = ui.TextInput(label='What role are you applying for?', placeholder="Enter the role here: head staff, mod, staff", style=discord.TextStyle.short)
    experience  = ui.TextInput(label='What experience do you have?', placeholder="Tell me here", style=discord.TextStyle.long)
    why = ui.TextInput(label="Why should i add you?", placeholder="Tell me here", style=discord.TextStyle.long)
    active = ui.TextInput(label="How active are you? scale of 1-10", placeholder="Tell me here", style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(description=f"> `🪐` **__Staff Application__**\n\n**Sent from**: <@{interaction.user.id}>\n\n**Experience**\n{self.experience.value}\n\n**Why**\n{self.why.value}\n\n**Active**: {self.active.value}", color=0x2b2d31)
        embed.set_footer(text=interaction.user.id, icon_url=interaction.user.display_avatar)
        embed.set_thumbnail(url=interaction.user.display_avatar)
        channel = interaction.client.get_channel(1228842574866022533)
        await channel.send(embed=embed)
        await interaction.response.send_message(f'Your staff application for {self.role.value} has been sent successfully', ephemeral=True)

class kanzen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.emoji = "<:shooky:1121909564799987722>"

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def info(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1224699045834919978/welc_banner_00000.png?ex=661e70de&is=660bfbde&hm=e0fd22d8e884fda1ec8e4257378cc7177c4e89ca3de21fbc7f1b9251ea9199c0&")
        embed1 = discord.Embed(title="> __Kanzen Rules__", description="<a:Arrow_1:1145603161701224528> No NSFW content or sexual discussions"
        "\n<a:Arrow_1:1145603161701224528> No offensive slurs (instant ban)"
        "\n<a:Arrow_1:1145603161701224528> Must have age roles from ⁠⁠<id:customize>"
        "\n<a:Arrow_1:1145603161701224528> Only use bots in designated channels"
        '\n<a:Arrow_1:1145603161701224528> Set nickname as "your name | username"'
        "\n<a:Arrow_1:1145603161701224528> No impersonating other editors / members"
        "\n<a:Arrow_1:1145603161701224528> No trash talking other members or groups"
        "\n<a:Arrow_1:1145603161701224528> Breaking rules leads to warning/kick", color=0x2b2d31)
        view = infobuttons()
        await ctx.send(embed=embed)
        await ctx.send(embed=embed1, view=view)

    def is_booster():
        async def predicate(ctx):
            role_id = 1128460924886458489
            role = ctx.guild.get_role(role_id)
            return role in ctx.author.roles
        return commands.check(predicate)
    
    @commands.command()
    @is_booster()
    async def perks(self, ctx):
        await ctx.author.send("https://mega.nz/folder/BwcTiSKS#oB8-ffeutzGzFLSFi81l5Q")
        await ctx.author.send("https://cdn.discordapp.com/attachments/1198665603897118720/1223868316771160074/image.png?ex=661b6b31&is=6608f631&hm=5cf4e9697bcbaea6aa1c585a42db671f664d37c2e7a1daa4b6d0924748a06186&")
        await ctx.reply("Check dms! i have sent you our perks")

    @commands.command()
    async def xplol(self, ctx):
        embed = discord.Embed(description="> `✨` **__Logo and Hashtag rep__**"
        "\n\n<a:Arrow_1:1145603161701224528>  Using one of our logos and the hashtag under you post will get you **500xp** towards your levels"
        "\n\n<a:Arrow_1:1145603161701224528> Please bare in mind that you do need to use both the logos and hashtag to receive xp! you can no longer use just the hashtag or logos for xp"
        "\n\n<a:Arrow_1:1145603161701224528> Your edit needs to be from this month only, so say its December, you need your edits to be from this month only, they cant be from November or even older, ones January 1st starts, edits from December are no longer allowed", color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1198665603897118720/1224407264002183279/welc_banner_00000_1_00000.png?ex=661d6120&is=660aec20&hm=140f45cedbf4a3c5fbacdee15d344b1299ec5501f89906e5043403b9e31deeee&")
        await ctx.send(embed=embed)

    @app_commands.command(name="feedback", description="give feedback")
    async def feedback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(feedback())

    @commands.command()
    async def staffguide(self, ctx):
        staff = discord.Embed(description="> **__Staff__**"
"\nAs a staff member you can host events such as game nights, movie nights or anything else you can think off, except a group collab or edit wars. You also need to help out with applications when we have a recruit"
"\n\nIf you happen to see anyone breaking our rules, you should either tell them to stop whatever it is they're doing, or give them a warning via Hoshi. The warning command is </warn:1182987258056409230>. If a member has 2 warnings, they're instantly banned from Kanzengrp. If the command does not work, you can give them a warning by just saying it and letting us know in <#1178952898273628200>"
"\n\nIf you have anymore questions on what you can do as a staff member, feel free to ping Reece!", color=0x2b2d31)
        staff.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=staff)
        mods = discord.Embed(description="> **__Moderator__**"
"\nAs a moderator you can do everything a staff member can do. But you're able to ban and kick members yourself. Also make sure members are following the server rules!"
"\n\n- Make sure members have their age roles (the correct ones)"
"\n- If a member doesn't have their nickname as **name | instagram** ask them to change it, or do it yourself"
"\n- If members are sending NSFW content in the server or using words that can be offensive (slurs, sexist comments, homophobia etc), instantly kick them from the server"
"\n- If any other rules such as, trash talk, impersonating people, not using the right channels for things you can use our warn command </warn:1182987258056409230>", color=0x2b2d31)
        mods.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=mods, view=staffguide())

    @commands.command()
    async def staffapps(self, ctx):
        embed=discord.Embed(title="> `🪐` **__Staff Apps__**", description="Before applying here is a little bit of information you need to know", color=0x2b2d31)
        embed.add_field(name="__Head Staff__:", value="• Work closely with <@603077306956644353> and manage all team roles (admins, mods, staff, zennies)."
        "\n• Choose one person for the head staff role who has good experience and leadership skills."
        "\n• Keep the staff team running well and encourage them to be active."
        "\n• Stay active in the server yourself."
        "\n• And everything else from the other roles", inline=False)
        embed.add_field(name="__Moderator__:", value="• Basic moderator role: moderate messages, nicknames, and profile pics."
        "\n• Issue warnings with /warning for rule-breaking; report to head staff or Reece."
        "\n• if they break the first 2 rules of our server, you can kick or ban without permission."
        "\n• And anything else from staff", inline=False)
        embed.add_field(name="__Staff__:", value="• Plan events (game / movie nights or editing challenges)"
        "\n• Help members when they need it"
        "\n• Help out with normal stuff within the server (sorting channels, roles, members)"
        "\n• Review apps when we have a recruit"
        "\n• When we have collabs you can help host one of them", inline=False)
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.reply(embed=embed, view=staffappsbutton())

async def setup(bot):
    await bot.add_cog(kanzen(bot))