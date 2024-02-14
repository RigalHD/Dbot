import disnake
from disnake.ui import StringSelect, View
from cogs.Dbot_Embed_Folder.Modal_Classes_Embed import EmbModal
class DropDownView(View):
    def __init__(self, channel):
        self.channel = channel
        
        super().__init__()
        self.add_item(DropDown(self.channel))

class DropDown(StringSelect):
    def __init__(self, channel):
        self.channel = channel
        super().__init__(
            placeholder="Меню",
            max_values=1,
            min_values=1,
            options=[
                disnake.SelectOption(label="синий"),
                disnake.SelectOption(label="красный"),
                disnake.SelectOption(label="зелёный"),
                disnake.SelectOption(label="жёлтый"),
                disnake.SelectOption(label="фиолетовый")
            ]
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if self.values[0] == "синий":
            clr=0x00a2ff

        elif self.values[0] == "красный":
            clr=0xff0000

        elif self.values[0] == "зелёный":
            clr=0x135c19   
                
        elif self.values[0] == "жёлтый":
            clr=0xffff00

        elif self.values[0] == "фиолетовый":
            clr=0x8400ff

        embed = disnake.Embed(
            title="Выбери что будет в эмбеде",
            description="Если ничего кроме описания не будет, то выбери только \"Будет описание\"",
            color=0x00a2ff
            )
        await inter.send(embed=embed, view=DropDownView_img(self.channel, clr), ephemeral=True, delete_after=20)


class DropDownView_img(View):

    def __init__(self, channel, color):
        self.channel = channel
        self.color = color
        self.list_of_choice = [False, False, False, False]

        super().__init__()
        self.add_item(DropDownView_img.DropDown_Img_Select(self.channel, color, self.list_of_choice))

    class DropDown_Img_Select(StringSelect):
        def __init__(self, channel, color, list_of_choice):
            self.channel = channel
            self.clr = color
            self.list_of_choice = list_of_choice

            
            super().__init__(
                placeholder="Меню",
                max_values=3,
                min_values=1,
                options=[
                    disnake.SelectOption(label="Будет описание"),
                    disnake.SelectOption(label="Будет картинка"),
                    disnake.SelectOption(label="Будет указан автор"),
                    disnake.SelectOption(label="Будет название")
                ]
            )

        async def callback(self, inter: disnake.MessageInteraction):
            
            if "Будет картинка" in self.values:
                self.list_of_choice[0] = True
                # print(self.list_of_choice)
            
            if "Будет указан автор" in self.values:
                self.list_of_choice[1] = True

            if "Будет название" in self.values:
                self.list_of_choice[2] = True

            if "Будет описание" in self.values:
                self.list_of_choice[3] = True
                # print(self.list_of_choice)
            # print(self.list_of_choice)
            await inter.response.send_modal(modal=EmbModal(
            self.channel,
            self.clr,
            self.list_of_choice,
            ))


