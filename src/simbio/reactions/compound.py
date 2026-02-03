"""
simbio.reactions
~~~~~~~~~~~~~~~~

A reaction connects species to their rate of change.

:copyright: 2020 by SimBio Authors, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import annotations

from poincare.types import EquationGroup, Equation, Constant
from symbolite import Real

from ..core import System, Parameter, Species, Reactant, assign, reaction_initial
from .single import Conversion, Dissociation, Synthesis


class ReversibleSynthesis(System):
    """A Synthesis and Dissociation reactions.

    A + B <-> AB
    """

    A: Reactant = reaction_initial()
    B: Reactant = reaction_initial()
    AB: Reactant = reaction_initial()
    forward_rate: Parameter = assign()
    reverse_rate: Parameter = assign()

    forward_reaction = Synthesis(A=A, B=B, AB=AB, rate=forward_rate)
    backward_reaction = Dissociation(AB=AB, A=A, B=B, rate=reverse_rate)


class Equilibration(System):
    """A forward and backward Conversion reactions.

    A <-> B
    """

    A: Reactant = reaction_initial()
    B: Reactant = reaction_initial()
    forward_rate: Parameter = assign()
    reverse_rate: Parameter = assign()

    forward_reaction = Conversion(A=A, B=B, rate=forward_rate)
    backward_reaction = Conversion(A=B, B=A, rate=reverse_rate)


class CatalyzeConvert(System):
    """

    A + B <--> A:B --> P
    """

    A: Reactant = reaction_initial()
    B: Reactant = reaction_initial()
    AB: Reactant = reaction_initial()
    P: Reactant = reaction_initial()
    forward_rate: Parameter = assign()
    reverse_rate: Parameter = assign()
    conversion_rate: Parameter = assign()

    binding_reaction = ReversibleSynthesis(
        A=A, B=B, AB=AB, forward_rate=forward_rate, reverse_rate=reverse_rate
    )
    conversion_reaction = Conversion(A=AB, B=P, rate=conversion_rate)
