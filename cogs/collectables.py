import json
import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.unlocked_items = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.unlocked_items = {}

    @commands.command(aliases=['crate', 'crates'])
    async def opencrate(self, ctx):
        guild_id = 1121841073673736215
        member = ctx.author

        if ctx.guild.id != guild_id:
            await ctx.reply("This command can only be used in the specified server.")
            return

        unlock_levels = {
            "common": {
                "message": "Hey! You found a **COMMON** item! Here's a cool badge to add to your collection :",
                "xp": 0,
                "emojis": ["<:y_kissy:1126153163901255710>", "<:pr_whatthefuck1:1126153390393655408>", "<:cuteface:1126153241235820574>", "<:brown4:1126153489370861618>", "<:baldpeppa:1126153356323344464>",
                           "<:Cherry_Blossom:1126153286022594571>", "<:BARKKK:1126153208805458083>", "<:855647520058114078:1126153445582323913>"]  
            },
            "uncommon": {
                "message": "Hey! You found an **UNCOMMON** item! Here's a cool badge to add to your collection :",
                "xp": 0,
                "emojis": ["<:brazy_milksip:1126154944404279336>", "<:silly:1126154885050683484>", "<:Lumi_purple_star:1126154848346325082>", "<:evilmilkbear:1126154798257938553>", 
                           "<:teddy2:1126154757967462411>", "<:5106_Sakurahana:1126154666472898662>", "<:9115_HotLove:1126154597354979388>", "<:868918555939315773:1126154516497170493>"]  
            },
            "rare": {
                "message": "Hey! You found a **RARE** item! You found **500 XP** and an badge to add to your collection :",
                "xp": 500,
                "emojis": ["<:chimmy:1126187703243911278>", "<:frogyay:1126187746520731668>", "<:cooky:1126187789965340752>", "<:koya:1126187845271429260>", "<:mang:1126187898652332102>",
                           "<:shooky:1126187943061622886>", "<:rj:1126187982819446825>", "<:tata:1126188044098220134>"]  
            },
            "epic": {
                "message": "Hey! You found an **EPIC** item! You found **1000 XP** and an badge to add to your collection :",
                "xp": 1000,
                "emojis": ["<a:Lumi_penguinfall:1126190036627496970>", "<a:Spongebob:1126189963269124156>", "<a:cinnamorollhappylollipop:1126189918713028709>", "<a:GARY:1126189877952778340>", 
                           "<a:9440bugcatb2:1126189832725598309>", "<a:bun:1126189794196717588>", "<a:bearhugz:1126189744922050702>", "<a:cred:1126189703423602860>", "<a:abounce:1126190811554525346>",
                           "<a:abounce:1126189618824499271>", "<a:btstaekook:1126189565472948384>", "<a:btscooky:1126191193584312350>", "<a:btschimmy:1126189488419381371>", "<a:btsrj:1126189228242509876>",
                           "<a:btsshooky:1126189405044998244>", "<a:cpurple:1126189354411380906>", "<a:btskoyashooky:1126189313311391855>", "<a:p:1126189265383079966>", "<a:btsrj:1126189447021604916>", 
                           "<a:btstata:1126189188635701248>", "<a:btskoya:1126189143957975051>", "<a:btsmang:1126189090635776041>", "<a:koyalove:1126189052622798869>"]  
            },
            "legendary": {
                "message": "Hey! You found a <a:Lumi_star_spin:1126224020052910200> **LEGENDARY** item! You found **2000 XP** and a legendary Kanzen logo! Also here's an badge to add to your collection :",
                "xp": 2000,
                "emojis": ["e<a:811648167112212491:837044274868387862>", "<a:blobHYPERS:1076908032803479632>", "<a:miaumiau:1079242555310489610>", "<a:jeb:736589028991959090>", "<a:bunnygirl:1126202805833695242>",
                           "<a:blobcatdance:1101809422147268678>", "<a:blobparty:869277338779648100>", "<a:taesip:1126193847278510101>", "<:boobs:1126193765762203770><:boobs:1126197577189179462>", "<:hobi:1126193730538459287>", 
                           "<:lemmelick:1126193693804732456>", "<:jkfire:1126193638817411145>", "<a:yoonji:901535511116664852>", "<a:jungshook:1126193560966930462>", "<a:9514momotorture:1126193520487702588>", "<a:2109hyunjinwhat:1126193481648439417>", 
                           "<a:1406kpopsip:1126193443589333043>", "<a:9518sponjdance:1126193406117429248>", "<a:013ilysm:1126193366288318618>", "<a:000_chuufight:1126193332465447033>", "<a:2x_nom:1126193300819431524>", "<a:CHUUKISS:1126193261829165076>", "<a:catcat:1126193159664316416>"]  
            }
        }

        unlock_level = random.choices(
            ["common", "uncommon", "rare", "epic", "legendary"],
            weights=[40, 30, 15, 10, 5],
            k=1
        )[0]
        unlock_data = unlock_levels[unlock_level]

        if unlock_level in ["rare", "epic", "legendary"]:
            xp = unlock_data["xp"]
            xp_message = unlock_data["message"]
            unlock_channel_id = 1125999933149949982  # ID of the unlock channel
            unlock_channel = self.bot.get_channel(unlock_channel_id)
            await unlock_channel.send(f"{member.mention} has found {xp} XP!")

            if unlock_level == "legendary":
                logos = ['https://mega.nz/file/2R0nBCYT#itQpn374M_BMNKHIeLub0iOk2Z-YZfPe36OrcgMoadc',
                         'https://mega.nz/file/DdEglTgb#oaP2yiLhBrBn1PHaVeJyQEOaUChWKleIXC_lhEuE460',
                         'https://mega.nz/file/Xc8mAArA#NpaPbCZDqgPQlzUt0Tfz-za3WSaXibHmhNgpxc_lyC8']
                logolinks = random.choice(logos)
                embed = discord.Embed(
                    title="Legendary Unlock",
                    description=f"You have unlocked a legendary logo! please don't share the link with anyone else\n[click here]({logolinks})",
                    color=discord.Color.gold()
                )
                await member.send(embed=embed)
                await unlock_channel.send(f"{member.mention} has unlocked 2000 XP!")

        else:
            xp_message = unlock_data["message"]

        emoji = random.choice(unlock_data["emojis"])

        # Check if the member has already unlocked the current rarity
        if member.id in self.unlocked_items:
            unlocked_rarities = [item['rarity'] for item in self.unlocked_items[member.id]]
            if unlock_level in unlocked_rarities:
                # Rarity already unlocked, append emoji to the existing rarity entry
                for item in self.unlocked_items[member.id]:
                    if item['rarity'] == unlock_level:
                        item['emoji'] += f" {emoji}"
                        break
            else:
                # Rarity not unlocked yet, create a new entry
                self.unlocked_items[member.id].append({'rarity': unlock_level, 'emoji': emoji})
        else:
            # First unlocked item for the member, create a new entry
            self.unlocked_items[member.id] = [{'rarity': unlock_level, 'emoji': emoji}]

        await ctx.reply(f"{xp_message} {emoji}")

    @commands.command(aliases=['unlocks', 'badges', 'cratesunlocked'])
    async def unlocked(self, ctx):
        guild_id = 1121841073673736215
        member = ctx.author

        if ctx.guild.id != guild_id:
            await ctx.reply("This command can only be used in the specified server.")
            return

        unlocked_items = self.unlocked_items.get(member.id, [])

        if unlocked_items:
            embed = discord.Embed(title="Unlocked Items", color=0x2b2d31)
            for item in unlocked_items:
                rarity = item['rarity'].capitalize()
                emoji = item['emoji']
                embed.add_field(name=rarity, value=emoji, inline=False)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply(f"You have not unlocked any items yet.")

    @commands.command(aliases=['resetcrates', 'rc'])
    async def resetunlocks(self, ctx, member: discord.Member = None):
        guild_id = 1121841073673736215

        if ctx.guild.id != guild_id:
            await ctx.reply("This command can only be used in the specified server.")
            return

        member = member or ctx.author

        if member.id in self.unlocked_items:
            del self.unlocked_items[member.id]
            await ctx.send(f"Unlocked items for {member.mention} have been reset.")
        else:
            await ctx.reply(f"{member.mention} does not have any unlocked items.")


async def setup(bot):
    await bot.add_cog(Unlock(bot))
