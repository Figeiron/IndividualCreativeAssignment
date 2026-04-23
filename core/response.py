from dataclasses import dataclass
from typing import List, Tuple
from abc import ABC


class BaseBox(ABC):
    pass


@dataclass
class TextBox(BaseBox):
    text: str

@dataclass
class TableCell:
    pos: Tuple[int, int]
    text: str

@dataclass
class TableBox(BaseBox):
    cells: List[TableCell]    

@dataclass
class PlotBox(BaseBox):
    plot_points: List[Tuple[int, int]]


@dataclass(frozen=True)
class Response:
    boxes: List[BaseBox]
