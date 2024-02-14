import disnake
from disnake.ext import commands


class DbotBanCommands(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.slash_command()
    async def temp_command(self, inter):
        return

