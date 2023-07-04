from discord import ui, Embed
from discord.interactions import Interaction
from collections import deque
from typing import List

class Paginator(ui.View):
    def __init__(self, embeds: List[Embed]):
        self._embeds = embeds
        self._queue = deque(embeds)
        self._len = len(embeds)
        self._index = 1
        self._initial = embeds[0].set_footer(text=f"Page {self._index} / {self._len}")

        super().__init__(timeout=90)

    @ui.button(emoji='\N{LEFTWARDS BLACK ARROW}')
    async def previous_embed(self, interaction: Interaction, _):
        self._queue.rotate(1)
        if self._index == 1:
            self._index = self._len
        else:
            self._index -= 1
        embed = self._queue[0]
        embed.set_footer(text=f"Page {self._index} / {self._len}")
        await interaction.response.edit_message(embed=embed)

    @ui.button(emoji='\N{BLACK RIGHTWARDS ARROW}')
    async def next_embed(self, interaction: Interaction, _):
        self._queue.rotate(-1)
        if self._index == self._len:
            self._index = 1
        else:
            self._index += 1
        embed = self._queue[0]
        embed.set_footer(text=f"Page {self._index} / {self._len}")
        await interaction.response.edit_message(embed=embed)

    @property
    def initial(self) -> Embed:
        return self._initial