from pydantic import Field

from App.Models.Base import CustomBaseModel


class Admin(CustomBaseModel):
    chatId: str = Field()
    name: str = Field()