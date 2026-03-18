from dataclasses import dataclass
from abc import ABC
from typing import Union


@dataclass(frozen=True)
class UIHint(ABC):
    pass


@dataclass(frozen=True)
class RangeHint(UIHint):
    min_value: Union[int, float]
    max_value: Union[int, float]

@dataclass(frozen=True)
class ParseHint(UIHint):
    parse: type

@dataclass(frozen=True)
class OrderHint(UIHint):
    order_number: int

@dataclass(frozen=True)
class ChoiceHint(UIHint):
    choices: list
