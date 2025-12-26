from poincare.types import EquationGroup
from symbolite import Real

from ..core import (
    Compartment,
    Parameter,
    RateLaw,
    Species,
    assign,
    initial,
    ReactionSpecies,
)
from .compound import Dissociation, ReversibleSynthesis


class MichaelisMenten(EquationGroup):
    def __init__(
        self,
        E: Species | ReactionSpecies | Real,
        S: Species | ReactionSpecies | Real,
        ES: Species | ReactionSpecies | Real,
        P: Species | ReactionSpecies | Real,
        forward_rate: float | Real,
        reverse_rate: float | Real,
        catalytic_rate: float | Real,
    ):
        binding_reaction = ReversibleSynthesis(
            A=E,
            B=S,
            AB=ES,
            forward_rate=forward_rate,
            reverse_rate=reverse_rate,
        )
        dissociation_reaction = Dissociation(
            AB=ES,
            A=E,
            B=P,
            rate=catalytic_rate,
        )
        self.equations = binding_reaction.equations + dissociation_reaction.equations


class MichaelisMentenEqApprox(EquationGroup):
    def __init__(
        self,
        S: Species | ReactionSpecies | Real,
        P: Species | ReactionSpecies | Real,
        maximum_velocity: float | Real,
        dissociation_constant: float | Real,
    ):
        self.equations = RateLaw(
            reactants=[S],
            products=[P],
            rate_law=maximum_velocity * S / (dissociation_constant + S),
        ).equations


class MichaelisMentenQuasiSSAprox(EquationGroup):
    def __init__(
        self,
        S: Species | ReactionSpecies | Real,
        P: Species | ReactionSpecies | Real,
        maximum_velocity: float | Real,
        michaelis_constant: float | Real,
    ):
        self.equations = RateLaw(
            reactants=[S],
            products=[P],
            rate_law=maximum_velocity * S / (michaelis_constant + S),
        ).equations
