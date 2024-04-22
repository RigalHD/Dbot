import disnake
from typing import Optional
from disnake import TextInputStyle
from Dbot import bot
import sqlite3
from . import commands as request_commands

class newbieconfirm(disnake.ui.View):
    def __init__(self, requests_dict):
        super().__init__(timeout=None)
        self.requests_dict = requests_dict
        self.value = Optional[bool]
        self.guild = bot.get_guild(requests_dict["guild_id"])
        self.new_member = bot.get_user(self.requests_dict["new_member_id"])
        self.new_member_guild = self.guild.get_member(self.new_member.id)

    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green, emoji="✔️")
    async def newbieconfirm(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        try:
            for role_id in self.requests_dict["roles"]:
                role = self.guild.get_role(role_id)
                await self.new_member_guild.add_roles(role)
        except disnake.errors.Forbidden:
            await inter.response.send_message("У бота нет прав на выдачу этих ролей на Вашем сервере")
            return

        embed = disnake.Embed(
            title="Новый игрок!",
            description=(
                f"Игрок {self.new_member.mention} присоединяется к нам!\n"
                "Хорошей игры!\n"
            ),
            color=0x00a2ff
        )
        
        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            cursor.execute("UPDATE requests_to_server SET p_status = ? WHERE in_db_user_id = ?",
                            ("Принят", self.requests_dict["last_request"]))
            db.commit() 
        
        await self.requests_dict['channel'].send(embed=embed, delete_after=30)
        await inter.response.send_message(f"{self.new_member.mention}, присоединяется к нам!")
        self.value = True
        self.stop()

    @disnake.ui.button(label="Отказать", style=disnake.ButtonStyle.red, emoji="👎")
    async def newbiecancel(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(modal=Modal_Request_Cancel(self.requests_dict))
        
        self.value = False
        self.stop()


class Modal_Request_Cancel(disnake.ui.Modal):
    def __init__(self, data_of_request: dict):
        self.requests_dict: dict = data_of_request
        components = [
            disnake.ui.TextInput(
                label="Причина отказа",
                placeholder="Пример: \"Вы не подходите нам\"",
                custom_id="reason_of_cancel",
                style=TextInputStyle.paragraph,
                max_length=256,
            )
        ]
        super().__init__(
            title="Причина отказа",
            custom_id="cancel_emb_create",
            timeout=300,
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(
            title="Вам было отказано в принятии к нам",
            description=f"""Попытайте удачу в следующий раз. 
            Причина отказа: {inter.text_values['reason_of_cancel']}""",
            color=0xff0000
            )
        new_member = bot.get_user(int(self.requests_dict["new_member_id"]))
        await new_member.send(f"<@{new_member.id}>", embed=embed)
        await inter.response.send_message("Успешный отказ!")

        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            cursor.execute("UPDATE requests_to_server SET p_status = ?, cancel_reason = ? WHERE in_db_user_id = ?",
                            ("Отказано", inter.text_values['reason_of_cancel'], self.requests_dict["last_request"]))
            db.commit()


class ConfirmFormAddButton(disnake.ui.View):
    def __init__(self, id_of_request) -> None:
        super().__init__(timeout=None)
        self.id_of_request: int = id_of_request
    
    @disnake.ui.button(label="Принять", style=disnake.ButtonStyle.green, emoji="✔️")
    async def confirm(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            cursor.execute("""
                           UPDATE forms_to_add_requests
                           SET status_of_request = ? WHERE id = ?
                           """,
                           ("CONFIRMED", self.id_of_request)
                           )
            data_of_request = cursor.execute("""
                                             SELECT guild_of_request, id_of_role, channel_for_requests, 
                                             channel_for_checking_requests, id_of_sender 
                                             FROM forms_to_add_requests WHERE id = ?
                                             """,
                                             (self.id_of_request,)
                                             ).fetchone()
            confirmed_user = bot.get_user(int(data_of_request[4]))
            channel = bot.get_channel(int(data_of_request[2]))
            db.commit()
        
        button_embed = disnake.Embed(
            title="Отправь заявку на вступление к нам!",
            description="Если бот в сети, то вам для написания заявки нужно нажать кнопку **✍️Заявка**",
            color=0x03fc6b
        )
        check_channel = bot.get_channel(int(data_of_request[3]))
        roles_tuple = tuple(data_of_request[1].replace(",", " ").split())
        channel = bot.get_channel(int(data_of_request[2]))
        roles = tuple(int(role) for role in roles_tuple)
        guild_id = int(data_of_request[0])
        
        if not(None in data_of_request):
            requests_dict = {
                "channel": channel,
                "roles": roles,
                "guild_id": guild_id,
                "check_channel": check_channel
                }
        await channel.purge(limit=1)
        await channel.send(embed=button_embed, view=request_commands.SendRequestButton(requests_dict))
        await inter.response.send_message("Заявка успешно принята!")
        await confirmed_user.send("Ваша заявка рассмотрена и успешна принята. Теперь на Вашем сервере есть система заявок")
        self.value = True
        self.stop()

    @disnake.ui.button(label="Отказать", style=disnake.ButtonStyle.red, emoji="👎")
    async def cancel(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE forms_to_add_requests
                            SET status_of_request = ? WHERE id = ?""",
                            ("CANCELED", self.id_of_request))
            canceled_user_id = int(cursor.execute("SELECT id_of_sender FROM forms_to_add_requests WHERE id = ?",
                                               (self.id_of_request,)).fetchone()[0])
            canceled_user = bot.get_user(canceled_user_id)
            db.commit()

        await inter.response.send_message("Успешный отказ!")
        await canceled_user.send("Вам было отказано в добавлении заявок")
        self.value = False
        self.stop()

