from Dbot import bot
import disnake
from disnake import TextInputStyle


class EmbModal(disnake.ui.Modal):
    def __init__(self, channel, color, list_of_choices):
        self.channel = channel
        self.color = color
        self.emb_list = []
        self.list_of_choice = list_of_choices

        self.components_emb= []

        self.name_enable = disnake.ui.TextInput(
                label="Название",
                placeholder="Название эмбеда",
                custom_id="embed_name",
                required=False,
                style=TextInputStyle.short,
                max_length=100,
            ),
            
        self.description_enable = disnake.ui.TextInput(
                label="Описание",
                placeholder="Описание эмбеда",
                custom_id="embed_description",
                style=TextInputStyle.paragraph,
                max_length=3000,
            ),

        self.img_enable = disnake.ui.TextInput(
                label="Картинка",
                placeholder="Вставь сюда ссылку на картинку",
                custom_id="embed_img_link",
                style=TextInputStyle.paragraph,
                max_length=3000,
            )
        
        self.author_ava = disnake.ui.TextInput(
                label="Аватарка автора",
                placeholder="Вставь сюда ссылку на аватарку, если она есть",
                custom_id="embed_author_img_link",
                style=TextInputStyle.paragraph,
                max_length=3000,
            )
        
        self.author_name = disnake.ui.TextInput(
                label="Имя автора",
                placeholder="Введи имя автора",
                custom_id="embed_author_name",
                style=TextInputStyle.paragraph,
                max_length=100,
            )
        
        if self.list_of_choice[0] is True:
            self.components_emb.append(self.img_enable)

        if self.list_of_choice[1] is True:
            self.components_emb.append(self.author_ava)
            self.components_emb.append(self.author_name)
        
        if self.list_of_choice[2] is True:
            self.components_emb.append(self.name_enable)
        
        if self.list_of_choice[3] is True:
            self.components_emb.append(self.description_enable)

        super().__init__(
            title="Эмбед",
            custom_id="create_embed",
            components=self.components_emb,
        )
    
    async def callback(self, inter: disnake.ModalInteraction):
        if self.name_enable in self.components_emb:
            if self.description_enable in self.components_emb:
                self.embed = disnake.Embed(
                    title=inter.text_values["embed_name"],
                    description=inter.text_values["embed_description"],
                    color=self.color
                    )
            else:
                self.embed = disnake.Embed(
                    title=inter.text_values["embed_name"],
                    color=self.color
                    )
        elif self.description_enable in self.components_emb:
                self.embed = disnake.Embed(
                    description=inter.text_values["embed_description"],
                    color=self.color
                    )
        if self.img_enable in self.components_emb:
            try:
                self.embed.set_image(url=inter.text_values["embed_img_link"])
            except disnake.errors.HTTPException:
                modal_user = bot.get_user(int(inter.user.id))
                await modal_user.send("При создании эмбеда возникла ошибка с ссылкой на картинку. Убедитесь, что ссылка верна")
                return
        
        if (self.author_ava in self.components_emb)\
            and (self.author_name in self.components_emb):
            self.embed.set_author(
                name = inter.text_values["embed_author_name"],
                icon_url = inter.text_values["embed_author_img_link"],
            )       
            
        await self.channel.send(embed=self.embed)
        await inter.response.send_message(f"Эмбед отправлен!", ephemeral=True, delete_after=20)

