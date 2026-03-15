import discord
from discord.ext import commands
from bot import LalisaBot
from typing import Union

ALL_COLOUR_ROLE_IDS: set[int] = set()

class SingleRoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role, emoji: Union[discord.PartialEmoji, None] = None):
        kwargs: dict = {"style": discord.ButtonStyle.secondary}
        if emoji is not None:
            kwargs["emoji"] = emoji
        kwargs["label"] = None
        super().__init__(**kwargs)
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        added = []
        removed = []

        for r in list(member.roles):
            if r.id in ALL_COLOUR_ROLE_IDS and r != self.role:
                await member.remove_roles(r)
                removed.append(r.mention)

        if self.role not in member.roles:
            await member.add_roles(self.role)
            added.append(self.role.mention)

        msg = ""
        if added:
            msg += f"You added: {', '.join(added)}\n"
        if removed:
            msg += f"You removed: {', '.join(removed)}\n"
        if not msg:
            msg = "No roles were added or removed."

        await interaction.response.send_message(msg, ephemeral=True)

class FirstColourView(discord.ui.View):
    def __init__(self, roles: list[discord.Role]):
        super().__init__(timeout=None)
        self.roles = roles
        emoji_map = [
            "<:cherry:1477655091153735681>",
            "<:peach:1477655115413459006>",
            "<:luxe:1477655128424190281>",
            "<:envy:1477655160204562553>",
            "<:ivy:1477655167741591582>",
            "<:ice:1477655182048231749>"
        ]
        for role, emoji_str in zip(roles, emoji_map):
            emoji_id = int(emoji_str.split(":")[2][:-1])
            emoji = discord.PartialEmoji(name=None, id=emoji_id)
            self.add_item(SingleRoleButton(role, emoji))
        ALL_COLOUR_ROLE_IDS.update(r.id for r in roles)


class SecondColourView(discord.ui.View):
    def __init__(self, roles: list[discord.Role]):
        super().__init__(timeout=None)
        self.roles = roles
        emoji_map = [
            "<:azure:1477655188675498084>",
            "<:void:1477655229972353114>",
            "<:air:1477655224771547282>",
            "<:haze:1477655219100848169>",
            "<:gloss:1477655212939546675>",
            "<:reign:1477655194962493552>"
        ]
        for role, emoji_str in zip(roles, emoji_map):
            emoji_id = int(emoji_str.split(":")[2][:-1])
            emoji = discord.PartialEmoji(name=None, id=emoji_id)
            self.add_item(SingleRoleButton(role, emoji))
        ALL_COLOUR_ROLE_IDS.update(r.id for r in roles)

class ThirdColourView(discord.ui.View):
    def __init__(self, roles: list[discord.Role]):
        super().__init__(timeout=None)
        self.roles = roles
        emoji_map = [
            "<:dusk:1477655201086177332>",
            "<:bliss:1477655207503593565>",
            "<:aloe:1477655139514056918>",
            "<:chrome:1477655242316320789>",
            "<:pearl:1477655236054089879>",
            "<:smoke:1477655247911522316>"
        ]
        for role, emoji_str in zip(roles, emoji_map):
            emoji_id = int(emoji_str.split(":")[2][:-1])
            emoji = discord.PartialEmoji(name=None, id=emoji_id)
            self.add_item(SingleRoleButton(role, emoji))
        ALL_COLOUR_ROLE_IDS.update(r.id for r in roles)

class colours(commands.Cog):
    def __init__(self, bot: LalisaBot):
        self.bot = bot

    @commands.command()
    async def cgpcolours(self, ctx):
        ariana_embed = discord.Embed()
        ariana_embed.set_image(url="https://cdn.discordapp.com/attachments/1477651776139427872/1477659310292209737/Palette.png?ex=69a590f9&is=69a43f79&hm=0218b206af5a9b62e9ab2c2bb54220abeaf9f765d6bfe25e217c83a4e5ad75d1&")

        first_colours = discord.Embed(description="**        †       Name Colours     ༝ ⁺  **")
        first_colours.add_field(name=" ", value="<:cherry:1477655091153735681><@&1462465113310236702>"
            "\n<:peach:1477655115413459006><@&1462465066778624070>"
            "\n<:luxe:1477655128424190281><@&1462162217251246233>", inline=True)
        first_colours.add_field(name=" ", value="<:envy:1477655160204562553><@&1462465333527973982>"
            "\n<:ivy:1477655167741591582><@&1462465304285286451>"
            "\n<:ice:1477655182048231749><@&1462162383719104554>", inline=True)
        first_colours.set_image(url="https://cdn.discordapp.com/attachments/1477651776139427872/1477661228955467889/Comp_2_00000.png?ex=69a592c2&is=69a44142&hm=a91386b25458a1ef556bd93441ad781cf22d889146c42b373e89e407ca00f50f&")

        await ctx.send(embed=ariana_embed)

        first_role_ids = [
            1462465113310236702, 1462465066778624070, 1462162217251246233, 1462465333527973982, 1462465304285286451, 1462162383719104554
        ]
        first_roles = [ctx.guild.get_role(rid) for rid in first_role_ids if ctx.guild.get_role(rid)]
        await ctx.send(embed=first_colours, view=FirstColourView(first_roles))

        second_colours = discord.Embed()
        second_colours.add_field(name=" ", value="<:azure:1477655188675498084><@&1462464107142713454>"
            "\n<:void:1477655229972353114><@&1462465400695558317>"
            "\n<:air:1477655224771547282><@&1462465364842516584>", inline=True)
        second_colours.add_field(name=" ", value="<:haze:1477655219100848169><@&1462464732132016231>"
            "\n<:gloss:1477655212939546675><@&1462464728801742939>"
            "\n<:reign:1477655194962493552><@&1462465435520991388>", inline=True)
        second_colours.set_image(url="https://cdn.discordapp.com/attachments/1477651776139427872/1477661228955467889/Comp_2_00000.png?ex=69a592c2&is=69a44142&hm=a91386b25458a1ef556bd93441ad781cf22d889146c42b373e89e407ca00f50f&")

        second_role_ids = [
            1462464107142713454, 1462465400695558317, 1462465364842516584, 1462464732132016231, 1462464728801742939, 1462465435520991388
        ]
        second_roles = [ctx.guild.get_role(rid) for rid in second_role_ids if ctx.guild.get_role(rid)]
        await ctx.send(embed=second_colours, view=SecondColourView(second_roles))

        third_colours = discord.Embed()
        third_colours.add_field(name=" ", value="<:dusk:1477655201086177332><@&1462465182289760309>"
            "\n<:bliss:1477655207503593565><@&1462464962009108686>"
            "\n<:aloe:1477655139514056918><@&1462464736733040775>", inline=True)
        third_colours.add_field(name=" ", value="<:chrome:1477655242316320789><@&1462465221594579156>"
            "\n<:pearl:1477655236054089879><@&1462464734531162183>"
            "\n<:smoke:1477655247911522316><@&1462465261834866976>", inline=True)
        third_colours.set_image(url="https://cdn.discordapp.com/attachments/1477651776139427872/1477661228955467889/Comp_2_00000.png?ex=69a592c2&is=69a44142&hm=a91386b25458a1ef556bd93441ad781cf22d889146c42b373e89e407ca00f50f&")

        third_roles_ids = [
            1462465182289760309, 1462464962009108686, 1462464736733040775, 1462465221594579156, 1462464734531162183, 1462465261834866976
        ]
        third_roles = [ctx.guild.get_role(rid) for rid in third_roles_ids if ctx.guild.get_role(rid)]
        await ctx.send(embed=third_colours, view=ThirdColourView(third_roles))

async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(colours(bot))

# Message from Joshua: I love my Reece. He is the most beautiful most sexy man I have ever met. I love him, my dear favourite boy