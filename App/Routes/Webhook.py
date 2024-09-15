from flask import request

from App import app
from App.Controller.approveController import approveWebhookController
from App.Middleware.identifyRequest import identifyRequest
from App.Middleware.isAdmin import isAdmin


@app.route("/webhook", methods=["POST"])
@identifyRequest()
@isAdmin()
def webhook(**kwargs):
    content: dict = request.json
    callbackText: str = content["callback_query"]["data"]
    chatId: str= str(content["callback_query"]["from"]["id"])
    return approveWebhookController(chatId=chatId, callbackText=callbackText)
