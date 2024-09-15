from App import app
from App.Controller.salesController import findSalesController, sendSaleToAdminsController, \
    generateTextForSales


@app.route("/sales", methods=["GET"])
def findSalesRoute():
    return findSalesController()



@app.route("/sales/generate/text", methods=["POST"])
def generateText():
    return generateTextForSales()


@app.route("/sales/send/admins", methods=["POST"])
def sendPromotionToAdmins():
    return sendSaleToAdminsController()
