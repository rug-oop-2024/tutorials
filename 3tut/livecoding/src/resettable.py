from abc import ABC, abstractmethod
from pydantic import PrivateAttr, BaseModel
from typing import List

class Resettable(BaseModel, ABC):
    _first_round: bool = PrivateAttr(default=True)

    @abstractmethod
    def reset(self) -> None:
        pass