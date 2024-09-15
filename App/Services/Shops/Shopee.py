import hashlib
import json
import os
import time
from datetime import datetime
from typing import List, Dict

import requests

from App.Resources.Error import CustomException
from App.Services.Shops.Shop import Shop
from App.Utils.Utils import generateUuid
from App.Models.Sale import Sale



class Shopee(Shop):
    APP_ID: str = os.getenv("SHOPEE_API_ID")
    SECRET: str = os.getenv("SHOPEE_API_SECRET_KEY")
    URL: str = "https://open-api.affiliate.shopee.com.br/graphql"

    @classmethod
    def generateSignature(cls, appId: str, payload: str, secret: str):
        timestamp = int(time.time())

        factor = appId + str(timestamp) + payload + secret

        signature = hashlib.sha256(factor.encode()).hexdigest()
        return f'SHA256 Credential={appId},Timestamp={timestamp},Signature={signature}'

    @classmethod
    def getSales(cls, pages: int = 10, salesGt: int = 1000, discountRateGt: int = 70) -> List[Sale]:
        query: str = """
        query Fetch($limit: Int, $page: Int) {
          productOfferV2(
            page: $page,
            limit: $limit,
          ) {
            nodes {
              productName
              itemId
              commissionRate
              commission
              price
              productLink
              offerLink
              imageUrl
              sales
              periodStartTime
              periodEndTime
              priceMin
              priceMax
              ratingStar
              priceDiscountRate
            }
          }
        }
        """

        allProducts: List[Sale] = []

        for x in range(1, pages):

            payloadJson: dict = {
                "query": query,
                "variables": {
                    "limit": 50,
                    "page": 1 * x,
                }
            }

            payload: str = json.dumps(payloadJson)
            payload = payload.replace('\n', '')

            headers = {
                'Content-type': 'application/json',
                'Authorization': cls.generateSignature(appId=cls.APP_ID, secret=cls.SECRET, payload=payload)
            }

            response = requests.post(cls.URL, payload, headers=headers)
            data = response.json()

            if response.status_code == 200 and data.get("data", None) is not None:
                # print(data["data"]["productOfferV2"]["nodes"][0])
                products: List[Sale] = [Sale(id=generateUuid(), name=x["productName"], website="SHOPEE",
                                             priceMin=float(x["priceMin"]), priceMax=float(x["priceMax"]),
                                             price=float(x["price"]), priceDiscountRate=x["priceDiscountRate"],
                                             periodStartTime=datetime.fromtimestamp(x["periodStartTime"]),
                                             periodEndTime=datetime.fromtimestamp(x["periodEndTime"]),
                                             commissionRate=float(x["commissionRate"]),
                                             link=x["offerLink"],
                                             imageUrl=x["imageUrl"],
                                             salesQtd=x["sales"]
                                             )
                                        for x in data["data"]["productOfferV2"]["nodes"]
                                        ]
                allProducts.extend(products)

        allProducts = list(
            filter(lambda x: x.priceDiscountRate >= discountRateGt and x.salesQtd > salesGt, allProducts))

        uniqueLinks = set()

        allProducts = list(
            filter(lambda product: product.link not in uniqueLinks and not uniqueLinks.add(product.link), allProducts))


        return allProducts
