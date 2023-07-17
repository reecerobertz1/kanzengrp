import traceback
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.applications = {}  # Initialize the applications dictionary here

    @commands.Cog.listener()  # This is required for the on_ready event to work in the cog
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def accept(self, ctx, member: discord.Member):
        if ctx.guild.id == 1123347338841313331:  # Aura
            invite_server_id = 957987670787764224
            accepted_channel_id = 1123588246614577213
            add_role_id = 1123356130970701878
            remove_role_id = 1123356165246566491
            message = f"{member.mention} has been accepted."
            embed_color = 0x2b2d31
        elif ctx.guild.id == 1122181605591621692:  # Kanzen
            invite_server_id = 1121841073673736215
            accepted_channel_id = 1123588044180684800
            add_role_id = 1122191098006224906
            remove_role_id = 1122191119430733835
            message = f"{member.mention} has been accepted."
            embed_color = 0x2b2d31
        elif ctx.guild.id == 901409710572466217:  # daegu
            invite_server_id = 896619762354892821  
            accepted_channel_id = 901410829218492456
            add_role_id = 1119012138640494594
            remove_role_id = 901412966241554462
            message = f"{member.mention} has been accepted."
            embed_color = 0x2b2d31
        else:
            await ctx.reply("You can only use this command in specific servers.")
            return

        accepted_channel = self.bot.get_channel(accepted_channel_id)
        if accepted_channel:
            await accepted_channel.send(message)
            await ctx.reply(f"Accept message sent to {member.mention}.")
        else:
            await ctx.reply("Failed to find the specified channel.")

        invite = await self.generate_invite(invite_server_id)

        # Create server-specific embed
        embed = None
        if ctx.guild.id == 1122181605591621692:
            embed = discord.Embed(color=embed_color)
            embed.set_image(url='https://cdn.discordapp.com/attachments/1121841074512605186/1128394231115948072/theme_3_00000.png')
            embed.add_field(name="You have been accepted into Kanzen!", value=f"[**Click here to join**]({invite})")
        elif ctx.guild.id == 1123347338841313331:
            embed = discord.Embed(color=embed_color)
            embed.set_image(url='https://cdn.discordapp.com/banners/957987670787764224/3b81da990294e7cf80a6b53d3ee98a1f.png?size=1024')
            embed.add_field(name="You have been accepted into Auragrp!", value=f"[**Click here to join**]({invite})")
        elif ctx.guild.id == 901409710572466217:
            embed = discord.Embed(color=embed_color)
            embed.set_image(url='https://cdn.discordapp.com/banners/896619762354892821/906d72346deed85c1abe719216180be0.png?size=1024')
            embed.add_field(name="You have been accepted into Daegu!", value=f"[**Click here to join**]({invite})")
        else:
            await ctx.reply("You can only use this command in specific servers.")
            return

        # Add the new "Status" field to the embed
        embed.add_field(name="Status", value="Accepted ✅", inline=False)

        guild = self.bot.get_guild(ctx.guild.id)
        role_to_add = guild.get_role(add_role_id)
        role_to_remove = guild.get_role(remove_role_id)

        if role_to_add:
            await member.add_roles(role_to_add)
        else:
            await ctx.reply("Failed to find the role to add.")

        if role_to_remove:
            await member.remove_roles(role_to_remove)
        else:
            await ctx.reply("Failed to find the role to remove.")

        # Extract Instagram account from the application data
        user_id = str(member.id)
        if user_id in self.applications:
            application = self.applications[user_id]
            instagram_account = application.get("edit_link", "").split("|")[-1].strip()
            if instagram_account.startswith("https://www.instagram.com/"):
                instagram_account = instagram_account.replace("https://www.instagram.com/", "")
                embed.add_field(name="Instagram Account", value=instagram_account)

        # Send the server-specific embed to the author's DM
        await ctx.author.send(embed=embed)

        # Edit the reply message with the "Accepted ✅" status
        await ctx.message.edit(embed=embed)

    async def generate_invite(self, server_id):
        server = self.bot.get_guild(server_id)
        if server:
            invites = await server.invites()
            if invites:
                return invites[0].url
            else:
                invite = await server.text_channels[0].create_invite()
                return invite.url
        else:
            raise ValueError("Failed to find the specified server.")

# slash commands

    @app_commands.command(name='test', description='testing slash commands')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('testing')

    @app_commands.command(name='lol', description='testing slash commands')
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('testing')

    @app_commands.command(name='kanzen', description='Get Kanzen logos')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def kanzenlogos(self, interaction: discord.Interaction):
        await interaction.response.send_message('https://mega.nz/folder/J40zCTYY#L73pTeQKWpCh15wpuQaIFA', ephemeral=True)

    @app_commands.command(name='aura', description='Get Aura logos')
    @app_commands.guilds(discord.Object(id=957987670787764224))
    async def auralogos(self, interaction: discord.Interaction):
        await interaction.response.send_message('https://mega.nz/folder/SNkySBBb#kNViVZOVnHzEFmFsuhtLOQ', ephemeral=True)


    @app_commands.command(name='modal', description='open testing modal')
    async def testmodal(self, interaction: discord.Interaction):
         await interaction.response.send_modal(testmodal())

    @app_commands.command(name='ia', description='Send an inactivity message!')
    @app_commands.guilds(discord.Object(id=1121841073673736215))
    async def ia(self, interaction: discord.Interaction):
         await interaction.response.send_modal(ia())

    @app_commands.command(name='apply', description='Apply for kanzen!')
    @app_commands.guilds(discord.Object(id=1122181605591621692))
    async def apps(self, interaction: discord.Interaction):
         await interaction.response.send_modal(apps())

# modals

class testmodal(ui.Modal, title='Testing it'):
     test1 = ui.TextInput(label='Testing modals', placeholder="you're ugly...", style=discord.TextStyle.short)
     test2 = ui.TextInput(label='Testing modals', placeholder="you make me wanna die...", style=discord.TextStyle.long)
     test3 = ui.TextInput(label='Testing modals', placeholder="lol jk....", style=discord.TextStyle.short)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.send_message(f"https://instagram.com/{self.test1}")

class ia(ui.Modal, title='Inactivity Message'):
     instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     reason = ui.TextInput(label='Inactivity Reason', placeholder="", style=discord.TextStyle.long)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Inactivity Message', color=0x2b2d31)
          embed.add_field(name='Instagram Name:', value=f'{self.instagram.value}', inline=False)
          embed.add_field(name='Instagram Account Link:', value=f'https://instagram.com/{self.instagram.value}', inline=False)
          embed.add_field(name='Inactivity Reason:', value=f'{self.reason.value}', inline=False)
          embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
          channel = interaction.client.get_channel(1121913672822968330)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your inactive message has been sent successfully', ephemeral=True)

class apps(ui.Modal, title='Kanzengrp Applications'):
     instagram = ui.TextInput(label='Instagram username', placeholder="Enter your Instagram username here...", style=discord.TextStyle.short)
     dcname = ui.TextInput(label='Discord username', placeholder="Enter your Discord username here...", style=discord.TextStyle.short)
     edit = ui.TextInput(label='Edit link (Instagran or Streamable)', placeholder="Paste link here...", style=discord.TextStyle.short)
     app = ui.TextInput(label='What app do you use for editing', placeholder="Editing app name...", style=discord.TextStyle.short)
     extra = ui.TextInput(label='Anything else you would like us to know?', placeholder="Extra info here...", style=discord.TextStyle.paragraph, required=False)
     async def on_submit(self, interaction: discord.Interaction):
          await interaction.response.defer()
          embed = discord.Embed(title='Kanzen Forms', color=0x2b2d31)
          embed.add_field(name='Instagram Name:', value=f'{self.instagram.value}', inline=False)
          embed.add_field(name='Instagram Account Link:', value=f'https://instagram.com/{self.instagram.value}', inline=False)
          embed.add_field(name='Discord Username:', value=f'{self.dcname.value}', inline=False)
          embed.add_field(name='Edit:', value=f'{self.edit.value}', inline=False)
          embed.add_field(name='Editing app:', value=f'{self.app.value}', inline=False)
          embed.add_field(name='Anything else:', value=f'{self.extra.value}', inline=False)
          embed.add_field(name="Discord ID:", value=interaction.user.id, inline=False)
          channel = interaction.client.get_channel(1122183100038905908)
          await channel.send(embed=embed)
          await interaction.followup.send(f'Your application has been sent successfully', ephemeral=True)

    # normal commands

async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Slash(bot))