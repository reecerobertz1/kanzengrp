import asyncio
import math
import random
import discord
from discord.ext import commands
from discord.ui import View, Button
from typing import List
from discord import app_commands

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int, player1, player2):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
        self.player1 = player1
        self.player2 = player2

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.player_1:
            if interaction.user == view.player_1:
                self.style = discord.ButtonStyle.blurple
                self.label = 'X'
                self.disabled = True
                view.board[self.y][self.x] = view.X
                view.current_player = view.player_2
                content = f"<:o_:1087132605876555807> It's {self.player2.mention}'s turn"
            else:
                return await interaction.response.send_message('Not your turn!', ephemeral=True)
        else:
            if interaction.user == view.player_2:
                self.style = discord.ButtonStyle.red
                self.label = 'O'
                self.disabled = True
                view.board[self.y][self.x] = view.O
                view.current_player = view.player_1
                content = f"<:x_:1087132262400794644> It's {self.player1.mention}'s turn"
            else:
                return await interaction.response.send_message('Not your turn!', ephemeral=True)

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f'{self.player1.mention} won!'
            elif winner == view.O:
                content = f'{self.player2.mention} won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)

class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, player1, player2):
        super().__init__()
        self.current_player = self.X
        self.player_1 = player1
        self.player_2 = player2
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y, player1, player2))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X
        
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

class Player:
    def __init__(self, member):
        self.member = member
        self.hp = 100
        self.defense = 0

class BattleView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Attack")
    async def attack_button(self, button: discord.Button, interaction: discord.Interaction):
        self.value = "attack"
        self.stop()

    @discord.ui.button(label="Defend")
    async def defend_button(self, button: discord.Button, interaction: discord.Interaction):
        self.value = "defend"
        self.stop()

    @discord.ui.button(label="Escape", style=discord.ButtonStyle.danger)
    async def escape_button(self, button: discord.Button, interaction: discord.Interaction):
        self.value = "escape"
        self.stop()

class Games(commands.Cog):
    """Play some games with Hoshi or other members"""
    def __init__(self, bot):
        self.bot = bot
        self.occupied = []
        self.emoji="<:van:1148235344437846107>"

    async def attack(self, player):
        damage = int((math.pow(random.randrange(30, 95), 1.35) / 10)
                     * 1 - player.defense / 100)
        player.hp -= damage
        return damage

    async def defend(self, player):
        player.defense += 5
        heal = random.randrange(20, 38)
        player.hp += heal
        if player.hp > 115:
            player.hp = 115
            heal = 0
        if player.defense > 45:
            player.defense = 45
            return heal, True
        return heal, False

    async def turn(self, ctx, p1, p2):
        view = BattleView()
        await ctx.send(f"{p1.member.mention} **choose a move**:", view=view)

        try:
            await view.wait()
            choice = view.value

            if choice == "defend":
                healAmount, defenseMaxed = await self.defend(p1)
                if defenseMaxed:
                    await ctx.reply(f"You healed for `{healAmount}`, but your defense is maxed out")
                else:
                    await ctx.reply(f"You healed for `{healAmount}`, and your defense rose by `5`")
            elif choice == "attack":
                damage = await self.attack(p2)
                await ctx.reply(f"You attacked dealing **{damage}** damage")
            elif choice == "escape":
                await ctx.send(f"{p1.member.name} tried escaping. **tried**")
                await ctx.send(embed=discord.Embed(title="CRITICAL HIT", description="9999 Damage!",
                                                   colour=0x2b2d31))
                p1.hp = -9999

        except asyncio.TimeoutError:
            await ctx.send(f"`{p2.member.name}` got tired of waiting and bonked `{p1.member.name}` on the head.")
            await ctx.send(embed=discord.Embed(title="CRITICAL HIT", description="9999 Damage!",
                                               colour=0x2b2d31))
            p1.hp = -9999

        await ctx.send(embed=discord.Embed(title="Stats", description=f" {p1.member.mention}\n**HP:** `{p1.hp}`\n**Defense**: `{p1.defense}`\n \n {p2.member.mention}\n**HP**: `{p2.hp}`\n**Defense**: `{p2.defense}`", color=0x2b2d31))

    @commands.hybrid_command(description="Fight other members to the death", extras="+fight @member : alias +battle")
    async def fight(self, ctx, opponent: discord.Member):
        if ctx.channel.id in self.occupied:
            await ctx.reply("This battlefield is occupied")
            return
        else:
            self.occupied.append(ctx.channel.id)
        if opponent == ctx.message.author:
            await ctx.send(f"{ctx.author.mention} hurt itself in its confusion")
            self.occupied.remove(ctx.channel.id)
            return
        if opponent.bot:
            await ctx.reply(f"You try fighting the robot.\n\n*pieces of you can be found cut up on the battlefield*")
            self.occupied.remove(ctx.channel.id)
            return
        if opponent is None:
            await ctx.reply("You need to mention someone else to battle!")
            return
        if (random.randrange(0, 2)) == 0:
            p1 = Player(ctx.message.author)
            p2 = Player(opponent)
        else:
            p1 = Player(opponent)
            p2 = Player(ctx.message.author)
        await ctx.send(embed=discord.Embed(title="Battle",
                                           description=f"""{ctx.author.mention} is challenging {opponent.mention}!
        let the games begin.""", color=0x2b2d31))
        toggle = True
        while p1.hp >= 0 and p2.hp >= 0:
            if toggle:
                await self.turn(ctx, p1, p2)
                toggle = False
            else:
                await self.turn(ctx, p2, p1)
                toggle = True

        self.occupied.remove(ctx.channel.id)
        if p1.hp > 0:
            winner = p1
            loser = p2
        else:
            winner = p2
            loser = p1
        case = random.randrange(0, 6)
        if case == 0:
            await ctx.send(f"{winner.member.mention} is having human meat for dinner tonight.")
        if case == 1:
            await ctx.send(f"{winner.member.mention} is dancing on `{loser.member.name}`'s corpse.")
        if case == 2:
            await ctx.send(f"{winner.member.mention} did some good stabbing.")
        if case == 3:
            await ctx.send(f"{winner.member.mention} Is victorious!")
        if case == 4:
            await ctx.send(f'{winner.member.mention} really just did a fortnite dance after winning... embarrassing <a:fortnitekid12:1132210068847329322>')
        if case == 5:
            await ctx.send(f'{loser.member.mention} will get their revenge on {winner.member.mention} soon...\n{winner.member.mention} better sleep with one eye open')
        if case == 6:
            await ctx.send(f'RIP {loser.member.mention} you will not be missed....  because {winner.member.mention} has won the battle')

    @app_commands.command(description="Starts a tic-tac-toe game with another member.", extras="+tictactoe @member : alias +ttt")
    async def tictactoe(self, interaction: discord.Interaction, member: discord.Member):
        member = member

        if member == None:
            await interaction.response.send_message("You need to mention someone before playing.", ephemeral=True)
            return

        player1 = interaction.user
        player2 = member

        if player2.bot:
            await interaction.response.send_message("You cannot play with a bot.", ephemeral=True)
            return

        embed = discord.Embed(title="🎮 TicTacToe Game", description=f"{player1.mention} vs {player2.mention}", color=0x2b2d31)
        message = await interaction.response.send_message(embed=embed, view=TicTacToe(player1, player2))

async def setup(bot):
    await bot.add_cog(Games(bot))