import asyncio
from typing import Optional
import discord
from discord.ext import commands
import random

class TicTacToe:
    def __init__(self, ctx, player1, player2):
        self.ctx = ctx
        self.current_player = player1
        self.player_1 = player1
        self.player_2 = player2
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

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

    async def show_board(self):
        content = f"**Tic Tac Toe**\n<:x_:1087132262400794644> {self.player_1.mention} vs <:o_:1087132605876555807> {self.player_2.mention}\n\n"
        for y in range(3):
            row = ""
            for x in range(3):
                state = self.board[y][x]
                if state is None:
                    row += "🟦"
                elif state == 'X':
                    row += "<:x_:1087132262400794644>"
                elif state == 'O':
                    row += "<:o_:1087132605876555807>"
            content += f"{row}\n"

        return await self.ctx.send(content)

    async def play(self):
        message = await self.show_board()
        for y in range(3):
            for x in range(3):
                await message.add_reaction(f"{x+1}\u20e3")
        await message.add_reaction("🔄")

        def check(reaction, user):
            return user == self.current_player and reaction.message == message

        while True:
            try:
                reaction, user = await self.ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if str(reaction.emoji) == '🔄':
                    return await message.delete()
                
                x = int(reaction.emoji[0]) - 1
                y = {
                    '1️⃣': 0,
                    '2️⃣': 1,
                    '3️⃣': 2
                }.get(reaction.emoji)
                
                if self.board[y][x] is None:
                    self.board[y][x] = 'X' if self.current_player == self.player_1 else 'O'
                    winner = self.check_board_winner()
                    if winner:
                        content = f"{self.current_player.mention} won!" if winner != "tie" else "It's a tie!"
                        await self.show_board()
                        await message.edit(content=content)
                        for reaction in message.reactions:
                            await reaction.clear()
                        return

                    self.current_player = self.player_1 if self.current_player == self.player_2 else self.player_2
                    await message.remove_reaction(reaction, user)
                    await self.show_board()
            except asyncio.TimeoutError:
                await message.delete()
                return

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ttt'])
    async def tictactoe(self, ctx: commands.Context, player2: discord.Member):
        if player2 == ctx.author:
            return await ctx.reply("You can't play yourself.")

        ttt_game = TicTacToe(ctx, player1=ctx.author, player2=player2)
        await ttt_game.play()
        
async def setup(bot):
    await bot.add_cog(Games(bot))