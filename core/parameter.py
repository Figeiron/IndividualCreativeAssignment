from abc import ABC
from dataclasses import dataclass, field, replace
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

    def _convert(self, value: str):
        if self.parse == bool:
            raise TypeError("You must be use BoolParameter")

        converted_value = self.parse(value)

        for validator in self.validators:
            validator(converted_value)

        return converted_value

    def convert(self, value: str) -> Any:
        try:
            return self._convert(value)

        except (ValueError, TypeError, ValidationError) as e:
            if str(e):
                raise ValueError(str(e))

            type_name = getattr(self.parse, "__name__", "заданого типу")
            raise ValueError(f"Невірний формат для '{self.display_name}'. Очікується {type_name}.")


@dataclass(frozen=True)
class BoolParameter(Parameter):
    parse: Callable[[str], Any] = bool

    def _convert(self, value: str):
        if self.parse != bool:
            raise TypeError("You must be use default Parameter")

        converted_value = value.lower() in ("yes", "true", "t", "y", "1", "так", "д", "true", "1")
        return converted_value


@dataclass(frozen=True)
class IndexParameter(Parameter):
    def _convert(self, value: str):
        converted_value = super()._convert(value)
        return converted_value - 1


@dataclass(frozen=True)
class ParameterSchema:
    name: str
    display_name: str
    description: str = ""
    parse_type: Any = str
    parameter_cls: Any = Parameter
    validators: List[Validator] = field(default_factory=list)

    def with_range(self, min_val: Optional[Any] = None, max_val: Optional[Any] = None):
        new_validators = list(self.validators)
        new_validators.append(RangeValidator(min_val=min_val, max_val=max_val))
        return replace(self, validators=new_validators)

    def build(self, custom_desc: Optional[str] = None, extra_validators: Optional[List[Validator]] = None) -> Parameter:
        all_validators = list(self.validators)
        if extra_validators:
            all_validators.extend(extra_validators)

        return self.parameter_cls(
            name=self.name,
            display_name=self.display_name,
            description=custom_desc or self.description,
            parse=self.parse_type,
            validators=all_validators
        )
