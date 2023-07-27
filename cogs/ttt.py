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
        if not view.game_over and view.board[self.y * 3 + self.x] == "⬜":
            view.board[self.y * 3 + self.x] = view.current_player.symbol
            if view.check_winner():
                view.game_over = True
                content = f"{view.current_player.mention} wins the game!"
            elif "⬜" not in view.board:
                view.game_over = True
                content = "It's a tie!"
            else:
                view.current_player, view.opponent_player = view.opponent_player, view.current_player
                content = f"It's {view.current_player.mention}'s turn"
            
            buttons = view.create_buttons()
            for y, row in enumerate(buttons):
                for x, button in enumerate(row):
                    button.label = view.board[y * 3 + x]

            await interaction.message.edit(content=content, components=buttons)

class TicTacToe(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def create_buttons(self):
        buttons = [
            [TicTacToeButton(x, y) for x in range(3)] for y in range(3)
        ]
        return buttons

    def print_board(self):
        line = "-------------"
        board_str = f"\n{line}"
        for i in range(0, 9, 3):
            board_str += f"\n| {' | '.join(self.board[i:i+3])} |"
            board_str += f"\n{line}"
        return board_str

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

    def initialize_game(self, ctx, player_o, player_x):
        self.ctx = ctx
        self.player_o = player_o
        self.player_x = player_x
        self.board = ["⬜" for _ in range(9)]
        self.current_player = player_o
        self.opponent_player = player_x
        self.game_over = False

    async def start_game(self):
        embed = discord.Embed(title="Tic-Tac-Toe", description=f"{self.print_board()}", color=0x2ECC71)
        message = await self.ctx.send(embed=embed, components=self.create_buttons())

        try:
            while not self.game_over:
                interaction = await self.bot.wait_for("button_click", timeout=30.0)
                await interaction.respond(type=6)  # Acknowledge the interaction to prevent timeout
                
                for row in self.create_buttons():
                    for button in row:
                        if interaction.custom_id == button.custom_id:
                            await button.callback(interaction)
                            break
        except asyncio.TimeoutError:
            await message.edit(content="The game has timed out!", components=None)
        
async def setup(bot):
    await bot.add_cog(TicTacToe(bot))