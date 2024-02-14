import disnake
from disnake.ui import StringSelect, View
from cogs.Dbot_Gymnansium36_Folder.Dbot_Reports_gm import ReportsModal
from cogs.Dbot_Gymnansium36_Folder.DbotOffers import OffersModal
from typing import Optional


class DropDownView_36(View):
    def __init__(self):
        
        super().__init__()
        self.add_item(DropDown_36())

class DropDown_36(StringSelect):
    def __init__(self):
        super().__init__(
            placeholder="Меню",
            max_values=1,
            min_values=1,
            options=[
                disnake.SelectOption(label="Связь с нами"),
                disnake.SelectOption(label="Предложение"),
                disnake.SelectOption(label="Жалоба")
            ]
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if self.values[0] == "Связь с нами":
            await inter.send("Данная опция сейчас в разработке. Следи за новостями!", ephemeral=True)

        elif self.values[0] == "Предложение":
            # await inter.send("Данная опция сейчас в разработке. Следи за новостями!", ephemeral=True)
            await inter.response.send_modal(modal = OffersModal())

        elif self.values[0] == "Жалоба":
            # await inter.send("Данная опция сейчас в разработке. Следи за новостями!", ephemeral=True)
            await inter.response.send_modal(modal = ReportsModal())            


class Menu_Button(disnake.ui.View): 

    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Меню", style=disnake.ButtonStyle.green)
    async def menu_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        embed = disnake.Embed(
            title="Выбирай, что тебя интересует!",
            description="Если не получается что-нибудь выбрать, то нажми на кнопку \"Меню\" (она выше) ещё раз",
            color=0x00a2ff
        
        )
        await inter.response.send_message(
            embed=embed,
            view=DropDownView_36(),
            ephemeral=True
            )

class Menu_Button_disabled(disnake.ui.View): 

    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Меню", style=disnake.ButtonStyle.green, disabled=False)
    async def menu_button(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        embed = disnake.Embed(
            title="Выбирай, что тебя интересует!",
            description="Если не получается что-нибудь выбрать, то нажми на кнопку \"Меню\" (она выше) ещё раз",
            color=0x00a2ff
        
        )
        await inter.response.send_message(
            embed=embed,
            view=DropDownView_36(),
            ephemeral=True
            )
