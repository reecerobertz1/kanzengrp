import json
import discord
from discord.ext import commands

class custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_commands = {}

        try:
            with open("custom.json", "r") as file:
                self.custom_commands = json.load(file)
        except FileNotFoundError:
            pass

    def save_custom_commands(self):
        with open("custom.json", "w") as file:
            json.dump(self.custom_commands, file, indent=4)

    @commands.command()
    @commands.guild_only()  # Make the command only work in guilds (servers)
    @commands.has_permissions(manage_guild=True)  # Make the command only accessible by users with 'manage_guild' permission
    async def newcmd(self, ctx, command_name, command_response):
        # Check if the command is being executed in the desired server
        if ctx.guild.id != 1121841073673736215:
            return

        server_id = str(ctx.guild.id)

        # Check if the custom commands for the server already exist
        if server_id not in self.custom_commands:
            self.custom_commands[server_id] = {}

        # Add the custom command to the dictionary
        command_name_with_prefix = "+" + command_name
        self.custom_commands[server_id][command_name_with_prefix.lower()] = command_response

        # Save the updated custom commands to JSON file
        self.save_custom_commands()

        await ctx.reply(f"Custom command '{command_name_with_prefix}' has been added!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        server_id = str(message.guild.id)

        # Check if the server has custom commands
        if server_id in self.custom_commands:
            content = message.content.lower()

            # Check if the message is a custom command
            if content in self.custom_commands[server_id]:
                response = self.custom_commands[server_id][content]
                await message.channel.send(response)

    @commands.command()
    async def removecmd(self, ctx, command_name):
        server_id = str(ctx.guild.id)

        if server_id in self.custom_commands and command_name in self.custom_commands[server_id]:
            del self.custom_commands[server_id][command_name]
            self.save_custom_commands()
            await ctx.reply(f"The custom command '{command_name}' has been removed.")
        else:
            await ctx.reply(f"The custom command '{command_name}' does not exist.")

    @commands.command()
    async def listcmds(self, ctx):
        server_id = str(ctx.guild.id)

        if server_id in self.custom_commands and self.custom_commands[server_id]:
            embed = discord.Embed(title="Custom Commands", color=0x2b2d31)

            for command_name, command_response in self.custom_commands[server_id].items():
                embed.add_field(name=f"Command: {command_name}", value=f"Response: {command_response}", inline=False)

            await ctx.reply(embed=embed)
        else:
            await ctx.reply("There are no custom commands.")

async def setup(bot):
    await bot.add_cog(custom(bot))