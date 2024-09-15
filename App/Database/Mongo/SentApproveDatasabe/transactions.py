import pymongo
from pymongo.client_session import ClientSession
from pymongo.database import Database
from pymongo.errors import WriteError

from App.Resources.Error import CustomException
from App.Utils.Utils import getTimeNow, generateUuid


class SentApproveTransactions:
    collectionName: str = "SentApprove"

    @classmethod
    def createSentApprove(cls, database: Database, session: ClientSession, id: str, saleId: str, chatId: str, platform: str, messageId: str, ended:bool):
        try:



            database[cls.collectionName].insert_one({"id": id,
                                               "chatId": chatId,
                                               "messageId": messageId,
                                               "saleId": saleId,
                                               "platform": platform,
                                               "ended": ended,
                                               "createdAt": getTimeNow()
                                               }, session=session)

        except WriteError as e:
            raise CustomException(message=str(e), statusCode=500)
        except pymongo.errors.ConnectionFailure as e:
            raise CustomException(message=str(e), statusCode=500)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)


    @classmethod
    def getSaleSent(cls, database: Database, session: ClientSession, filter: dict):
        try:
            data = database[cls.collectionName].find(filter,
                                                         {"_id": 0}, session=session)
            return [x for x in data]
        except pymongo.errors.ConnectionFailure as e:
            raise CustomException(message=str(e), statusCode=500)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)


    @classmethod
    def updateRegistry(cls, database: Database, session: ClientSession, filter: dict, dataToUpdate: dict):
        try:
            database[cls.collectionName].update_many(filter, {"$set": dataToUpdate}, session=session)

        except WriteError as e:
            raise CustomException(message=str(e), statusCode=500)
        except pymongo.errors.ConnectionFailure as e:
            raise CustomException(message=str(e), statusCode=500)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)