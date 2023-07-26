import asyncio
from typing import Optional
import discord
from discord.ext import commands
import random

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x, y):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b')
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToe = self.view
        if view.current_player == view.player_1:
            self.style = discord.ButtonStyle.blurple
            self.label = 'X'
            view.board[self.y][self.x] = 'X'
            view.current_player = view.player_2
        else:
            self.style = discord.ButtonStyle.red
            self.label = 'O'
            view.board[self.y][self.x] = 'O'
            view.current_player = view.player_1

        self.disabled = True
        winner = view.check_board_winner()
        if winner:
            for child in view.children:
                child.disabled = True

            if winner == 'tie':
                content = "It's a tie!"
            else:
                content = f"{view.current_player.mention} won!"

            await view.message.edit(content=content, view=view)

class TicTacToe(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def get_player_reaction(self, ctx, player, message):
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                check=lambda reaction, user: user == player and reaction.message == message and str(reaction.emoji) in ["↖️", "⬆️", "↗️", "⬅️", "⏺️", "➡️", "↙️", "⬇️", "↘️"],
                timeout=30.0,
            )
            return str(reaction.emoji)
        except asyncio.TimeoutError:
            return None

    async def display_board(self, ctx, board):
        message = "**Tic Tac Toe**\n"
        for row in board:
            message += " ".join([str(cell) if cell is not None else "\u200b" for cell in row])
            message += "\n"
        return await ctx.send(message)

    async def tictactoe(self, ctx: commands.Context, player2: discord.Member):
        if player2 == ctx.author:
            return await ctx.reply("You can't play yourself.")

        player_1 = ctx.author
        player_2 = player2
        current_player = player_1
        board = [[None, None, None], [None, None, None], [None, None, None]]

        message = await self.display_board(ctx, board)

        for x in range(3):
            for y in range(3):
                await TicTacToeButton(x, y).send(message)

        while True:
            reaction = await self.get_player_reaction(ctx, current_player, message)

            if reaction is None:
                return await ctx.send(f"{current_player.mention} didn't make a move in time. The game has ended.")

            emoji_to_coords = {
                "↖️": (0, 0),
                "⬆️": (0, 1),
                "↗️": (0, 2),
                "⬅️": (1, 0),
                "⏺️": (1, 1),
                "➡️": (1, 2),
                "↙️": (2, 0),
                "⬇️": (2, 1),
                "↘️": (2, 2),
            }

            x, y = emoji_to_coords[reaction]

            if board[y][x] is not None:
                await ctx.send("Invalid move! That cell is already taken.")
                continue

            if current_player == player_1:
                board[y][x] = "X"
                current_player = player_2
            else:
                board[y][x] = "O"
                current_player = player_1

            await message.edit(content=None)
            await self.display_board(ctx, board)

class Games(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(aliases=['ttt'])
    async def tictactoe(self, ctx: commands.Context, player2: discord.Member):
        if player2 == ctx.author:
            return await ctx.reply("You can't play yourself.")

        view = TicTacToe(player1=ctx.author, player2=player2)
        content = f'**Tic Tac Toe**\n<:x_:1087132262400794644> {ctx.author.mention} vs <:o_:1087132605876555807> {player2.mention}\n\nIt\'s {ctx.author.mention}\'s turn'
        view.message = await ctx.send(content, view=view)
        await view.wait()
        
async def setup(bot):
    await bot.add_cog(Games(bot))