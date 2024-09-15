from __future__ import annotations

from typing import List

from pymongo.errors import PyMongoError

from App.Database.Mongo.AdminsDatabase.transactions import AdminsTransactions
from App.Database.Mongo.MongoDB import MongoDBConnection
from App.Logging.Logging import LOGGER
from App.Models.Admin import Admin
from App.Resources.Error import CustomException


class AdminsDatabase(MongoDBConnection):


    @classmethod
    def getAdmin(cls, chatId: str) -> Admin | None:
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                    data = AdminsTransactions.getAdmin(database=cls.db, session=sessionDB, filter={"chatId": chatId})

                    return None if data is None else Admin(**data)
        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            LOGGER.error(e)
            raise e

    @classmethod
    def getAdmins(cls) -> List[Admin]:
        try:
            with cls.client.start_session() as sessionDB:
                with sessionDB.start_transaction():
                    data = AdminsTransactions.getAdmins(database=cls.db, session=sessionDB, filter={})


                    admins = [Admin(**admin) for admin in data]
                    return admins
        except PyMongoError as e:
            LOGGER.error(e)
            raise CustomException(message=str(e), statusCode=500)
        except CustomException as e:
            LOGGER.error(e.message)
            raise e
        except Exception as e:
            LOGGER.error(e)
            raise e