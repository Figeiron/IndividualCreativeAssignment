from dataclasses import dataclass
from abc import ABC
from typing import Optional

@dataclass(frozen=True)
class UIHint(ABC):
    pass


@dataclass(frozen=True)
class RangeHint(UIHint):
    min_value: Optional[int, float]
    max_value: Optional[int, float]

