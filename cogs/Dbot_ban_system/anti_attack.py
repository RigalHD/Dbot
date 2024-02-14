import disnake
import sqlite3

ban_usrs = [469580941174505494, 616198681426657280,]


async def ban_check(user: disnake.User):
    with sqlite3.connect("banned_users.db") as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS banned_bot_users(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id TEXT,
                       reason_of_ban TEXT,
                       date_of_ban DATETIME,
                       status TEXT
                       )""")
        db.commit()
    if user.id in ban_usrs or user.bot:
        return True
    return False

