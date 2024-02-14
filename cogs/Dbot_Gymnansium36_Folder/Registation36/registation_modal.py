import disnake
from disnake import TextInputStyle
from Dbot import bot
import sqlite3

class Registration_Modal(disnake.ui.Modal):
    def __init__(self, new_member, reg_guild):
        self.new_member_id = new_member
        self.new_member = bot.get_user(int(new_member))
        self.new_member_data = []
        self.reg_guild = reg_guild
        self.send_channel = bot.get_channel(int(1145772769037004800))
        self.role_not_authorized = self.reg_guild.get_role(int(1104761162945527939))
        self.role_authorized = self.reg_guild.get_role(int(1104761018124619826))
        self.cash = 0


        components = [
            disnake.ui.TextInput(
                label="Имя",
                placeholder="Здесь введи своё имя",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Фамилия",
                placeholder="Здесь введи свою фамилию",
                custom_id="forname",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="В каком классе ты учишься?",
                placeholder="Здесь введите класс в котором учитесь. Примеры: 10А, 8Б, 5В",
                custom_id="member_class",
                style=TextInputStyle.short,
                max_length=3,
                
            )
        ]
        super().__init__(
            title="Регистрация",
            custom_id="registration_modal",
            timeout=400,
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        # user = bot.get_user(int(581348510830690344))
        embed = disnake.Embed(
            title="Новая регистрация",
            description=f"<@{self.new_member_id}> зарегистрировался!",
            color=0x00a2ff
            )


        for key, value in inter.text_values.items():
            self.new_member_data.append(value)
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )

        values = (self.new_member_data[0], self.new_member_data[1], self.new_member_data[2], self.cash, self.new_member_id)

        with sqlite3.connect("server.db") as db:
            cursor = db.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                in_db_user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT,
                login_forname TEXT,
                clas TEXT,
                cash BIGINT,
                discordaccountid BIGINT
            )""")

            cursor.execute("INSERT INTO users(login, login_forname, clas, cash, discordaccountid) VALUES (?, ?, ?, ?, ?)", values)

            db.commit()


        await inter.user.remove_roles(self.role_not_authorized)
        await inter.user.add_roles(self.role_authorized)
        await self.send_channel.send(embed=embed) 
        # await inter.response.send_message(f"<@{self.new_member_id}> а!", delete_after=5, ephemeral=True)
        await inter.response.send_message(f"Успешная регистрация! <@{self.new_member_id}>", ephemeral=True, delete_after=60)