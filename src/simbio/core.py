from __future__ import annotations

import inspect
from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Iterator, Mapping, Sequence, TypeVar

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike
from poincare import Constant, Parameter, initial
from poincare import Variable as Species

# from poincare import System as Compartment
from poincare.reactions import ReactionVariable as ReactionSpecies
from poincare._node import Node, NodeMapper, _ClassInfo
from poincare._utils import class_and_instance_method
from poincare.simulator import Backend, Components
from poincare.simulator import Simulator
from poincare.types import Equation, EquationGroup, Initial, System, assign
from symbolite import Real

from symbolite import substitute
from typing_extensions import Self, dataclass_transform
from poincare.reactions import RateLaw, MassAction, ReactionVariable

if TYPE_CHECKING:
    import ipywidgets

T = TypeVar("T")


@dataclass_transform(kw_only_default=True, field_specifiers=(initial, assign))
class Compartment(System, abstract=True):
    # def __init_subclass__(cls, **kwargs) -> None:
    #     super().__init_subclass__(**kwargs)
    #     signature: inspect.Signature = cls.__signature__
    #     parameters = dict(signature.parameters)
    #     for k in cls._annotations.keys():
    #         v = getattr(cls, k)
    #         if isinstance(v, Species):
    #             default = v.initial
    #             if default is None:
    #                 cls._required.add(k)
    #                 default = inspect.Parameter.empty
    #             parameters[k] = parameters[k].replace(default=default)
    #     cls.__signature__ = signature.replace(parameters=parameters.values())

    pass
