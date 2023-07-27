import discord
from discord.ext import commands
from discord.ui import Button, ButtonStyle, View

class TicTacToeGame:
    def __init__(self, ctx, player_o, player_x):
        self.ctx = ctx
        self.player_o = player_o
        self.player_x = player_x
        self.board = ["⬜" for _ in range(9)]
        self.current_player = player_o
        self.opponent_player = player_x
        self.game_over = False

    def print_board(self):
        line = "-------------"
        board_str = f"\n{line}"
        for i in range(0, 9, 3):
            board_str += f"\n| {' | '.join(self.board[i:i+3])} |"
            board_str += f"\n{line}"
        return board_str

    def make_move(self, position):
        if not self.game_over and self.board[position] == "⬜":
            self.board[position] = self.current_player.symbol
            if self.check_winner():
                self.game_over = True
                return f"{self.current_player.mention} wins the game!"
            elif "⬜" not in self.board:
                self.game_over = True
                return "It's a tie!"
            self.current_player, self.opponent_player = self.opponent_player, self.current_player
        return None

    def check_winner(self):
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for pattern in win_patterns:
            if self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] != "⬜":
                return True
        return False

class Player:
    def __init__(self, member, symbol):
        self.member = member
        self.symbol = symbol

    @property
    def mention(self):
        return self.member.mention

class TicTacToeView(View):
    def __init__(self, game):
        super().__init__(timeout=None)
        self.game = game

    async def on_timeout(self):
        self.stop()
        await self.message.edit(content="The game has timed out!")

    @Button(style=ButtonStyle.grey, label="1", custom_id="1")
    async def button_1(self, button, interaction):
        await self.on_button_click(0)

    @Button(style=ButtonStyle.grey, label="2", custom_id="2")
    async def button_2(self, button, interaction):
        await self.on_button_click(1)

    @Button(style=ButtonStyle.grey, label="3", custom_id="3")
    async def button_3(self, button, interaction):
        await self.on_button_click(2)

    @Button(style=ButtonStyle.grey, label="4", custom_id="4")
    async def button_4(self, button, interaction):
        await self.on_button_click(3)

    @Button(style=ButtonStyle.grey, label="5", custom_id="5")
    async def button_5(self, button, interaction):
        await self.on_button_click(4)

    @Button(style=ButtonStyle.grey, label="6", custom_id="6")
    async def button_6(self, button, interaction):
        await self.on_button_click(5)

    @Button(style=ButtonStyle.grey, label="7", custom_id="7")
    async def button_7(self, button, interaction):
        await self.on_button_click(6)

    @Button(style=ButtonStyle.grey, label="8", custom_id="8")
    async def button_8(self, button, interaction):
        await self.on_button_click(7)

    @Button(style=ButtonStyle.grey, label="9", custom_id="9")
    async def button_9(self, button, interaction):
        await self.on_button_click(8)

    async def on_button_click(self, position):
        result = self.game.make_move(position)

        if result is not None:
            self.stop()
            embed = discord.Embed(title="Tic-Tac-Toe", description=f"{self.game.print_board()}\n{result}", color=0x2b2d31)
            await self.message.edit(content=None, embed=embed, view=None)
            return

        embed = discord.Embed(title="Tic-Tac-Toe", description=f"{self.game.print_board()}", color=0x2ECC71)
        await self.message.edit(content=None, embed=embed)

class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tictactoe')
    async def tictactoe(self, ctx, opponent: discord.Member):
        if opponent == ctx.author:
            await ctx.send("You cannot play against yourself!")
            return

        if ctx.guild is None:
            await ctx.send("This command can only be used in a server!")
            return

        game = TicTacToeGame(ctx, Player(ctx.author, "⭕"), Player(opponent, "❌"))

        embed = discord.Embed(title="Tic-Tac-Toe", description=f"{game.print_board()}", color=0x2ECC71)
        message = await ctx.send(embed=embed, view=TicTacToeView(game))
        
async def setup(bot):
    await bot.add_cog(TicTacToe(bot))