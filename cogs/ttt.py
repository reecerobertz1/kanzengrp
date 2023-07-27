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
    def __init__(self, bot):
        self.bot = bot

    def print_board(self, board):
        line = "-------------"
        board_str = f"\n{line}"
        for i in range(0, 9, 3):
            board_str += f"\n| {' | '.join(board[i:i+3])} |"
            board_str += f"\n{line}"
        return board_str

    async def display_board(self, ctx, board, current_player):
        embed = discord.Embed(title="Tic-Tac-Toe", description=self.print_board(board), color=0x2ECC71)
        embed.add_field(name="Current Turn", value=current_player.mention, inline=False)
        message = await ctx.reply(embed=embed)
        return message

    @commands.command(name='tictactoe', aliases=['ttt'])
    async def tictactoe(self, ctx: commands.Context, player2: discord.Member):
        if player2 == ctx.author:
            return await ctx.reply("You can't play against yourself.")

        player_1 = Player(ctx.author, "⭕")
        player_2 = Player(player2, "❌")
        current_player = player_1
        board = ["⬜" for _ in range(9)]

        message = await self.display_board(ctx, board, current_player)

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

                if self.check_winner(board):
                    return await ctx.send(f"{current_player.mention} wins the game!")
                elif "⬜" not in board:
                    return await ctx.send("It's a tie!")

                current_player = player_1 if current_player == player_2 else player_2
                await self.display_board(ctx, board, current_player)

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

    @tictactoe.error
    async def tictactoe_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid opponent. Please mention a valid user.")
        
async def setup(bot):
    await bot.add_cog(TicTacToe(bot))