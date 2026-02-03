import numpy as np
from pytest import mark

import inspect

from poincare.types import EquationGroup
from ..core import (
    System,
    Parameter,
    RateLaw,
    MassAction,
    Simulator,
    Variable,
    assign,
    initial,
    reaction_initial,
)

from ..reactions import compound, enzymatic, single


reactions = []
for mod in (single, compound, enzymatic):
    for name in dir(mod):
        value = getattr(mod, name)
        if isinstance(value, type(System)) and value != System:
            reactions.append(value)


@mark.parametrize("reaction", reactions)
def test_reactions(reaction):
    model = reaction(**dict.fromkeys(reaction._required, 1))
    sim = Simulator(model)
    sim.solve(save_at=np.linspace(0, 1, 10))
