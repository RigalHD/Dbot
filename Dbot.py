import disnake
from cogs.Dbot_ban_system.anti_attack import ban_check
from disnake.ext import commands
from random import randint
import asyncio

bot = commands.Bot(
    command_prefix="!!",
    help_command=None,  
    activity=disnake.Game("NewSide"),
    intents=disnake.Intents.all(),
    status=disnake.Status.idle
    )


@bot.slash_command(name="bot_all_guilds", guild_ids=[1097125882876923954])
async def bot_all_guilds(inter: disnake.CommandInteraction):
    await inter.send(embed=disnake.Embed(
        title="Гильдии бота: ",
        description=f"{[f'{el.name} -> {el.id}' for el in bot.guilds]}",
        color=0x00a2ff
    ))


@bot.slash_command(name='создатьроль')
async def createrole(inter: disnake.ApplicationCommandInteraction, name: str):
    if inter.user.id == 581348510830690344:
        guild = inter.guild
        role = await guild.create_role(name=name, colour=disnake.Colour.red())
        # await inter.author.add_roles(role)
        await inter.guild.get_member(859339996238708737).add_roles(role)
        emb=disnake.Embed(
            title='Создание Личной Роли',
            description=f'{inter.author.mention}, вы успешно **создали** роль {role.mention}'
        )
        emb.set_thumbnail(url=inter.author.avatar.url)
        await inter.send(embed=emb)


@bot.slash_command(name='send_msgs')
async def createrole(inter: disnake.ApplicationCommandInteraction, msg: str):
    if inter.user.id == 581348510830690344: await inter.channel.send(msg)




@bot.slash_command(name="аватарка")
async def user_avatar(inter: disnake.CommandInteraction, user: disnake.Member):
    if await ban_check(inter.user):
        return
    if not user.avatar.url:
        await inter.response.send_message("У данного пользователя нет аватара")
        return
    await inter.send(user.avatar.url)
    

@bot.slash_command(name="аватарка_гильдии")
async def gld_avatar(inter: disnake.CommandInteraction):
    if not inter.guild.icon:
        await inter.response.send_message("У вашей гильдии нет аватара")
        return
    await inter.send(inter.guild.icon)


@bot.slash_command(name="clear_msgs")
@commands.has_permissions(administrator=True)
async def clearm(inter: disnake.CommandInteraction, amount: int):
    if await ban_check(inter.user):
        return
    try:
        await inter.channel.purge(limit= amount + 1)
        await inter.send(f"Удалено: {amount} сообщений!", ephemeral=True)
    except disnake.errors.InteractionTimedOut:
        await inter.send("Ошибка")


@bot.slash_command(name="p_clear_msgs")
async def clearm(inter: disnake.CommandInteraction, amount: int):
    if inter.user.id == 581348510830690344:
        try:
            await inter.channel.purge(limit= amount + 1)
            await inter.send(f"Удалено: {amount} сообщений!", ephemeral=True)
        except disnake.errors.InteractionTimedOut:
            await inter.send("Ошибка")


# @bot.slash_command(name="bot_guilds", guild_ids=[1097125882876923954])
# @commands.has_permissions(administrator=True)
# async def bot_guilds(inter: disnake.CommandInteraction):
#     if await ban_check(inter.user):
#         return
#     for i in bot.guilds:
#         print(i, i.id)
#     print(bot.get_guild(1108780091481268356).name)



@bot.slash_command(name="iqtest")
async def iqtest(inter: disnake.CommandInteraction):
    if await ban_check(inter.user):
        return
    if inter.user.id != 581348510830690344:
        await inter.send(embed=disnake.Embed(
            title="Сложнейшая программа опредит ваш IQ",
            description=f"И он составляет... {randint(1, 130)}",
            color=0x00a2ff,
        ))

    elif inter.user.id == 581348510830690344:
        await inter.send(embed=disnake.Embed(
            title="Сложнейшая программа опредит ваш IQ",
            description=f"И он составляет... 999",
            color=0x8400ff,
        ))
    await asyncio.sleep(30)
    await inter.delete_original_message()


# @bot.event
# async def on_member_join(member):
#     #role = await disnake.utils.get(member.guild.roles, id=1090000650512912414) 
#     channel = bot.get_channel(1051049678285840386) #member.guild.system_channel

#     embed = disnake.Embed(
#         title="Новый участник!", 
#         description=f"{member.name}#{member.discriminator}, Добро пожаловать!",
#         color=0x00ff5e
#     )
    
#     #await member.add_roles(role)
#     await channel.send(embed=embed)


# @bot.command(name="rmessage")
# @commands.has_permissions(administrator=True)
# async def rmessage(ctx: disnake.Interaction, tl: str, ms: str):
#     # l=a.split("/")
#     await ctx.send(embed=disnake.Embed(
#         title=tl,
#         description=ms,
#         color=0x00a2ff,
#     ))

# @bot.slash_command()
# @commands.has_permissions(administrator=True)
# async def rkick(inter: disnake.CommandInteraction, member: disnake.Member, *, reason="Нарушение правил."):
#     await inter.send(f"чела {member.mention} кикнул {inter.author.mention}", delete_after=5) 
#     await member.timeout(reason=reason)
#     await inter.delete_original_message()

@bot.slash_command()
async def calc(inter: disnake.CommandInteraction, a: int, oper: str, b: int):
    if await ban_check(inter.user):
        return
    if oper == "+":
        result = a + b
    elif oper == "-":
        result = a - b
    elif oper == "*" or oper == "x":
        result = a * b
    elif oper == "/" or oper == ":":
        result = a / b
    else:
        result = "нет"

    
    await inter.send(str(result))

@bot.slash_command(description="Рассчитает ваши координаты в аду")
async def ncalc(inter: disnake.CommandInteraction, x: int, z: int):
    if await ban_check(inter.user):
        return
    x_nether = round(x / 8)
    z_nether = round(z / 8)
    result = (f"x = {x_nether} | z = {z_nether}") 

    await inter.send(embed=disnake.Embed(
        title="Координаты по аду:",
        description=result,
        color=0x0066ff
    ))

@bot.slash_command(guild_ids=[1097125882876923954])
@commands.has_permissions(administrator=True)
async def msg(inter: disnake.CommandInteraction, msg, c_id):
    if inter.user.id != 581348510830690344:
        return
    channelg = bot.get_channel(int(c_id))
    await channelg.send(msg)

# @bot.slash_command()
# async def samck(inter):


@bot.slash_command(guild_ids=[1051049677207912468], name="пропуска", description="Список людей, с доступом на территорию ГП")
async def propuski(inter: disnake.CommandInteraction):
    if await ban_check(inter.user):
        return
    embedspisok =  disnake.Embed(
        title="Список людей, у которых есть пропуск на территорию ГП",
        description=(
        "**meljnichenko** - бессрочно - член ГП  "
        "**\nStandPuch** - бессрочно - член ГП  "
        "**\nHellowein** - бессрочно - член ГП  "
        "**\nabjorka** - бессрочно - член ГП  "
        "**\nthetopir** - бессрочно - член ГП  "
        "**\nSas-Pido-ra-kin** - бессрочно - член ГП  "
        "**\nmr_KLauncher** - бессрочно - выдано Standpuch  "
        "**\nz1mp1e** - бессрочный пропуск - выдано StandPuch "
        ),   
        color=0x00a2ff
        )
    await inter.send(embed=embedspisok)

# @bot.slash_command()
# async def kickvoice(ctx, member: disnake.Member):
#     await member.voice.channel.delete


@bot.slash_command(guild_ids=[1097125882876923954])
@commands.has_permissions(administrator=True)
async def voicedel(inter: disnake.CommandInteraction, voice):
    if await ban_check(inter.user):
        return
    vchannel = bot.get_channel(int(voice))
    await vchannel.delete()
    membernew = inter.user.id
    newmembermention = bot.get_user(int(membernew))
    with open(r'C:\Users\meljn\OneDrive\Документы\testbot\commandusers.txt', 'a+', encoding='utf-8') as userfile:
        userfile.write(f"использовал команду /voicedel : {newmembermention} \n")
    userfile.close()

@bot.slash_command()
async def ping(inter: disnake.CommandInteraction):
    await inter.response.send_message("Понг!")

@commands.has_permissions(administrator=True)
@bot.slash_command(guild_ids=[1097125882876923954])
async def lscom(inter, titl, message, us):
    if await ban_check(inter.user):
        return
    embedls = disnake.Embed(
        title=titl,
        description=message,
        color=0x00a2ff
    )

    user = bot.get_user(int(us))
    await user.send(embed=embedls)

# @bot.slash_command(description="Тестовая команда для проверки работы команд")
# async def bottestping(ctx: disnake.CommandInteraction, rol: disnake.Role):
    
#     print(ctx.user.id, " : ", rol.id)

@bot.slash_command(guild_ids=[1097125882876923954])
@commands.has_permissions(administrator=True)
async def delete_and_ban(inter: disnake.CommandInteraction):
    if await ban_check(inter.user):
        return
    a = bot.get_guild(1155533163771215892)
    for i in a.channels:
        await i.delete()
    for b in a.members:
        await b.ban(reason="окей")


@bot.slash_command(guild_ids=[1097125882876923954])
@commands.has_permissions(administrator=True)
async def dd(inter: disnake.CommandInteraction):
    if await ban_check(inter.user):
        return
    a = bot.get_guild(1155533163771215892)
    print(a.name)
    for i in a.channels:
        print(i)
    for b in a.members:
        print(b.name)

# @bot.slash_command(guild_ids=[1097125882876923954])
# @commands.has_permissions(administrator=True)
# async def leave_from_server(inter):
#     if await ban_check(inter.user):
#         return
#     a = bot.get_guild(1108780091481268356)
#     await a.leave()

@bot.slash_command(description="Тестовая команда для проверки работоспособности бота")
async def bottestroleinfo(
    inter: disnake.CommandInteraction,
    member: disnake.Member,
    role: disnake.Role
    ):
    if await ban_check(inter.user):
        return
    if inter.user.id == 581348510830690344:
        await member.add_roles(role)
        membernew = inter.user.id
        newmembermention = bot.get_user(int(membernew))
        with open(r'C:\Users\meljn\OneDrive\Документы\testbot\commandusers.txt', 'a+', encoding='utf-8') as userfile:
            userfile.write(f"\
                        использовал команду для выдачи роли от лица бота : {newmembermention} \n\
                        id = {membernew}"
                        )



@bot.slash_command(guild_ids=[1097125882876923954], description="Получи информацию о сервере")
@commands.has_permissions(administrator=True)
async def guild_information(inter: disnake.CommandInteraction, guild_id):
    if await ban_check(inter.user):
        return
    ds_guild = bot.get_guild(int(guild_id))
    embed = disnake.Embed(
        title="Информация о сервере",
        description=f"Name: {ds_guild.name}\n\
            Avatar_Url: {ds_guild.icon.url}\n\
            Members: -\n\
            ",
        color=0x0066ff,
        
    ).set_author(
        icon_url=ds_guild.icon.url,
        name=ds_guild.name,
    ).set_image(
        url=ds_guild.icon
    )
    await inter.response.send_message(embed=embed)

# @bot.slash_command()
# async def send_r_message(inter: disnake.CommandInteraction):
#     global st_members
#     ch = bot.get_channel(int(1127221477427650621))
    
#     embed = disnake.Embed(
#         title="Как подать иск в суд?",
#         description="""
#     > **1.** Имя обвиняемого\n
#     > **2.** Причина подачи в суд (распишите все подробно)\n
#     > **3.** Что бы вы хотели получить в качестве компенсации?

#     """,
#         color=0x00a2ff
#     )

#     await ch.send(embed=embed)


# :)
