import json
from typing import Any
import discord
from discord.ext import commands
from discord import app_commands
from discord.interactions import Interaction
from discord.ui import View, Select
from typing import List, Optional
from discord import ui

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

    @discord.ui.button(label="Kanzen Ranked")
    async def ranks(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("https://cdn.discordapp.com/attachments/1181419043153002546/1216065287120748714/ranked_badges_00000.png?ex=661ab78d&is=6608428d&hm=13dad2c986b6354387a6f119079e76418faccfdfaf7ad82f87f42cc992fa1667&", ephemeral=True)

    @discord.ui.button(label="Booster Perks")
    async def bp(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("https://cdn.discordapp.com/attachments/1198665603897118720/1223868316771160074/image.png?ex=661b6b31&is=6608f631&hm=5cf4e9697bcbaea6aa1c585a42db671f664d37c2e7a1daa4b6d0924748a06186&", ephemeral=True)

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
        channel = interaction.client.get_channel(1121913672822968330)
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

class kanzen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.emoji = "<:shooky:1121909564799987722>"

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def info(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(description="### **[Welcome*!*](https://instagram.com/kanzengrp/)**"
                              "\nThank you for joining. We hope you enjoy your time here!"
                              "\n<:1166196254141861979:1208228728472076308> Make sure to be following [@kanzengrp](https://instagram.com/kanzengrp/) + [@remqsi](https://instagram.com/remqsi/)"
                              "\n<:1166196254141861979:1208228728472076308> If you ever decide to leave kanzengrp please DM and let us know"
                              "\n<:1166196254141861979:1208228728472076308> Always watermark the logos"
                              "\n<:1166196254141861979:1208228728472076308> Do not share the logos link outside the server!"
                              "\n<:1166196258499727480:1208228386842087554> And please remain as active as possible!", color=0x2b2d31)
        embed.set_author(name="Kanzengrp", icon_url=ctx.guild.icon)
        embed2 = discord.Embed(description='### | `✿` __**Chat Rules**__'
                               '\n<a:Arrow_1:1145603161701224528> Do not send nsfw content or speak sexually with other members'
                               "\n<a:Arrow_1:1145603161701224528> No using any slurs / words that can be offensive (instant ban)"
                               "\n<a:Arrow_1:1145603161701224528> Make sure to have your age roles from ⁠<id:customize>"
                               "\n<a:Arrow_1:1145603161701224528> Please do not use bots outside of spam channels!"
                               '\n<a:Arrow_1:1145603161701224528> Please set your nickname as "your name | username"'
                               "\n<a:Arrow_1:1145603161701224528> No impersonation as other editors or members"
                               "\n<a:Arrow_1:1145603161701224528> No trash talking other editors and groups!"
                               '\n<a:Arrow_1:1145603161701224528> Any rules above broken, you will receive a warning/get kicked', color=0x2b2d31)
        embed2.set_image(url="https://cdn.discordapp.com/attachments/1184208577120960632/1208238170446241842/welc_banner_00000.png?ex=65e28e7b&is=65d0197b&hm=6b49f32da0368e84e7c14c89cd0313f831723f44289064a1aff6b831843ec078&")
        view = infobuttons()
        message = await ctx.send(embed=embed)
        await ctx.send(embed=embed2, view=view)

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
        embed1 = discord.Embed(title="Logo & Hashtag rep", description="Using one of our logos and the hashtag under you post will get you **1,000xp** towards your levels", color=0x2b2d31)
        embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/1157492645086646384/1185339757656555631/K_00000-min.png?ex=658f40ac&is=657ccbac&hm=c5243f72aebf161710ea63ec97a155b700495fce7152e790137e1ed46130a8a2&")
        embed1.set_footer(text="Send your edits below to receive your xp!")
        embed2 = discord.Embed(description="<a:arrow:1185338703204331622> Please bare in mind that you do need to use both the logos and hashtag to receive xp! you can no longer use just the hashtag or logos for xp", color=0x2b2d31)
        embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/1157492645086646384/1185340989905322025/fghjfghjjgjfghjghj.png?ex=658f41d2&is=657cccd2&hm=9770aede5cbbc4369d63c6f5964050d28cba908fd5e7095cef48bb945f517d18&")
        embed3 = discord.Embed(description="<a:arrow:1185338703204331622> Your edit needs to be from this month only, so say its December, you need your edits to be from this month only, they cant be from November or even older, ones January 1st starts, edits from December are no longer allowed", color=0x2b2d31)
        embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/1157492645086646384/1185340989905322025/fghjfghjjgjfghjghj.png?ex=658f41d2&is=657cccd2&hm=9770aede5cbbc4369d63c6f5964050d28cba908fd5e7095cef48bb945f517d18&")
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)

    @app_commands.command(name="feedback", description="give feedback")
    async def feedback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(feedback())

async def setup(bot):
    await bot.add_cog(kanzen(bot))