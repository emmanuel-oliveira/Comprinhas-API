from flask import jsonify
from App.Flows.flows import handlerApprove





def approveWebhookController(chatId: str, callbackText: str):
    status, saleId = callbackText.split("|")
    handlerApprove(chatId=chatId, saleId=saleId, status=status)
    return jsonify(True), 200







