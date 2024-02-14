from typing import Optional
import disnake
from disnake.ext import commands
from disnake import TextInputStyle
from disnake.interactions import MessageInteraction
from Dbot import bot
# from DbotGymnasium36_Folder.DbotOffers import OfferButton


class Bot_Reports(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.slash_command(guild_ids=[1097125882876923954])
    # async def reportnotanon(inter):
    #     view_report = ReportButton()
    #     channel_report = bot.get_channel(int(1102629461792399392))
    #     button_embed_report = disnake.Embed(
    #         title="Напиши свою жалобу!",
    #         description='Если бот в сети, то ты можешь написать жалобу президенту школы, используя кнопку "Пожаловаться" ',
    #         color=0x03fc6b
    #     )
        
    #     await channel_report.send(embed=button_embed_report, view = view_report)
    

    # @commands.slash_command(guild_ids=[1097125882876923954])
    # async def rep_offers_send(inter):
    #     view_report = ReportButton()
    #     channel_report = bot.get_channel(int(1102629461792399392))
    #     button_embed_report = disnake.Embed(
    #         title="Напиши свою жалобу!",
    #         description='Если бот в сети, то ты можешь написать жалобу президенту школы, используя кнопку "Пожаловаться" ',
    #         color=0x03fc6b
    #     )
        
    #     channel_report_anon = bot.get_channel(int(1102629782539214848))
    #     button_embed_report_anon = disnake.Embed(
    #         title="Напиши анонимную жалобу!",
    #         description='Если бот в сети, то ты можешь написать анонимную жалобу президенту школы, используя кнопку "Пожаловаться" ',
    #         color=0x03fc6b
    #     )
    #     view_offer = OfferButton()
    #     channel_offer_anon= bot.get_channel(int(1102629326236684338))
    #     button_embed_offer_anon = disnake.Embed(
    #         title="Напиши анонимное предложение для нашей школы!",
    #         description='Если бот в сети, то ты можешь написать анонимное предложение президенту школы используя кнопку "Предложить" ',
    #         color=0x03fc6b
    #     )
    #     channel_offer = bot.get_channel(int(1102629280615252029))
    #     button_embed_offer = disnake.Embed(
    #         title="Напиши предложение для нашей школы!",
    #         description='Если бот в сети, то ты можешь написать предложение президенту школы используя кнопку "Предложить" ',
    #         color=0x03fc6b
    #     )
        
    #     await channel_report.send(embed=button_embed_report, view = view_report)
    #     await channel_report_anon.send(embed=button_embed_report_anon, view = view_report)
    #     await channel_offer_anon.send(embed=button_embed_offer_anon, view = view_offer)
    #     await channel_offer.send(embed=button_embed_offer, view = view_offer)

    # @commands.slash_command(guild_ids=[1097125882876923954])
    # async def reportannon(inter):
    #     view = ReportButton()
    #     channelanon = bot.get_channel(int(1102629782539214848))
    #     button_embed = disnake.Embed(
    #         title="Напиши анонимную жалобу!",
    #         description='Если бот в сети, то ты можешь написать анонимную жалобу президенту школы, используя кнопку "Пожаловаться" ',
    #         color=0x03fc6b
    #     )
        
    #     await channelanon.send(embed=button_embed, view = view)


class ReportsModal(disnake.ui.Modal):
    def __init__(self):
        global components_reports
        components_reports = [
            disnake.ui.TextInput(
                label="Опиши свою жалобу",
                placeholder="Опиши свою жалобу максимально подробно",
                custom_id="описаниe",
                style=TextInputStyle.paragraph,
                max_length=1000,
            ),
            disnake.ui.TextInput(
                label="Оцени важность своей жалобы",
                placeholder="?/10",
                custom_id="оценка",
                style=TextInputStyle.short,
                max_length=2,
            ),
        ]
        super().__init__(
            title="Напиши жалобу",
            custom_id="create_report",
            components=components_reports,
        )
    
    # global offerwriter
    async def callback(self, inter: disnake.ModalInteraction):
        report_writer = inter.user.id
        embed = disnake.Embed(
            title="Новая жалоба",
            description=(f"<@{report_writer}> написал жалобу!"),
            color=0x8400ff
            )
        
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        
        admin_channel = bot.get_channel(int(1141835778528383036))
        # print(components_reports)
        await admin_channel.send(embed=embed)
        await inter.response.send_message(f" <@{report_writer}>, жалоба отправлена!", ephemeral=True)


# class ReportButton(disnake.ui.View): 

#     def __init__(self):
#         super().__init__(timeout=None)
#         self.value = Optional[bool]

#     @disnake.ui.button(label="Пожаловаться", style=disnake.ButtonStyle.green, emoji="✍️")
#     async def offerbutt(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
#         self.value = True
#         await inter.response.send_modal(modal=ReportsModal())

#     async def interaction_check(self, interaction: MessageInteraction):
        
#         global reportwriter
#         reportwriter = interaction.user.id

#         return await super().interaction_check(interaction)