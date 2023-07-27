import asyncio
import discord
from discord.ext import commands

class Player:
    def __init__(self, member, symbol):
        self.member = member
        self.symbol = symbol

    @property
    def mention(self):
        return self.member.mention

class TicTacToe(commands.Cog):
    def __init__(self, bot, player_o, player_x):
        self.bot = bot
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

class TicTacToeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    def print_board(self, board):
        line = "-------------"
        board_str = f"\n{line}"
        for i in range(0, 9, 3):
            board_str += f"\n| {' | '.join(board[i:i+3])} |"
            board_str += f"\n{line}"
        return board_str

    async def display_board(self, ctx, board):
        message = "**Tic Tac Toe**\n" + self.print_board(board)
        return await ctx.send(message)

    @commands.command(name='tictactoe', aliases=['ttt'])
    async def tictactoe(self, ctx: commands.Context, player2: discord.Member):
        if player2 == ctx.author:
            return await ctx.reply("You can't play against yourself.")

        player_1 = Player(ctx.author, "⭕")
        player_2 = Player(player2, "❌")
        current_player = player_1
        board = ["⬜" for _ in range(9)]

        message = await self.display_board(ctx, board)

        for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return (
                user == current_player.member
                and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
                and reaction.message.id == message.id
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                await message.edit(content="The game has timed out!")
                return

            position = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"].index(str(reaction.emoji))

            if board[position] == "⬜":
                board[position] = current_player.symbol
                await reaction.remove(user)
                await self.update_game(ctx, message, board)

                if self.check_winner(board):
                    return await ctx.send(f"{current_player.mention} wins the game!")
                elif "⬜" not in board:
                    return await ctx.send("It's a tie!")

                current_player = player_1 if current_player == player_2 else player_2

    def check_winner(self, board):
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for pattern in win_patterns:
            if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != "⬜":
                return True
        return False

    async def update_game(self, ctx, message, board):
        embed = discord.Embed(title="Tic-Tac-Toe", description=self.print_board(board), color=0x2ECC71)
        await message.edit(embed=embed)

    @tictactoe.error
    async def tictactoe_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid opponent. Please mention a valid user.")
        
async def setup(bot):
    await bot.add_cog(TicTacToe(bot))