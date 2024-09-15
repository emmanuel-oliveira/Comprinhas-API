from __future__ import annotations

from abc import abstractmethod
from typing import Tuple

from App.Services.LLM.Prompt import PROMPT


class LLM:
    modelName: None = None

    @classmethod
    @abstractmethod
    def task(cls, prompt: PROMPT, arguments: dict) -> Tuple[str]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def status(cls) -> bool:
        raise NotImplementedError
