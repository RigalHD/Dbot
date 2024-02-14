import disnake
from disnake.ext import commands
from Dbot import bot
import sqlite3


class Bot_Registration_DB_Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(guild_ids=[1097125882876923954])
    @commands.has_permissions(administrator=True)
    async def registration_db_clear_g36(inter: disnake.CommandInteraction, db_user_id):
        with sqlite3.connect("server.db") as db:
            cursor = db.cursor()
            
            cursor.execute("DELETE FROM users WHERE in_db_user_id = ? ", (db_user_id,))
            db.commit()

            print(f"В базе данных был очищен столбец с айди {db_user_id} ! -> {inter.user.id} ")
            await inter.send("Столбец очищен!")
    
    @commands.slash_command(guild_ids=[1097125882876923954])
    @commands.has_permissions(administrator=True)
    async def user_class_update_g36(inter: disnake.CommandInteraction, db_user_id, clas):
        with sqlite3.connect("server.db") as db:
            cursor = db.cursor()

            cursor.execute("UPDATE users SET clas = ? WHERE in_db_user_id = ? ", (clas, db_user_id,))
            db.commit()

            cursor.execute("SELECT login FROM users WHERE in_db_user_id = ? ", (db_user_id,))
            user_name = cursor.fetchone()

            cursor.execute("SELECT login_forname FROM users WHERE in_db_user_id = ?", (db_user_id,))
            user_forname = cursor.fetchone()

            print(f"В базе данных был изменён класс человека {user_name} {user_forname} | с айди {db_user_id} ! | Изменил человек с айди  -> {inter.user.id} ")
            await inter.send("Класс успешно изменён!")

    # @commands.slash_command(guild_ids=[1097125882876923954])
    # async def test_c(inter):
    #     pass