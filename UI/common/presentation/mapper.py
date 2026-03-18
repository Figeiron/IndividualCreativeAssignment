from dataclasses import dataclass

from typing import Callable

from core.validator import Validator, RangeValidator, ChoiceValidator
from UI.common.presentation.hint import UIHint, RangeHint, ChoiceHint


@dataclass(frozen=True)
class HintMapper:
    validator_type: type
    hint_factory: Callable[[Validator], UIHint]


HINT_REGISTRY = [
    HintMapper(
        RangeValidator,
        lambda x: RangeHint(
            min_value=x.min_val,
            max_value=x.max_val
        )
    ),
    HintMapper(
        ChoiceValidator,
        lambda x: ChoiceHint(
            choices=x.choices
        )
    )
]

HINT_LOOKUP = {m.validator_type: m.hint_factory for m in HINT_REGISTRY}
