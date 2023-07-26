import asyncio
from typing import Optional
import discord
from discord.ext import commands
import random

class InvitationButtons(discord.ui.View):
    def __init__(self, player_invited: discord.Member, timeout: Optional[float] = 180.0):
        super().__init__(timeout=timeout)
        self.player_invited: discord.Member = player_invited
        self.answer: bool = None

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def on_accept(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.player_invited:
            self.answer = True
            self.stop()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def on_decline(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.player_invited:
            self.answer = False
            self.stop()

class TicTacToe(discord.ui.View):
    def __init__(self, player1, player2):
        super().__init__(timeout=30.0)
        self.player_1 = player1
        self.player_2 = player2
        self.current_player = player1
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]

        if all(self.board[y][x] is not None for x in range(3) for y in range(3)):
            return "tie"

        return None

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == self.current_player

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x, y):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b')
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToe = self.view
        if interaction.user == view.current_player:
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