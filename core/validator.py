from abc import ABC
from typing import Optional, Any

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

