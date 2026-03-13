import discord
from discord.ext import commands
from bot import LalisaBot
from typing import List, Optional, Set

ALL_ROLE_IDS: Set[int] = set()

class RoleSelect(discord.ui.Select):
    def __init__(self, roles: List[discord.Role], emoji_map: Optional[List[str]] = None):
        self.roles = roles
        options = []

        for i, role in enumerate(roles):
            label = role.name
            emoji = None

            if emoji_map and i < len(emoji_map):
                emoji_str = emoji_map[i]
                emoji = discord.PartialEmoji.from_str(emoji_str)

            options.append(
                discord.SelectOption(
                    label=label,
                    value=str(role.id),
                    emoji=emoji
                )
            )

        super().__init__(
            placeholder="Click here to select your roles!",
            options=options,
            max_values=len(roles),
            min_values=0
        )

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        selected_ids = set(int(v) for v in self.values)

        added = []
        removed = []

        for role in self.roles:

            if role.id in selected_ids:
                if role not in member.roles:
                    await member.add_roles(role)
                    added.append(role.mention)

            else:
                if role in member.roles:
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


class PronounsAges(discord.ui.View):
    def __init__(self, roles: List[discord.Role]):
        super().__init__(timeout=None)
        self.roles = roles
        self.add_item(RoleSelect(roles))
        ALL_ROLE_IDS.update(r.id for r in roles)


class ServerPings(discord.ui.View):
    def __init__(self, roles: List[discord.Role]):
        super().__init__(timeout=None)
        self.roles = roles
        self.add_item(RoleSelect(roles))
        ALL_ROLE_IDS.update(r.id for r in roles)


class ProgramsRoles(discord.ui.View):
    def __init__(self, roles: List[discord.Role]):
        super().__init__(timeout=None)

        emoji_map = [
            "<:icon_aftereffects:1464997718844903486>",
            "<:icon_alightmotion:1464997732081995941>",
            "<:icon_videostar:1464997794702950537>",
            "<:icon_funimate:1464997770652946489>",
            "<:icon_svp:1464997783210561557>",
            "<:icon_cutecut:1464997744866234608>"
        ]

        self.add_item(RoleSelect(roles, emoji_map))
        ALL_ROLE_IDS.update(r.id for r in roles)


class GameRoles(discord.ui.View):
    def __init__(self, roles: List[discord.Role]):
        super().__init__(timeout=None)

        emoji_map = [
            "<:game_WutheringWaves:1464997546102358141>",
            "<:game_HonkaiStarRail:1464997514976559258>",
            "<:game_GenshinImpact:1464997488489402430>",
            "<:game_ZenlessZoneZero:1464997562355286229>",
            "<:game_ProjectSekai:1464997530038304778>",
            "<:game_minecraft:1464997578134388889>",
            "<:game_roblox:1464997591078141994>",
            "<:game_fortnite:1467223921345564734>",
            "<:game_valorant:1464997606781620326>"
        ]

        self.add_item(RoleSelect(roles, emoji_map))
        ALL_ROLE_IDS.update(r.id for r in roles)


class cgproles(commands.Cog):
    def __init__(self, bot: LalisaBot):
        self.bot = bot

    @commands.command()
    async def cgproles(self, ctx):

        banner_embed = discord.Embed()
        banner_embed.set_image(
            url="https://cdn.discordapp.com/attachments/1477651776139427872/1482102173021114480/iDENTITY.png"
        )

        pronouns_ages = discord.Embed(
            description="**        †       Pronouns & Age Roles     ༝ ⁺  **"
        )

        pronouns_ages.add_field(
            name="Pronouns",
            value="<@&1462501883229765757>\n"
                  "<@&1462501904084111581>\n"
                  "<@&1462501928218132571>",
            inline=True
        )

        pronouns_ages.add_field(
            name="<:Empty:1467219995191935192>",
            value="<@&1462501948791193884>\n"
                  "<@&1462501965765410847>\n"
                  "<@&1462501984874795070>",
            inline=True
        )

        pronouns_ages.add_field(
            name="Age Roles",
            value="<@&1464983054861733918>\n"
                  "<@&1464983147690065961>",
            inline=True
        )

        pronouns_ages.set_image(
            url="https://cdn.discordapp.com/attachments/1477651776139427872/1477661228955467889/Comp_2_00000.png"
        )

        await ctx.send(embed=banner_embed)

        first_role_ids = [
            1462501883229765757,
            1462501904084111581,
            1462501928218132571,
            1462501948791193884,
            1462501965765410847,
            1462501984874795070,
            1464983054861733918,
            1464983147690065961
        ]

        first_roles = [
            ctx.guild.get_role(rid)
            for rid in first_role_ids
            if ctx.guild.get_role(rid)
        ]

        await ctx.send(
            embed=pronouns_ages,
            view=PronounsAges(first_roles)
        )

        serverping = discord.Embed(
            description="**        †       Server Pings     ༝ ⁺  **"
        )

        serverping.add_field(
            name=" ",
            value="<@&1462502104571707412>\n"
                  "<@&1467224887578853480>\n"
                  "<@&1462502119818006528>",
            inline=True
        )

        serverping.add_field(
            name=" ",
            value="<@&1462502166358130740>\n"
                  "<@&1462502777220759604>\n"
                  "<@&1472040865173209168>",
            inline=True
        )

        serverping.set_image(
            url="https://cdn.discordapp.com/attachments/1477651776139427872/1477661228955467889/Comp_2_00000.png"
        )

        second_role_ids = [
            1462502104571707412,
            1467224887578853480,
            1462502119818006528,
            1462502166358130740,
            1462502777220759604,
            1472040865173209168
        ]

        second_roles = [
            ctx.guild.get_role(rid)
            for rid in second_role_ids
            if ctx.guild.get_role(rid)
        ]

        await ctx.send(
            embed=serverping,
            view=ServerPings(second_roles)
        )

        programs = discord.Embed(
            description="**        †       Editing Programs     ༝ ⁺  **"
        )

        programs.add_field(
            name=" ",
            value="<:icon_aftereffects:1464997718844903486> <@&1462502534819221682>\n"
                  "<:icon_alightmotion:1464997732081995941> <@&1462502556260368384>\n"
                  "<:icon_videostar:1464997794702950537> <@&1462502586451099751>",
            inline=True
        )

        programs.add_field(
            name=" ",
            value="<:icon_funimate:1464997770652946489> <@&1462502609641275584>\n"
                  "<:icon_svp:1464997783210561557> <@&1462502625307005002>\n"
                  "<:icon_cutecut:1464997744866234608> <@&1462502627785965781>",
            inline=True
        )

        programs.set_image(
            url="https://cdn.discordapp.com/attachments/1477651776139427872/1477661228955467889/Comp_2_00000.png"
        )

        third_roles_ids = [
            1462502534819221682,
            1462502556260368384,
            1462502586451099751,
            1462502609641275584,
            1462502625307005002,
            1462502627785965781
        ]

        third_roles = [
            ctx.guild.get_role(rid)
            for rid in third_roles_ids
            if ctx.guild.get_role(rid)
        ]

        await ctx.send(
            embed=programs,
            view=ProgramsRoles(third_roles)
        )

        games = discord.Embed(
            description="**        †       Favorite Games     ༝ ⁺  **"
        )

        games.add_field(
            name=" ",
            value="<:game_WutheringWaves:1464997546102358141> <@&1464985323950964933>\n"
                  "<:game_HonkaiStarRail:1464997514976559258> <@&1464985619821367331>\n"
                  "<:game_GenshinImpact:1464997488489402430> <@&1464985380792041627>\n"
                  "<:game_ZenlessZoneZero:1464997562355286229> <@&1464985735487557868>\n"
                  "<:game_ProjectSekai:1464997530038304778> <@&1464985929033846917>",
            inline=True
        )

        games.add_field(
            name=" ",
            value="<:game_minecraft:1464997578134388889> <@&1464986007744282748>\n"
                  "<:game_roblox:1464997591078141994> <@&1464986056930623689>\n"
                  "<:game_fortnite:1467223921345564734> <@&1464985449947729960>\n"
                  "<:game_valorant:1464997606781620326> <@&1464986105165381716>",
            inline=True
        )

        games.set_image(
            url="https://cdn.discordapp.com/attachments/1477651776139427872/1477661228955467889/Comp_2_00000.png"
        )

        fourth_roles_ids = [
            1464985323950964933,
            1464985619821367331,
            1464985380792041627,
            1464985735487557868,
            1464985929033846917,
            1464986007744282748,
            1464986056930623689,
            1464985449947729960,
            1464986105165381716
        ]

        fourth_roles = [
            ctx.guild.get_role(rid)
            for rid in fourth_roles_ids
            if ctx.guild.get_role(rid)
        ]

        await ctx.send(
            embed=games,
            view=GameRoles(fourth_roles)
        )


async def setup(bot: LalisaBot) -> None:
    await bot.add_cog(cgproles(bot))