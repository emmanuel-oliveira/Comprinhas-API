from typing import Tuple
from flask.wrappers import Response as FlaskResponse

from flask import jsonify


class CustomException(Exception):
    def __init__(self, message: str, statusCode: int, name: str = None, content: str = None):
        self.message = message
        self.statusCode = statusCode
        self.name = name
        self.content = content
        super().__init__()

    def __str__(self) -> str:
        return self.message

    def jsonify(self) -> Tuple[FlaskResponse, int]:
        return jsonify({"message": self.message}), self.statusCode


def callCustomError(message: str, statusCode: int) -> None:
    raise CustomException(message=message, statusCode=statusCode)