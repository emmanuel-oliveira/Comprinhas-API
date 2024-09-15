import os

import requests

from App.Resources.Error import CustomException




class TelegramMessenger:
    URL_TELEGRAM: str = os.getenv("TELEGRAM_BASE_URL")

    def __init__(self, telegramId: str):
        self.telegramId = telegramId

    @classmethod
    def sendTextMessage(cls, text: str):
        try:
            message = {
                "chat_id": "6760193852",
                "text": text,
            }
            r = requests.post(cls.URL_TELEGRAM + "/sendMessage", json=message)
            if r.status_code != 200:
                raise CustomException(message=r.json()["description"], statusCode=r.status_code)
        except CustomException as e:
            raise CustomException(message=e.message, statusCode=e.statusCode)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=200)

    def clearMessageButton(self):
        try:
            message = {
                "chat_id": self.chatId,
                "message_id": self.messageId,
                "reply_markup": {
                    "inline_keyboard":
                        []
                }
            }

            r = requests.post(self.URL_TELEGRAM + "/editMessageReplyMarkup", json=message)
            if r.status_code != 200:
                raise CustomException(message=r.json()["description"], statusCode=r.status_code)
        except CustomException as e:
            raise CustomException(message=e.message, statusCode=e.statusCode)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)

    @classmethod
    def sendSimpleMessage(cls, userId: str, message: str, botKey: str):
        """
        It sends a simple text message to a user

        :param userId: The user's Telegram ID
        :type userId: str
        :param message: The text of the message to be sent
        :type message: str
        """
        try:
            message = {
                "chat_id": int(userId),
                "text": message,
            }
            r = requests.post(cls.URL_TELEGRAM + botKey + "/sendMessage", json=message)
            print(r.json())
            if r.status_code != 200:
                raise CustomException(message=r.json()["description"], statusCode=r.status_code)
        except CustomException as e:
            raise CustomException(message=e.message, statusCode=e.statusCode)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)

    @classmethod
    def sendMessageWithButtons(cls, userId: str, text: str, buttons: list):
        try:
            message = {
                "chat_id": userId,
                "text": text,
                "reply_markup": {
                    "inline_keyboard":
                        [
                            [
                                {"text": "Botão 1", "callback_data": "botao1"},
                                {"text": "Botão 2", "callback_data": "botao2"}
                            ],
                            [
                                {"text": "Botão 3", "callback_data": "botao3"}
                            ]
                        ]
                }
            }

            r = requests.post(cls.URL_TELEGRAM + "/sendMessage", json=message)
            print(r)
            if r.status_code != 200:
                raise CustomException(message=r.json()["description"], statusCode=r.status_code)
        except CustomException as e:
            raise CustomException(message=e.message, statusCode=e.statusCode)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)

    @classmethod
    def sendMessageWithButtonsAndImage(cls, userId: str, text: str, buttons: list, imageUrl: str, botKey: str):
        try:
            message = {
                "chat_id": userId,
                "photo": imageUrl,
                "caption": text,
                "parse_mode": "Markdown",
                "reply_markup": {
                    "inline_keyboard":
                        [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
                }
            }

            r = requests.post(cls.URL_TELEGRAM + botKey + "/sendPhoto", json=message)

            if r.status_code != 200:
                raise CustomException(message=r.json()["description"], statusCode=r.status_code)

            response = r.json()
            return response['result']["message_id"]
        except CustomException as e:
            raise CustomException(message=e.message, statusCode=e.statusCode)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)

    @classmethod
    def clearMessageButton(cls, chatId: str, messageId: str, botKey: str):
        try:
            message = {
                "chat_id": chatId,
                "message_id": messageId,
                "reply_markup": {
                    "inline_keyboard":
                        []
                }
            }

            r = requests.post(cls.URL_TELEGRAM + botKey + "/editMessageReplyMarkup", json=message)
            if r.status_code != 200:
                raise CustomException(message=r.json()["description"], statusCode=r.status_code)
        except CustomException as e:
            raise CustomException(message=e.message, statusCode=e.statusCode)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)

    @classmethod
    def deleteMessage(cls, chatId: str, messageId: str, botKey: str):
        try:
            message = {
                "chat_id": chatId,
                "message_id": messageId,
            }

            r = requests.post(cls.URL_TELEGRAM + botKey + "/deleteMessage", json=message)
            if r.status_code != 200:
                raise CustomException(message=r.json()["description"], statusCode=r.status_code)
        except CustomException as e:
            raise CustomException(message=e.message, statusCode=e.statusCode)
        except Exception as e:
            raise CustomException(message=str(e), statusCode=500)

    @classmethod
    def identifyRequest(cls, request: dict) -> str:
        """
        The identifyRequest function is used to identify the type of request that was sent by the user.
        It returns a string with one of these values: &quot;command&quot;, &quot;text&quot;, &quot;voice&quot;, &quot;sticker&quot; or None.

        :param cls: Pass the class itself to the function
        :param request: dict: Get the request from telegram
        :return: A string that identifies the type of request
        """
        print(request)
        if request.get("message", {}).get("text", None) is not None:
            return "text"
        if request.get("message", {}).get("voice", None) is not None:
            return "voice"
        if request.get("message", {}).get("sticker", None) is not None:
            return "sticker"
        if request.get("message", {}).get("photo", None) is not None:
            return "photo"
        if request.get("message", {}).get("document", None) is not None:
            # especificar o tipo de documento
            return "document"
        if request.get("callback_query", {}).get("message", {}).get("reply_markup", None) is not None:
            return "interactive"