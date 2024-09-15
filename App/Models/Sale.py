from __future__ import annotations

from datetime import datetime

from pydantic import Field

from App.Models.Base import CustomBaseModel


class Sale(CustomBaseModel):
    id: str = Field()
    name: str = Field()
    website: str = Field()
    priceMin: float = Field()
    priceMax: float = Field()
    price: float = Field()
    priceDiscountRate: int = Field()

    periodStartTime:datetime = Field()
    periodEndTime: datetime = Field()


    salesQtd: int = Field()

    commissionRate: float = Field()
    link: str = Field()
    imageUrl: str = Field()
    sentToApproval:bool =  Field(default=False)

    messageText: str | None = Field(default=None)
    sentToGroups: bool =  Field(default=False)
    approved: bool = Field(default=False)


