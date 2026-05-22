from enum import IntEnum, auto
from dataclasses import dataclass
from typing import Protocol, Generator, Any, Iterator
from random import Random


type Category = IntEnum

class safe_category(IntEnum):
    unsafe = auto()
    safe = auto()

class Hypothesis:
    "A function that accepts a stimulus, and categorizes it between two categories"

    lower_category:safe_category = safe_category.unsafe
    upper_category:safe_category = safe_category.safe

    min_bound:float = 0
    max_bound:float = 1

    def __init__(self, category_boundary: float) -> None:
        assert category_boundary >= Hypothesis.min_bound
        assert category_boundary <= Hypothesis.max_bound

        self.category_boundary: float = category_boundary
    
    def eval(self, stimulus: float) -> safe_category:
        return Hypothesis.lower_category if stimulus < self.category_boundary else Hypothesis.upper_category


@dataclass(frozen=True,slots=False)
class Datapoint:
    position: float
    category: safe_category

class HistoryManager:
    "This manages the history of observations seen, and implements any memory restrictions assumend in the model."

    def __init__(self, max_memory_length:int|None) -> None:
        self.contents:list[Datapoint] = []
        self.max_memory_length:int|None = max_memory_length
    
    def __iter__(self)->Iterator[Datapoint]:
        return self.contents.__iter__()
    
    def add(self,data:Datapoint)-> None:
        self.contents.append(data)
        while self.max_memory_length is not None and self.max_memory_length > len(self.contents):
            self.contents.pop(0)

type HypothesisUpdater = Generator[Hypothesis,Any,None]

def UpdateConsistantWithData(data_list:HistoryManager,rand:Random)-> Generator[Hypothesis,None,None]:
    "Selects uniformly at random"

    def get_plausible_hyposthesis_boundaries(data_list:HistoryManager)->tuple[float,float]:
        lower_category_data = [d.position for d in data_list if d.category == Hypothesis.lower_category]
        upper_category_data = [d.position for d in data_list if d.category == Hypothesis.upper_category]
        lower_category_data.append(Hypothesis.min_bound)
        upper_category_data.append(Hypothesis.max_bound)

        max_lower_position = max(lower_category_data)
        min_upper_position = min(upper_category_data)

        return (max_lower_position, min_upper_position)
    
    while True:
        min_pos, max_pos = get_plausible_hyposthesis_boundaries(data_list)
        boundary = rand.uniform(min_pos,max_pos)
        yield Hypothesis(category_boundary=boundary)
        

    
class HypothesisBank(Protocol):
    "These classes are what is used to determine when a hypothesis should be updated and how."
    pass

@dataclass
class MultiHypothesisBankConfig:
    num_hypotheses: int
    "The total number of hypotheses that the model considers at once"
    num_hypotheses_kept: int
    """
    The total number of hypotheses that the model keeps between run itterations. 
    This number should be < num_hypotheses or no hypotheses will be updated between trials. 
    """

class Multi_HypothesisBank(HypothesisBank):
    def __init__(self, config:MultiHypothesisBankConfig) -> None:
        self.active_hypotheses:list[Hypothesis] = []
        self.config = config

class ReplaceWhenWrong_HypothesisBank(HypothesisBank):
    def __init__(self,history:HistoryManager,updater:HypothesisUpdater) -> None:
        self.history = history
        self.updater = updater

        self.active_hypothesis:Hypothesis = next(self.updater)