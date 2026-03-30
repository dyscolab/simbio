import numpy as np
from pytest import mark

from .. import Simulator, System, Variable, initial, MassAction
from ..reactions import compound, enzymatic, single
from ..reactions.single import Synthesis

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


def test_external_stoichiometry_in_reaction():
    class Model1(System):
        A: Variable = initial(default=10)
        B: Variable = initial(default=5)
        AB: Variable = initial(default=5)

        r = Synthesis(A=10 * A, B=B, AB=AB, rate=2)

    class Model2(System):
        A: Variable = initial(default=10)
        B: Variable = initial(default=5)
        AB: Variable = initial(default=5)

        r = MassAction(reactants=[10 * A, B], products=[AB], rate=2)

    assert Model1.r.reaction.reactants[0].stoichiometry == 10

    sim1 = Simulator(Model1)
    result1 = np.asarray(sim1.solve(save_at=np.linspace(0, 10, 10)).to_array())

    sim2 = Simulator(Model2)
    result2 = np.asarray(sim2.solve(save_at=np.linspace(0, 10, 10)).to_array())

    assert np.all(result1 == result2)
