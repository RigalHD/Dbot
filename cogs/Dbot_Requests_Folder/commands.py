import disnake
from cogs.Dbot_ban_system.anti_attack import ban_check
from disnake.ext import commands
from Dbot import bot
from .modals import FormToAddRequestsModal, MyModal
import sqlite3


class DbotRequestsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(guild_ids=[1097125882876923954])
    async def embedbutton(self, inter):
        channel = bot.get_channel(1118583261824815236)
        button_embed = disnake.Embed(
            title="Новый способ писать заявки!",
            description="Если бот в сети, то вам для написания заявки нужно нажать кнопку **✍️Заявка**",
            color=0x03fc6b
        )

        await channel.send(embed=button_embed, view = SendRequestButton())

    @commands.slash_command(name="добавить_заявки_на_мой_сервер")
    @commands.has_guild_permissions(administrator=True)
    async def addition_requests_to_server(self, inter: disnake.ApplicationCommandInteraction):
        if inter.user.id != 581348510830690344:
            await inter.response.send_message("Временно недоступно")
            return
        if await ban_check(inter.user):
            return
        embed = disnake.Embed(
            title="Приветствуем!",
            description="""Похоже, что Вы захотели добавить систему заявок в майнкрафт город через дискорд бота на свой сервер!
            Тогда Вы должны будете заполнить форму.
            Она будет передана на рассмотрение администрации бота.
            После проверки вы получите ответ в ЛС.
            """,
            color=0x00a2ff,
        )

        await inter.response.send_message(embed=embed, ephemeral=True, view=ContinueButtonsRequests(inter.delete_original_message))


    @addition_requests_to_server.error
    async def addition_requests_to_server_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.NoPrivateMessage):
            # вызывается когда команда выполнена в лс
            await inter.send("Эта команда предназначена только для дискорд серверов")
        else:
            raise error

        
class ContinueButtonsRequests(disnake.ui.View):
    def __init__(self, delete_button_message):
        super().__init__(timeout=None)
        self.delete_button_message = delete_button_message

    @disnake.ui.button(label="Продолжить", style=disnake.ButtonStyle.green, emoji="✔️")
    async def continuebutton(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            info_about_requests = cursor.execute("SELECT id FROM forms_to_add_requests WHERE id_of_sender = ? AND status_of_request = ?",
                                (inter.user.id, "IS NOT CHECKED")).fetchall()
            if info_about_requests:
                await inter.response.send_message("У вас уже имеется заявка, которая сейчас на рассмотрении администрации")
                return 

        await inter.response.send_modal(modal=FormToAddRequestsModal())

    @disnake.ui.button(label="Отмена", style=disnake.ButtonStyle.red, emoji="✖️")
    async def cancelbutton(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await self.delete_button_message()


class SendRequestButton(disnake.ui.View):
    def __init__(self, requests_dict):
        super().__init__(timeout=None)
        self.requests_dict = requests_dict

    @disnake.ui.button(label="Заявка", style=disnake.ButtonStyle.green, emoji="✍️")
    async def confirm(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_modal(modal=MyModal(self.requests_dict))
