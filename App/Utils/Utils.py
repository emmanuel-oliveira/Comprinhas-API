import uuid
from datetime import datetime

import pytz

TIME_ZONE = pytz.timezone("America/Sao_Paulo")


def generateUuid() -> str:
    """
    The generateUuid function generates a random UUID string.

    :return: A string
    """
    return str(uuid.uuid4())


def getTimeNow():
    """
    No parameters.

    :return: hour (GMT-3) type(datetime)
    """
    today = datetime.now(TIME_ZONE)
    today = today.replace(tzinfo=None)
    return today