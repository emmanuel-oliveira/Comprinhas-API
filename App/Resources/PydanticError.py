from __future__ import annotations

pydanticErrors = {
    "greater_than_equal": "Campo '{fieldName}' inválido, dever ser maior que {ge}",
    "less_than_equal": "Campo '{fieldName}' inválido, dever ser menor que {le}",
    "missing": "Campo '{fieldName}' faltando",
    "string_pattern_mismatch": "{fieldName} inválido",
    "float_type": "{fieldName} deve ser float"
}


def parseErrorPydantic(fieldName: str, type: str, message: str, input, context: dict | None) -> str:
    try:

        error = pydanticErrors[type]
        newMessage = error.format(**context, fieldName=fieldName)
        return newMessage

    except KeyError as e:
        return f"Erro no campo {str(e)}"