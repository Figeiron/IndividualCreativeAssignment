from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional

from core.errors import ValidationError


class Validator(ABC):
    def __call__(self, *args, **kwargs):
        pass


class RangeValidator(Validator):
    def __init__(self, min_val: Optional[Any] = None, max_val: Optional[Any] = None):
        self.min_val = min_val
        self.max_val = max_val

    def __call__(self, value: Any):
        if self.min_val is not None and value < self.min_val:
            raise ValidationError(f"Значення повинно бути більше {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValidationError(f"Значення повинно бути менше {self.max_val}")


@dataclass(frozen=True)
class Parameter:
    name: str
    display_name: str
    description: str = ""
    parse: Callable[[str], Any] = str
    validators: List[Validator] = field(default_factory=list)

    def convert(self, value: str) -> Any:
        try:
            if self.parse == bool:
                converted_value = value.lower() in ("yes", "true", "t", "y", "1", "так", "д", "true", "1")
            else:
                converted_value = self.parse(value)

            for validator in self.validators:
                validator(converted_value)

            return converted_value

        except (ValueError, TypeError, ValidationError) as e:
            if str(e):
                raise ValueError(str(e))

            type_name = getattr(self.parse, "__name__", "заданого типу")
            raise ValueError(f"Невірний формат для '{self.display_name}'. Очікується {type_name}.")


@dataclass(frozen=True)
class IndexParameter(Parameter):
    def convert(self, value: str) -> Any:
        converted_value = super().convert(value)
        return converted_value - 1
