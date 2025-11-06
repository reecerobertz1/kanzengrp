import discord
from discord.ext import commands
from discord import app_commands


class TicTacToeButton(discord.ui.Button):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view

        
        if interaction.user != view.current_player:
            await interaction.response.send_message("❌ It’s not your turn!", ephemeral=True)
            return

        
        if self.label != "\u200b":
            await interaction.response.send_message("⚠️ That spot is already taken!", ephemeral=True)
            return

        
        symbol = "❌" if view.current_player == view.player1 else "⭕"
        self.label = symbol
        self.style = discord.ButtonStyle.secondary if symbol == "❌" else discord.ButtonStyle.secondary 
        self.disabled = True
        view.board[self.y][self.x] = symbol

        
        winner = view.check_winner()
        if winner:
            for child in view.children:
                child.disabled = True
            await interaction.response.edit_message(
                content=f"🎉 {interaction.user.mention} wins!",
                view=view
            )
            view.stop()
            return

       
        if view.is_draw():
            for child in view.children:
                child.disabled = True
            await interaction.response.edit_message(content="🤝 It's a draw!", view=view)
            view.stop()
            return

        
        view.current_player = view.player2 if view.current_player == view.player1 else view.player1
        await interaction.response.edit_message(
            content=f"It’s now {view.current_player.mention}'s turn!",
            view=view
        )


class TicTacToeView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board = [["" for _ in range(3)] for _ in range(3)]

        
        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_winner(self):
        lines = []

        
        lines.extend(self.board)
        lines.extend([[self.board[y][x] for y in range(3)] for x in range(3)])
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2 - i] for i in range(3)])

        for line in lines:
            if line[0] and all(cell == line[0] for cell in line):
                return line[0]
        return None

    def is_draw(self):
        return all(all(cell for cell in row) for row in self.board)


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="tictactoe", description="Challenge someone to a game of Tic Tac Toe.")
    @app_commands.describe(opponent="The user you want to challenge.")
    async def tictactoe(self, interaction: discord.Interaction, opponent: discord.Member):
        player1 = interaction.user
        player2 = opponent

        if player1 == player2:
            await interaction.response.send_message("❌ You can’t play against yourself!", ephemeral=True)
            return

        await interaction.response.send_message(
            f"🎮 {player1.mention} has challenged {player2.mention} to Tic Tac Toe!\n"
            f"{player2.mention}, do you accept?",
        )

        def check(i: discord.Interaction):
            return i.user == player2 and i.message.id == interaction.channel.last_message.id
        try:
            await interaction.followup.send(
                f"{player2.mention}, type `accept` in chat to start the game (30s timeout)."
            )

            msg = await self.bot.wait_for("message", timeout=30.0, check=lambda m: m.author == player2 and m.content.lower() == "accept")
        except Exception:
            await interaction.followup.send("⌛ Challenge timed out.")
            return

        view = TicTacToeView(player1, player2)
        await interaction.followup.send(
            f"✅ Game started between {player1.mention} (❌) and {player2.mention} (⭕)\n"
            f"It’s {player1.mention}'s turn!",
            view=view
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))