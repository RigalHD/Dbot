from disnake.ext import commands
import disnake
from Dbot import bot
import sqlite3


class ServerTochka_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[1051049677207912468], name="репутация", description="Узнай сколько у тебя SocialCredit")
    async def socialcredit(self, inter: disnake.CommandInteraction, member: disnake.Member):
        with sqlite3.connect("servertochka.db") as dbt:

            cursortochka = dbt.cursor()
            membermention = bot.get_user(int(member.id))
            mbr = str(member)
            cursortochka.execute('SELECT scredits FROM socialcredits WHERE ds_account = ?', (mbr,))
            result = cursortochka.fetchone()
            reputation = result[0] if result else 0
            results = f"Репутация **{membermention.mention}**: **{reputation}** SocialCredits"

            embed = disnake.Embed(
                title="Репутация",
                description=results,
                color=0x00a2ff
            )
            embed.set_author(
                name=f"{member.name}",
                icon_url=member.avatar.url
            )
            await inter.response.send_message(embed=embed)
            print(member)

    # @bot.slash_command(guild_ids=[1051049677207912468], name="всярепутация", description="Узнай сколько у всех SocialCredit")
    # async def socialcreditfull(inter: disnake.CommandInteraction):
    #     with sqlite3.connect("servertochka.db")  as dbt:
    #         cursortochka = dbt.cursor()
    #         for value in cursortochka.execute("SELECT ds_account, scredits FROM socialcredits"):
    #             await inter.send(value)
            
    @commands.slash_command(guild_ids=[1051049677207912468])
    @commands.has_permissions(administrator=True)
    async def socialcreditset(self, inter, member: disnake.Member, credits: int):
        try:
            with sqlite3.connect("servertochka.db") as dbt:
                cursortochka = dbt.cursor()
                mbr = str(member)

                cursortochka.execute("""
                CREATE TABLE IF NOT EXISTS socialcredits(
                    in_db_user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ds_account TEXT,
                    scredits BIGINT 
                )""")

                cursortochka.execute("UPDATE socialcredits SET scredits = ? WHERE ds_account = ?", (credits, mbr))
                dbt.commit()

                for value in cursortochka.execute("SELECT ds_account, scredits FROM socialcredits"):
                    print(value)

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    @commands.slash_command(guild_ids=[1097125882876923954])
    async def membrsofst(self, inter):
        global st_members
        st_members = []
        guild = bot.get_guild(int(1051049677207912468))
        for member in guild.members:
            st_members.append(str(member))

        print(st_members)