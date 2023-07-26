import discord
from discord.ext import commands
from typing import List, Optional
import random

class InvitationButtons(discord.ui.View):
    def __init__(self, player_invited: discord.Member, timeout: Optional[float] = 180.0):
        super().__init__(timeout=timeout)
        self.player_invited: discord.Member = player_invited
        self.answer: bool = None

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.player_invited:
            self.answer = True
            self.stop()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.player_invited:
            self.answer = False
            self.stop()

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.player_1:
            if interaction.user == view.current_player:
                self.style = discord.ButtonStyle.blurple
                self.label = 'X'
                self.disabled = True
                view.board[self.y][self.x] = view.X
                view.current_player = view.player_2
                content = f"<:o_:1087132605876555807> It's {view.player_2.name}'s turn"
            else:
                return await interaction.response.send_message('Not your turn!', ephemeral=True)
        else:
            if interaction.user == view.current_player:
                self.style = discord.ButtonStyle.red
                self.label = 'O'
                self.disabled = True
                view.board[self.y][self.x] = view.O
                view.current_player = view.player_1
                content = f"<:x_:1087132262400794644> It's {view.player_1.name}'s turn"
            else:
                return await interaction.response.send_message('Not your turn!', ephemeral=True)

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f'<:x_:1087132262400794644> {view.player_1.name} won!'
            elif winner == view.O:
                content = f'<:o_:1087132605876555807> {view.player_2.name} won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)

class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, player1, player2, starter, timeout: Optional[float] = 30.0):
        super().__init__(timeout=timeout)
        if starter == player1:
            self.current_player = starter
            self.player_1 = player1
            self.player_2 = player2
        elif starter == player2:
            self.current_player = starter
            self.player_1 = player2
            self.player_2 = player1
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(content=f"❗ {self.current_player.name} didn't make a move in time.\nGame has ended in a tie.", view=self)

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
        embed = discord.Embed(title="📥 Invitation", description=f"{ctx.author.mention} invited you to play tic-tac-toe!", color=0x2B2D31)
        view = InvitationButtons(player2)
        invite = await ctx.send(content=player2.mention, embed=embed, view=view)
        await view.wait()
        if view.answer:
            await invite.delete()
            starter = random.choice([ctx.author, player2])
            view = TicTacToe(player1=ctx.author, player2=player2, starter=starter)
            view.message = await ctx.send(f'**Tic Tac Toe**\n<:x_:1087132262400794644> {starter.name} goes first', view=view)
        elif view.answer is None:
            embed = invite.embeds[0]
            original = invite.embeds[0].description
            new = f"~~{original}~~\n\n❗ You didn't respond to the invite in time"
            embed.description = new
            for item in view.children:
                item.disabled = True
            await invite.edit(embed=embed, view=view)
        else:
            return await invite.edit(content=f'❌ {player2.name} declined the invite', embed=None, view=None)
        

async def setup(bot):
    await bot.add_cog(Games(bot))