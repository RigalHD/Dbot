import disnake
from disnake import TextInputStyle
from Dbot import bot
import sqlite3
from cogs.Dbot_Requests_Folder.buttons import newbieconfirm, ConfirmFormAddButton
import datetime

class MyModal(disnake.ui.Modal):
    def __init__(self, requests_dict):
        self.requests_dict = requests_dict
        self.guild = bot.get_guild(self.requests_dict['guild_id'])
        self.new_member_data = []
        components = [
            disnake.ui.TextInput(
                label="Ваш ник в майнкрафте",
                placeholder="Пример: Mr_Axolotlik",
                custom_id="nickname",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Ваш возраст",
                placeholder="ВВЕДИТЕ ТОЛЬКО ЧИСЛО! Пример: 15",
                custom_id="age",
                style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Сколько времени играете в майнкрафт?",
                placeholder="Пример: Я играю в майнкрафт с 2018 года",
                custom_id="play_time",
                style=TextInputStyle.paragraph,
            ),
            disnake.ui.TextInput(
                label="Чем на вы занимались на сервере до нас?",
                placeholder="Пример: я - новичек ИЛИ я был в городе таком-то и занимался тем-то",
                custom_id="past",
                style=TextInputStyle.paragraph,
            )
        ]
        super().__init__(
            title="Заявка на сервер",
            custom_id="emb_create",
            timeout=300,
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            int(inter.text_values["age"])
        except ValueError:
            embed_error = disnake.Embed(
                title="При отправке заявки возникла ошибка",
                description="""Введён некорректный возраст.
                При отправке заявки нужно указать только число.
                Пример: 15""",
                color=0xff0000
            )
            await inter.response.send_message(embed=embed_error, ephemeral=True)
            return

        embed = disnake.Embed(
            title="Новая заявка",
            description=f"<@{inter.user.id}> написал заявку на сервере {self.guild.name}! Принять или отказать?",
            color=0x00a2ff
            )
        

        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS requests_to_server(
                in_db_user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_id BIGINT,
                nick TEXT,
                age INTEGER,
                play_time TEXT,
                past TEXT,
                p_status TEXT,
                cancel_reason TEXT,
                guild_of_request TEXT,
                date_of_request DATETIME
                )""") 
            # все записи date_of_request с датой 2024-01-31 22:32:50.777804
            # - это записи, в которых не было предусмотрено сохранение даты отправки заявки
            db.commit()

        self.requests_dict["new_member_id"] = inter.user.id
        vals = [inter.user.id]

        for key, value in inter.text_values.items():
            vals.append(value)
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )

        vals += ['-', '-', self.guild.name, datetime.datetime.now()]

        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO requests_to_server(
                        discord_id, nick, age, play_time, past,
                        p_status, cancel_reason, guild_of_request, date_of_request
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", vals)
            db.commit()
            print("В базу данных внесена новая заявка!")
            self.requests_dict["last_request"] = cursor.lastrowid
        
        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            ban_user = cursor.execute("SELECT discord_id FROM requests_no_access WHERE discord_id = ?", (inter.user.id,)).fetchall()
            if ban_user:
                cursor.execute("SELECT cause FROM requests_no_access WHERE discord_id = ?", (inter.user.id,))
                fetch_reason = cursor.fetchone()
                reason = fetch_reason[0] if fetch_reason else "Спросите у администрации города"
                await inter.send(f"Вам запрещено отправлять заявку в данный город.\nПричина: {reason}", ephemeral=True)
                return
        
        
        await self.requests_dict["check_channel"].send(embed=embed, view=newbieconfirm(self.requests_dict))
        await inter.response.send_message(f"<@{inter.user.id}> заявка отправлена!", ephemeral=True, delete_after=20)
        await inter.user.send(f"Твоя заявка на рассмотрении, <@{inter.user.id}>")



class FormToAddRequestsModal(disnake.ui.Modal):
    def __init__(self) -> None:
        self.names_of_table_columns = []
        self.id_of_request: int
        self.components = [
            disnake.ui.TextInput(
                label="Причина добавления заявок",
                placeholder="",
                custom_id="reason_of_addition",
                style=TextInputStyle.paragraph,
            ),
            disnake.ui.TextInput(
                label="Айди канала отправки заявок",
                placeholder="Сюда нужно ввести айди канала, куда бот отправит сообщение с кнопкой",
                custom_id="channel_id",
                style=TextInputStyle.paragraph,
            ),
            disnake.ui.TextInput(
                label="Айди канала проверки заявок",
                placeholder="Сюда нужно ввести айди канала, куда бот будет отправлять все заявки",
                custom_id="channel_for_checking_requests_id",
                style=TextInputStyle.paragraph,
            ),
            disnake.ui.TextInput(
                label="Айди ролей для новичка",
                placeholder="Сюда нужно ввести айди ролей через запятую (они будут выданы новичку при принятии его заявки)", # Учтите, что у бота должны быть права на выдачу этой роли на Вашем сервере.
                custom_id="role_id",
                style=TextInputStyle.paragraph,
            ),
        ]
        super().__init__(
            title="Форма на добавление заявок",
            custom_id="form_to_add_requests",
            timeout=600,
            components=self.components,
        )
    
    async def callback(self, inter: disnake.ModalInteraction):
        id_error_embed = disnake.Embed(
            title="Возникла ошибка!",
            description="Один или несколько из введенных Вами айди не соответствуют формату.",
            color=0xff0000
        )
        try:
            check_tuple = (
            inter.guild.get_channel(int(inter.text_values["channel_id"])),
            inter.guild.get_channel(int(inter.text_values["channel_for_checking_requests_id"])),
            [int(role) for role in inter.text_values["role_id"].replace(",", " ").split()]
            )
            if None in (check_tuple, check_tuple[2]):
                await inter.response.send_message(embed=id_error_embed, ephemeral=True)
                return

        except ValueError:
            await inter.response.send_message(embed=id_error_embed, ephemeral=True)
            return

        if len(inter.text_values.items()) != len(self.components) or\
            inter.text_values["channel_id"] == "":
            error_embed = disnake.Embed(
            title="Возникла ошибка!",
            description="""Похоже, что с отображением всех полей модального окна возникла ошибка!
            Попробуйте ещё раз""",
            color=0xff0000
            )
            await inter.response.send_message(embed=error_embed)
            return

        # await inter.response.send_message(
        #     f"Да ладно. Херня - твоя причина: **{list(inter.text_values.values())[0]}**", ephemeral=True)
        await inter.response.send_message("Ваша заявка отправлена!", ephemeral=True)

        values = (
            inter.text_values["reason_of_addition"],
            inter.guild.id,
            inter.text_values["role_id"],
            inter.text_values["channel_id"],
            inter.text_values["channel_for_checking_requests_id"],
            inter.user.id,
            datetime.datetime.now(),
            "IS NOT CHECKED",
            )
        # print(f"-> {len(self.components)}")
        # print(len(inter.text_values.items()))
        # print(inter.text_values.items())
        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            # cursor.execute("DROP TABLE forms_to_add_requests")  # Применять только при тестах
            # cursor.execute("""CREATE TABLE IF NOT EXISTS forms_to_add_requests (
            # id INTEGER PRIMARY KEY AUTOINCREMENT,
            # text_of_request TEXT,
            # guild_of_request TEXT,
            # id_of_role TEXT,
            # channel_for_requests TEXT,
            # channel_for_checking_requests TEXT,
            # date_of_request DATETIME,
            # status_of_request TEXT
            # )""")
            # СТАРАЯ ВЕРСИЯ БАЗЫ ДАННЫХ

            cursor.execute("""INSERT INTO forms_to_add_requests (
                        text_of_request, guild_of_request, id_of_role, channel_for_requests, 
                        channel_for_checking_requests, id_of_sender, date_of_request, status_of_request)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", values)
            self.id_of_request = cursor.lastrowid
            
        
            db.commit()
            self.names_of_table_columns = [column[1] for column in cursor.execute(
                "PRAGMA table_info(forms_to_add_requests)").fetchall()]
            # print(cursor.execute("SELECT * FROM forms_to_add_requests WHERE id = ?", (cursor.lastrowid,)).fetchone())
        owner_of_bot = bot.get_user(581348510830690344)
        notification_embed = disnake.Embed(
            title="Заявка на добавление заявок!",
            description=f"Похоже, что **{inter.user.mention}**\
                захотел добавить систему заявок на свой сервер **{inter.guild.name}**",
            color=0x21c24c,
        )
        form_embed = disnake.Embed(
            title="Содержание заявки",
            color=0x00a2ff,
            )

        for i in range(1, len(self.names_of_table_columns)):
            form_embed.add_field(
                name=self.names_of_table_columns[i].capitalize(),
                value=values[i - 1],
                inline=False,
            )

        await owner_of_bot.send(
            embeds=(notification_embed, form_embed),
            view=ConfirmFormAddButton(self.id_of_request)
            )
