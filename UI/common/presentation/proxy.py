from dataclasses import dataclass, field
from typing import List

from core.command import Command
from core.parameter import Parameter
from UI.common.presentation.hint import UIHint, ParseHint
from UI.common.presentation.mapper import HINT_LOOKUP
from core.service import Service


@dataclass(frozen=True)
class ParameterUIProxy:
    __parameter: Parameter
    ui_hints: List[UIHint] = field(default_factory=list)

    @property
    def name(self):
        return self.__parameter.name

    @property
    def display_name(self):
        return self.__parameter.display_name

    @property
    def description(self):
        return self.__parameter.description

    def convert(self, value: str):
        return self.__parameter.convert(value)

    def __post_init__(self):
        hints = list(self.ui_hints)
        hints.extend(self.__get_validator_hints())
        hints.append(self.__get_parse_hints())
        object.__setattr__(self, "ui_hints", hints)

    def __get_parse_hints(self) -> UIHint:
        return ParseHint(self.__parameter.parse)

    def __get_validator_hints(self) -> list[UIHint]:
        hints = []
        for validator in self.__parameter.validators:
            factory = HINT_LOOKUP[type(validator)]
            if factory:
                hints.append(factory(validator))

        return hints


class ParameterUIAssembler:
    def __init__(self, command: Command, service: Service):
        self.raw_parameters = command.get_params(service)

    @staticmethod
    def __get_parameter_presentation(parameter: Parameter):
        return ParameterUIProxy(parameter, ui_hints=parameter.hints)

    def __call__(self):
        return [self.__get_parameter_presentation(p) for p in self.raw_parameters]
