from enum import IntEnum, auto
from dataclasses import dataclass
import functools as ft
from typing import Protocol, Generator, Any, Iterator, Callable
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

######################################################[ Manage Storing Data ]###################################################################

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

#########################################################[ Hypothesis updater ]#######################################################################

def get_plausible_hyposthesis_boundaries(data_list:HistoryManager)->tuple[float,float]:
    lower_category_data = [d.position for d in data_list if d.category == Hypothesis.lower_category]
    upper_category_data = [d.position for d in data_list if d.category == Hypothesis.upper_category]
    lower_category_data.append(Hypothesis.min_bound)
    upper_category_data.append(Hypothesis.max_bound)

    max_lower_position = max(lower_category_data)
    min_upper_position = min(upper_category_data)

    return (max_lower_position, min_upper_position)

type HypothesisUpdater = Generator[Hypothesis,Any,None]

def UpdateConsistantWithData(data_list:HistoryManager,rand:Random=Random())-> Generator[Hypothesis,None,None]:
    "Selects a new hypothesis uniformly at random from all prior hypotheses"
    
    while True:
        min_pos, max_pos = get_plausible_hyposthesis_boundaries(data_list)
        boundary = rand.uniform(min_pos,max_pos)
        yield Hypothesis(category_boundary=boundary)

###############################################[ Stimulus Selection Strategy ]#########################################################
        
# type StimulusSelector = Callable[[],float]
class StimulusSelector(Protocol):
    def select_stimulus(self,current_hypothesis:Hypothesis)->float:
        ...

class Random_StimulusSelector:
    def __init__(self, random:Random=Random()) -> None:
        "Sampling bias is how far from the current"
        self.rand = random

    def select_stimulus(self,current_hypothesis:Hypothesis)->float:
        lower=Hypothesis.min_bound
        upper=Hypothesis.max_bound
        return self.rand.uniform(lower, upper)
    
class HistoricallyInformedRandom_StimulusSelector:
    def __init__(self, history:HistoryManager, random:Random=Random()) -> None:
        "Sampling bias is how far from the current"
        self.rand = random
        self.history = history

    def select_stimulus(self,current_hypothesis:Hypothesis)->float:
        lower, upper = get_plausible_hyposthesis_boundaries(self.history)
        return self.rand.uniform(lower, upper)

class HypothesisOffset_StimulusSelector:
    def __init__(self, sampling_bias:float,random:Random=Random()) -> None:
        "Sampling bias is how far from the current"
        self.rand = random
        self.sampling_bias=sampling_bias

    def select_stimulus(self,current_hypothesis:Hypothesis)->float:
        lower=Hypothesis.min_bound
        upper=Hypothesis.max_bound
        lower = max(lower, current_hypothesis.category_boundary - self.sampling_bias)
        upper = min(upper, current_hypothesis.category_boundary + self.sampling_bias)
        return self.rand.uniform(lower, upper)

class HistoricallyInformedHypothesisOffset_StimulusSelector:
    def __init__(self, sampling_bias:float, history:HistoryManager, random:Random=Random()) -> None:
        "Sampling bias is how far from the current"
        self.rand = random
        self.sampling_bias=sampling_bias
        self.history = history

    def select_stimulus(self,current_hypothesis:Hypothesis)->float:
        lower, upper = get_plausible_hyposthesis_boundaries(self.history)
        lower = max(lower, current_hypothesis.category_boundary - self.sampling_bias)
        upper = min(upper, current_hypothesis.category_boundary + self.sampling_bias)
        return self.rand.uniform(lower, upper)

###################################################[ Hypothesis Bank ]################################################################
    
class HypothesisBank(Protocol):
    "These classes are what is used to determine when a hypothesis should be updated and how."
    pass

# @dataclass
# class MultiHypothesisBankConfig:
#     num_hypotheses: int
#     "The total number of hypotheses that the model considers at once"
#     num_hypotheses_kept: int
#     """
#     The total number of hypotheses that the model keeps between run itterations. 
#     This number should be < num_hypotheses or no hypotheses will be updated between trials. 
#     """

# class Multi_HypothesisBank(HypothesisBank):
#     def __init__(self, config:MultiHypothesisBankConfig) -> None:
#         self.active_hypotheses:list[Hypothesis] = []
#         self.config = config

class ReplaceWhenWrong_HypothesisBank(HypothesisBank):
    def __init__(self,history:HistoryManager, updater:HypothesisUpdater, selector:StimulusSelector, initial_hypothesis:Hypothesis|None=None) -> None:
        self.history = history
        self.updater = updater
        self.selector = selector

        self.active_hypothesis:Hypothesis = next(self.updater) # Need this to start the iterator.
        if initial_hypothesis is not None: self.active_hypothesis = initial_hypothesis

    def learn_data(self,data:Datapoint) -> None:
        "This method represents the model getting data from the environment. If this conflicts with the current model, it will replace it."
        self.history.add(data)

        # Update the active hypothesis if it is inconsistant with the data.
        if self.active_hypothesis.eval(stimulus=data.position) != data.category:
            self.active_hypothesis = next(self.updater)

    def predict_categorization(self, stimulus: float) -> safe_category:
        "Given the currently accepted hypothesis, how would we expect the current stimulus be categorized."
        return self.active_hypothesis.eval(stimulus=stimulus)
    
    def select_next_stimulus(self) -> float:
        "Given the current history, what stimulus would be the best"
        return self.selector.select_stimulus(self.active_hypothesis)