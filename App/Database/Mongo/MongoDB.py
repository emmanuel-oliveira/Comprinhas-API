import os

from pymongo import MongoClient
from pymongo.database import Database

DATABASE: str = "COMPRINHAS"


class MongoDBConnection:
    client: MongoClient = MongoClient(os.getenv("MONGO_URL"))
    db: Database = client[DATABASE]