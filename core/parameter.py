from abc import ABC
from dataclasses import dataclass, field, replace
from typing import Any, Callable, List, Optional

from core.errors import ValidationError, ChoiceError


class Validator(ABC):
    def __call__(self, *args, **kwargs):
        pass


class RangeValidator(Validator):
    def __init__(self, min_val: Optional[Any] = None, max_val: Optional[Any] = None):
        self.min_val = min_val
        self.max_val = max_val

    def __call__(self, value: Any):
        if self.min_val is not None and value < self.min_val:
            raise ValidationError(f"Value must be greater than {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValidationError(f"Value must be less than {self.max_val}")


class ChoiceValidator(Validator):
    def __init__(self, choice_parse_type: type, choices: list):
        self.choice_parse_type = choice_parse_type
        self.choices = choices

        for idx, choice in enumerate(self.choices):
            if not isinstance(choice, self.choice_parse_type):
                raise ChoiceError(f"Element [{idx}] in choice list must be of type {self.choice_parse_type.__name__}")

    def __call__(self, value):
        if not isinstance(value, self.choice_parse_type):
            raise ChoiceError(f"Value must be of type {self.choice_parse_type.__name__}")

        if not (value in self.choices):
            raise ValidationError(f"Value must be one of the available choices")


@dataclass(frozen=True)
class Parameter:
    name: str
    display_name: str
    description: str = ""
    parse: type = str
    validators: List[Validator] = field(default_factory=list)

    def to_ui(self):
        return ParameterUIProxy(self)

    def _convert(self, value: str) -> Any:
        if self.parse == bool:
            raise TypeError("Must use BoolParameter for boolean values")

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

            type_name = getattr(self.parse, "__name__", "given type")
            raise ValueError(f"Invalid format for '{self.display_name}'. Expected {type_name}.")


@dataclass(frozen=True)
class BoolParameter(Parameter):
    parse: Callable[[str], Any] = bool

    def _convert(self, value: str):
        if self.parse != bool:
            raise TypeError("Must use standard Parameter for this parameter")

        converted_value = value.lower() in ("yes", "true", "t", "y", "1", "так", "д", "true", "1")
        return converted_value


@dataclass(frozen=True)
class IndexParameter(Parameter):
    def _convert(self, value: str):
        converted_value = super()._convert(value)
        return converted_value - 1


@dataclass(frozen=True)
class ChoiceParameter(Parameter):
    choices: list = field(default_factory=list)

    def __post_init__(self):
        if self.choices:
            self.validators.append(ChoiceValidator(choice_parse_type=self.parse, choices=self.choices))


@dataclass(frozen=True)
class ParameterSchema:
    name: str
    display_name: str
    description: str = ""
    parse_type: Any = str
    parameter_cls: Any = Parameter
    validators: List[Validator] = field(default_factory=list)
    choices: list = field(default_factory=list)

    def with_range(self, min_val: Optional[Any] = None, max_val: Optional[Any] = None):
        new_validators = list(self.validators)
        new_validators.append(RangeValidator(min_val=min_val, max_val=max_val))
        return replace(self, validators=new_validators)

    def with_choices(self, choices: list):
        if not issubclass(self.parameter_cls, ChoiceParameter):
            raise ChoiceError("Must use ChoiceParameter for working with choice lists")

        return replace(self, choices=choices)

    def build(self, custom_desc: Optional[str] = None, extra_validators: Optional[List[Validator]] = None) -> Parameter:
        all_validators = list(self.validators)
        if extra_validators:
            all_validators.extend(extra_validators)

        kwargs = {
            "name": self.name,
            "display_name": self.display_name,
            "description": custom_desc or self.description,
            "parse": self.parse_type,
            "validators": all_validators
        }

        if issubclass(self.parameter_cls, ChoiceParameter):
            if not self.choices:
                raise ChoiceError("Choice list cannot be empty")

            kwargs["choices"] = self.choices
            return self.parameter_cls(**kwargs)

        return self.parameter_cls(**kwargs)


@dataclass(frozen=True)
class UIHint(ABC):
    pass

@dataclass(frozen=True)
class RangeHint(UIHint):
    min_value: Any
    max_value: Any

@dataclass(frozen=True)
class ParameterUIProxy:
    __parameter: Parameter
    ui_hints: List[UIHint] = field(default_factory=list)

    def __post_init__(self):
        for validator in self.__parameter.validators:
            if isinstance(validator, RangeValidator):
                self.ui_hints.append(RangeHint(min_value=validator.min_val, max_value=validator.max_val))
