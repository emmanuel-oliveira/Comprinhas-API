from __future__ import annotations

import functools

from flask import request, jsonify

from App.Database.Mongo.AdminsDatabase.AdminsDatabase import AdminsDatabase
from App.Logging.Logging import LOGGER
from App.Models.Admin import Admin
from App.Services.SocialNetworks.Telegram.telegram import TelegramMessenger


def isAdmin():
    def wrapper(fn):
        @functools.wraps(fn)
        def decorator(*args, **kwargs):
            try:
                content: dict = request.json
                admin: Admin | None = AdminsDatabase.getAdmin(chatId=str(content["callback_query"]["from"]["id"]))

                if admin is None:
                    LOGGER.log("DESCARTANDO MENSAGEM, NÃO É ADMIN")
                    return jsonify(True), 200

                return fn(**kwargs)
            except Exception as e:
                print(e)
                data = {
                    "message": str(e)
                }
                return jsonify(data), 200

        return decorator

    return wrapper
