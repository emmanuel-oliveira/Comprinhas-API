from dataclasses import dataclass

from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from App.Resources.Error import CustomException
from App.Resources.prompts import SYSTEM_PROMPT_PROMO_TEXT, PROMPT_PROMO_ASSISTANT, PROMPT_REFINE_PROMO_ASSISTANT


@dataclass()
class PROMPT:
    SYSTEM: SystemMessagePromptTemplate
    PROMPT: HumanMessagePromptTemplate


class PROMPTS:
    PROMO_ASSISTANT: PROMPT = PROMPT(
        SYSTEM=SystemMessagePromptTemplate.from_template(template=SYSTEM_PROMPT_PROMO_TEXT),
        PROMPT=HumanMessagePromptTemplate.from_template(
            template=PROMPT_PROMO_ASSISTANT,
            input_variables=["saleInfo"]))

    REFINE_PROMO_ASSISTANT: PROMPT = PROMPT(
        SYSTEM=SystemMessagePromptTemplate.from_template(template=SYSTEM_PROMPT_PROMO_TEXT),
        PROMPT=HumanMessagePromptTemplate.from_template(
            template=PROMPT_REFINE_PROMO_ASSISTANT,
            input_variables=["oldText", "saleInfo"]))


def promptHandler(taskName: str):
    try:
        HANDLER: dict = {"makeSaleText": PROMPTS.PROMO_ASSISTANT,
                         "refineSaleText": PROMPTS.REFINE_PROMO_ASSISTANT}
        return HANDLER[taskName]
    except KeyError as e:
        raise CustomException(message=f"A task '{taskName}' não está disponível", statusCode=400)
