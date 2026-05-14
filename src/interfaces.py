from typing import Any, Protocol
from collections.abc import Iterable


type Category = Any
type Categories = Iterable[Category]
type Stimulus = Any 


class Hypothesis(Protocol):
    "A function that accepts a stimulus, and outputs the corresponding category"
    def __call__(self, stimulus:Stimulus) -> Category:
        ...

