from Dbot import bot
import disnake
from disnake.ext import commands
from cogs.Dbot_Gymnansium36_Folder.Registation36.registation_modal import Registration_Modal


class Bot_Registaration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(
            guild_ids=[1097125882876923954, 1102624788582760498],
            name="регистрация",
            description="Регистарция. Регистрацию можно проводить лишь раз"
            )
    # @bot.slash_command(
    #         guild_ids=[1097125882876923954, 1102624788582760498],
    #         name="регистрация",
    #         description="Регистарция. Регистрацию можно проводить лишь раз"
    #         )
    @commands.has_any_role(int(1104761162945527939))
    async def registration(inter: disnake.CommandInteraction):
        membernew = inter.user.id
        # owner = bot.get_user(int(581348510830690344))
        # newmembermention = bot.get_user(int(membernew))
        reg_guild = bot.get_guild(inter.guild.id)
        await inter.response.send_modal(modal=Registration_Modal(membernew, reg_guild))

        # with open(r'C:\Users\meljn\OneDrive\Документы\testbot\users.txt', 'a+', encoding='utf-8') as userfile:
        #     userfile.write(f"{имя} {фамилия} {класс} {newmembermention} \n")
        
        # await owner.send(f"{имя} {фамилия} {класс} <@{membernew}> \n")
        # await inter.response.send_message(f"Успешная регистрация, <@{membernew}>!", delete_after=5)
        # userfile.close()

        # role_not_authorized = inter.guild.get_role(int(1104761162945527939))
        # role_authorized = inter.guild.get_role(int(1104761018124619826))

        # await inter.user.remove_roles(role_not_authorized)
        # await inter.user.add_roles(role_authorized)
        # userfile.close()    

        # values = (имя, фамилия, класс, 0, membernew)

        # with sqlite3.connect("server.db") as db:
        #     cursor = db.cursor()

        #     cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        #         in_db_user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         login TEXT,
        #         login_forname TEXT,
        #         clas TEXT,
        #         cash BIGINT,
        #         discordaccountid BIGINT
        #     )""")

        #     cursor.execute("INSERT INTO users(login, login_forname, clas, cash, discordaccountid) VALUES (?, ?, ?, ?, ?)", values)

        #     db.commit()

            # cursor.execute('SELECT COUNT(*) FROM users WHERE login_forname = ?', (фамилия,))
            # result = cursor.fetchone()

            # Если количество найденных записей больше 0, значит имя уже существует в базе данных
            # if result[0] > 0:
            #     await inter.response.send_message('Фамилия уже есть в базе данных. Обратитесь в поддержку')
            # else:
            #     print('Имя не найдено в базе данных')

            # for value in cursor.execute("SELECT * FROM users"):
            #     print(value)