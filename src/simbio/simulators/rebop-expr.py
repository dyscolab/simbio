import dataclasses
from collections import ChainMap
from collections.abc import Iterable

from poincare import Variable
from rebop import Gillespie
from simbio import RateLaw, Simulator, Species
from symbolite.abstract import symbol
from symbolite.core import substitute

rebop_subs = {
    symbol.pow: dataclasses.replace(symbol.pow, fmt="{}^{}"),
}


class Renamer:
    @staticmethod
    def forward(x: str, /):
        return x.replace(".", "__")

    @staticmethod
    def reverse(x: str, /):
        return x.replace("__", ".")


def yield_species(species: Iterable[Species], /, variable_map: dict[Variable, str]):
    for s in species:
        if not s.stoichiometry.is_integer():
            raise NotImplementedError

        name = variable_map[s.variable]
        for _ in range(int(s.stoichiometry)):
            yield name


sim = Simulator(ARM)
variable_map = {k: Renamer.forward(str(k)) for k in sim.compiled.variables}
parameter_map = {k: Renamer.forward(str(k)) for k in sim.compiled.parameters}


subs = ChainMap(rebop_subs, variable_map, parameter_map)

rebop = Gillespie()
for r in ARM._yield(RateLaw):
    rebop.add_reaction(
        rate=str(substitute(r.rate_law, subs)),
        reactants=list(yield_species(r.reactants, variable_map)),
        products=list(yield_species(r.products, variable_map)),
    )

p = sim.create_problem()