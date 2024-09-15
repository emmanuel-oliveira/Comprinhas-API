from __future__ import annotations

from typing import List

from pymongo.errors import PyMongoError

from App.Database.Mongo.SalesDatabase.transactions import SalesTransactions
from App.Database.Mongo.MongoDB import MongoDBConnection
from App.Logging.Logging import LOGGER
from App.Models.Sale import Sale
from App.Resources.Error import CustomException
from App.Utils.Utils import getTimeNow


class SalesDatabase(MongoDBConnection):

    @classmethod
    def createSales(cls, sales: List[Sale]):
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                    for sale in sales:
                        data = SalesTransactions.getSaleExistByLinkAndValidTime(database=cls.db, session=sessionDB, productLink=sale.link, periodEndTime=getTimeNow())
                        if not data:
                            SalesTransactions.createSale(database=cls.db, session=sessionDB, sale=sale)
        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            print(e)
            raise e


    @classmethod
    def getSalesNotSent(cls) -> List[Sale]:
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                    data = SalesTransactions.getSales(database=cls.db, session=sessionDB, filter={"messageText": None, "sentToApproval": False, "periodEndTime": {"$gt": getTimeNow()}})

                    sales: List[Sale] = [Sale(**x) for x in data]

                    return sales
        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            print(e)
            raise e



    @classmethod
    def updateSalesMessage(cls, sale: Sale) -> None:
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                   SalesTransactions.updateSale(database=cls.db, session=sessionDB, filter={"id": sale.id}, dataToUpdate={"messageText": sale.messageText})
        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            print(e)
            raise e


    @classmethod
    def getSalesToSendToApprove(cls) -> List[Sale]:
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                    data = SalesTransactions.getSales(database=cls.db, session=sessionDB, filter={"sentToApproval": False, "approved": False, "sentToGroups": False, "messageText": {"$ne": None}})

                    sales: List[Sale] = [Sale(**x) for x in data]

                    return sales
        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            print(e)
            raise e


    @classmethod
    def updateSalesStatusSent(cls, sale: Sale) -> None:
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                   SalesTransactions.updateSale(database=cls.db, session=sessionDB, filter={"id": sale.id}, dataToUpdate={"sentToApproval": sale.sentToApproval})
        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            print(e)
            raise e

    @classmethod
    def getSaleReadyToSend(cls, saleId: str) -> Sale:
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                    data = SalesTransactions.getSale(database=cls.db, session=sessionDB, filter={"id": saleId, "approved": False, "sentToGroups": False})

                    sale: Sale = Sale(**data)

                    return sale
        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            print(e)
            raise e

    @classmethod
    def updateApproveStatus(cls, saleId, approved: bool, sentToGroups: bool, approvedBy: str):
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                    SalesTransactions.updateSale(database=cls.db, session=sessionDB, filter={"id": saleId},
                                                 dataToUpdate={"approved": approved, "sentToGroups": sentToGroups,
                                                               "approvedBy": approvedBy})


        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            print(e)
            raise e


    @classmethod
    def updateSaleMessage(cls, saleId: str, message: str, approved: bool = False, sentToGroups: bool = False):
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                    SalesTransactions.updateSale(database=cls.db, session=sessionDB, filter={"id": saleId, "approved": approved, "sentToGroups": sentToGroups}, dataToUpdate={"message": message})


        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            print(e)
            raise e