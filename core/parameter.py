from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Parameter:
    name: str
    display_name: str
    description: str = ""
    parse: Callable[[str], Any] = str

    def convert(self, value: str) -> Any:
        try:
            if self.parse == bool:
                return value.lower() in ("yes", "true", "t", "y", "1", "так", "д", "true", "1")
            
            return self.parse(value)

        except (ValueError, TypeError) as e:
            if str(e):
                raise ValueError(f"Помилка в '{self.display_name}': {str(e)}")
            
            type_name = getattr(self.parse, "__name__", "заданого типу")
            raise ValueError(f"Невірний формат для '{self.display_name}'. Очікується {type_name}.")
