from discord import ui, Embed, ButtonStyle
from discord.interactions import Interaction
from typing import List

class Paginator(ui.View):
    def __init__(self, embeds: List[Embed]):
        self._embeds = embeds
        self._len = len(embeds)
        self._index = 0
        self._initial = embeds[self._index].set_footer(text=f"Page {self._index + 1}/{self._len}")
        super().__init__(timeout=90)
        self.update_page_number_label()

    def update_page_number_label(self):
        """Helper function to update the page number label"""
        self.page_number.label = f"{self._index + 1}/{self._len}"

    @ui.button(label='<<')
    async def first_embed(self, interaction: Interaction, button: ui.Button):
        self._index = 0
        embed = self._embeds[self._index]
        self.update_page_number_label()
        embed.set_footer(text=f"Page {self._index + 1}/{self._len}")
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label='<')
    async def previous_embed(self, interaction: Interaction, button: ui.Button):
        if self._index > 0:
            self._index -= 1
        else:
            self._index = self._len - 1
        embed = self._embeds[self._index]
        self.update_page_number_label()
        embed.set_footer(text=f"Page {self._index + 1}/{self._len}")
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="1/1", disabled=True, style=ButtonStyle.secondary)
    async def page_number(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message("This button just shows the page number.", ephemeral=True)

    @ui.button(label='>')
    async def next_embed(self, interaction: Interaction, button: ui.Button):
        if self._index < self._len - 1:
            self._index += 1
        else:
            self._index = 0
        embed = self._embeds[self._index]
        self.update_page_number_label()
        embed.set_footer(text=f"Page {self._index + 1}/{self._len}")
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label='>>')
    async def last_embed(self, interaction: Interaction, button: ui.Button):
        self._index = self._len - 1
        embed = self._embeds[self._index]
        self.update_page_number_label()
        embed.set_footer(text=f"Page {self._index + 1}/{self._len}")
        await interaction.response.edit_message(embed=embed, view=self)

    @property
    def initial(self) -> Embed:
        return self._initial
