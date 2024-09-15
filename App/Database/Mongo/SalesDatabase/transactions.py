import pymongo
from pymongo.client_session import ClientSession
from pymongo.database import Database
from pymongo.errors import WriteError

from App.Models.Sale import Sale
from App.Resources.Error import CustomException
from App.Utils.Utils import getTimeNow


class SalesTransactions:
    collectionName: str = "Sales"



    @classmethod
    def createSale(cls, database: Database, session: ClientSession, sale: Sale, **kwargs):
        try:

            payload: dict = {**sale.model_dump(exclude_none=True), **kwargs, **{"createdAt": getTimeNow()}}

            database[cls.collectionName].insert_one(document=payload, session=session)

        except WriteError as e:
            raise CustomException(message=str(e), statusCode=500)
        except pymongo.errors.ConnectionFailure as e:
            raise CustomException(message=str(e), statusCode=500)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)


    @classmethod
    def getSaleExistByLinkAndValidTime(cls, database: Database, session: ClientSession, productLink: str, periodEndTime: int):
        try:
            data = database[cls.collectionName].find_one({"link": productLink,
                                                                "periodEndTime": {"$gt": periodEndTime}},
                                                         {"_id": 0}, session=session)
            return data
        except pymongo.errors.ConnectionFailure as e:
            raise CustomException(message=str(e), statusCode=500)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)



    @classmethod
    def getSales(cls, database: Database, session: ClientSession, filter: dict):
        try:
            data = database[cls.collectionName].find(filter,
                                                         {"_id": 0}, session=session)
            return [x for x in data]
        except pymongo.errors.ConnectionFailure as e:
            raise CustomException(message=str(e), statusCode=500)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)


    @classmethod
    def getSale(cls, database: Database, session: ClientSession, filter: dict):
        try:
            data = database[cls.collectionName].find_one(filter,
                                                         {"_id": 0}, session=session)
            return data
        except pymongo.errors.ConnectionFailure as e:
            raise CustomException(message=str(e), statusCode=500)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)


    @classmethod
    def updateSale(cls, database: Database, session: ClientSession, filter: dict, dataToUpdate: dict):
        try:
            database[cls.collectionName].update_one(filter,
                                                         {"$set": dataToUpdate}, session=session)

        except WriteError as e:
            raise CustomException(message=str(e), statusCode=500)
        except pymongo.errors.ConnectionFailure as e:
            raise CustomException(message=str(e), statusCode=500)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)





