from sys import platform

from pymongo.errors import PyMongoError

from App.Database.Mongo.MongoDB import MongoDBConnection
from App.Database.Mongo.SentApproveDatasabe.transactions import SentApproveTransactions
from App.Logging.Logging import LOGGER
from App.Resources.Error import CustomException
from App.Utils.Utils import generateUuid


class SentApproveDatabase(MongoDBConnection):

    @classmethod
    def addSentRegistry(cls, messageId: str, chatId: str, saleId: str, platform: str, ended: bool):
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                   SentApproveTransactions.createSentApprove(
                       database=cls.db,
                           id=generateUuid(),
                           session=sessionDB,
                           messageId=messageId,
                           chatId=chatId,
                           platform=platform,
                           saleId=saleId,
                          ended=ended
                   )
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
    def getSentRegistry(cls, saleId: str, ended: bool):
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                    data = SentApproveTransactions.getSaleSent(database=cls.db, session=sessionDB, filter={"saleId": saleId, "ended": ended})

                    return data

                #{"promotionId": saleId, "replaced": False}
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
    def updateRegistryEndStatus(cls, saleId: str, ended: bool):
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                    SentApproveTransactions.updateRegistry(database=cls.db, session=sessionDB,
                                                           filter={"saleId": saleId},
                                                           dataToUpdate={"ended": ended}
                                                                  )
        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            print(e)
            raise e