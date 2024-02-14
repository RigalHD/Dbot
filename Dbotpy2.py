from Dbot import bot
from Dbotevents import Bot_Events
from cogs.Dbot_Gymnansium36_Folder.Registation36.Dbotregistration import Bot_Registaration
from cfg_s import TOKEN
# from DbotGymnasium36_Folder.DbotOffers import Bot_Offers
from cogs.Dbot_Embed_Folder.DbotEmbed import For_Embed_Writing
from cogs.Dbot_Requests_Folder.commands import DbotRequestsCommands
from cogs.Dbot_Requests_Folder.DB_control_commands import Bot_Requests_DB_Control
from cogs.Dbot_Gymnansium36_Folder.Registation36.Dbot_regdb_control import Bot_Registration_DB_Control
from cogs.Dbot_Gymnansium36_Folder.Dbot_Reports_gm import Bot_Reports
from cogs.Dbot_ServerTochka_Folder.servertochka_db_control import ServerTochka_Commands
from cogs.Dbot_Gymnansium36_Folder.DbotMenu_36 import Bot_Act_Menu_36
from cogs.Dbot_ban_system.commands import DbotBanCommands
# from menuf import Bot_test_DropDown_Menu

def main() -> None:
    # bot.add_cog(Bot_test_DropDown_Menu(bot))
    bot.add_cog(ServerTochka_Commands(bot))
    bot.add_cog(Bot_Reports(bot))
    bot.add_cog(Bot_Registration_DB_Control(bot))
    bot.add_cog(Bot_Requests_DB_Control(bot))
    bot.add_cog(DbotRequestsCommands(bot))
    bot.add_cog(For_Embed_Writing(bot))
    # bot.add_cog(Bot_Offers(bot))
    bot.add_cog(Bot_Registaration(bot))
    bot.add_cog(Bot_Events(bot))
    bot.add_cog(Bot_Act_Menu_36(bot))
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
