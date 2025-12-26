"""
simbio.reactions
~~~~~~~~~~~~~~~~

A reaction connects species to their rate of change.

:copyright: 2020 by SimBio Authors, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

from __future__ import annotations

from poincare.types import EquationGroup, Equation
from symbolite import Real

from ..core import Compartment, Parameter, Species, ReactionSpecies, assign, initial
from .single import Conversion, Dissociation, Synthesis


class ReversibleSynthesis(EquationGroup):
    """A Synthesis and Dissociation reactions.

    A + B <-> AB
    """

    def __init__(
        self,
        A: Species | ReactionSpecies | Real,
        B: Species | ReactionSpecies | Real,
        AB: Species | ReactionSpecies | Real,
        forward_rate: float | Real,
        reverse_rate: float | Real,
    ):
        forward_reaction = Synthesis(A=A, B=B, AB=AB, rate=forward_rate)
        backward_reaction = Dissociation(AB=AB, A=A, B=B, rate=reverse_rate)
        self.equations = forward_reaction.equations + backward_reaction.equations


class Equilibration(EquationGroup):
    """A forward and backward Conversion reactions.

    A <-> B
    """

    def __init__(
        self,
        A: Species | ReactionSpecies | Real,
        B: Species | ReactionSpecies | Real,
        forward_rate: float | Real,
        reverse_rate: float | Real,
    ):
        forward_reaction = Conversion(A=A, B=B, rate=forward_rate)
        backward_reaction = Conversion(A=B, B=A, rate=reverse_rate)
        self.equations = forward_reaction.equations + backward_reaction.equations


class CatalyzeConvert(EquationGroup):
    """

    A + B <--> A:B --> P
    """

    def __init__(
        self,
        A: Species | ReactionSpecies | Real,
        B: Species | ReactionSpecies | Real,
        AB: Species | ReactionSpecies | Real,
        P: Species | ReactionSpecies | Real,
        forward_rate: float | Real,
        reverse_rate: float | Real,
        conversion_rate: float | Real,
    ):
        binding_reaction = ReversibleSynthesis(
            A=A, B=B, AB=AB, forward_rate=forward_rate, reverse_rate=reverse_rate
        )
        conversion_reaction = Conversion(A=AB, B=P, rate=conversion_rate)
        self.equations = binding_reaction.equations + conversion_reaction.equations
