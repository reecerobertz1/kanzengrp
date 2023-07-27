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

    def check_winner(self, board, symbol):
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for pattern in win_patterns:
            if all(board[i] == symbol for i in pattern):
                return True
        return False

    async def get_player_reaction(self, ctx, player, message):
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                check=lambda reaction, user: user == player.member and reaction.message == message and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"],
                timeout=30.0,
            )
            return str(reaction.emoji)
        except asyncio.TimeoutError:
            return None

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
            return await ctx.reply("You cannot play against yourself!")

        if ctx.guild is None:
            return await ctx.send("This command can only be used in a server!")

        player_o = Player(ctx.author, "⭕")
        player_x = Player(opponent, "❌")
        current_player = player_o
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

        while "⬜" in board:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                await message.edit(content="The game has timed out!")
                return

            position = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"].index(str(reaction.emoji))
            if board[position] == "⬜":
                board[position] = current_player.symbol

                if self.check_winner(board, current_player.symbol):
                    await message.clear_reactions()
                    embed = discord.Embed(title="Tic-Tac-Toe", description=f"{self.display_board(ctx, board)}\n{current_player.mention} wins the game!", color=0x2b2d31)
                    return await ctx.send(embed=embed)

                current_player = player_o if current_player == player_x else player_x
                await reaction.remove(user)
                await message.edit(content=None)
                await self.display_board(ctx, board)

        await message.clear_reactions()
        return await ctx.send("It's a tie!")
        
async def setup(bot):
    await bot.add_cog(TicTacToe(bot))