import discord
from discord.ext import commands
from bot import LalisaBot

class ColourRoleDropdown(discord.ui.Select):
    def __init__(self, roles: list[discord.Role]):
        emoji_map = [
            "<:flower_red:836955512994136085>",
            "<:flower_peach:836955649883635772>",
            "<:flower_orange:836955588742742077>",
            "<:flower_yellow:836955637086158848>",
            "<:flower_lightgreen:836955686595461140>",
            "<:flower_green:836955698595889172>",
            "<:flower_lightteal:836955718522634300>",
            "<:flower_teal:836955735262625803>",
            "<:flower_lightblue:836955768346902549>",
            "<:flower_blue:836955781743378463>",
            "<:flower_lilac:836955801524109363>",
            "<:flower_purple:836955820272386048>",
            "<:flower_pink:836955936416595998>",
            "<:flower_lightpink:836955836278243398>",
            "<:flower_black:836955494689669130>",
        ]

        options = []
        for role, emoji_str in zip(roles, emoji_map):
            emoji_id = int(emoji_str.split(":")[2][:-1])
            emoji = discord.PartialEmoji(name=None, id=emoji_id)
            options.append(
                discord.SelectOption(
                    label=role.name,
                    value=str(role.id),
                    emoji=emoji
                )
            )

        super().__init__(
            placeholder=".　　　　 Select the name colour you'd like",
            min_values=0,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        selected_ids = set(int(v) for v in self.values)
        dropdown_role_ids = [int(opt.value) for opt in self.options]
        guild_roles = {role.id: role for role in interaction.guild.roles if role.id in dropdown_role_ids}

        added = []
        removed = []

        for role_id, role in guild_roles.items():
            if role_id in selected_ids and role not in member.roles:
                await member.add_roles(role)
                added.append(role.mention)
            elif role_id not in selected_ids and role in member.roles:
                await member.remove_roles(role)
                removed.append(role.mention)

        msg = ""
        if added:
            msg += f"You aded: {', '.join(added)}\n"
        if removed:
            msg += f"You removed: {', '.join(removed)}\n"
        if not msg:
            msg = "No roles were added or removed"

        await interaction.response.send_message(msg, ephemeral=True)

class ColourRoleView(discord.ui.View):
    def __init__(self, roles: list[discord.Role]):
        super().__init__(timeout=None)
        self.add_item(ColourRoleDropdown(roles))

class ProgramRolesDropDown(discord.ui.Select):
    def __init__(self, roles: list[discord.Role]):
        emoji_map = [
            "<:icon_aftereffects:1358784511210422472>",
            "<:icon_alightmotion:1358784733626106106>",
            "<:icon_videostar:1358785021921595533>",
            "<:icon_cutecut:1358785336553115880>",
            "<:icon_svp:1358785529889558578>",
            "<:icon_funimate:1364228674798358599>"
        ]

        options = []
        for role, emoji_str in zip(roles, emoji_map):
            emoji_id = int(emoji_str.split(":")[2][:-1])
            emoji = discord.PartialEmoji(name=None, id=emoji_id)
            options.append(
                discord.SelectOption(
                    label=role.name,
                    value=str(role.id),
                    emoji=emoji
                )
            )

        super().__init__(
            placeholder=".　　　　 Select the editing program you use",
            min_values=0,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        selected_ids = set(int(v) for v in self.values)
        dropdown_role_ids = [int(opt.value) for opt in self.options]
        guild_roles = {role.id: role for role in interaction.guild.roles if role.id in dropdown_role_ids}

        added = []
        removed = []

        for role_id, role in guild_roles.items():
            if role_id in selected_ids and role not in member.roles:
                await member.add_roles(role)
                added.append(role.mention)
            elif role_id not in selected_ids and role in member.roles:
                await member.remove_roles(role)
                removed.append(role.mention)

        msg = ""
        if added:
            msg += f"You aded: {', '.join(added)}\n"
        if removed:
            msg += f"You removed: {', '.join(removed)}\n"
        if not msg:
            msg = "No roles were added or removed"

        await interaction.response.send_message(msg, ephemeral=True)

class ProgramRoles(discord.ui.View):
    def __init__(self, roles: list[discord.Role]):
        super().__init__(timeout=None)
        self.add_item(ProgramRolesDropDown(roles))

class PronounsRolesDropDown(discord.ui.Select):
    def __init__(self, roles: list[discord.Role]):
        options = []
        for role in roles:
            options.append(
                discord.SelectOption(
                    label=role.name,
                    value=str(role.id)
                )
            )

        super().__init__(
            placeholder=".　　　　 Select your pronouns + age",
            min_values=0,
            max_values=len(options),
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        selected_ids = set(int(v) for v in self.values)
        dropdown_role_ids = [int(opt.value) for opt in self.options]
        guild_roles = {role.id: role for role in interaction.guild.roles if role.id in dropdown_role_ids}

        added = []
        removed = []

        for role_id, role in guild_roles.items():
            if role_id in selected_ids and role not in member.roles:
                await member.add_roles(role)
                added.append(role.mention)
            elif role_id not in selected_ids and role in member.roles:
                await member.remove_roles(role)
                removed.append(role.mention)

        msg = ""
        if added:
            msg += f"You added: {', '.join(added)}\n"
        if removed:
            msg += f"You removed: {', '.join(removed)}\n"
        if not msg:
            msg = "No roles were added or removed."

        await interaction.response.send_message(msg, ephemeral=True)

class PronounsRoles(discord.ui.View):
    def __init__(self, roles: list[discord.Role]):
        super().__init__(timeout=None)
        self.add_item(PronounsRolesDropDown(roles))

class GamesRolesDropDown(discord.ui.Select):
    def __init__(self, roles: list[discord.Role]):
        emoji_map = [
            "<:game_WutheringWaves:1334957321096269919>",
            "<:game_HonkaiStarRail:1334957545424556062>",
            "<:game_GenshinImpact:1334957721161695273>",
            "<:game_ZenlessZoneZero:1334957918382067785>",
            "<:game_DuetNightAbyss:1431984077497434123>",
            "<:game_ProjectSekai:1380146074156793976>",
            "<:game_minecraft:838325085679910913>",
            "<:game_roblox:838324839781236748>",
            "<:game_valorant:838325478384205834>",
            "<:game_vbucks:1285692390652510309>",
            "<:icon_discord:1358790160799502608>"
        ]

        options = []
        for role, emoji_str in zip(roles, emoji_map):
            emoji_id = int(emoji_str.split(":")[2][:-1])
            emoji = discord.PartialEmoji(name=None, id=emoji_id)
            options.append(
                discord.SelectOption(
                    label=role.name,
                    value=str(role.id),
                    emoji=emoji
                )
            )

        super().__init__(
            placeholder=".　　　　 Select your favourite games",
            min_values=0,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        selected_ids = set(int(v) for v in self.values)
        dropdown_role_ids = [int(opt.value) for opt in self.options]
        guild_roles = {role.id: role for role in interaction.guild.roles if role.id in dropdown_role_ids}

        added = []
        removed = []

        for role_id, role in guild_roles.items():
            if role_id in selected_ids and role not in member.roles:
                await member.add_roles(role)
                added.append(role.mention)
            elif role_id not in selected_ids and role in member.roles:
                await member.remove_roles(role)
                removed.append(role.mention)

        msg = ""
        if added:
            msg += f"You aded: {', '.join(added)}\n"
        if removed:
            msg += f"You removed: {', '.join(removed)}\n"
        if not msg:
            msg = "No roles were added or removed"

        await interaction.response.send_message(msg, ephemeral=True)


class gameRoles(discord.ui.View):
    def __init__(self, roles: list[discord.Role]):
        super().__init__(timeout=None)
        self.add_item(GamesRolesDropDown(roles))

class ServerPingsDropDown(discord.ui.Select):
    def __init__(self, roles: list[discord.Role]):
        options = []
        for role in roles:
            options.append(
                discord.SelectOption(
                    label=role.name,
                    value=str(role.id)
                )
            )

        super().__init__(
            placeholder=".　　　　 Select the server pings you want",
            min_values=0,
            max_values=len(options),
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        selected_ids = set(int(v) for v in self.values)
        dropdown_role_ids = [int(opt.value) for opt in self.options]
        guild_roles = {role.id: role for role in interaction.guild.roles if role.id in dropdown_role_ids}

        added = []
        removed = []

        for role_id, role in guild_roles.items():
            if role_id in selected_ids and role not in member.roles:
                await member.add_roles(role)
                added.append(role.mention)
            elif role_id not in selected_ids and role in member.roles:
                await member.remove_roles(role)
                removed.append(role.mention)

        msg = ""
        if added:
            msg += f"You added: {', '.join(added)}\n"
        if removed:
            msg += f"You removed: {', '.join(removed)}\n"
        if not msg:
            msg = "No roles were added or removed."

        await interaction.response.send_message(msg, ephemeral=True)


class ServerPingRoles(discord.ui.View):
    def __init__(self, roles: list[discord.Role]):
        super().__init__(timeout=None)
        self.add_item(ServerPingsDropDown(roles))

class roles(commands.Cog):
    def __init__(self, bot: LalisaBot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx):
        ariana_embed = discord.Embed()
        ariana_embed.set_image(url="https://cdn.discordapp.com/attachments/1248039148888129647/1393624914522804394/Comp_9_00000.png?ex=687d1457&is=687bc2d7&hm=4aa950c88caddc8eaf3e30c977b6da95fa97b3af6cd33e1887bb3b70c0405697&")

        colours_embed = discord.Embed(description="**        ×       Name Colours     ༝ ⁺  **")
        colours_embed.add_field(name=" ", value="<:flower_red:836955512994136085><@&694018826261495839>"
            "\n<:flower_peach:836955649883635772><@&836821013043871814>"
            "\n<:flower_orange:836955588742742077><@&694018911204802571>"
            "\n<:flower_yellow:836955637086158848><@&694018962362728499>"
            "\n<:flower_lightgreen:836955686595461140><@&694019069602693191>", inline=True)
        colours_embed.add_field(name=" ", value="<:flower_green:836955698595889172><@&694019161331990579>"
            "\n<:flower_lightteal:836955718522634300><@&836821613709623296>"
            "\n<:flower_teal:836955735262625803><@&836821414283182110>"
            "\n<:flower_lightblue:836955768346902549><@&694019059624312902> "
            "\n<:flower_blue:836955781743378463><@&694019170114994248>", inline=True)
        colours_embed.add_field(name=" ", value="<:flower_lilac:836955801524109363><@&836820371788267540>"
            "\n<:flower_purple:836955820272386048><@&694019276012781658>"
            "\n<:flower_pink:836955936416595998><@&694019530711891969>"
            "\n<:flower_lightpink:836955836278243398><@&836819911065993217> "
            "\n<:flower_black:836955494689669130><@&754756697708429312>", inline=True)
        colours_embed.set_image(url="https://cdn.discordapp.com/attachments/1248039148888129647/1393627203249508373/Comp_10_00000.png?ex=687d1679&is=687bc4f9&hm=9d4554d8cef4cdb9921328a07f6efb1fafd34d5fbed30a90fe609ff492eb7d2c&")

        await ctx.send(embed=ariana_embed)

        role_ids = [
            694018826261495839, 836821013043871814, 694018911204802571, 694018962362728499, 694019069602693191,
            694019161331990579, 836821613709623296, 836821414283182110, 694019059624312902, 694019170114994248,
            836820371788267540, 694019276012781658, 694019530711891969, 836819911065993217, 754756697708429312
        ]
        roles = [ctx.guild.get_role(rid) for rid in role_ids if ctx.guild.get_role(rid)]

        await ctx.send(embed=colours_embed, view=ColourRoleView(roles))

        programs_embed = discord.Embed(description="**        ×       Editing Programs     ༝ ⁺  **")
        programs_embed.add_field(name=" ", value="<:icon_aftereffects:1358784511210422472><@&736846447491678319>"
        "\n<:icon_alightmotion:1358784733626106106><@&736846565238374420>"
        "\n<:icon_videostar:1358785021921595533><@&736846542409039916>", inline=True)
        programs_embed.add_field(name=" ", value="<:icon_cutecut:1358785336553115880><@&736846596641128478>"
        "\n<:icon_svp:1358785529889558578><@&736859413578645546>"
        "\n<:icon_funimate:1364228674798358599><@&1364228043102621716>", inline=True)
        programs_embed.set_image(url="https://cdn.discordapp.com/attachments/1248039148888129647/1393627203249508373/Comp_10_00000.png?ex=687d1679&is=687bc4f9&hm=9d4554d8cef4cdb9921328a07f6efb1fafd34d5fbed30a90fe609ff492eb7d2c&")

        role_ids = [
            736846447491678319, 736846565238374420, 736846542409039916, 736846596641128478, 736859413578645546,
            1364228043102621716
        ]
        roles = [ctx.guild.get_role(rid) for rid in role_ids if ctx.guild.get_role(rid)]

        await ctx.send(embed=programs_embed, view=ProgramRoles(roles))

        pronouns_embed = discord.Embed(description="**        ×       Pronouns & Age     ༝ ⁺  **")
        pronouns_embed.add_field(name="Pronouns:", value="<@&759783514320797726>"
        "\n<@&759783680217448478> "
        "\n<@&759783924620328972>", inline=True)
        pronouns_embed.add_field(name="<:Empty:1393634494048899072>", value="<@&784223801030082600>"
        "\n<@&784223876326228039>"
        "\n<@&838369320094007348>", inline=True)
        pronouns_embed.add_field(name="Ages:", value="<@&1271907010098495518>"
        "\n<@&1271907025579937832>", inline=True)
        pronouns_embed.set_image(url="https://cdn.discordapp.com/attachments/1248039148888129647/1393627203249508373/Comp_10_00000.png?ex=687d1679&is=687bc4f9&hm=9d4554d8cef4cdb9921328a07f6efb1fafd34d5fbed30a90fe609ff492eb7d2c&")

        role_ids = [
            759783514320797726, 759783680217448478, 759783924620328972, 784223801030082600, 784223876326228039,
            838369320094007348, 1271907010098495518, 1271907025579937832
        ]
        roles = [ctx.guild.get_role(rid) for rid in role_ids if ctx.guild.get_role(rid)]

        await ctx.send(embed=pronouns_embed, view=PronounsRoles(roles))

        pings_embed = discord.Embed(description="**        ×       Server Pings     ༝ ⁺  **")
        pings_embed.add_field(name=" ", value="<@&839861270147498034> "
        "\n<@&839861195284283465> "
        "\n<@&1015997553524883496> "
        "\n<@&1080275631830470696> "
        "\n<@&803626435154804766>", inline=True)
        pings_embed.add_field(name=" ", value="<@&1271908619696340993> "
        "\n<@&1312389423807332463> "
        "\n<@&1350946646841626635> "
        "\n<@&1352451309822804098>", inline=True)
        pings_embed.set_image(url="https://cdn.discordapp.com/attachments/1248039148888129647/1393627203249508373/Comp_10_00000.png?ex=687d1679&is=687bc4f9&hm=9d4554d8cef4cdb9921328a07f6efb1fafd34d5fbed30a90fe609ff492eb7d2c&")

        role_ids = [
            839861270147498034, 839861195284283465, 1015997553524883496, 1080275631830470696, 803626435154804766,
            1271908619696340993, 1312389423807332463, 1350946646841626635, 1352451309822804098
        ]
        roles = [ctx.guild.get_role(rid) for rid in role_ids if ctx.guild.get_role(rid)]

        await ctx.send(embed=pings_embed, view=ServerPingRoles(roles))

        games_embed = discord.Embed(description="**        ×       Favourite Games     ༝ ⁺  **")
        games_embed.add_field(name=" ", value="<:game_WutheringWaves:1334957321096269919><@&1334956809445970055>"
        "\n<:game_HonkaiStarRail:1334957545424556062><@&1285680260955770910>"
        "\n<:game_GenshinImpact:1334957721161695273><@&836939480215846932>"
        "\n<:game_ZenlessZoneZero:1334957918382067785><@&1285679969627803739>"
        "\n<:game_DuetNightAbyss:1431984077497434123><@&1431984148880424970>", inline=True)
        games_embed.add_field(name=" ", value="<:game_ProjectSekai:1380146074156793976><@&1295758757506060348>"
        "\n<:game_minecraft:838325085679910913><@&740236368931979377>"
        "\n<:game_roblox:838324839781236748><@&838323307765170236>"
        "\n<:game_valorant:838325478384205834><@&838323263041175572>"
        "\n<:game_vbucks:1285692390652510309><@&1285692240169013350>", inline=True)
        games_embed.add_field(name=" ", value="<:icon_discord:1358790160799502608><@&1310217573262163978>", inline=True)
        games_embed.set_image(url="https://cdn.discordapp.com/attachments/1248039148888129647/1393627203249508373/Comp_10_00000.png?ex=687d1679&is=687bc4f9&hm=9d4554d8cef4cdb9921328a07f6efb1fafd34d5fbed30a90fe609ff492eb7d2c&")
        role_ids = [
            1334956809445970055, 1285680260955770910, 836939480215846932, 1285679969627803739, 1431984148880424970,
            1295758757506060348, 740236368931979377, 838323307765170236, 838323263041175572, 1285692240169013350,
            1310217573262163978
        ]
        roles = [ctx.guild.get_role(rid) for rid in role_ids if ctx.guild.get_role(rid)]
        await ctx.send(embed=games_embed, view=gameRoles(roles))

async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(roles(bot))

# Message from Joshua: I love my Reece. He is the most beautiful most sexy man I have ever met. I love him, my dear favourite boy