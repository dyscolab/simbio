import numpy as np
from pytest import mark

import inspect

from poincare.types import EquationGroup
from ..core import (
    Compartment,
    Parameter,
    RateLaw,
    MassAction,
    Simulator,
    Species,
    assign,
    initial,
)
from ..reactions import compound, enzymatic, single

reactions = set()
for mod in (single, compound, enzymatic):
    for name in dir(mod):
        value = getattr(mod, name)
        try:
            if (
                issubclass(value, EquationGroup)
                and value is not EquationGroup
                and value is not MassAction
                and value is not RateLaw
            ):
                reactions.add(value)
        except TypeError:
            pass


@mark.parametrize("reaction", reactions)
def test_reactions(reaction):
    class Model(Compartment):
        A: Species = initial(default=0)
        B: Species = initial(default=0)
        C: Species = initial(default=0)
        D: Species = initial(default=0)
        species = [A, B, C, D]
        init_parameters = inspect.signature(reaction.__init__).parameters
        rate_num = sum(
            ("rate" in param or "constant" in param or "velocity" in param)
            for param in init_parameters
        )
        species_num = (
            len(inspect.signature(reaction.__init__).parameters) - rate_num - 1
        )
        model = reaction(*species[0:species_num], *([1] * rate_num))

    sim = Simulator(Model)
    sim.solve(save_at=np.linspace(0, 1, 10))


@mark.parametrize("reaction", reactions)
def test_reactions_with_stochiometry(reaction):
    class Model(Compartment):
        A: Species = initial(default=0)
        B: Species = initial(default=0)
        C: Species = initial(default=0)
        D: Species = initial(default=0)
        species = [A, B, C, D]
        init_parameters = inspect.signature(reaction.__init__).parameters
        rate_num = sum(
            ("rate" in param or "constant" in param or "velocity" in param)
            for param in init_parameters
        )
        species_num = (
            len(inspect.signature(reaction.__init__).parameters) - rate_num - 1
        )
        model = reaction(*[2 * s for s in species[0:species_num]], *([1] * rate_num))

    sim = Simulator(Model)
    sim.solve(save_at=np.linspace(0, 1, 10))


def test_reaction_with_species():
    class Model(Compartment):
        s: Species = initial(default=0)
        k: Parameter = assign(default=0)
        r_with_species = RateLaw(reactants=[s], products=[], rate_law=k * s)
        r_with_variable = RateLaw(reactants=[s], products=[], rate_law=k * s)

    assert Model.r_with_species.rate_law == Model.r_with_variable.rate_law
