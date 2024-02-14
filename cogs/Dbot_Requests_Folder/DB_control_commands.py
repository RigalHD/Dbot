import disnake
from disnake.ext import commands
from Dbot import bot
import sqlite3

class Bot_Requests_DB_Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # @commands.slash_command(guild_ids=[1097125882876923954])
    # @commands.has_permissions(administrator=True)
    # async def clear_requests_db(self, inter: disnake.CommandInteraction):
    #     if inter.user.id != 581348510830690344:
    #         return
    #     with sqlite3.connect("no_access_to_requests.db") as db:
    #         cursor = db.cursor()
    #         cursor.execute("DELETE FROM requests_to_server")
    #         db.commit()
    #         print(f"База данных очищена! -> {inter.user.id} ")
    #         await inter.send("База данных очищена!")
    
    @commands.slash_command(guild_ids=[1097125882876923954], name="удалить_из_черного_списка")
    @commands.has_permissions(administrator=True)
    async def requests_no_accses_db_clear(inter: disnake.CommandInteraction, db_user_id):
        if inter.user.id != 581348510830690344:
            return
        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM requests_no_access WHERE in_db_user_id = ? ",
                (db_user_id,),
                )
            db.commit()

            print(f"В базе данных был очищен столбец с айди {db_user_id} ! -> {inter.user.id} ")
            await inter.send("Столбец очищен!")
    
    @commands.slash_command(guild_ids=[1097125882876923954])
    @commands.has_permissions(administrator=True)
    async def requests_tests_clear(inter: disnake.CommandInteraction):
        if inter.user.id != 581348510830690344:
            return
        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM requests_to_server WHERE discord_id = ? ",
                (581348510830690344,),
                )
            db.commit()

            print(f"В базе данных были удалены тестовые заявки {581348510830690344} ! -> {inter.user.id} ")
            await inter.send("Тестовые заявки удалены!")
    
    # @commands.slash_command(guild_ids=[1097125882876923954])
    # @commands.has_permissions(administrator=True)
    # async def col_addd(self, inter: disnake.CommandInteraction):
    #     if inter.user.id != 581348510830690344:
    #         return
    #     with sqlite3.connect("no_access_to_requests.db") as db:
    #         cursor = db.cursor()
    #         cursor.execute("ALTER TABLE requests_to_server ADD COLUMN date_of_request DATETIME DEFAULT '2024-01-31 22:32:50.777804';")
    #         db.commit()
    #         await inter.send("Тестовые заявки удалены!", ephemeral=True)


    @commands.slash_command(guild_ids=[1097125882876923954, 1117027821827670089], name = "запрет_заявок")
    @commands.has_permissions(administrator=True)
    async def no_accses(self, inter: disnake.CommandInteraction, user: disnake.Member, cause):
        if inter.user.id != 581348510830690344:
            return
        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS requests_no_access(
                in_db_user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_id BIGINT,
                cause TEXT
            )""")

            values = (user.id, cause)

            cursor.execute("INSERT INTO requests_no_access(discord_id, cause) VALUES (?, ?)", values)

            db.commit()

    @commands.slash_command(guild_ids=[1097125882876923954])
    @commands.has_permissions(administrator=True)
    async def remove_guild_from_requests(inter: disnake.CommandInteraction, db_guild_id):
        if inter.user.id != 581348510830690344:
            return
        with sqlite3.connect("no_access_to_requests.db") as db:
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM forms_to_add_requests WHERE id = ? ",
                (db_guild_id,))
            db.commit()

        print(f"В базе данных гильдий с системой заявок было очищено поле с айди {db_guild_id} ! -> {inter.user.id} ")
        await inter.response.send_message("Гильдия удалена из заявок!")

    # @commands.slash_command(guild_ids=[1097125882876923954])
    # @commands.has_permissions(administrator=True)
    # async def renew_form_table(self, inter: disnake.CommandInteraction):
    #     if inter.user.id != 581348510830690344:
    #         return
    #     with sqlite3.connect("no_access_to_requests.db") as db:
    #         cursor = db.cursor()

    #         # cursor.execute("DELETE FROM forms_to_add_requests")
    #         cursor.execute("DROP TABLE IF EXISTS forms_to_add_requests")
    #         cursor.execute("""CREATE TABLE IF NOT EXISTS forms_to_add_requests (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         text_of_request TEXT,
    #         guild_of_request TEXT,
    #         id_of_role TEXT,
    #         channel_for_requests TEXT,
    #         channel_for_checking_requests TEXT,
    #         id_of_sender TEXT,
    #         date_of_request DATETIME,
    #         status_of_request TEXT
    #         )""")
    #         db.commit()
