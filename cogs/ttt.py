import asyncio
import discord
from discord.ext import commands
import random

class TicTacToe:
    X = -1
    O = 1
    Tie = 2

    def __init__(self, player1, player2, starter):
        self.current_player = starter
        self.player_1 = player1
        self.player_2 = player2
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

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

class Games(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(aliases=['ttt'])
    async def tictactoe(self, ctx: commands.Context, player2: discord.Member):
        """Play tic-tac-toe
        
        Parameters
        -----------
        player2: discord.Member
            who you want to play against
        """
        if player2 == ctx.author:
            return await ctx.reply("You can't play yourself.")

        starter = random.choice([ctx.author, player2])
        game = TicTacToe(player1=ctx.author, player2=player2, starter=starter)
        content = f'**Tic Tac Toe**\n<:x_:1087132262400794644> {starter.name} goes first'
        message = await ctx.send(content)

        def check_move(m):
            return m.author == game.current_player and m.channel == ctx.channel

        while not (winner := game.check_board_winner()):
            try:
                move = await self.bot.wait_for('message', check=check_move, timeout=30.0)
            except asyncio.TimeoutError:
                content = f'❗ {game.current_player.name} didnt make a move in time.\nGame has ended in a tie.'
                return await message.edit(content=content)

            move_content = move.content
            if move_content.lower() == 'stop':
                return await ctx.send(f'The game was ended by {game.current_player.mention}.')

            if len(move_content) != 2 or not move_content[0].isdigit() or not move_content[1].isdigit():
                await ctx.send('Invalid move! Please enter a move in the format "row column", e.g., "1 2".')
                continue

            row = int(move_content[0]) - 1
            col = int(move_content[1]) - 1

            if not (0 <= row < 3 and 0 <= col < 3):
                await ctx.send('Invalid move! Row and column should be between 1 and 3.')
                continue

            if game.board[row][col] in (game.X, game.O):
                await ctx.send('Invalid move! That cell is already taken.')
                continue

            game.board[row][col] = game.X if game.current_player == game.player_1 else game.O
            content = f'**Tic Tac Toe**\n<:x_:1087132262400794644> {game.player_1.name} vs <:o_:1087132605876555807> {game.player_2.name}\n\n'
            for y in range(3):
                for x in range(3):
                    if game.board[y][x] == game.X:
                        content += "<:x_:1087132262400794644>"
                    elif game.board[y][x] == game.O:
                        content += "<:o_:1087132605876555807>"
                    else:
                        content += "<:empty:1234567890>"
                content += '\n'
            content += f"\n{game.current_player.name}'s turn"
            await message.edit(content=content)
            game.current_player = game.player_1 if game.current_player == game.player_2 else game.player_2

        if winner == game.Tie:
            content = "It's a tie!"
        else:
            content = f"{game.current_player.name} won!"
        await ctx.send(content)
        
async def setup(bot):
    await bot.add_cog(Games(bot))