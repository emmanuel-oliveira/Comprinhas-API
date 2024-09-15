import functools

from flask import request, jsonify

from App.Logging.Logging import LOGGER
from App.Services.SocialNetworks.Telegram.telegram import TelegramMessenger


def identifyRequest():
    def wrapper(fn):
        @functools.wraps(fn)
        def decorator(*args, **kwargs):
            try:
                content: dict = request.json
                messageType: str = TelegramMessenger.identifyRequest(request=content)
                if messageType not in ["interactive"]:
                    LOGGER.log("DESCARTANDO MENSAGEM, FORMATO INVÁLIDO")
                    return jsonify(True), 200
                content["messageType"] = messageType
                return fn(messageType=messageType)
            except Exception as e:
                print(e)
                data = {
                    "message": str(e)
                }
                return jsonify(data), 200

        return decorator

    return wrapper