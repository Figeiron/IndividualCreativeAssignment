from dataclasses import dataclass, field
from typing import List

from core.parameter import Parameter
from core.validator import RangeValidator
from core.presentation.hint import UIHint, RangeHint


@dataclass(frozen=True)
class ParameterUIProxy:
    __parameter: Parameter
    ui_hints: List[UIHint] = field(default_factory=list)

    def __post_init__(self):
        for validator in self.__parameter.validators:
            if isinstance(validator, RangeValidator):
                self.ui_hints.append(RangeHint(min_value=validator.min_val, max_value=validator.max_val))
