from App.Database.Mongo.SalesDatabase.SalesDatabase import SalesDatabase
from App.Flows.salesFlow import SALE_APPROVE_FLOWS
from App.Models.Sale import Sale


def handlerApprove(chatId: str, saleId: str, status: str):
    sale: Sale = SalesDatabase.getSaleReadyToSend(saleId=saleId)
    SALE_APPROVE_FLOWS[status](chatId=chatId, sale=sale)