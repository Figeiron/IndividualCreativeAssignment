from dataclasses import dataclass, field, replace
from typing import Any, Callable, List, Optional

from UI.common.presentation.hint import UIHint
from core.errors import ValidationError, ChoiceError
from core.validator import Validator, RangeValidator, ChoiceValidator


@dataclass(frozen=True)
class Parameter:
    name: str
    display_name: str
    description: str = ""
    parse: type = str
    validators: List[Validator] = field(default_factory=list)
    hints: list[UIHint] = field(default_factory=list)

    def _convert(self, value: str) -> Any:
        if not value:
            raise ValueError("Value must be not None")

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
class MappedChoiceParameter(ChoiceParameter):
    @property
    def labels(self):
        return [c[0] for c in self.choices]

    @property
    def mapping(self):
        return {c[0]: c[1] for c in self.choices}

    def __post_init__(self):
        if self.choices:
            self.validators.append(ChoiceValidator(choice_parse_type=str, choices=self.labels))

    def _convert(self, value: str):
        label = str(value)
        if label not in self.mapping:
            raise ValidationError(f"Invalid choice '{label}'")
        
        return self.mapping[label]


@dataclass(frozen=True)
class ParameterSchema:
    name: str
    display_name: str
    description: str = ""
    parse_type: Any = str
    parameter_cls: Any = Parameter
    validators: List[Validator] = field(default_factory=list)
    choices: list = field(default_factory=list)
    hints: list = field(default_factory=list)

    def with_hints(self, additional_hints: List[UIHint]):
        custom_hints = additional_hints if additional_hints else []
        return replace(self, hints=custom_hints)

    def with_range(self, min_val: Optional[Any] = None, max_val: Optional[Any] = None):
        new_validators = list(self.validators)
        new_validators.append(RangeValidator(min_val=min_val, max_val=max_val))
        return replace(self, validators=new_validators)

    def with_choices(self, choices: list):
        if not issubclass(self.parameter_cls, ChoiceParameter):
            raise ChoiceError("Must use ChoiceParameter for working with choice lists")

        return replace(self, choices=choices)

    def with_mapped_choices(self, choices: list):
        if not issubclass(self.parameter_cls, MappedChoiceParameter):
            raise ChoiceError("Must use MappedChoiceParameter for working with mapped choice lists")

        return replace(self, choices=choices)

    def build(self, custom_name: Optional[str] = None, custom_desc: Optional[str] = None, extra_validators: Optional[List[Validator]] = None) -> Parameter:
        all_validators = list(self.validators)
        if extra_validators:
            all_validators.extend(extra_validators)

        kwargs = {
            "name": custom_name or self.name,
            "display_name": self.display_name,
            "description": custom_desc or self.description,
            "parse": self.parse_type,
            "validators": all_validators,
            "hints": self.hints
        }

        if issubclass(self.parameter_cls, ChoiceParameter):
            if not self.choices:
                raise ChoiceError("Choice list cannot be empty")

            kwargs["choices"] = self.choices
            return self.parameter_cls(**kwargs)

        return self.parameter_cls(**kwargs)
