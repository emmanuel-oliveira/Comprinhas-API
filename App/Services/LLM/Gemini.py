from __future__ import annotations

import os
from abc import ABC

import google.generativeai as genai
from google.generativeai import GenerativeModel
from google.generativeai.types import HarmBlockThreshold, HarmCategory

from App.Resources.Error import CustomException
from App.Services.LLM.LLM import LLM
from App.Services.LLM.Prompt import PROMPT

API_KEY: str = os.getenv("GEMINI_API_KEY")


class Gemini(LLM, ABC):
    modelName: str = "gemini-1.5-flash"
    genai.configure(api_key=API_KEY)
    model: GenerativeModel = genai.GenerativeModel(modelName)

    @classmethod
    def run(cls, prompt: PROMPT, maxTokens: int = 512, arguments: dict | None = None) -> str:
        try:
            if arguments is None:
                arguments = {}

            fullPrompt: str = prompt.SYSTEM.prompt.template + prompt.PROMPT.prompt.template.format(**arguments)

            response = cls.model.generate_content(contents=fullPrompt,
                                                  generation_config=genai.types.GenerationConfig(temperature=0.9,
                                                                                     max_output_tokens=maxTokens,
                                                                                     top_p=1, top_k=32),
                                                  safety_settings={
                                                      HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                                      HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                                      HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                                      HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                                  })


            return response.text
        except KeyError as e:
            print(e)
            raise CustomException(message="O prompt precisa dos argumentos [{arguments}]".format(
                arguments=e.args[0]), statusCode=400)

    @classmethod
    def task(cls, prompt: PROMPT, arguments: dict, maxTokens: int = 512) -> str:
        try:
            response = cls.run(prompt=prompt, maxTokens=maxTokens, arguments=arguments)
            return response
        except KeyError as e:
            raise CustomException(message="O prompt precisa dos argumentos [{arguments}]".format(
                arguments=e.args[0]), statusCode=400)
        except CustomException as e:
            raise CustomException(message=e.message, statusCode=e.statusCode)