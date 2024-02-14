from Dbot import bot
import disnake
import sqlite3
from disnake.ext import commands
from DbotConfig import cens_words
from cogs.Dbot_Requests_Folder.commands import SendRequestButton
from cogs.Dbot_Gymnansium36_Folder.DropDown36 import Menu_Button

class Bot_Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        await bot.process_commands(message)
        for content in message.content.split():
            for cens_word in cens_words:
                if content.lower() == "brook":
                    await message.delete()
                    await message.channel.send(f"брук лох")
                elif content.lower() == cens_word:
                    await message.delete()
                    await message.channel.send(f"**Как тебе не стыдно, **{message.author.mention}?")

    # @commands.Cog.listener()
    # async def on_command_error(self, message: disnake.Message):
    #     await message.channel.send("К сожалению с командой возникла ошибка!")
    @commands.Cog.listener()
    async def on_command_error(inter: disnake.CommandInteraction, error: disnake):
        if isinstance(error, commands.MissingPermissions):
            await inter.response.send_message(f"{inter.author.mention}, у тебя нет прав")
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {bot.user} is ready to work!")
        button_embed = disnake.Embed(
            title="Отправь заявку на вступление к нам!",
            description="Если бот в сети, то вам для написания заявки нужно нажать кнопку **✍️Заявка**",
            color=0x03fc6b
        )

        # channel_litecraft = bot.get_channel(int(1118583261824815236))
        # roles_litecraft = (1118848120806178877, 1117027821827670095,)
        # requests_dict = {
        #     "channel": channel_litecraft,
        #     "roles": roles_litecraft,
        #     "guild_id": channel_litecraft.guild,
        # }
        # await channel_litecraft.purge(limit=1)
        # await channel_litecraft.send(embed=button_embed, view = SendRequestButton(requests_dict))


        # xenopia_channel = bot.get_channel(int(1186695166640267368))
        # roles_xenopia = (1186695165340028957, 1186695165310685221,)
        # requests_dict = {
        #     "channel": xenopia_channel,
        #     "roles": roles_xenopia,
        #     "guild_id": xenopia_channel.guild,
        # }
        # await xenopia_channel.purge(limit=1)
        # await xenopia_channel.send(embed=button_embed, view=SendRequestButton(requests_dict))

        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()

            data_of_guilds = cursor.execute("""
                                            SELECT guild_of_request, id_of_role, 
                                            channel_for_requests, channel_for_checking_requests
                                            FROM forms_to_add_requests 
                                            WHERE status_of_request = ?""",
                                            ("CONFIRMED",)).fetchall()
            
            for GUILD in data_of_guilds:
                if not(None in GUILD):
                    check_channel = bot.get_channel(int(GUILD[3]))
                    roles_tuple = tuple(GUILD[1].replace(",", " ").split())
                    channel = bot.get_channel(int(GUILD[2]))
                    roles = tuple(int(role) for role in roles_tuple)
                    guild_id = int(GUILD[0])
                    new_data_of_guids = (check_channel, roles_tuple, check_channel, roles, guild_id)
                    
                    if not(None in new_data_of_guids):
                        requests_dict = {
                            "channel": channel,
                            "roles": roles,
                            "guild_id": guild_id,
                            "check_channel": check_channel
                        }
                        await channel.purge(limit=1)
                        await channel.send(embed=button_embed, view=SendRequestButton(requests_dict))

                else:
                    owner = bot.get_user(581348510830690344)
                    await owner.send(embed=disnake.Embed(
                        title="ВОЗНИКЛА ОШИБКА!",
                        description=f"Не удалось отправить сообщение с заявкой с содержанием \n```{GUILD}```",
                        color=0xff0000,
                    ))
        

        view_menu_36 = Menu_Button()
        channel_menu = bot.get_channel(int(1150855646133104722))
        await channel_menu.purge(limit=1)
        button_embed_report = disnake.Embed(
            title="Меню выбора",
            description='Чтобы выбрать то, что тебя интересует нажми кнопку "Меню"',
            color=0x03fc6b
        )
        await channel_menu.send(embed=button_embed_report, view = view_menu_36)

    # @commands.Cog.listener()
    # async def on_message_edit(self, before: disnake.message.Message, after: disnake.message.Message):
    #     await bot.process_commands(after.content)
    #     for content in after.content.split():
    #         for cens_word in cens_words:

    #             if content.lower() == "brook":
    #                 await after.delete()
    #                 await after.channel.send(f"брук лох")
    #             elif content.lower() == cens_word:
    #                 await after.delete()
    #                 await after.channel.send(f"**Как тебе не стыдно, **{after.author.mention}?")