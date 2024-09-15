
import pymongo
from pymongo.client_session import ClientSession
from pymongo.database import Database
from pymongo.errors import WriteError

from App.Resources.Error import CustomException


class AdminsTransactions:
    collectionName: str = "Admins"

    @classmethod
    def getAdmin(cls, database: Database, session: ClientSession, filter: dict):
        try:
            data = database[cls.collectionName].find_one(filter,
                                                         {"_id": 0}, session=session)
            return [x for x in data]
        except pymongo.errors.ConnectionFailure as e:
            raise CustomException(message=str(e), statusCode=500)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)

    @classmethod
    def getAdmins(cls, database: Database, session: ClientSession, filter: dict):
        try:
            data = database[cls.collectionName].find(filter,
                                                         {"_id": 0}, session=session)
            return [x for x in data]
        except pymongo.errors.ConnectionFailure as e:
            raise CustomException(message=str(e), statusCode=500)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)