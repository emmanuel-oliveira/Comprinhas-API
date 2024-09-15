import os
from typing import List

from App.Database.Mongo.AdminsDatabase.AdminsDatabase import AdminsDatabase
from App.Database.Mongo.SalesDatabase.SalesDatabase import SalesDatabase
from App.Database.Mongo.SentApproveDatasabe.SentApproveDatabase import SentApproveDatabase
from App.Logging.Logging import LOGGER
from App.Models.Admin import Admin
from App.Models.Sale import Sale
from App.Resources.Buttons import ADMIN_APPROVE_BUTTONS
from App.Resources.Strings import SALE_INFO_TEXT, SALE_INFO_METADATA
from App.Services.LLM.Gemini import Gemini
from App.Services.LLM.Prompt import PROMPT, promptHandler
from App.Services.SocialNetworks.Telegram.telegram import TelegramMessenger



def approveSaleFlow(chatId: str, sale: Sale):
    LOGGER.info("LISTANDO OS ADMINS DOS QUAIS FOI ENVIADO A PROMOÇÃO PARA APROVAÇÃO")

    registries = SentApproveDatabase.getSentRegistry(saleId=sale.id, ended=False)

    for registry in registries:
        TelegramMessenger.clearMessageButton(chatId=registry["chatId"], messageId=registry["messageId"],
                                             botKey=os.getenv("TELEGRAM_API_ADMIN"))


        TelegramMessenger.sendSimpleMessage(userId=registry["chatId"],
                                            botKey=os.getenv("TELEGRAM_API_ADMIN"),
                                            message=sale.messageText + "\n APROVADO")

        TelegramMessenger.deleteMessage(chatId=registry["chatId"], messageId=registry["messageId"],
                                        botKey=os.getenv("TELEGRAM_API_ADMIN"))


    LOGGER.info("ENVIANDO A PROMOÇÃO PARA O CANAL")

    SentApproveDatabase.updateRegistryEndStatus(saleId=sale.id, ended=True)

    TelegramMessenger.sendMessageWithButtonsAndImage(userId=os.getenv("TELEGRAM_CHANNEL_ID"),
                                                     botKey=os.getenv("TELEGRAM_API_BOT_SENDER"),
                                                     imageUrl=sale.imageUrl, buttons=[],
                                                     text=sale.messageText)


def refineSaleFlow(chatId: str, sale: Sale):
    admins: List[Admin] = AdminsDatabase.getAdmins()

    registries = SentApproveDatabase.getSentRegistry(saleId=sale.id, ended=False)

    LOGGER.info("REMOVENDO A MENSAGEM ANTIGA DO CHAT DOS ADMINS PARA SUBSTITUIR POR UMA NOVA")
    for registry in registries:

        TelegramMessenger.clearMessageButton(chatId=registry["chatId"], messageId=registry["messageId"],
                                             botKey=os.getenv("TELEGRAM_API_ADMIN"))


        TelegramMessenger.deleteMessage(chatId=registry["chatId"], messageId=registry["messageId"],
                                        botKey=os.getenv("TELEGRAM_API_ADMIN"))


    SentApproveDatabase.updateRegistryEndStatus(saleId=sale.id, ended=True)

    prompt: PROMPT = promptHandler(taskName="refineSaleText")


    saleInfo = SALE_INFO_TEXT.format(
        productName=sale.name,
        price=sale.price,
        priceMax=sale.priceMax,
        link=sale.link,
        periodStartTime=sale.periodStartTime,
        periodEndTime=sale.periodEndTime,
        priceMin=sale.priceMin
    )


    LOGGER.info("GERANDO NOVO TEXTO")

    text: str = Gemini.task(prompt=prompt, arguments={"saleInfo": saleInfo, "oldText": sale.messageText},
                            maxTokens=250)


    SalesDatabase.updateSaleMessage(saleId=sale.id, message=text)

    LOGGER.info("FORMATANDO A MENSAGEM NOVA")


    buttons = [{"text": x["text"], "callback_data": x["callback_data"].format(saleId=sale.id)} for
               x
               in ADMIN_APPROVE_BUTTONS]


    LOGGER.info("ENVIANDO A PROMOÇÃO COM NOVO TEXTO PARA TODOS OS ADMINS")
    for admin in admins:

        message: str = text + SALE_INFO_METADATA.format(
                    priceMin=sale.priceMin, priceMax=sale.priceMax, price=sale.price,  periodEndTime=sale.periodEndTime.strftime('%d/%m/%Y %H:%M:%S'), priceDiscountRate=sale.priceDiscountRate
                ) + "\nPRODUTO COM MENSAGEM REFINADA"

        messageId: str = TelegramMessenger.sendMessageWithButtonsAndImage(userId=admin.chatId,
                                                                          botKey=os.getenv("TELEGRAM_API_ADMIN"),
                                                                          imageUrl=sale.imageUrl,
                                                                          buttons=buttons,
                                                                          text=message)



        SentApproveDatabase.addSentRegistry(chatId=admin.chatId, messageId=messageId,
                                              saleId=sale.id,
                                              ended=False,
                                              platform="Telegram")



def declineSaleFlow(chatId:str, sale: Sale):

    registries = SentApproveDatabase.getSentRegistry(saleId=sale.id, ended=False)


    LOGGER.info("REMOVENDO A MENSAGEM DO CHAT DE TODOS OS ADMINS QUE RECEBERAM")

    for registry in registries:
        TelegramMessenger.clearMessageButton(chatId=registry["chatId"], messageId=registry["messageId"],
                                                     botKey=os.getenv("TELEGRAM_API_ADMIN"))

        TelegramMessenger.deleteMessage(chatId=registry["chatId"], messageId=registry["messageId"],
                                        botKey=os.getenv("TELEGRAM_API_ADMIN"))

    SentApproveDatabase.updateRegistryEndStatus(saleId=sale.id, ended=True)

    SalesDatabase.updateApproveStatus(saleId=sale.id, approvedBy=chatId, approved=True, sentToGroups=True)



SALE_APPROVE_FLOWS= {
    "approve": approveSaleFlow,
    "refine": refineSaleFlow,
    "decline": declineSaleFlow
}



