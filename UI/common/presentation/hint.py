from dataclasses import dataclass
from abc import ABC
from typing import Union


@dataclass(frozen=True)
class UIHint(ABC):
    pass


@dataclass(frozen=True)
class RangeHint(UIHint):
    min_value: Union[int, float, None] = None
    max_value: Union[int, float, None] = None

@dataclass(frozen=True)
class OrderHint(UIHint):
    order_number: int

@dataclass(frozen=True)
class ChoiceHint(UIHint):
    choices: list

@dataclass(frozen=True)
class LargeTextHint(UIHint):
    pass

@dataclass(frozen=True)
class ListboxHint(UIHint):
    choices: list
    height: int = 5
