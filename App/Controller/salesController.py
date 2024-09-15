import os
from typing import Tuple, List

from flask import jsonify
from flask.wrappers import Response as FlaskResponse
from pydantic import ValidationError

from App.Database.Mongo.AdminsDatabase.AdminsDatabase import AdminsDatabase
from App.Database.Mongo.SalesDatabase.SalesDatabase import SalesDatabase
from App.Database.Mongo.SentApproveDatasabe.SentApproveDatabase import SentApproveDatabase
from App.Logging.Logging import LOGGER
from App.Models.Admin import Admin
from App.Models.Sale import Sale
from App.Resources.Buttons import ADMIN_APPROVE_BUTTONS
from App.Resources.Error import CustomException
from App.Resources.PydanticError import parseErrorPydantic
from App.Resources.Strings import SALE_INFO_METADATA, SALE_INFO_TEXT
from App.Services.LLM.Gemini import Gemini
from App.Services.LLM.Prompt import promptHandler, PROMPT
from App.Services.Shops.Shopee import Shopee
from App.Services.SocialNetworks.Telegram.telegram import TelegramMessenger


def findSalesController() -> Tuple[FlaskResponse, int]:
    try:

        LOGGER.log("BUSCANDO PROMOÇÕES")
        sales: List[Sale] = Shopee.getSales(pages=10, salesGt=1000, discountRateGt=70)

        if not sales:
            raise CustomException(message="Nenhuma promoção atende os requisitos", statusCode=204)

        LOGGER.log("REGISTRANDO PROMOÇÕES ENCONTRADAS")

        SalesDatabase.createSales(sales=sales)

        return jsonify({"data": {"sales": [x.model_dump(exclude_none=False) for x in sales]}}), 200

    except ValidationError as e:
        pydanticError = e.errors()[0]
        print(pydanticError)
        return CustomException(
            message=parseErrorPydantic(fieldName=pydanticError["loc"][0], type=pydanticError["type"],
                                       message=pydanticError["msg"],
                                       input=pydanticError["input"],
                                       context=pydanticError.get("ctx", {})),
            statusCode=400).jsonify()
    except CustomException as e:
        print(e)
        return e.jsonify()
    except Exception as e:
        print(e)
        return jsonify(e), 500


def generateTextForSales() -> Tuple[FlaskResponse, int]:
    try:

        LOGGER.log("LISTANDO PROMOÇÕES SEM TEXTO")

        sales = SalesDatabase.getSalesNotSent()

        if not sales:
            raise CustomException(message="Nenhuma promoção sem texto", statusCode=204)


        prompt: PROMPT = promptHandler(taskName="makeSaleText")

        LOGGER.log("GERANDO TEXTO PARA AS PROMOÇÕES")
        for sale in sales:
            saleInfoText: str = SALE_INFO_TEXT.format(
                productName=sale.name,
                price=sale.price,
                priceMax=sale.priceMax,
                link=sale.link,
                periodStartTime=str(sale.periodStartTime),
                periodEndTime=str(sale.periodEndTime),
                priceMin=sale.priceMin
            )

            text: str = Gemini.task(prompt=prompt, arguments={"saleInfo": saleInfoText}, maxTokens=250)

            sale.messageText = text
            SalesDatabase.updateSalesMessage(sale=sale)

        return jsonify({"sales": [x.model_dump(exclude_none=True) for x in sales]}), 200
    except CustomException as e:
        print(e)
        return e.jsonify()
    except Exception as e:
        print(e)
        return jsonify(e), 500


def sendSaleToAdminsController() -> Tuple[FlaskResponse, int]:
    try:

        LOGGER.log("LISTANDO OS ADMINS PARA ENVIO DA APROVAÇÃO")
        admins: List[Admin] = AdminsDatabase.getAdmins()


        LOGGER.log("LISTANDO AS PROMOS NÃO ENVIADAS PARA APROVAÇÃO")
        sales: List[Sale] = SalesDatabase.getSalesToSendToApprove()

        if not sales:
            raise CustomException("Não há promoções a serem enviadas", statusCode=204)

        LOGGER.log("ENVIANDO AS PROMOS PARA OS ADMINS")
        for sale in sales:
            for admin in admins:
                buttons = [{"text": x["text"], "callback_data": x["callback_data"].format(saleId=sale.id)} for
                           x
                           in ADMIN_APPROVE_BUTTONS]

                # mensagem que será enviada + algumas informações para ajudar na aprovação da tomada de decisão

                message: str = sale.messageText + SALE_INFO_METADATA.format(
                    priceMin=sale.priceMin, priceMax=sale.priceMax, price=sale.price,  periodEndTime=sale.periodEndTime.strftime('%d/%m/%Y %H:%M:%S'), priceDiscountRate=sale.priceDiscountRate
                )

                messageId: str = TelegramMessenger.sendMessageWithButtonsAndImage(text=message,
                                                                                  userId=admin.chatId,
                                                                                  buttons=buttons,
                                                                                  imageUrl=sale.imageUrl,
                                                                                  botKey=os.getenv(
                                                                                      "TELEGRAM_API_ADMIN"))

                sale.sentToApproval = True

                SalesDatabase.updateSalesStatusSent(sale=sale)

                SentApproveDatabase.addSentRegistry(chatId=admin.chatId, messageId=messageId,
                                                      saleId=sale.id,
                                                      platform="Telegram", ended=False)

        return jsonify({"text": True}), 200
    except CustomException as e:
        print(e)
        return e.jsonify()
    except Exception as e:
        print(e)
        return jsonify(e), 500
