import asyncio
import discord
from discord.ext import commands

class TicTacToe:
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

class TicTacToeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def display_board(self, ctx, board):
        line = "-------------"
        board_str = f"\n{line}"
        for i in range(0, 9, 3):
            board_str += f"\n| {' | '.join(board[i:i+3])} |"
            board_str += f"\n{line}"
        return await ctx.send(board_str)

    @commands.command(aliases=['ttt'])
    async def tictactoe(self, ctx: commands.Context, opponent: discord.Member):
        if opponent == ctx.author:
            await ctx.send("You cannot play against yourself!")
            return

        if ctx.guild is None:
            await ctx.send("This command can only be used in a server!")
            return

        player_o = Player(ctx.author, "⭕")
        player_x = Player(opponent, "❌")

        game = TicTacToe(ctx, player_o, player_x)

        embed = discord.Embed(title="Tic-Tac-Toe", description=f"{game.print_board()}", color=0x2ECC71)
        message = await ctx.send(embed=embed)

        for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return (
                user == game.current_player.member
                and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
                and reaction.message.id == message.id
            )

        def check_board_full(board):
            return "⬜" not in board

        async def update_game():
            if game.check_winner():
                await message.clear_reactions()
                embed = discord.Embed(title="Tic-Tac-Toe", description=f"{await self.display_board(ctx, game.board)}\n{game.current_player.mention} wins the game!", color=0x2b2d31)
                return await ctx.send(embed=embed)

            if check_board_full(game.board):
                await message.clear_reactions()
                return await ctx.send("It's a tie!")

            game.current_player, game.opponent_player = game.opponent_player, game.current_player
            await message.edit(content=None)
            await self.display_board(ctx, game.board)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id == self.message.id and self.check(reaction, user):
            position = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"].index(str(reaction.emoji))
            if self.game.board[position] == "⬜":
                self.game.board[position] = self.game.current_player.symbol
                await reaction.remove(user)
                await self.update_game()
        
async def setup(bot):
    await bot.add_cog(TicTacToe(bot))