import json
import discord
from discord.ext import commands

class custom(commands.Cog):
    """Help with custom commands (Kanzen Only)"""
    def __init__(self, bot):
        self.bot = bot
        self.custom_commands = {}

        try:
            with open("./json files/custom.json", "r") as file:
                self.custom_commands = json.load(file)
        except FileNotFoundError:
            pass

    def save_custom_commands(self):
        with open("./json files/custom.json", "w") as file:
            json.dump(self.custom_commands, file, indent=4)

    @commands.command(description="Add a custom command")
    @commands.guild_only()
    async def cmdnew(self, ctx, command_name, *, command_response):
        if ctx.guild.id != 1121841073673736215:
            return

        server_id = str(ctx.guild.id)

        
        if server_id not in self.custom_commands:
            self.custom_commands[server_id] = {}

        
        command_name_with_prefix = "+" + command_name
        self.custom_commands[server_id][command_name_with_prefix.lower()] = command_response

        
        self.save_custom_commands()

        await ctx.reply(f"Custom command '{command_name_with_prefix}' has been added!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        server_id = str(message.guild.id)


        if server_id in self.custom_commands:
            content = message.content.lower()

            if content in self.custom_commands[server_id]:
                response = self.custom_commands[server_id][content]
                await message.channel.send(response)

    @commands.command(description="Remove a custom command")
    async def cmdremove(self, ctx, command_name):
        server_id = str(ctx.guild.id)

        if server_id in self.custom_commands and command_name in self.custom_commands[server_id]:
            del self.custom_commands[server_id][command_name]
            self.save_custom_commands()
            await ctx.reply(f"The custom command '{command_name}' has been removed.")
        else:
            await ctx.reply(f"The custom command '{command_name}' does not exist.")

    @commands.command(description="See the list of custom commands")
    async def cmdlist(self, ctx):
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